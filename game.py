import numpy as np
from card import Card


class Game():
    """A Love Letter Game"""

    def __init__(self, deck, players, turn_index):
        self._deck = deck
        self._players = players
        self._turn_index = turn_index

        total_playing = sum(
            [1 for player in players if PlayerTools.is_playing(player)])
        self._game_active = total_playing > 1 and self.cards_left() > 0

    def players(self):
        """List of current players."""
        return self._players[:]

    def deck(self):
        """
        List of current cards.
        NOTE: The LAST card [-1] is always held out
        """
        return self._deck

    def draw_card(self):
        """
        Card currently available to the next player.
        Only valid if the game is not over (otherwise No Card)
        """
        return self._deck[0] if len(self._deck) > 1 else Card.noCard

    def held_card(self):
        """
        Card withheld from the game
        """
        return self._deck[-1]

    def turn_index(self):
        """
        Overall turn index of the game.
        This points to the actual action number
        """
        return self._turn_index

    def player_turn(self):
        """Player number of current player."""
        return self._turn_index % len(self._players)

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

    def player(self):
        """Returns the current player"""
        return self._players[self.player_turn()]

    def cards_left(self):
        """
        Number of cards left in deck to distribute
        Does not include the held back card
        """
        return len(self._deck) - 1

    def active(self):
        """Return True if the game is still playing"""
        return self._game_active

    def over(self):
        """Return True if the game is over"""
        return not self.active()
