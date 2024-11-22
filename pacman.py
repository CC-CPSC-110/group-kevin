from dataclasses import dataclass
from character import Character
from typing import List, Self

@dataclass
class Pacman(Character):
    lives: int
    boosted: bool

    def move(self, deltaT: float, dirs: List[str]) -> Self:
        """
        Purpose: Moves a player by speed per change in time in given directions.
        Examples:
            player = Pacman(x=100, y=100, size=10, speed=10, color="red")
            move(player, 10, ["UP"])    -> Player(100,   0, 10, 10, "red")
            move(player, 10, ["DOWN"])  -> Player(100, 200, 10, 10, "red")
            move(player, 10, ["RIGHT"]) -> Player(200, 100, 10, 10, "red")
            move(player, 10, ["LEFT"])  -> Player(  0, 100, 10, 10, "red")

        """
        amount = self.speed * deltaT
        # we index from the top left so negative-y direction is up
        if "UP" in dirs:
            self.y -= amount 
        if "DOWN" in dirs:
            self.y += amount
        if "LEFT" in dirs:
            self.x -= amount
        if "RIGHT" in dirs:
            self.x += amount
        return self