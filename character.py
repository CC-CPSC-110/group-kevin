from dataclasses import dataclass
from typing import List

@dataclass
class Character:
    direction: tuple
    x_position: int
    y_position: int
    speed: float

@dataclass
class CharacterTyped:
    field_name: str
    type: str
    presence: str
    description: str

def parse_row_to_character(row: str) -> CharacterTyped:
    """
    Purpose: Convert a comma-separated string row into a Character instance.
    Example:
        parse_row_to_character("direction,tuple,required,the unit vector which the character is pointing towards") 
            -> CharacterTyped(field_name="direction", type="tuple", presence="required", ...)
    """
    columns = row.split(',')

    # Manually parsing each field
    field_name = columns[0]
    type = columns[1]
    presence = columns[2]
    description = columns[3]

    # Return a RouteTyped instance
    return CharacterTyped(
        field_name=field_name,
        type=type,
        presence=presence,
        description=description,
    )
# Helper function to parse all rows
def parse_characters(rows: List[str]) -> List[CharacterTyped]:
    """
    Purpose: Parse multiple rows of route data into a list of CharacterTyped instances.
    Example:
        parse_characters([
            "direction,tuple,required,the unit vector which the character is pointing towards",
            "x_position,screen_x,required,the x-position of character on screen"
        ]) -> [CharacterTyped(...), CharacterTyped(...)]
    """
    return [parse_row_to_character(row) for row in rows]


def query_characters(characters: list[CharacterTyped], **filters) -> list[CharacterTyped]:
    """
    Purpose: Query the list of characters based on filters such as field_name, type, presence, description.
    Example:
        query_characters(characters, field_name="direction") -> list of matching RouteTyped instances
    Args:
        characters: List of CharacterTyped instances.
        **filters: Keyword arguments for filtering the characters (e.g., field_name="x_position").
    Returns:
        List of CharacterTyped instances that match all the provided filters.
    """
    results = characters

    for attr, value in filters.items():
        results = [character for character in results if getattr(character, attr) == value]
    
    return results


