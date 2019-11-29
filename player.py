# have to import Card object somehow
from card import Card # map of total count
from collections import namedtuple
import numpy as np
import random

PlayerAction = namedtuple('PlayerAction', 'card player_target guess')


class Player():
    def __init__(self, player, starting_hand):
        #self.my_discards = []
        #self.opponent_discards = []
        #self.pool_discards = []
        self.discards = []
        self.player = player
        self.other_hand = Card.noCard #or it can be a number, which is the other persons hand
        self.my_hand = starting_hand
        self.new_card = Card.noCard
        self.am_known = False
        self.protected = False
        #self.other_protected = False
        self.win = None

    def get_hand(self):
        return [self.my_hand, self.new_card]

    def draw(self,card):
        #print('draw: ',card)
        if self.new_card != Card.noCard:
            raise RuntimeError("already holding two cards {} and {}".format(self.my_hand, self.new_card))
        if self.my_hand == Card.noCard:
            self.my_hand = card
        else:
            self.new_card = card
        #print('draw: ',self.get_hand())

    def discard(self,card=None):
        if card == None:
            self.discards.append(self.my_hand)
            self.my_hand = Card.noCard
            self.new_card = Card.noCard
            return

        if card == self.my_hand:
            self.my_hand = self.new_card
            self.new_card = Card.noCard
        elif card == self.new_card:
            self.new_card = Card.noCard
        else:
            raise RuntimeError("discard error, cards {} and {} dont match {}".format(self.my_hand, self.new_card, card))
        self.discards.append(card)

    def take_turn(self,game_state,players):
        self.protected = False
        A = self.possible_actions(game_state,players)
        if not A:
            for card in self.get_hand():
                A.append(PlayerAction(card,None,Card.noCard))
        a = random.choice(A) #tuple of (card, target, guess)
        #print(a)
        self.discard(a.card)
        return a

    def possible_actions(self,game_state,players):
        # Game perform card drawing such that self.my_hand now has 2 cards
        all_actions=[]
        current_hand=self.get_hand()
        #print("current_hand ",current_hand)
        # might want to make a method to return all players instead of direcly accessing it
        opponents=list(set(players) - set([players[self.player]]))
        # find possible cards to guess given the known state
        '''
        stateMap looks like
        {allSeenCards:{guard:1,...,princess:0}, canTarget:True ,knowledge: {p0:king, p1:priest}}
        '''
        #allSeenCards=game_state['allSeenCards']
        #canTarget=game_state['canTarget']
        #knowledge=game_state['knowledge']

        if Card.countess in current_hand and (Card.king in current_hand or Card.prince in current_hand):
            all_actions.append(PlayerAction(Card.countess,self.player,Card.noCard))
            return all_actions

        for card in current_hand:
            if card in Card.only_self:
                all_actions.append(PlayerAction(card,self.player,Card.noCard))
            elif card in Card.only_other:
                for opponent in opponents:
                    if opponent.protected:
                        continue
                    if card == Card.guard:
                        for guess in range(2,9):
                            all_actions.append(PlayerAction(card,opponent.player,guess))
                    elif card == Card.priest:
                        all_actions.append(PlayerAction(card,opponent.player,Card.noCard))
                    elif card == Card.baron:
                        all_actions.append(PlayerAction(card,opponent.player,Card.noCard))
                    elif card == Card.king:
                        all_actions.append(PlayerAction(card,opponent.player,Card.noCard))
            else:
                if card == Card.prince:
                    for player in players:
                        if player.protected:
                            continue
                        all_actions.append(PlayerAction(card,player.player,Card.noCard))
        return all_actions

    def heuristic(self, A):
        #Eventually we can implement the heuristic here
        return A[0]
