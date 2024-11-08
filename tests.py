from cs110 import expect, summarize
from gamestate import *

#------------------------------------------------------------------------------#
# Testing for gamestate.py
#------------------------------------------------------------------------------#

# Setting up a screen and clock for consistency in the Game class
screen = pygame.Surface((800, 600))
clock = pygame.time.Clock()

# Creating Game instances with different scores and timestamps
game1 = Game(screen=screen, score=100, level=1, fps=60.0, running=True,
             background="bg1", clock=clock, keymap={}, deltaT=0.0, play_time=300.0,
             timestamp=datetime.now() - timedelta(days=1))
game2 = Game(screen=screen, score=250, level=2, fps=60.0, running=True,
             background="bg2", clock=clock, keymap={}, deltaT=0.0, play_time=450.0,
             timestamp=datetime.now() - timedelta(hours=5))
game3 = Game(screen=screen, score=180, level=3, fps=60.0, running=True,
             background="bg3", clock=clock, keymap={}, deltaT=0.0, play_time=500.0,
             timestamp=datetime.now())

# Test for an empty GameLinkedList
empty_list = GameLinkedList()
expect(empty_list.head, None)


# Inserting into the GameLinkedList and verifying order

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


summarize()