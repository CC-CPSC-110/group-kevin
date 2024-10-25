from dataclasses import dataclass
from character import Character

@dataclass
class Player(Character):
    name: str

    