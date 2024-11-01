"""Manages Game state."""
import sys
from typing import Dict
from dataclasses import dataclass
import pygame

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
    """"A game object represents all data necessary to run a game instance."""

    screen: pygame.Surface
    score: int
    level: int
    fps: float
    running: bool
    background: str
    clock: pygame.time.Clock
    keymap: Dict[str, str]
    deltaT: float
    
    def tick(self) -> Self:
        """
        Purpose: Limits FPS. Used for framerate-independent physics.
        Examples:
            game.deltaT -> game.clock.tick(game.fps) / 1000
        """
        self.deltaT = self.clock.tick(self.fps) / 1000
        return self

    def save(self, file_path: str) -> None:
        """Saves the current game state and writes to the game.csv"""
        pass # stub

    def load(self, file_path: str) -> Self:
        """Load the game state and reads from the game.csv"""
        return self # stub
