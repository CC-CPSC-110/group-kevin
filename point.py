from dataclasses import dataclass
from typing import List


@dataclass
class Point:
    points: int
    collected: bool

@dataclass
class PointTyped:
    field_name: str
    type: str
    presence: str
    description: str

def parse_row_to_point(row: str) -> PointTyped:
    """
    Purpose: Convert a comma-separated string row into a Point instance.
    Example:
        parse_row_to_point("points, int, required, The collected points from the game.") 
            -> PointTyped(field_name="points", type="int", presence="required", ...)
    """
    columns = row.split(',')

    # Manually parsing each field
    field_name = columns[0]
    type = columns[1]
    presence = columns[2]
    description = columns[3]

    # Return a PointTyped instance
    return PointTyped(
        field_name=field_name,
        type=type,
        presence=presence,
        description=description,
    )
# Helper function to parse all rows
def parse_point(rows: List[str]) -> List[PointTyped]:
    """
    Purpose: Parse multiple rows of route data into a list of PointTyped instances.
    Example:
        parse_maze([
            "points, int, required, The collected points from the game.",
            "collected, Boolean, required, Whether the points have been collected or not."
        ]) -> [PointTyped(...), PointTyped(...)]
    """
    return [parse_row_to_point(row) for row in rows]


def query_point(point: list[PointTyped], **filters) -> list[PointTyped]:
    """
    Purpose: Query the list of points based on filters such as field_name, type, presence, description.
    Example:
        query_point(point, field_name="points") -> list of matching PointTyped instances
    Args:
        ghost: List of PointTyped instances.
        **filters: Keyword arguments for filtering the characters (e.g., field_name="points").
    Returns:
        List of PointTyped instances that match all the provided filters.
    """
    results = point

    for attr, value in filters.items():
        results = [point for point in results if getattr(point, attr) == value]
    
    return results


with open("point.csv", 'r') as file:
    lines = file.readlines()
    point = parse_point(lines[1:])
    print(f"There were {len(point)} Points.")

    def query(**kwargs):
        """
        Purpose: Convenience function for querying players.
        Examples:
            query(field_name="maze_id")
            query(type="walls")
        """
        for s in query_point(point, **kwargs):
            print(s)