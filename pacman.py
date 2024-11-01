from dataclasses import dataclass
from character import Character
from typing import List


@dataclass
class Player(Character):
    pacman_id: int
    lives: int
    is_powered_up: bool

@dataclass
class PlayerTyped:
    field_name: str
    type: str
    presence: str
    description: str

def parse_row_to_player(row: str) -> PlayerTyped:
    """
    Purpose: Convert a comma-separated string row into a Player instance.
    Example:
        parse_row_to_player("pacman_id,Unique ID, required, A unique identifier for Pacman.") 
            -> PlayerTyped(field_name="pacman_id", type="Unique ID", presence="required", ...)
    """
    columns = row.split(',')

    # Manually parsing each field
    field_name = columns[0]
    type = columns[1]
    presence = columns[2]
    description = columns[3]

    # Return a PlayerTyped instance
    return PlayerTyped(
        field_name=field_name,
        type=type,
        presence=presence,
        description=description,
    )
# Helper function to parse all rows
def parse_players(rows: List[str]) -> List[PlayerTyped]:
    """
    Purpose: Parse multiple rows of route data into a list of PlayerTyped instances.
    Example:
        parse_players([
            "pacman_id,Unique ID, required, A unique identifier for Pacman.",
            "lives, int, required, The number of lives remaining for Pacman."
        ]) -> [PlayerTyped(...), PlayerTyped(...)]
    """
    return [parse_row_to_player(row) for row in rows]


def query_players(players: list[PlayerTyped], **filters) -> list[PlayerTyped]:
    """
    Purpose: Query the list of characters based on filters such as field_name, type, presence, description.
    Example:
        query_players(players, field_name="pacman_id") -> list of matching PlayerTyped instances
    Args:
        players: List of PlayerTyped instances.
        **filters: Keyword arguments for filtering the characters (e.g., field_name="lives").
    Returns:
        List of PlayerTyped instances that match all the provided filters.
    """
    results = players

    for attr, value in filters.items():
        results = [player for player in results if getattr(player, attr) == value]
    
    return results


with open("player.csv", 'r') as file:
    lines = file.readlines()
    players = parse_players(lines[1:])
    print(f"There were {len(players)} Players.")

    def query(**kwargs):
        """
        Purpose: Convenience function for querying players.
        Examples:
            query(field_name="direction")
            query(type="tuple")
        """
        for s in query_players(players, **kwargs):
            print(s)