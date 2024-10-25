from dataclasses import dataclass

@dataclass
class Character:
    x_postion: int
    y_position: int
    direction: tuple
    speed: float
    life_status: bool


