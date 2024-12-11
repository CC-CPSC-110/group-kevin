import pygame
import math

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
