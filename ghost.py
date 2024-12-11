""" Manages Ghost class. """
from dataclasses import dataclass
from typing import List, Any, Tuple, Dict, Optional
import pygame
import random
from copy import deepcopy
from collections import deque, defaultdict
from game import *
from character import Character

@dataclass
class Ghost(Character):
    dead: bool
    img: Any
    id: int
    in_box: bool
    respawn_timer: int = 0

    scared_img: Any = pygame.transform.scale(pygame.image.load('assets/ghost_images/scared.png'), (40, 40))
    dead_img: Any = pygame.transform.scale(pygame.image.load('assets/ghost_images/dead.png'), (40, 40))

    def draw_ghost(self, screen, boosted, eaten_ghosts, unit_width, unit_height):
        """
        Purpose: Renders the ghost on the screen, choosing its image based on its state:
                 normal, frightened, or dead.
        Examples:
            ghost = Ghost(x=100, y=200, size=40, speed=2.0, counter=0, dead=False, direction=0, img=img, id=1, turns=[], in_box=False)
            ghost.draw_ghost(screen, boosted=True, eaten_ghosts={"1": False}, unit_width=30, unit_height=30)
        """
        if (not boosted and not self.dead) or (eaten_ghosts[self.id] and boosted and not self.dead):
            screen.blit(self.img, (self.x, self.y))
        elif boosted and not self.dead and not eaten_ghosts[self.id]:
            screen.blit(self.scared_img, (self.x, self.y))
        else:
            screen.blit(self.dead_img, (self.x, self.y))
        
        ghost_hitbox = pygame.rect.Rect((self.x, self.y), (unit_width, unit_height))
        return ghost_hitbox

    def check_collisions(self, cx, cy, unit_width, unit_height, maze):
        """
        Purpose: Determines which directions the ghost can move based on its current position
                 and the maze structure.
        Examples:
            maze = [
                ["#", ".", "#"],
                [".", " ", "."],
                ["#", "#", "#"]
            ]
            ghost = Ghost(...)
            ghost.check_collisions(cx=30, cy=30, unit_width=10, unit_height=10, maze=maze)
        """
        valid = get_valid_moves(maze, (cx // unit_width, cy // unit_height))
        turns = [False, False, False, False]  # [right, left, up, down]
        # direction mapping: 0:right, 1:left, 2:up, 3:down
        if (cx // unit_width + 1, cy // unit_height) in valid:
            turns[0] = True
        if (cx // unit_width - 1, cy // unit_height) in valid:
            turns[1] = True
        if (cx // unit_width, cy // unit_height - 1) in valid:
            turns[2] = True
        if (cx // unit_width, cy // unit_height + 1) in valid:
            turns[3] = True

        in_box = False
        return turns, in_box

@dataclass
class EatenGhostList:
    eaten_ghosts: Dict[str, bool]

    def __getitem__(self, ghost_id: str) -> bool:
        """
        Purpose: Provides dictionary-like access to check if a ghost has been eaten.
        Examples:
            egl = EatenGhostList(eaten_ghosts={"ghost1": True, "ghost2": False})
            egl["ghost1"] -> True
            egl["ghost2"] -> False
        """
        return self.eaten_ghosts.get(ghost_id, False)

    def __setitem__(self, ghost_id: str, value: bool) -> None:
        """
        Purpose: Provides dictionary-like functionality to update a ghost's eaten status.
        Examples:
            egl = EatenGhostList(eaten_ghosts={})
            egl["ghost1"] = True  # Updates the status of "ghost1"
        """
        self.eaten_ghosts[ghost_id] = value

def is_valid_position(maze: List[List[str]], pos: Tuple[int, int]) -> bool:
    """
    Purpose: Checks if the given position in the maze is valid, ensuring it is within bounds,
             not a wall ('#'), and represented by integer coordinates.
    Examples:
        maze = [
            ["#", ".", "#"],
            [".", " ", "."],
            ["#", "#", "#"]
        ]
        is_valid_position(maze, (1, 1)) -> True  # Valid position (not a wall)
        is_valid_position(maze, (0, 0)) -> False  # Invalid position (wall)
        is_valid_position(maze, (3, 3)) -> False  # Invalid position (out of bounds)
    """
    x, y = pos
    x = int(x)
    y = int(y)
    
    if x < 0 or y < 0 or y >= len(maze) or x >= len(maze[0]):
        return False
    return maze[y][x] != '#'


def get_valid_moves(maze: List[List[str]], current_pos: Tuple[int, int]) -> List[Tuple[int, int]]:
    """
    Purpose: Computes all valid moves (adjacent positions) from the current position in the maze.
             Valid moves are determined by the `is_valid_position` function.
    Examples:
        maze = [
            ["#", ".", "#"],
            [".", " ", "."],
            ["#", "#", "#"]
        ]
        get_valid_moves(maze, (1, 1)) -> [(1, 2), (1, 0)]  # Down and Up are valid moves
    """
    directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]  # Down, Up, Right, Left
    moves = []
    for dx, dy in directions:
        new_pos = (current_pos[0] + dx, current_pos[1] + dy)
        if is_valid_position(maze, new_pos):
            moves.append(new_pos)
    return moves


def bfs_shortest_path(maze: List[List[str]], start: Tuple[int, int], goal: Tuple[int, int]) -> Optional[List[Tuple[int, int]]]:
    """
    Purpose: Finds the shortest path between the `start` and `goal` positions in the maze
             using the Breadth-First Search (BFS) algorithm.
    Examples:
        maze = [
            ["#", ".", "#"],
            [".", " ", "."],
            ["#", ".", "#"]
        ]
        bfs_shortest_path(maze, (1, 0), (1, 2)) -> [(1, 0), (1, 1), (1, 2)]
        bfs_shortest_path(maze, (0, 0), (2, 2)) -> None  # No valid path exists
    """
    if not is_valid_position(maze, start):
        return None
    if not is_valid_position(maze, goal):
        return None
    if start == goal:
        return [start]

    queue = deque()
    queue.append([start])
    visited = set([start])

    while queue:
        path = queue.popleft()
        current = path[-1]

        for neighbor in get_valid_moves(maze, current):
            if neighbor == goal:
                return path + [neighbor]
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(path + [neighbor])
    return None

def move_ghost_towards_tile(ghost, target_tile, unit_width, unit_height, deltaT):
    """
    Purpose: Moves the ghost incrementally towards the specified target tile based on its 
             speed and the elapsed time (`deltaT`). Stops once the ghost reaches the tile.
    Examples:
        ghost = Ghost(x=50, y=50, size=40, speed=2.0, ...)
        move_ghost_towards_tile(ghost, (5, 5), unit_width=20, unit_height=20, deltaT=0.016)
        # Ghost moves closer to tile (5, 5) at a rate determined by its speed and `deltaT`.
    """
    target_x = target_tile[0] * unit_width
    target_y = target_tile[1] * unit_height

    dx = target_x - ghost.x
    dy = target_y - ghost.y
    dist = (dx**2 + dy**2)**0.5

    if dist < 1:
        ghost.x = target_x
        ghost.y = target_y
        return True  # Reached the tile

    pixels_per_second = ghost.speed * unit_width
    step = pixels_per_second * deltaT

    if step > dist:
        step = dist

    ghost.x += (dx / dist) * step
    ghost.y += (dy / dist) * step

    return False


class GhostStrategy:
    """
    Purpose: Abstract base class for ghost AI strategies. Subclasses must implement the 
             `get_next_position` method to define ghost behavior.
    """
    def get_next_position(self, state: GameState, ghost_id: str) -> Tuple[int, int]:
        raise NotImplementedError


class RandomGhostStrategy(GhostStrategy):
    """
    Purpose: Implements a random movement strategy for ghosts, ensuring they don't revisit 
             recent positions to avoid repetitive behavior.
    Examples:
        strategy = RandomGhostStrategy(history_length=3)
        next_pos = strategy.get_next_position(state, ghost_id="ghost1")
        # Returns a random valid position near the current position.
    """
    def __init__(self, history_length: int = 3):
        self.history_length = history_length
        self.position_history: Dict[str, List[Tuple[int, int]]] = defaultdict(list)

    def get_next_position(self, state: GameState, ghost_id: str) -> Tuple[int, int]:
        current_pos = state.ghost_positions[ghost_id]
        valid_moves = get_valid_moves(state.maze, current_pos)

        # Ensure valid_moves doesn't allow diagonal movement
        valid_moves = [move for move in valid_moves if self.is_straight_move(current_pos, move)]

        if not valid_moves:
            return current_pos

        recent_positions = self.position_history[ghost_id]
        filtered_moves = [m for m in valid_moves if m not in recent_positions]

        chosen = random.choice(filtered_moves) if filtered_moves else random.choice(valid_moves)
        recent_positions.append(chosen)
        if len(recent_positions) > self.history_length:
            recent_positions.pop(0)

        return chosen

    def is_straight_move(self, current_pos: Tuple[int, int], next_pos: Tuple[int, int]) -> bool:
        """
        Purpose: Checks if the move is a straight (non-diagonal) move.
        Examples:
            current_pos = (2, 2)
            next_pos = (3, 2)
            is_straight_move(current_pos, next_pos) -> True
            is_straight_move((2, 2), (3, 3)) -> False
        """
        dx = abs(current_pos[0] - next_pos[0])
        dy = abs(current_pos[1] - next_pos[1])
        return (dx == 1 and dy == 0) or (dx == 0 and dy == 1)


class ChasingGhostStrategy(GhostStrategy):
    """
    Purpose: Implements a chasing strategy where the ghost calculates the shortest path to Pacman 
             using BFS and moves along that path.
    Examples:
        strategy = ChasingGhostStrategy()
        next_pos = strategy.get_next_position(state, ghost_id="ghost2")
        # Returns the next position along the shortest path to Pacman.
    """
    def get_next_position(self, state: GameState, ghost_id: str) -> Tuple[int, int]:
        current_pos = state.ghost_positions[ghost_id]
        pacman_pos = state.pacman_pos

        if current_pos == pacman_pos:
            return current_pos

        path = bfs_shortest_path(state.maze, current_pos, pacman_pos)
        if not path or len(path) < 2:
            return current_pos
        return path[1]


class PalletHoveringGhostStrategy(GhostStrategy):
    """
    Purpose: Implements a strategy where the ghost hovers near pellets, aiming to protect them 
             and impede Pacman's progress.
    Examples:
        strategy = PalletHoveringGhostStrategy()
        next_pos = strategy.get_next_position(state, ghost_id="ghost3")
        # Returns a position near the pellet or moves towards a new target pellet.
    """
    def __init__(self):
        self.target_pellet: Optional[Tuple[int, int]] = None
        self.hover_positions: List[Tuple[int, int]] = []

    def get_next_position(self, state: GameState, ghost_id: str) -> Tuple[int, int]:
        current_pos = state.ghost_positions[ghost_id]
        maze = state.maze

        # Find the nearest pellet if no target
        if not self.target_pellet or not self.is_pellet_present(maze, self.target_pellet):
            self.target_pellet = self.find_nearest_pellet(maze, current_pos)

        if not self.target_pellet:
            valid_moves = get_valid_moves(maze, current_pos)
            return random.choice(valid_moves) if valid_moves else current_pos

        self.hover_positions = self.get_hover_positions(maze, self.target_pellet)

        if current_pos in self.hover_positions:
            # Hover around the pellet
            index = self.hover_positions.index(current_pos)
            next_pos = self.hover_positions[(index + 1) % len(self.hover_positions)]
            if is_valid_position(maze, next_pos):
                return next_pos
            return current_pos
        else:
            # Move towards hover positions
            path = bfs_shortest_path(maze, current_pos, self.target_pellet)
            return path[1] if path and len(path) > 1 else current_pos

    def find_nearest_pellet(self, maze: List[List[str]], start: Tuple[int, int]) -> Optional[Tuple[int, int]]:
        """
        Purpose: Finds the nearest pellet ('o') in the maze from the given start position using BFS.
        Examples:
            maze = [["#", ".", "o"], [".", " ", "#"], ["#", ".", "#"]]
            find_nearest_pellet(maze, (0, 0)) -> (0, 2)
        """
        visited = set([start])
        queue = deque([start])
        while queue:
            current = queue.popleft()
            x, y = int(current[0]), int(current[1])  # Ensure integer indices
            if maze[y][x] == 'o':  # Check if this is a pellet
                return current
            for move in get_valid_moves(maze, (x, y)):
                if move not in visited:
                    visited.add(move)
                    queue.append(move)
        return None

    def is_pellet_present(self, maze: List[List[str]], pellet: Tuple[int, int]) -> bool:
        """
        Purpose: Checks if a pellet ('o') exists at the specified location in the maze.
        Examples:
            maze = [["#", ".", "o"], [".", " ", "#"], ["#", ".", "#"]]
            is_pellet_present(maze, (0, 2)) -> True
            is_pellet_present(maze, (1, 1)) -> False
        """
        x, y = pellet
        return 0 <= y < len(maze) and 0 <= x < len(maze[0]) and maze[y][x] == 'o'

    def get_hover_positions(self, maze: List[List[str]], pellet: Tuple[int, int]) -> List[Tuple[int, int]]:
        """
        Purpose: Generates a list of valid positions surrounding a pellet for hovering behavior.
        Examples:
            pellet = (1, 1)
            maze = [["#", ".", "#"], [".", "o", "."], ["#", ".", "#"]]
            get_hover_positions(maze, pellet) -> [(0, 1), (2, 1), (1, 0), (1, 2)]
        """
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        x, y = pellet
        potential_positions = [(x + dx, y + dy) for dx, dy in directions]
        return [pos for pos in potential_positions if is_valid_position(maze, pos)]