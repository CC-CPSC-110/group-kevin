from dataclasses import dataclass

@dataclass
class Player:
    x : int
    y : int
    hp : int
    atk : int
    name: str

    