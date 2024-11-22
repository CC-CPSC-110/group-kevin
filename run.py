"""Example game showing a circle moving on screen."""
import pygame

from game import Game
from pacman import Pacman
from food import FoodList
from keys import pressed_keys, directions
from opponent import Opponent
from pacman_parser import parse_pacman, lines

# TODO: Refactor draw to act on list of Sprite and draw all Sprites
def draw(game: Game, pacman: Pacman, opponent: Opponent, food_list: FoodList):
    """
    Draws the player and game on the screen.
    
    Note that because this function has only side-effects, it would take a
    simulation to test. We can do that, but for this class, it's a bit much.
    Therefore, we don't have any tests for this.
    """
    game.screen.fill(game.background)
    pygame.draw.circle(
        game.screen,
        pacman.color,
        pygame.Vector2(player.x, player.y),
        player.size
    )
    pygame.draw.circle(
        game.screen,
        opponent.color,
        pygame.Vector2(opponent.x, opponent.y),
        opponent.size
    )
    for f in food_list.food:
        pygame.draw.circle(
            game.screen,
            "brown",
            pygame.Vector2(f.x, f.y),
            f.size
        )
    pygame.display.flip()
    

def main():
    """
    Run the main game loop.
    
    Note: again, because this is a function that only has side effects, there's
    not really a clean way to test this. Main loops usually follow a command
    pattern like this where they coordinate functions from different files.
    """
    
    # Define the Game state
    game = Game(
        screen     = pygame.display.set_mode((1280, 720)),
        clock      = pygame.time.Clock(),
        background = "white",
        fps        = 120,
        running    = True,
        deltaT     = 0,
        keymap     = {
                        "w": "UP",
                        "s": "DOWN",
                        "a": "LEFT",
                        "d": "RIGHT",
        },
    )

    # Define the player
    pacman = parse_pacman(lines[1:])
    
    # TODO: Initialize the Opponent
    opponent = Opponent(
        x = game.screen.get_width() / 2,
        y = game.screen.get_height() / 2,
        size = 40,
        speed = 2,
        color = "red"
    )
    
    # Initialze pygame
    pygame.init()

    food_list = FoodList([])
    food_list.populate(100, (game.screen.get_width(), game.screen.get_height()))
    
    # Run forever in a loop until quit
    while game.running:
        # poll for events
        # pygame.QUIT event means the user clicked X to close your window
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game.running = False
                pygame.quit()

        # Move the game clock forward
        game.tick()

        # Get pressed keys and directions
        pressed = pressed_keys(pygame.key.get_pressed())
        dirs = directions(game.keymap, pressed)
        
        # Move the player
        pacman.move(game.deltaT, dirs)

        # TODO: move the Opponent
        if len(food_list.food) != 0:
            opponent.move(food_list)

        if pygame.mouse.get_focused():
            player.move_to(pygame.mouse.get_pos())
        
        food_list.eat(player)
        # TODO: make the Opponent eat Food too
        food_list.eat(opponent)
        food_list.move()

        # Draw the game
        draw(game, player, opponent, food_list)


# Run the main function
if __name__ == "__main__":
    main()

