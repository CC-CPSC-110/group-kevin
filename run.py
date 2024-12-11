""" Responsible for running the game. """
import pygame
from dataclasses import dataclass
from copy import deepcopy
from typing import List, Tuple, Optional, Dict
from ghost import *
from pacman import Pacman
from game import *
from keys import pressed_keys, directions
from board import *

def main():
    """
    Purpose: The main function initializes the game environment, sets up game objects 
             (Pacman, ghosts, maze), and prepares the game loop.
    Examples:
        main()
        # Initializes the Pacman game, sets up the game window, reads the maze layout 
        # from "maze.txt", and prepares Pacman and ghost objects for gameplay.
    """
    pygame.init()  # Initialize the Pygame library
    screen = pygame.display.set_mode((WIDTH, HEIGHT))  # Set up the game window
    pygame.display.set_caption("Pacman Game")  # Set the game window title
    clock = pygame.time.Clock()  # Create a clock object to control the frame rate
    font = pygame.font.Font('freesansbold.ttf', 20)  # Load a font for rendering text

    global game_state
    # Parse the game state from the maze file
    try:
        game_state = parse_game_state_from_txt("maze.txt")  # Load the maze and positions
    except ValueError as e:
        print(f"Error parsing game state: {e}")  # Print error if parsing fails
        pygame.quit()  # Quit Pygame
        return

    # Extract maze dimensions and calculate unit size
    maze = game_state.maze
    num_rows = len(maze)
    num_cols = len(maze[0]) if num_rows > 0 else 0
    unit_height = (HEIGHT - 50) // num_rows  # Adjust for UI elements
    unit_width = WIDTH // num_cols
    
    # High score file path
    high_score_file = "high_score.txt"
    high_score = load_high_score(high_score_file)  # Load the high score from the file


    # Initialize the Game object with screen, clock, and other configurations
    game = Game(
        id="",
        screen=screen,
        clock=clock,
        keymap={
            "w": "UP",  # Map 'w' to "UP"
            "s": "DOWN",  # Map 's' to "DOWN"
            "a": "LEFT",  # Map 'a' to "LEFT"
            "d": "RIGHT"  # Map 'd' to "RIGHT"
        },
        background='black',  # Set the background color
        fps=60.0,  # Set frames per second
        running=True,  # Flag to indicate if the game is running
        deltaT=0,  # Time since the last frame
        unit_height=unit_height,  # Unit height for maze cells
        unit_width=unit_width,  # Unit width for maze cells
        font=font  # Font for rendering UI
    )

    # Initialize Pacman using its starting position from the game state
    px, py = game_state.pacman_pos
    pacman = Pacman(
        x=px * unit_width,  # Convert maze position to screen coordinates
        y=py * unit_height,
        size=40,  # Size of Pacman
        speed=2,  # Speed of Pacman in tiles per second
        counter=0,  # Animation frame counter
        lives=3,  # Starting number of lives
        boosted=False,  # Boosted state flag
        direction=0,  # Initial direction (0 = right)
        turns=[False, False, False, False],  # Valid turns
        score=0,  # Initial score
        direction_command=0,  # Initial movement direction
        boost_timer=0  # Timer for boosted state
    )

    # Load ghost images or create placeholder images if loading fails
    try:
        ghost_images = {
            "G1": pygame.transform.scale(pygame.image.load('assets/ghost_images/red.png'), (40, 40)),
            "G2": pygame.transform.scale(pygame.image.load('assets/ghost_images/blue.png'), (40, 40)),
            "G3": pygame.transform.scale(pygame.image.load('assets/ghost_images/yellow.png'), (40, 40))
        }
    except pygame.error as e:
        print(f"Error loading ghost images: {e}")  # Print error if loading fails
        # Create placeholder images with solid colors
        ghost_images = {
            "G1": pygame.Surface((40, 40)),
            "G2": pygame.Surface((40, 40)),
            "G3": pygame.Surface((40, 40))
        }
        ghost_images["G1"].fill('red')  # Red placeholder for G1
        ghost_images["G2"].fill('blue')  # Blue placeholder for G2
        ghost_images["G3"].fill('yellow')  # Yellow placeholder for G3

    # Initialize ghosts and assign them strategies
    ghosts = []
    ghost_strategies = {}

    for g_id, (gx, gy) in game_state.ghost_positions.items():
        # Create a ghost object with its position and attributes
        ghost_obj = Ghost(
            x=gx * unit_width,  # Convert maze position to screen coordinates
            y=gy * unit_height,
            size=40,  # Size of ghost
            speed=1,  # Speed in tiles per second
            counter=0,  # Animation frame counter
            dead=False,  # Initial state is alive
            direction=0,  # Initial direction (0 = right)
            img=ghost_images.get(g_id, pygame.Surface((40, 40))),  # Image for the ghost
            id=g_id,  # Ghost ID (e.g., "G1", "G2")
            turns=[False, False, False, False],  # Valid turns
            in_box=False  # Flag for starting in a box
        )
        ghost_obj.target_tile = (gx, gy)  # Initial target tile is its starting position
        ghosts.append(ghost_obj)

        # Assign strategies based on ghost ID
        if g_id == "G1":
            ghost_strategies[g_id] = RandomGhostStrategy()  # G1 uses random movement
        elif g_id == "G2":
            ghost_strategies[g_id] = ChasingGhostStrategy()  # G2 chases Pacman
        elif g_id == "G3":
            ghost_strategies[g_id] = PalletHoveringGhostStrategy()  # G3 hovers near pellets
        else:
            ghost_strategies[g_id] = RandomGhostStrategy()  # Default to random strategy

    # Initialize a tracker for eaten ghosts
    eaten_ghosts = EatenGhostList({ghost.id: False for ghost in ghosts})

    # Map direction strings to integer codes
    direction_map = {
        "RIGHT": 0,  # Right direction code
        "LEFT": 1,  # Left direction code
        "UP": 2,  # Up direction code
        "DOWN": 3  # Down direction code
    }

    # Debugging: Print starting positions
    # Print initial positions of Pacman and ghosts for debugging purposes
    print(f"Pacman is at: ({pacman.x}, {pacman.y})")
    for ghost in ghosts:
        print(f"Ghost {ghost.id} is at: ({ghost.x}, {ghost.y})")

    # Main game loop
    while game.running:
        game.tick()  # Update the game clock and regulate FPS
        game.screen.fill(game.background)  # Clear the screen with the background color

        # Check for user events like quitting the game
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # Exit game if the quit event is triggered
                game.running = False

        # Capture the current state of keyboard keys
        keys_state = pygame.key.get_pressed()
        pressed = pressed_keys(keys_state)  # Get list of pressed keys
        dirs = directions(game.keymap, pressed)  # Map pressed keys to directions

        # Update Pacman's direction based on input, if valid
        if dirs:
            chosen_dir = dirs[0]
            pacman.direction_command = direction_map.get(chosen_dir, pacman.direction)
        else:
            pacman.direction_command = None  # Stop movement if no keys are pressed

        # Increment animation counter for smoother animations
        pacman.counter = (pacman.counter + 1) % 40

        # Handle boosted state logic
        if pacman.boosted:
            if pacman.boost_timer < 600:  # Boost lasts for 600 frames
                pacman.boost_timer += 1
            else:  # Reset boost state after timeout
                pacman.boosted = False
                pacman.boost_timer = 0
                eaten_ghosts.eaten_ghosts = {ghost.id: False for ghost in ghosts}

        # Draw the maze, score, and lives
        draw_board(game.screen, maze, pacman.score, game.font, pacman.lives, high_score)
        # Draw Pacman with updated animation and position
        draw_player(game.screen, pacman.x, pacman.y, pacman.size, pacman.direction, pacman.counter)

        # Calculate Pacman's current grid position
        cx, cy = round(pacman.x / unit_width), round(pacman.y / unit_height)

        # Determine valid moves from Pacman's current position
        valid_moves = get_valid_moves(maze, (cx, cy))
        pacman.turns = [False, False, False, False]  # Reset possible turns

        if (cx + 1, cy) in valid_moves:  # Right
            pacman.turns[0] = True
        if (cx - 1, cy) in valid_moves:  # Left
            pacman.turns[1] = True
        if (cx, cy - 1) in valid_moves:  # Up
            pacman.turns[2] = True
        if (cx, cy + 1) in valid_moves:  # Down
            pacman.turns[3] = True

        # Move Pacman based on the current direction command and valid moves
        pacman.move_player(pacman.direction_command, pacman.turns, unit_width, unit_height, maze)

        # Update Pacman's position in the game state
        game_state.pacman_pos = (pacman.x // unit_width, pacman.y // unit_height)

        # Check collisions and update the maze (e.g., eat dots or power-ups)
        check_collisions_and_update_maze(pacman, maze)
        
        # Update the high score if Pacman's score exceeds it
        if pacman.score > high_score:
            high_score = pacman.score
            save_high_score(high_score_file, high_score)

        # Update ghost positions based on their target tiles
        for ghost in ghosts:
            g_tile_x = ghost.x // unit_width  # Current grid x-position
            g_tile_y = ghost.y // unit_height  # Current grid y-position
            game_state.ghost_positions[ghost.id] = (g_tile_x, g_tile_y)

        for ghost in ghosts:
            ghost_id_str = ghost.id
            # Check if ghost reached its target tile
            if (abs(ghost.x - ghost.target_tile[0] * unit_width) < 1 and
                abs(ghost.y - ghost.target_tile[1] * unit_height) < 1):
                # Get the next target tile using the assigned strategy
                new_pos = ghost_strategies[ghost_id_str].get_next_position(game_state, ghost_id_str)
                if new_pos:
                    ghost.target_tile = new_pos

            # Move the ghost incrementally toward its target tile
            reached = move_ghost_towards_tile(ghost, ghost.target_tile, unit_width, unit_height, game.deltaT)
            # Draw the ghost with its updated state
            g_rect = ghost.draw_ghost(game.screen, pacman.boosted, eaten_ghosts.eaten_ghosts, unit_width, unit_height)

        # Handle collisions between Pacman and ghosts
        player_hit_box = pygame.Rect(pacman.x, pacman.y, pacman.size, pacman.size)
        
        for ghost in ghosts:
            g_rect = pygame.Rect(ghost.x, ghost.y, ghost.size, ghost.size)

            if not pacman.boosted:
                if player_hit_box.colliderect(g_rect) and not ghost.dead:
                    # Pacman loses a life if colliding with a live ghost while not boosted
                    if pacman.lives > 0:
                        pacman.lives -= 1
                        pacman.x = game_state.pacman_pos[0] * unit_width
                        pacman.y = game_state.pacman_pos[1] * unit_height
                        for g in ghosts:
                            g.x = game_state.ghost_positions[g.id][0] * unit_width
                            g.y = game_state.ghost_positions[g.id][1] * unit_height
                            g.dead = False
            else:
                if player_hit_box.colliderect(g_rect) and not ghost.dead and not eaten_ghosts[ghost.id]:
                    ghost.dead = True
                    ghost.speed = 0  # Stop ghost movement
                    eaten_ghosts[ghost.id] = True
                    ghost.respawn_timer = 180  # Set respawn delay (e.g., 3 seconds at 60 FPS)

                    # Reset position to initial spawn coordinates
                    spawn_x, spawn_y = game_state.ghost_positions[ghost.id]
                    ghost.x = spawn_x * unit_width
                    ghost.y = spawn_y * unit_height
                    print(f"Respawning ghost {ghost.id} to ({spawn_x}, {spawn_y})")

        for ghost in ghosts:
            if ghost.dead and ghost.respawn_timer > 0:
                ghost.respawn_timer -= 1  # Countdown the respawn timer
                if ghost.respawn_timer == 0:
                    ghost.dead = False  # Bring the ghost back to life
                    ghost.speed = 1  # Restore ghost speed
                    print(f"Ghost {ghost.id} is back in play!")


        # Check if all pellets are eaten (win condition)
        if not any('o' in row or '.' in row for row in maze):
            save_high_score(high_score_file, high_score)  # Save the high score before displaying the win message
            display_message(screen, font, "YOU WIN!!!")  # Display win message
            game.running = False

        # Check if Pacman is out of lives (lose condition)
        if pacman.lives == 0:
            save_high_score(high_score_file, high_score)  # Save the high score before displaying the lose message
            display_message(screen, font, "YOU LOSE!!!")  # Display lose message
            game.running = False

        pygame.display.flip()  # Update the display with the latest frame

pygame.quit()  # Quit Pygame after exiting the game loop

# Run the main function if the script is executed directly
if __name__ == "__main__":
    main()