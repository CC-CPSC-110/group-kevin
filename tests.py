from cs110 import expect, summarize
from game import *

#------------------------------------------------------------------------------#
# Testing for gamestate.py
#------------------------------------------------------------------------------#

# Setup for pygame elements
screen = pygame.Surface((800, 600))  # Create a dummy screen
clock = pygame.time.Clock()  # Create a dummy clock

# Initialize Game instances with the new attributes
game1 = Game(
    id='1', screen=screen, clock=clock, keymap={}, background="bg1", fps=60.0,
    running=True, deltaT=0.0, unit_height=32, unit_width=32, font=None,
    score=100
)
game2 = Game(
    id='2', screen=screen, clock=clock, keymap={}, background="bg2", fps=60.0,
    running=True, deltaT=0.0, unit_height=32, unit_width=32, font=None,
    score=250
)
game3 = Game(
    id='3', screen=screen, clock=clock, keymap={}, background="bg3", fps=60.0,
    running=True, deltaT=0.0, unit_height=32, unit_width=32, font=None,
    score=180
)

# Test for an empty GameLinkedList
empty_list = GameLinkedList()
expect(empty_list.head, None)

# Test: Verify attribute initialization
expect(game1.score, 100)
expect(game2.score, 250)

# Create a linked list and add games
game_list = GameLinkedList()
game_list.insert(game1)
game_list.insert(game2)
game_list.insert(game3)

# Verifying the head is the most recent game added (game3)
expect(game_list.head.game, game3)
expect(game_list.head.next.game, game2)
expect(game_list.head.next.next.game, game1)

# Verify the highest score in the list
expect(highest_score(game_list), 250)

# Verify the most recent game by timestamp (should be game3)
expect(most_recent_game(game_list), game3)

# Test for game comparable of equals
expect(game1 == game2, False)

# Test for game comparable of less than
expect(game1 < game2, True)

# Test for game comparable of greater than
expect(game2 > game1, True)

# Test for game comparable of less than or equal to
expect(game1 <= game2, True)

# Test for game comparable of greater than or equal to
expect(game1 >= game2, False)
expect(game2 >= game1, True)

# Test for min_index of list of games
list_one = [game1, game2, game3]
list_two = [game3, game2, game1]

expect(min_index(list_one), 0)
expect(min_index(list_two), 2)

# Test for swap of list of games
expect(swap(list_one, 0, 1), [game2, game1, game3])

# Test for selection sort list of games
expect(selection_sort_games(list_two), [game1, game2, game3])

summarize()