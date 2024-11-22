from dataclasses import dataclass
from typing import List
import os

@dataclass
class PacmanTyped:
    x_position: int
    y_position: int
    speed: int
    lives: int
    boosted: bool
    direction: int


def parse_row_to_pacman(row: str) -> PacmanTyped:
    """
    Purpose: Convert a comma-separated string row into a Pacman instance.
    Example:
        parse_row_to_pacman("x_position, y_position, speed, lives, boosted") 
            -> PacmanTyped(x_position = 500, y_position = 500, speed = 2, int = 3, boosted = "False")
    """
    columns = row.split(',')

    # Manually parsing each field
    x_position = int(columns[0])
    y_position = int(columns[1])
    speed = int(columns[2])
    lives = int(columns[3])
    boosted = columns[4]
    direction = int(columns[5])

    # Return a PacmanTyped instance
    return PacmanTyped(
        x_position = x_position,
        y_position = y_position,
        speed = speed,
        lives = lives,
        boosted = boosted,
        direction = direction
    )
# Helper function to parse all rows
def parse_pacman(rows: List[str]) -> List[PacmanTyped]:
    """
    Purpose: Parse multiple rows of route data into a list of PacmanTyped instances.
    Example:
        parse_pacman([
            "500, 500, 2, 3, False"
        ]) -> [PacmanTyped(...), PacmanTyped(...)]
    """
    return [parse_row_to_pacman(row) for row in rows]


def query_pacman(pacman: list[PacmanTyped], **filters) -> list[PacmanTyped]:
    """
    Purpose: Query the list of characters based on filters such as x_position, y_position, speed, boosted.
    Example:
        query_pacman(pacman, x_position = 500) -> list of matching PacmanTyped instances
    Args:
        pacman: List of PacmanTyped instances.
        **filters: Keyword arguments for filtering the characters (e.g., x_position = 500).
    Returns:
        List of PacmanTyped instances that match all the provided filters.
    """
    results = pacman

    for attr, value in filters.items():
        results = [pacman for pacman in results if getattr(pacman, attr) == value]
    
    return results

full_path = os.path.expanduser('/Users/batbilegerdenebayar/desktop/FINAL CS GROUP PROJECT/group-kevin/csv/pacman.csv')

with open(full_path, 'r') as file:
    lines = file.readlines()
    pacman = parse_pacman(lines[1:])
    print(f"There were {len(pacman)} Players.")

    def query(**kwargs):
        """
        Purpose: Convenience function for querying players.
        Examples:
            query(x_position = 500)
            query(y_position = 500)
        """
        for s in query_pacman(pacman, **kwargs):
            print(s)