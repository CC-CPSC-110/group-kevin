from dataclasses import dataclass
from character import Character
from typing import List


@dataclass
class Maze(Character):
    maze_id: int
    walls: List[Wall]
    pellets: List[Pellets]
    power_pellets: List[PowerPellet]

@dataclass
class MazeTyped:
    field_name: str
    type: str
    presence: str
    description: str

def parse_row_to_maze(row: str) -> MazeTyped:
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

    # Return a MazeTyped instance
    return MazeTyped(
        field_name=field_name,
        type=type,
        presence=presence,
        description=description,
    )
# Helper function to parse all rows
def parse_maze(rows: List[str]) -> List[MazeTyped]:
    """
    Purpose: Parse multiple rows of route data into a list of MazeTyped instances.
    Example:
        parse_maze([
            "maze_id, Unique ID, required, A unique identifier for the maze.",
            "maze_id, Unique ID, required, A unique identifier for the maze."
        ]) -> [MazeTyped(...), MazeTyped(...)]
    """
    return [parse_row_to_maze(row) for row in rows]


def query_maze(maze: list[MazeTyped], **filters) -> list[MazeTyped]:
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
    results = maze

    for attr, value in filters.items():
        results = [maze for maze in results if getattr(maze, attr) == value]
    
    return results


with open("maze.csv", 'r') as file:
    lines = file.readlines()
    maze = parse_maze(lines[1:])
    print(f"There were {len(maze)} Ghost.")

    def query(**kwargs):
        """
        Purpose: Convenience function for querying players.
        Examples:
            query(field_name="maze_id")
            query(type="walls")
        """
        for s in query_maze(maze, **kwargs):
            print(s)