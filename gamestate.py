"""Manages Game state."""
import sys
from typing import Dict
from dataclasses import dataclass, field
from functools import reduce
from datetime import datetime, timedelta
import pygame
import csv


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
    play_time: float
    timestamp: datetime = field(default_factory=datetime.now)
    
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
        with open(file_path, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['score', 'level'])
            writer.writerow([self.score, self.level])
            
    def load(self, file_path: str) -> Self:
        """Load the game state and reads from the game.csv"""
        with open(file_path, 'r') as file:
            reader = csv.reader(file)
            next(reader)
            row = next(reader)
            self.score = int(row[0])
            self.level = int(row[1])
            
        return self
    
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
        
# Helper functions using map, filter, and reduce
def highest_score(saved_games: GameLinkedList) -> int:
    """ Returns the highest score among all games. """
    scores = map(lambda game: game.score, saved_games.to_list())
    return reduce(lambda max_score, score: max(max_score, score), scores, 0)

def most_recent_game(saved_games: GameLinkedList) -> Game:
    """ Returns the most recent game based on the timestamp. """
    games = saved_games.to_list()
    return reduce(lambda recent, game: game if game.timestamp > recent.timestamp else recent, games) if games else None
    
    
    
            
