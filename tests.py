from cs110 import expect, summarize
from gamestate import *
from pellet import *
from ghost import *

#------------------------------------------------------------------------------#
# Testing for gamestate.py
#------------------------------------------------------------------------------#

# Setting up a screen and clock for consistency in the Game class
screen = pygame.Surface((800, 600))
clock = pygame.time.Clock()

# Creating Game instances with different scores and timestamps
game1 = Game(id="1", screen=screen, score=100, level=1, fps=60.0, running=True,
             background="bg1", clock=clock, keymap={}, deltaT=0.0, play_time=300.0,
             timestamp=datetime.now() - timedelta(days=1))
game2 = Game(id="2", screen=screen, score=250, level=2, fps=60.0, running=True,
             background="bg2", clock=clock, keymap={}, deltaT=0.0, play_time=450.0,
             timestamp=datetime.now() - timedelta(hours=5))
game3 = Game(id="3", screen=screen, score=180, level=3, fps=60.0, running=True,
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

# Test for game comparable of equals
game4 = Game(id="1", screen=screen, score=100, level=1, fps=60.0, running=True,
             background="bg1", clock=clock, keymap={}, deltaT=0.0, play_time=300.0,
             timestamp=datetime.now() - timedelta(days=1))

expect(game1 == game2, False)
expect(game1 == game4, True)

# Test for game comparable of less than
expect(game1 < game2, True)

# Test for game comparable of greater than
expect(game2 > game1, True)

# Test for game comparable of less than or equal to
expect(game1 <= game2, True)
expect(game1 <= game4, True)

# Test for game comparable of greater than or equal to
expect(game1 >= game2, False)
expect(game2 >= game1, True)
expect(game1 >= game4, True)

# Test for min_index of list of games
list_one = [game1, game2, game3]
list_two = [game3, game2, game1]

expect(min_index(list_one), 0)
expect(min_index(list_two), 2)

# Test for swap of list of games
expect(swap(list_one, 0, 1), [game2, game1, game3])

#------------------------------------------------------------------------------#
# Testing for pellet.py
#------------------------------------------------------------------------------#

# Sample pellets with different eaten states
pellet1 = Pellet(pellet_id="p1", eaten=True)
pellet2 = Pellet(pellet_id="p2", eaten=False)
pellet3 = Pellet(pellet_id="p3", eaten=True)
pellet4 = Pellet(pellet_id="p4", eaten=False)
pellets = [pellet1, pellet2, pellet3, pellet4]

# Test for total number of pellets
expect(total_pellets(pellets), 4)

# Test for counting eaten pellets
expect(count_eaten_pellets(pellets), 2)

# Test for remaining pellets (those that are not eaten)
remaining = remaining_pellets(pellets)
expect(len(remaining), 2)
expect(remaining[0].pellet_id, "p2")
expect(remaining[1].pellet_id, "p4")

# Test for toggling pellet states
toggled_pellets = toggle_pellet_state(pellets)
expect(toggled_pellets[0].eaten, not pellet1.eaten)
expect(toggled_pellets[1].eaten, not pellet2.eaten)
expect(toggled_pellets[2].eaten, not pellet3.eaten)
expect(toggled_pellets[3].eaten, not pellet4.eaten)

#------------------------------------------------------------------------------#
# Testing for ghost.py
#------------------------------------------------------------------------------#
ghost1 = Ghost(ghost_id="g1", ghost_state=0, ghost_type=0, color="Red")   # Chase
ghost2 = Ghost(ghost_id="g2", ghost_state=1, ghost_type=1, color="Pink")  # Scatter
ghost3 = Ghost(ghost_id="g3", ghost_state=3, ghost_type=2, color="Blue")  # Eaten
ghost4 = Ghost(ghost_id="g4", ghost_state=0, ghost_type=3, color="Orange")  # Chase

ghosts = [ghost1, ghost2, ghost3, ghost4]

frightened_ghosts = make_all_ghosts_frightened(ghosts)

expect(frightened_ghosts[0].ghost_state, 2)
expect(frightened_ghosts[0].ghost_id, "g1")
expect(frightened_ghosts[0].ghost_type, 0)
expect(frightened_ghosts[0].color, "Red")

expect(frightened_ghosts[1].ghost_state, 2)
expect(frightened_ghosts[1].ghost_id, "g2")
expect(frightened_ghosts[1].ghost_type, 1)
expect(frightened_ghosts[1].color, "Pink")

expect(frightened_ghosts[2].ghost_state, 2)
expect(frightened_ghosts[2].ghost_id, "g3")
expect(frightened_ghosts[2].ghost_type, 2)
expect(frightened_ghosts[2].color, "Blue")

expect(frightened_ghosts[3].ghost_state, 2)
expect(frightened_ghosts[3].ghost_id, "g4")
expect(frightened_ghosts[3].ghost_type, 3)
expect(frightened_ghosts[3].color, "Orange")

summarize()