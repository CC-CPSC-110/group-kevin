from dataclasses import dataclass
from typing import List
from wall import *
from pellet import *
from powerpellet import *


@dataclass
class Maze:
    walls: List[Wall]
    pellets: List[Pellet]
    power_pellets: List[PowerPellet]
