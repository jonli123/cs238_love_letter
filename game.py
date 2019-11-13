import numpy as np
from card import Card
from player import Player

class Game():
    """A Love Letter Game"""

    def __init__(self, deck, players):
        self._deck = deck
        self._players = players
        self._turn_index = 0

        total_playing = sum(
            [1 for player in players if PlayerTools.is_playing(player)])

    def do_action():
        

    def do_turn(self):
        if self._turn_index % 2 == 0:
            self.do_action()
        else:
            self.


    def is_winner(self, idx):
        """True iff that player has won the game"""
        if self.active():
            return False
        player = self._players[idx]
        if not PlayerTools.is_playing(player):
            return False
        other_scores = [
            p.hand_card > player.hand_card for p in self._players if PlayerTools.is_playing(p)]
        return sum(other_scores) == 0

    def winner(self):
        """Return the index of the winning player. -1 if none"""
        for idx in range(len(self._players)):
            if self.is_winner(idx):
                return idx
        return -1

    def simulate(self):
        winner = -1
        while winner == -1:
            self.do_turn()
            winner = self.winner()
        return winner
