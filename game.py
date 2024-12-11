"""Manages Game state."""
import sys
import os
from typing import Dict, Any, Tuple, List, Optional
from dataclasses import dataclass, field
import pygame
from datetime import datetime
from functools import reduce

# Get the Python version as a tuple
python_version = sys.version_info

if python_version >= (3, 11):
    # Import for Python 3.11 and above
    from typing import Self
else:
    # Import for Python versions below 3.11
    from typing_extensions import Self

@dataclass
class Game:
    """A game object represents all data necessary to run a game instance."""
    id: str
    screen: pygame.Surface
    clock: pygame.time.Clock
    keymap: Dict[str, str]
    background: str
    fps: float
    running: bool
    deltaT: float  # The delta time is the change in time in seconds since the last frame.
    unit_height: int
    unit_width: int
    font: Any
    score: int = 0
    timestamp: datetime = field(default_factory=datetime.now)  # Auto-set the current timestamp

    def __eq__(self, other: Self) -> bool:
        """ Checks if Games are equal. """
        return self.id == other.id
    
    def __lt__(self, other: Self) -> bool:
        """ Checks if Games' ids are less than the other. """
        return self.id < other.id
    
    def __gt__(self, other: Self) -> bool:
        """ Checks if Games' ids are greater than the other. """
        return self.id > other.id
    
    def __le__(self, other: Self) -> bool:
        """ Checks if Games' ids are less than or equal to the other. """
        return self.id <= other.id
    
    def __ge__(self, other: Self) -> bool:
        """ Checks if Games' ids are greater than or equal to the other. """
        return self.id >= other.id
    
    def update_timestamp(self):
        """Updates the timestamp to the current time."""
        self.timestamp = datetime.now()

    def tick(self) -> Self:
        """
        Purpose: Limits the FPS and updates the delta time (`deltaT`) for consistent physics
                 calculations, independent of frame rate.
        """
        self.deltaT = self.clock.tick(self.fps) / 1000
        return self

    def save(self, file_path: str, game_state: 'GameState') -> None:
        """
        Saves the current game state to a CSV file.
        """
        with open(file_path, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['score', 'level', 'timestamp', 'pacman_pos', 'ghost_positions', 'maze'])
            writer.writerow([
                self.score,
                self.level,
                self.timestamp.isoformat(),
                game_state.pacman_pos,
                {k: v for k, v in game_state.ghost_positions.items()},
                ["".join(row) for row in game_state.maze]
            ])

    def load(self, file_path: str) -> Tuple[Self, 'GameState']:
        """
        Loads a game state from a CSV file and returns it along with the GameState.
        """
        with open(file_path, 'r') as file:
            reader = csv.reader(file)
            next(reader)  # Skip header
            row = next(reader)
            self.score = int(row[0])
            self.level = int(row[1])
            self.timestamp = datetime.fromisoformat(row[2])
            pacman_pos = eval(row[3])
            ghost_positions = eval(row[4])
            maze = [list(row) for row in eval(row[5])]
        game_state = GameState(pacman_pos=pacman_pos, ghost_positions=ghost_positions, maze=maze)
        return self, game_state

@dataclass
class GameState:
    def __init__(self, pacman_pos: Tuple[int, int], ghost_positions: Dict[str, Tuple[int, int]], maze: List[List[str]], parent_action: str = None):
        """
        Purpose: Initializes the game state, including Pacman’s position, ghost positions,
                 the maze layout, and an optional parent action (useful for AI or debugging).
        Examples:
            pacman_pos = (5, 5)
            ghost_positions = {"ghost1": (10, 10), "ghost2": (15, 15)}
            maze = [["#", "#", "#"], ["#", ".", "#"], ["#", "#", "#"]]
            gs = GameState(pacman_pos, ghost_positions, maze, parent_action="move_left")
        """
        self.pacman_pos = pacman_pos
        self.ghost_positions = ghost_positions
        self.maze = maze
        self.parent_action = parent_action

    def copy(self) -> 'GameState':
        """
        Purpose: Creates a deep copy of the current game state, preserving all attributes 
                 for immutability and isolation of operations.
        Examples:
            original_state = GameState((5, 5), {"ghost1": (10, 10)}, [["#", ".", "#"]])
            state_copy = original_state.copy()
        """
        return GameState(
            pacman_pos=self.pacman_pos,
            ghost_positions=deepcopy(self.ghost_positions),
            maze=self.maze,
            parent_action=self.parent_action
        )

@dataclass
class GameNode:
    """ A node in the linked list representing a saved game state. """
    game: Game
    next: Self = None

@dataclass
class GameLinkedList:
    """ A linked list to store and amanage saved game states. """
    head: GameNode = None
    
    def insert(self, game: Game) -> None:
        """ Inserts a new saved game state at the beginning of the list """
        new_node = GameNode(game=game, next=self.head)
        self.head = new_node
        
    def to_list(self) -> list:
        """ Converts the linked list to a list for easier operations """
        current = self.head
        games = []
        while current:
            games.append(current.game)
            current = current.next
        return games

# Using selection sort to sort through Games
def min_index(log: List[Game]) -> int:
    """
    Purpose: Find the index of the minimum values of the list of Games
    Assume: List is non-empty
    Examples:
        min_index([
            Game("1", pygame.Surface((800, 600)), 500 ...),
            Game("2", pygame.Surface((800,600)), 650 ...)]) -> 0
    """
    minimum_value = log[0]
    minimum_index = 0
    for i in range(1, len(log)):
        if log[i] < minimum_value:
            minimum_value = log[i]
            minimum_index = i
    return minimum_index

def swap(log: List[Game], i: int, j:  int) -> List[Game]:
    """
    Purpose: Swap the values at the given indices
    Assume: List is non-empty, indices < len(list)
    Examples:
        swap([
            Game("1", pygame.Surface((800, 600)), 500 ...),
            Game("2", pygame.Surface((800,600)), 650 ...)], 0, 1) ->
            [Game("2", pygame.Surface((800,600)), 650 ...),
            Game("1", pygame.Surface((800, 600)), 500 ...)]
    """
    log[i], log[j] = log[j], log[i]
    return log

def selection_sort_games(log: List[Game]) -> List[Game]:
    """
    Purpose: Sort a list of games
    Examples:
        selection_sort_games([
            Game("2", pygame.Surface((800,600)), 650 ...),
            Game("3", pygame.Surface((800, 600)), 500 ...),
            Game("1", pygame.Surface((800, 600)), 500 ...)]) ->
            [Game("1", pygame.Surface((800, 600)), 500 ...),
            Game("2", pygame.Surface((800,600)), 650 ...),
            Game("3", pygame.Surface((800, 600)), 500 ...)]
    """
    for i in range(len(log)):
        min_i = i + min_index(log[i:])
        log = swap(log, i, min_i)
    return log

# Helper functions using map, filter, and reduce
def highest_score(saved_games: GameLinkedList) -> int:
    """ Returns the highest score among all games. """
    scores = map(lambda game: game.score, saved_games.to_list())
    return reduce(lambda max_score, score: max(max_score, score), scores, 0)

def most_recent_game(saved_games: GameLinkedList) -> Game:
    """ Returns the most recent game based on the timestamp. """
    games = saved_games.to_list()
    return reduce(lambda recent, game: game if game.timestamp > recent.timestamp else recent, games) if games else None

# Helper function for loading and saving scores
def load_high_score(file_path: str) -> int:
    """
    Load the high score from a file. If the file does not exist, return 0.
    """
    if not os.path.exists(file_path):
        return 0
    try:
        with open(file_path, 'r') as file:
            return int(file.read().strip())
    except ValueError:
        return 0  # Default to 0 if the file is corrupted or empty

def save_high_score(file_path: str, high_score: int):
    """
    Save the high score to a file.
    """
    try:
        with open(file_path, 'w') as file:
            file.write(str(high_score))
    except IOError as e:
        print(f"Error saving high score: {e}")

# Helper functions for parsing
def parse_maze(lines: List[str]) -> List[List[str]]:
    """
    Purpose: Converts a list of strings representing the maze into a 2D grid of characters.
    Examples:
        lines = ["###", "#. ", "###"]
        maze = parse_maze(lines)
        # maze -> [["#", "#", "#"], ["#", ".", " "], ["#", "#", "#"]]
    """
    maze = []
    for line in lines:
        cells = list(line)  # Each character represents a cell
        maze.append(cells)
    return maze


def parse_positions(lines: List[str]) -> Tuple[Optional[Tuple[int, int]], Dict[str, Tuple[int, int]]]:
    """
    Purpose: Parses Pacman and ghost positions from a list of strings.
    Examples:
        lines = ["PacmanPos 1 1", "GhostPos ghost1 2 2"]
        pacman_pos, ghost_positions = parse_positions(lines)
        # pacman_pos -> (1, 1)
        # ghost_positions -> {"ghost1": (2, 2)}
    """
    pacman_pos = None
    ghost_positions = {}
    for line in lines:
        if not line.strip():
            continue  # Skip empty lines
        parts = line.strip().split()
        if parts[0] == "PacmanPos":
            if len(parts) != 3:
                raise ValueError(f"Invalid PacmanPos line: {line}")
            pacman_pos = (int(parts[1]), int(parts[2]))
        elif parts[0] == "GhostPos":
            if len(parts) != 4:
                raise ValueError(f"Invalid GhostPos line: {line}")
            ghost_id = parts[1]
            ghost_positions[ghost_id] = (int(parts[2]), int(parts[3]))
        else:
            # Start of maze layout
            break
    return pacman_pos, ghost_positions

def parse_game_state_from_txt(file_path: str) -> GameState:
    """
    Purpose: Reads a TXT file to initialize a game state, including Pacman’s position, ghost
             positions, and the maze layout.
    Examples:
        game_state = parse_game_state_from_txt("game_state.txt")
    """
    with open(file_path, 'r') as file:
        lines = file.readlines()

    # Separate position definitions from maze layout
    positions_lines = []
    maze_lines = []
    maze_started = False
    for line in lines:
        if not line.strip():
            maze_started = True
            continue
        if not maze_started:
            positions_lines.append(line)
        else:
            maze_lines.append(line.rstrip('\n'))

    # Parse positions
    pacman_pos, ghost_positions = parse_positions(positions_lines)

    if pacman_pos is None:
        raise ValueError("Pacman position not found in TXT file.")

    # Parse maze
    maze = parse_maze(maze_lines)

    # Verify maze consistency
    verify_maze_consistency(maze)

    return GameState(
        pacman_pos=pacman_pos,
        ghost_positions=ghost_positions,
        maze=maze
    )

def verify_maze_consistency(maze: List[List[str]]):
    """
    Purpose: Validates the consistency of the maze structure by ensuring all rows are of the 
             same length. This is critical to maintain the integrity of game logic and rendering.
    Examples:
        maze = [["#", "#", "#"], [".", " ", "#"], ["#", "#", "#"]]
        verify_maze_consistency(maze)
        # No error is raised since all rows are the same length.

        invalid_maze = [["#", "#"], ["#", ".", "#"], ["#", "#"]]
        verify_maze_consistency(invalid_maze)
        # Raises ValueError: Maze row 1 length 3 doesn't match expected 2.
    """
    if not maze:
        raise ValueError("Maze is empty.")
    expected_length = len(maze[0])
    for idx, row in enumerate(maze):
        if len(row) != expected_length:
            raise ValueError(f"Maze row {idx} length {len(row)} doesn't match expected {expected_length}.")


# Helper functions for drawing
HEIGHT = 900  # Increased from 870 to 900 to accommodate UI elements
WIDTH = 760

high_score_file = "high_score.txt"
high_score = load_high_score(high_score_file)

def display_message(screen, font, message: str):
    """Displays a message in the center of the screen. """
    # Set up the background rectangle for the message
    rect_width, rect_height = 600, 300
    rect_x = (screen.get_width() - rect_width) // 2
    rect_y = (screen.get_height() - rect_height) // 2
    pygame.draw.rect(screen, 'white', [rect_x, rect_y, rect_width, rect_height], 0, 10)
    pygame.draw.rect(screen, 'grey', [rect_x, rect_y, rect_width, rect_height], 10, 8)
    
    # Render the message text
    text = font.render(message, True, 'black')
    text_rect = text.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2))
    
    # Display the text on the screen
    screen.blit(text, text_rect)
    pygame.display.flip()  # Update the display
    
    # Pause for 3 seconds to allow the user to see the message
    pygame.time.delay(3000)

def draw_board(screen, maze, score, font, lives, high_score):
    """
    Purpose: Draws the maze, score, and remaining lives on the game screen. 
             Each cell in the maze is rendered based on its type (e.g., walls, dots, power-ups).
    Examples:
        maze = [["#", ".", " "], ["o", " ", "#"], ["#", "D", "#"]]
        draw_board(screen, maze, score=100, font=font, lives=3, highscore=)
        # Renders the maze, updates the score display, and shows remaining lives.
    """
    num_rows = len(maze)
    num_cols = len(maze[0]) if num_rows > 0 else 0
    unit_height = (HEIGHT - 50) // num_rows  # Subtracting space for UI
    unit_width = WIDTH // num_cols
    
    for y in range(num_rows):
        for x in range(num_cols):
            cell = maze[y][x]
            if cell == '#':
                pygame.draw.rect(screen, 'blue', (x * unit_width, y * unit_height, unit_width, unit_height), 0, 8)
                pygame.draw.rect(screen, 'grey', (x * unit_width, y * unit_height, unit_width, unit_height), 3, 8)
            elif cell == '.':
                center_x = int(x * unit_width + 0.5 * unit_width)
                center_y = int(y * unit_height + 0.5 * unit_height)
                pygame.draw.circle(screen, 'white', (center_x, center_y), 4)
            elif cell == 'o':
                center_x = int(x * unit_width + 0.5 * unit_width)
                center_y = int(y * unit_height + 0.5 * unit_height)
                pygame.draw.circle(screen, 'white', (center_x, center_y), 10)
            elif cell == 'D':
                pygame.draw.rect(screen, 'orange', (x * unit_width, y * unit_height, unit_width, unit_height), 0, 8)  # Orange door
            elif cell == ' ':
                # Empty space; no drawing needed
                pass

    # Draw score
    score_text = font.render(f'Score: {score}', True, 'white')
    screen.blit(score_text, (10, HEIGHT - 35))
    
    # Draw high score
    high_score_text = font.render(f'High Score: {high_score}', True, 'white')
    screen.blit(high_score_text, (10, HEIGHT - 70))  

    # Draw lives
    for i in range(lives):
        try:
            life_img = pygame.transform.scale(pygame.image.load('assets/pacman_images/1.png'), (30, 30))
            screen.blit(life_img, (WIDTH - 100 + i * 40, HEIGHT - 35))
        except pygame.error as e:
            print(f"Error loading life image: {e}")
            # If life image not found, draw a simple circle
            pygame.draw.circle(screen, 'yellow', (WIDTH - 100 + i * 40 + 15, HEIGHT - 35 + 15), 15)
    
def draw_player(screen, pacman_x, pacman_y, size, direction, counter):
    """
    Purpose: Draws Pacman at the given position with directional animation determined by 
             the counter (frame-based animation).
    Examples:
        draw_player(screen, pacman_x=100, pacman_y=150, size=30, direction=1, counter=20)
        # Draws Pacman facing left (direction=1) at the specified position with the 
        # appropriate animation frame.
    """
    pacman_images = []
    try:
        for i in range(1, 5):
            pacman_images.append(pygame.transform.scale(pygame.image.load(f'assets/pacman_images/{i}.png'), (size, size)))
    except pygame.error as e:
        print(f"Error loading Pacman images: {e}")
        # If Pacman images not found, use a placeholder
        pacman_images = [pygame.Surface((size, size), pygame.SRCALPHA) for _ in range(4)]
        for img in pacman_images:
            pygame.draw.circle(img, 'yellow', (size // 2, size // 2), size // 2)

    img = pacman_images[counter // 10 % len(pacman_images)]
    if direction == 0:  # right
        screen.blit(img, (pacman_x, pacman_y))
    elif direction == 1:  # left
        screen.blit(pygame.transform.flip(img, True, False), (pacman_x, pacman_y))
    elif direction == 2:  # up
        screen.blit(pygame.transform.rotate(img, 90), (pacman_x, pacman_y))
    elif direction == 3:  # down
        screen.blit(pygame.transform.rotate(img, 270), (pacman_x, pacman_y))

def check_collisions_and_update_maze(pacman, maze):
    """
    Purpose: Detects collisions between Pacman and maze elements (e.g., dots, power-ups),
             updating Pacman’s score and attributes while modifying the maze as needed.
    Examples:
        pacman = Pacman(x=50, y=50, size=30, score=0, boosted=False, boost_timer=0)
        maze = [["#", ".", " "], ["o", " ", " "], ["#", "#", "#"]]
        check_collisions_and_update_maze(pacman, maze)
        # If Pacman eats a dot ('.'), the score is incremented, and the maze cell is cleared.
        # If Pacman eats a power-up ('o'), boosted mode is activated, and the boost timer starts.
    """
    num_rows = len(maze)
    num_cols = len(maze[0]) if num_rows > 0 else 0
    unit_height = (HEIGHT - 50) // num_rows
    unit_width = WIDTH // num_cols
    center_x = pacman.x + pacman.size // 2
    center_y = pacman.y + pacman.size // 2
    maze_x = center_x // unit_width
    maze_y = center_y // unit_height

    if 0 <= maze_y < len(maze) and 0 <= maze_x < len(maze[0]):
        cell = maze[maze_y][maze_x]
        if cell == '.':
            pacman.score += 1
            maze[maze_y][maze_x] = ' '
        elif cell == 'o':
            pacman.score += 2
            pacman.boosted = True
            pacman.boost_timer = 0
            maze[maze_y][maze_x] = ' '