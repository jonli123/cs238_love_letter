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
        self._num_players = len(players)

        #public knowledge
        self._discards = [0]*9
        self._targetable = [1 for player in players]


    def discard_card(self,card):
        self._discards[card]+=1


    def do_action(self,player,action):
        if action.player_target is None:
            #All actions just discard, no targets available
            return

        if action.card == Card.guard:
            #guess card
            #print("guess card")
            #print(action,self._players[action.player_target].my_hand == action.guess,self._targetable[action.player_target])
            if self._players[action.player_target].my_hand == action.guess and self._targetable[action.player_target]:
                #print('winner:',player.id )
                self._winner = player.id
                self._game_active = False

        elif action.card == Card.priest:
            #see other hand
            #print('priest',self._targetable,action.player_target,player.id)
            if self._targetable[action.player_target]:
                player.set_knowledge(action.player_target,self._players[action.player_target].my_hand)
                self._players[action.player_target].am_known = 1
                #player.information = self._players[action.player_target].my_hand

        elif action.card == Card.baron:
            #compare hands and eliminateac
            if self._targetable[action.player_target]:
                if self._players[action.player_target].my_hand < player.my_hand:
                    self._winner = player.id
                    self._game_active = False
                elif self._players[action.player_target].my_hand > player.my_hand:
                    self._winner = action.player_target
                    self._game_active = False
                else:
                    player.set_knowledge(action.player_target,self._players[action.player_target].my_hand)
                    self._players[action.player_target].am_known = 1
                    #player.information = self._players[action.player_target].my_hand

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
        player = self._players[self._turn_index % self._num_players]
        self._targetable[player.id] = 1
        player.draw(self._deck[0])
        self._deck = self._deck[1:]
        game_state = self.getGameState()
        player_ids = self.get_player_ids()
        #print("turn ",self._turn_index,player.id,self._targetable)
        #print("hands: ", [player.my_hand for player in self._players])
        action = player.take_turn(game_state,player_ids)
        player.update(game_state,action)
        #print(action)
        self.discard_card(action.card)
        self.do_action(player,action)

        self._turn_index += 1

    def get_player_ids(self):
        #print("player_ids:",[player.id for player in self._players])
        return [player.id for player in self._players]

    def simulate(self):
        while self._game_active:
            self.do_turn()
            if not self._game_active:
                break
            self._game_active = len(self._deck) > 1
        if self._winner == -1:
            if self._players[0].my_hand > self._players[1].my_hand:
                self._winner = 0
            elif self._players[0].my_hand < self._players[1].my_hand:
                self._winner = 1

        game_state = self.getGameState()
        if self._winner == 1:
            self._players[1].end_game(game_state, 1)
            self._players[0].end_game(game_state, 0)
        elif self._winner == 0:
            self._players[0].end_game(game_state, 1)
            self._players[1].end_game(game_state, 0)
        return self._winner
