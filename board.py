""" Board functions. """

import pygame
import math
from typing import List, Tuple

#0 - empty
#1 - small pellets
#2 - large pellets
#3 - verticle wall
#4 - ghost gate

boards = [
    [3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3],
    [3, 2, 2, 2, 2, 2, 2, 2, 2, 3, 2, 2, 2, 2, 2, 2, 2, 2, 3],
    [3, 1, 3, 3, 2, 3, 3, 3, 2, 3, 2, 3, 3, 3, 2, 3, 3, 1, 3],
    [3, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 3],
    [3, 2, 3, 3, 2, 3, 2, 3, 3, 3, 3, 3, 2, 3, 2, 3, 3, 2, 3],
    [3, 2, 2, 2, 2, 3, 2, 2, 2, 3, 2, 2, 2, 3, 2, 2, 2, 2, 3],
    [3, 3, 3, 3, 2, 3, 3, 3, 0, 3, 0, 3, 3, 3, 2, 3, 3, 3, 3],
    [0, 0, 0, 3, 2, 3, 0, 0, 0, 0, 0, 0, 0, 3, 2, 3, 0, 0, 0],
    [3, 3, 3, 3, 2, 3, 0, 3, 3, 3, 3, 3, 0, 3, 2, 3, 3, 3, 3],
    [3, 0, 0, 0, 2, 0, 0, 3, 0, 0, 0, 4, 0, 0, 2, 0, 0, 0, 3],
    [3, 3, 3, 3, 2, 3, 0, 3, 3, 3, 3, 3, 0, 3, 2, 3, 3, 3, 3],
    [0, 0, 0, 3, 2, 3, 0, 0, 0, 0, 0, 0, 0, 3, 2, 3, 0, 0, 0],
    [3, 3, 3, 3, 2, 3, 0, 3, 3, 3, 3, 3, 0, 3, 2, 3, 3, 3, 3],
    [3, 2, 2, 2, 2, 2, 2, 2, 2, 3, 2, 2, 2, 2, 2, 2, 2, 2, 3],
    [3, 2, 3, 3, 2, 3, 3, 3, 2, 3, 2, 3, 3, 3, 2, 3, 3, 2, 3],
    [3, 1, 2, 3, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 3, 2, 1, 3],
    [3, 3, 2, 3, 2, 3, 2, 3, 3, 3, 3, 3, 2, 3, 2, 3, 2, 3, 3],
    [3, 2, 2, 2, 2, 3, 2, 2, 2, 3, 2, 2, 2, 3, 2, 2, 2, 2, 3],
    [3, 2, 3, 3, 3, 3, 3, 3, 2, 3, 2, 3, 3, 3, 3, 3, 3, 2, 3],
    [3, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 3],
    [3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3],
]


pygame.init()
WIDTH = 900
HEIGHT = 950
screen = pygame.display.set_mode([WIDTH, HEIGHT])
timer = pygame.time.Clock()
fps = 60
font = pygame.font.Font('freesansbold.ttf', 20)
level = boards
color = 'blue'
PI = math.pi
flicker = False


def draw_board():
    num1 = ((HEIGHT - 50) // 21)
    num2 = (WIDTH // 19)
    for i in range(len(level)):
        for j in range(len(level[i])):
            if level[i][j] == 1:
                pygame.draw.circle(screen, 'white', (j * num2 + (0.5 * num2), i * num1 + (0.5 * num1)), 4)
            if level[i][j] == 2 and not flicker:
                pygame.draw.circle(screen, 'white', (j * num2 + (0.5 * num2), i * num1 + (0.5 * num1)), 10)
            if level[i][j] == 3:
                pygame.draw.line(screen, color, (j * num2 + (0.5 * num2), i * num1),
                                 (j * num2 + (0.5 * num2), i * num1 + num1), 3)
            if level[i][j] == 4:
                pygame.draw.line(screen, 'white', (j * num2, i * num1 + (0.5 * num1)),
                                 (j * num2 + num2, i * num1 + (0.5 * num1)), 3)
                
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
