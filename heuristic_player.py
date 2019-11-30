from player import Player, PlayerAction
from card import Card # map of total count
from collections import namedtuple
import numpy as np
import random

class HeuristicPlayer(Player):
    def take_turn(self,game_state,player_ids):
        #print('heuristic take_turn:',player_ids)
        A = self.possible_actions(game_state,player_ids)
        #print('heuristic after:',player_ids)
        if not A:
            for card in self.get_hand():
                A.append(PlayerAction(card,None,Card.noCard))
            a = random.choice(A) #tuple of (card, target, guess)
        else:
            #print('heuristic else:',player_ids)
            a = self.heuristic(A,game_state,player_ids)
        #print(a)
        self.discard(a.card)
        return a

    def heuristic(self, A, game_state, player_ids):
        #Given list of possible actions and game_state, return an action
        #print("heuristic: ", player_ids)
        allSeenCards=game_state['allSeenCards']
        canTarget=game_state['canTarget']
        current_hand=self.get_hand()
        opponent_ids=player_ids.copy()
        #print("heuristic opp:", opponent_ids)
        opponent_ids.remove(self.id)
        #action: card player_target guess
        #If we know the opponent card and we have a 1, play it and guess the card
        #If we know the opponent card is less than ours and we have a baron, play it
        for opponent in opponent_ids:
            if self.knowledge[opponent] != Card.noCard:
                if self.knowledge[opponent] != Card.guard and Card.guard in current_hand:
                    #print("win")
                    return PlayerAction(Card.guard,opponent,self.knowledge[opponent])
                if current_hand[0] == Card.baron and current_hand[1] > self.knowledge[opponent]:
                    #print("win")
                    return PlayerAction(Card.baron,opponent,Card.noCard)
                if current_hand[1] == Card.baron and current_hand[0] > self.knowledge[opponent]:
                    #print("win")
                    return PlayerAction(Card.baron,opponent,Card.noCard)
        #If we have a 4, play the 4
        if Card.handmaid in current_hand:
            return PlayerAction(Card.handmaid,self.id,Card.noCard)
        #If we have a 2, play the 2
        if Card.priest in current_hand:
            return PlayerAction(Card.priest,opponent,Card.noCard)
        #Never play an 8
        A_safe = [action for action in A if action.card != Card.princess]
        if not A_safe:
            for card in self.get_hand():
                A_safe.append(PlayerAction(card,None,Card.noCard))
        a = random.choice(A_safe)
        return a
