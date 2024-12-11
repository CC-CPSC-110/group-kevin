from typing import Dict, Tuple, List
import pygame

def pressed_keys(keys: Tuple[bool, ...]) -> List[str]:
    """
    Purpose: To return the names of all keys that are pressed.
    Example:
        pressed_keys((False,) * 8   + (True,) * 2) -> ['backspace', 'tab']
        pressed_keys((False,) * 97  + (True,) * 3) -> ['a', 'b', 'c']
    """
    pressed = []
    for scancode in range(len(keys)):
        if keys[scancode]:
            # Get the name of the key using its scancode
            key_name = pygame.key.name(scancode)
            if key_name != '':
                pressed.append(key_name)
    return pressed




def directions(keymap: Dict[str, str], keys: List[str]) -> List[str]:
    """
    Purpose: Return the directions from a keymap.
    Examples:
        keymap = {
            "w": "UP",
            "s": "DOWN",
            "a": "LEFT",
            "d": "RIGHT"
        }
        directions(keymap, ["w"])      -> ["UP"]
        directions(keymap, ["s"])      -> ["DOWN"]
        directions(keymap, ["a"])      -> ["LEFT"]
        directions(keymap, ["d"])      -> ["RIGHT"]

        directions(keymap, ["w", "a"]) -> ["UP", "LEFT"]
        directions(keymap, ["w", "d"]) -> ["UP", "RIGHT"]
        
        directions(keymap, ["s", "a"]) -> ["DOWN", "LEFT"]
        directions(keymap, ["s", "d"]) -> ["DOWN", "RIGHT"]

    """
    dirs = []
    for key in keys:
        if key in keymap:
            dirs.append(keymap[key])
    return dirs

