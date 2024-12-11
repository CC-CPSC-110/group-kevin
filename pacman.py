"""Manages Player state."""
import sys
from typing import List, Tuple
from dataclasses import dataclass
from character import Character

@dataclass
class Pacman(Character):
    lives: int
    boosted: bool
    score: int
    direction_command: int
    boost_timer: int

    def move_player(self, direction_command, turns, unit_width, unit_height, maze):
        """
        Purpose: Moves Pac-Man continuously on the grid while ensuring valid turns based on user input 
                 (via direction_command). Also handles snapping Pac-Man to the center of a tile when necessary.
        Examples:
            pacman = Pacman(x=50, y=50, size=20, speed=5.0, direction=0, ...)
            maze = [
                ["#", ".", "#"],
                [".", " ", "."],
                ["#", "#", "#"]
            ]
            pacman.move_player(direction_command=0, turns=[True, False, True, False], 
                               unit_width=20, unit_height=20, maze=maze)
            # Pac-Man moves right by its speed value if there are no walls in the way.
        """
        # Snap Pac-Man to the grid if near the center of a tile
        if self.direction == 0 or self.direction == 1:  # Horizontal movement
            self.y = round(self.y / unit_height) * unit_height
        elif self.direction == 2 or self.direction == 3:  # Vertical movement
            self.x = round(self.x / unit_width) * unit_width

        # Update direction if a valid turn is commanded
        if direction_command is not None and turns[direction_command]:
            self.direction = direction_command

        # Calculate the next position
        next_x, next_y = self.x, self.y
        if self.direction == 0:  # Moving right
            next_x += self.speed
        elif self.direction == 1:  # Moving left
            next_x -= self.speed
        elif self.direction == 2:  # Moving up
            next_y -= self.speed
        elif self.direction == 3:  # Moving down
            next_y += self.speed

        # Perform collision detection
        if not self.is_wall(next_x, next_y, unit_width, unit_height, maze):
            # Update position if no wall
            self.x, self.y = next_x, next_y

    def is_wall(self, x, y, unit_width, unit_height, maze):
        """
        Purpose: Checks if Pac-Man's next position collides with a wall ('#') or a restricted 
                 area ('D') in the maze.
        Examples:
            maze = [
                ["#", ".", "#"],
                [".", " ", "."],
                ["#", "D", "#"]
            ]
            pacman = Pacman(x=50, y=50, size=20, ...)
            pacman.is_wall(x=30, y=30, unit_width=20, unit_height=20, maze=maze) -> False
            pacman.is_wall(x=10, y=10, unit_width=20, unit_height=20, maze=maze) -> True
        """
        # Calculate grid position based on the center of Pac-Man's hitbox
        grid_x = int((x + self.size / 2) / unit_width)
        grid_y = int((y + self.size / 2) / unit_height)

        # Ensure grid indices are within bounds
        if 0 <= grid_y < len(maze) and 0 <= grid_x < len(maze[0]):
            cell = maze[grid_y][grid_x]
            return cell == '#' or cell == 'D'  # Treat 'D' as a wall for Pac-Man
        return True  # Treat out-of-bounds as walls

