from dataclasses import dataclass
from character import Character
from typing import List


@dataclass
class Pacman(Character):
    pacman_id: int
    lives: int
    is_powered_up: bool

@dataclass
class PacmanTyped:
    field_name: str
    type: str
    presence: str
    description: str

def parse_row_to_pacman(row: str) -> PacmanTyped:
    """
    Purpose: Convert a comma-separated string row into a Pacman instance.
    Example:
        parse_row_to_pacman("pacman_id,Unique ID, required, A unique identifier for Pacman.") 
            -> PacmanTyped(field_name="pacman_id", type="Unique ID", presence="required", ...)
    """
    columns = row.split(',')

    # Manually parsing each field
    field_name = columns[0]
    type = columns[1]
    presence = columns[2]
    description = columns[3]

    # Return a PacmanTyped instance
    return PacmanTyped(
        field_name=field_name,
        type=type,
        presence=presence,
        description=description,
    )
# Helper function to parse all rows
def parse_pacman(rows: List[str]) -> List[PacmanTyped]:
    """
    Purpose: Parse multiple rows of route data into a list of PacmanTyped instances.
    Example:
        parse_pacman([
            "pacman_id,Unique ID, required, A unique identifier for Pacman.",
            "lives, int, required, The number of lives remaining for Pacman."
        ]) -> [PacmanTyped(...), PacmanTyped(...)]
    """
    return [parse_row_to_pacman(row) for row in rows]


def query_pacman(pacman: list[PacmanTyped], **filters) -> list[PacmanTyped]:
    """
    Purpose: Query the list of characters based on filters such as field_name, type, presence, description.
    Example:
        query_pacman(pacman, field_name="pacman_id") -> list of matching PacmanTyped instances
    Args:
        pacman: List of PacmanTyped instances.
        **filters: Keyword arguments for filtering the characters (e.g., field_name="lives").
    Returns:
        List of PlayerTyped instances that match all the provided filters.
    """
    results = pacman

    for attr, value in filters.items():
        results = [pacman for pacman in results if getattr(pacman, attr) == value]
    
    return results


with open("pacman.csv", 'r') as file:
    lines = file.readlines()
    pacman = parse_pacman(lines[1:])
    print(f"There were {len(pacman)} Players.")

    def query(**kwargs):
        """
        Purpose: Convenience function for querying players.
        Examples:
            query(field_name="direction")
            query(type="tuple")
        """
        for s in query_pacman(pacman, **kwargs):
            print(s)