from dataclasses import dataclass
from character import Character
from typing import List


@dataclass
class Pellet:
    pellet_id: str
    eaten: bool

@dataclass
class PelletTyped:
    field_name: str
    type: str
    presence: str
    description: str

def parse_row_to_pellet(row: str) -> PelletTyped:
    """
    Purpose: Convert a comma-separated string row into a Maze instance.
    Example:
        parse_row_to_maze("maze_id, Unique ID, required, A unique identifier for the maze.") 
            -> MazeTyped(field_name="maze_id", type="Unique ID", presence="required", ...)
    """
    columns = row.split(',')

    # Manually parsing each field
    field_name = columns[0]
    type = columns[1]
    presence = columns[2]
    description = columns[3]

    # Return a PelletTyped instance
    return PelletTyped(
        field_name=field_name,
        type=type,
        presence=presence,
        description=description,
    )
# Helper function to parse all rows
def parse_pellet(rows: List[str]) -> List[PelletTyped]:
    """
    Purpose: Parse multiple rows of route data into a list of PelletTyped instances.
    Example:
        parse_pellet([
            "pellet_id, str, required, A unique identifier for each point object",
            "eaten, Boolean, required, Whether the pellet has been eaten or not"
        ]) -> [PelletTyped(...), PelletTyped(...)]
    """
    return [parse_row_to_maze(row) for row in rows]


def query_pellet(pellet: list[PelletTyped], **filters) -> list[PelletTyped]:
    """
    Purpose: Query the list of characters based on filters such as field_name, type, presence, description.
    Example:
        query_ghost(ghost, field_name="ghost_state") -> list of matching PacmanTyped instances
    Args:
        ghost: List of GhostTyped instances.
        **filters: Keyword arguments for filtering the characters (e.g., field_name="ghost_type").
    Returns:
        List of PlayerTyped instances that match all the provided filters.
    """
    results = pellet

    for attr, value in filters.items():
        results = [maze for maze in results if getattr(maze, attr) == value]
    
    return results


with open("pellet.csv", 'r') as file:
    lines = file.readlines()
    pellet = parse_pellet(lines[1:])
    print(f"There were {len(pellet)} Ghost.")

    def query(**kwargs):
        """
        Purpose: Convenience function for querying players.
        Examples:
            query(field_name="pellet_id")
            query(type="str")
        """
        for s in query_pellet(pellet, **kwargs):
            print(s)