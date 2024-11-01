from dataclasses import dataclass
from character import Character
from typing import List


@dataclass
class Ghost(Character):
    ghost_state: int
    ghost_type: int

@dataclass
class GhostTyped:
    field_name: str
    type: str
    presence: str
    description: str

def parse_row_to_ghost(row: str) -> GhostTyped:
    """
    Purpose: Convert a comma-separated string row into a Pacman instance.
    Example:
        parse_row_to_pacman("ghost_state, Enum, required, Indicates the current state of the ghosts. Valid options are: 0 - CHASE - The ghost is actively chasing the Pacman. 1 - SCATTER - The ghost retreats to a designated corner of the maze. 2 - FRIGHTENED - The ghost moves away from Pacman and can be eaten by Pacman. 3 - Eaten - The ghost returns to the ghost house after being eaten by Pacman.") 
            -> PacmanTyped(field_name="ghost_state", type="Enum", presence="required", ...)
    """
    columns = row.split(',')

    # Manually parsing each field
    field_name = columns[0]
    type = columns[1]
    presence = columns[2]
    description = columns[3]

    # Return a PacmanTyped instance
    return GhostTyped(
        field_name=field_name,
        type=type,
        presence=presence,
        description=description,
    )
# Helper function to parse all rows
def parse_ghost(rows: List[str]) -> List[GhostTyped]:
    """
    Purpose: Parse multiple rows of route data into a list of GhostTyped instances.
    Example:
        parse_ghost([
            "ghost_state, Enum, required, Indicates the current state of the ghosts. Valid options are: 0 - CHASE - The ghost is actively chasing the Pacman. 1 - SCATTER - The ghost retreats to a designated corner of the maze. 2 - FRIGHTENED - The ghost moves away from Pacman and can be eaten by Pacman. 3 - Eaten - The ghost returns to the ghost house after being eaten by Pacman.",
            "ghost_type, Enum, required, Indicates the ghost type. Valid options are: 0 - BLINKY - The red ghost. 1 - PINKY - The pink ghost. 2 - INKY - The blue ghost. 3 - CLYDE - The orange ghost."
        ]) -> [GhostTyped(...), GhostTyped(...)]
    """
    return [parse_row_to_ghost(row) for row in rows]


def query_ghost(ghost: list[GhostTyped], **filters) -> list[GhostTyped]:
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
    results = ghost

    for attr, value in filters.items():
        results = [ghost for ghost in results if getattr(ghost, attr) == value]
    
    return results


with open("ghost.csv", 'r') as file:
    lines = file.readlines()
    ghost = parse_ghost(lines[1:])
    print(f"There were {len(ghost)} Ghost.")

    def query(**kwargs):
        """
        Purpose: Convenience function for querying players.
        Examples:
            query(field_name="ghost_state")
            query(type="Enum")
        """
        for s in query_ghost(ghost, **kwargs):
            print(s)