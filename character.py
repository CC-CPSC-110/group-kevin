""" Manages Character class. """
from dataclasses import dataclass
from typing import List

@dataclass
class Character:
    x: int
    y: int
    size: int
    speed: float
    counter: int
    direction: int
    turns: List[bool]
