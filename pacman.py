from dataclasses import dataclass
from character import Character
from typing import List
import pygame

@dataclass
class Pacman(Character):
    lives: int
    boosted: bool
    direction: int
    
    def move(self):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    self.x_position += self.speed
                    self.direction = 0
                if event.key == pygame.K_LEFT:
                    self.direction = 1
                    self.x_position -= self.speed
                if event.key == pygame.K_UP:
                    self.direction = 2
                    self.y_position -= self.speed
                if event.key == pygame.K_DOWN:
                    self.direction = 3
                    self.y_position += self.speed