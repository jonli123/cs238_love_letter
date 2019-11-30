import numpy as np
from card import Card
from player import Player, PlayerAction

class Game():
    """A Love Letter Game"""

    def __init__(self, deck, players):
        self._deck = deck
        self._players = players
        self._turn_index = 0
        self._game_active = True
        self._winner = -1

        #public knowledge
        self._discards = {}
        self._targetable = [1 for player in players]


    def discard_card(self,card):
        if card not in self._discards:
            self._discards[card] = 0
        self._discards[card]+=1


    def do_action(self,player,action):
        if action.player_target is None:
            #All actions just discard, no targets available
            return

        if action.card == Card.guard:
            #guess card
            if self._players[action.player_target].my_hand == action.guess and self._targetable[action.player_target]:
                self._winner = player.id
                self._game_active = False

        elif action.card == Card.priest:
            #see other hand
            if self._targetable[action.player_target]:
                player.information = self._players[action.player_target].my_hand

        elif action.card == Card.baron:
            #compare hands and eliminateac
            if self._targetable[action.player_target]:
                if self._players[action.player_target].my_hand > player.my_hand:
                    self._winner = player.id
                    self._game_active = False
                elif self._players[action.player_target].my_hand < player.my_hand:
                    self._winner = action.player_target
                    self._game_active = False
                else:
                    player.information = self._players[action.player_target].my_hand

        elif action.card == Card.handmaid:
            #protect self
            self._targetable[player.id] = 0
        elif action.card == Card.prince:
            #Force discard
            if self._targetable[action.player_target]:
                self._players[action.player_target].discard()
                self._players[action.player_target].draw(self._deck[0])
                self._deck = self._deck[1:]
        elif action.card == Card.king:
            #Trade hands
            if self._targetable[action.player_target]:
                temp = self._players[action.player_target].my_hand
                self._players[action.player_target].my_hand = player.my_hand
                player.my_hand = temp
        elif action.card == Card.countess:
            #Do nothing
            return
        elif action.card == Card.princess:
            #Lose Game
            self._winner = (player.id + 1) % 2
            self._game_active = False
        else:
            raise RuntimeError('action.card with unexpected value: ',action.card)

    def getGameState(self):
        #TODO: Finish state implementation
        stateMap = {}
        stateMap['allSeenCards'] = self._discards
        stateMap['canTarget'] = self._targetable
        return stateMap

    def do_turn(self):
        player = self._players[self._turn_index % 2]
        self._targetable[player.id] = 1
        player.draw(self._deck[0])
        self._deck = self._deck[1:]
        game_state = self.getGameState()
        action = player.take_turn(game_state,self._players)
        self.discard_card(action.card)
        self.do_action(player,action)
        self._turn_index += 1

    def get_opponents(self,player_id):
        opponents=list(set(self._players) - set([self._players[player_id]]))
        return [opponent.id for opponent in opponents]

    def simulate(self):
        while self._game_active:
            self.do_turn()
            self._game_active = len(self._deck) > 1
        if self._winner == -1:
            if self._players[0].my_hand > self._players[1].my_hand:
                self._winner = 0
            elif self._players[0].my_hand < self._players[1].my_hand:
                self._winner = 1
        return self._winner
