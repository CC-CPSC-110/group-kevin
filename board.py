""" Board functions. """
from typing import List, Tuple


def is_valid_position(maze: List[List[str]], pos: Tuple[int, int]) -> bool:
    """
    Purpose: Checks whether a given position in the maze is valid and accessible. 
             A position is invalid if it is out of bounds or occupied by a wall ('#').
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
    if y < 0 or y >= len(maze) or x < 0 or x >= len(maze[0]):
        return False
    return maze[y][x] != '#'


def get_valid_moves(maze: List[List[str]], current_pos: Tuple[int, int]) -> List[Tuple[int, int]]:
    """
    Purpose: Returns a list of valid positions to which a player or entity can move 
             from the current position. Movement is restricted to adjacent cells that are 
             not walls ('#') and within maze boundaries.
    Examples:
        maze = [
            ["#", ".", "#"],
            [".", " ", "."],
            ["#", "#", "#"]
        ]
        get_valid_moves(maze, (1, 1)) -> [(1, 2), (1, 0)]  # Down, Up, Right, Left checked
        get_valid_moves(maze, (0, 0)) -> []  # No valid moves from wall
    """
    directions_list = [(0, 1), (0, -1), (1, 0), (-1, 0)]  # Down, Up, Right, Left
    moves = []
    for dx, dy in directions_list:
        new_pos = (current_pos[0] + dx, current_pos[1] + dy)
        if is_valid_position(maze, new_pos):
            moves.append(new_pos)
    return moves
