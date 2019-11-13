"""
Love Letter Player object
Everything required to represent a player.
"""

import numpy as np
from card import Card


# A record of an action taken during a turn.
# Card that was discarded and player that was targeted with the effect
#
#  discard - int card id discarded
#  player_target - int targeted player id
#  guess - int card guess being made - only useful if discard is 1 (guard), otherwise 0
#  revealed_card - int card of player_target - only useful if discard is 2 (priest), otherwise 0
#
# Note that the discarding player is a valid target and that is the only
# valid target for the non-effecting cards (ie handmaid or countess)

class Player():
    def __init__(self):
        self.hand = None

    def
