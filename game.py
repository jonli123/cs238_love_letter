import numpy as np
from card import Card
from player import Player

class Game():
    """A Love Letter Game"""

    def __init__(self, deck, players):
        self._deck = deck
        self._players = players
        self._turn_index = 0
        self._game_active = True
        self._winner = -1
        self._discards = []


    def discard_card(card):
        self._discards.append(card)


    def do_action(player,action):
        if action.card == Card.guard:
            #guess card
            if self._players[action.player_target].hand_card == action.guess and not self._players[action.player_target].protected:
                self._players[action.player_target].discard()
                self._winner = player.player
                self._game_active = False

        elif action.card == Card.priest:
            #see other hand
            if not self._players[action.player_target].protected:
                player.information = self._players[action.player_target].hand_card

        elif action.card == Card.baron:
            #compare hands and eliminate
            if not self._players[action.player_target].protected:
                if self._players[action.player_target].hand_card > player.hand_card:
                    self._winner = player.player
                    self._game_active = False
                elif self._players[action.player_target].hand_card < player.hand_card:
                    self._winner = action.player_target
                    self._game_active = False
                else:
                    player.information = self._players[action.player_target].hand_card

        elif action.card == Card.handmaid:
            #protect self
            player.protected = True
        elif action.card == Card.prince:
            #Force discard
            if not self._players[action.player_target].protected:
                action = self._players[action.player_target].discard()
                self._players[action.player_target].draw(deck[0])
                deck = deck[1:]
        elif action.card == Card.king:
            #Trade hands
            if not self._players[action.player_target].protected:
                temp = self._players[action.player_target].hand_card
                self._players[action.player_target].hand_card = player.hand_card
                player.hand_card = temp
        elif action.card == Card.countess:
            #Do nothing
            pass
        elif action.card == Card.princess:
            #Lose Game
            self._winner = (player.player + 1) % 2
            self._game_active = False
        else:
            throw("error")


    def do_turn(self):
        player = players[self._turn_index % 2]
        player.protected = False
        player.draw(deck[0])
        deck = deck[1:]
        action = player.discard()
        self.discard_card(action.card)
        self.do_action(player,action)
        self._turn_index += 1


    def simulate(self):
        while self._game_active:
            self.do_turn()
            self._game_active = len(self._deck) > 1
        if self.winner == -1:
            if self._players[0].hand_card > self._players[1].hand_card:
                self.winner = 0
            elif self._players[0].hand_card < self._players[1].hand_card:
                self.winner = 1
        return self._winner
