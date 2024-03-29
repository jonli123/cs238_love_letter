from player import Player, PlayerAction
from card import Card # map of total count
from collections import namedtuple
import numpy as np
import random
from heuristic_player import HeuristicPlayer 
from lambda_player import LambdaPlayer

class SarsaPlayer(Player):
    def __init__(self, player, starting_hand, num_players, Q, explore_prob=0.0, learning_rate=0.9, gamma=0.95, her=False, lam=False):
        super().__init__(player, starting_hand, num_players)
        self.Q = Q
        self.explore_prob = explore_prob
        self.learning_rate = learning_rate
        self.gamma = gamma
        self.her = her
        self.lam = lam
        self.previous_state = ()
        self.previous_action = ()

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
        #print(a)
        return a
    
    def take_turn(self,game_state,player_ids):
        explore = random.random() < self.explore_prob
        if self.lam and not explore:
            lam_player = LambdaPlayer(self.id, self.my_hand, len(self.knowledge))
            lam_player.knowledge = self.knowledge
            lam_player.am_known = self.am_known
            lam_player.new_card = self.new_card
            a = lam_player.take_turn(game_state, player_ids)
            self.discard(a.card)
            return a

        A = self.possible_actions(game_state,player_ids)
        if not A:
            for card in self.get_hand():
                A.append(PlayerAction(card,None,Card.noCard))
            a = random.choice(A) #tuple of (card, target, guess)
        else:
            #print('heuristic else:',player_ids)
            if explore:
                a = random.choice(A)
            elif self.her:
                a = self.heuristic(A,game_state,player_ids)
            else:
                max_a = []
                max_a_value = -1000
                s = self.get_state(game_state)
                for ap in A:
                    val = self.Q[(s, ap)]
                    if val > max_a_value:
                        max_a = [ap]
                    elif val == max_a_value:
                        max_a.append(ap)
                a = random.choice(max_a)
                #print(a)
        self.discard(a.card)
        return a
    

    def get_state(self, game_state):
        state = self.knowledge + self.get_hand() + [self.am_known] + game_state['allSeenCards'] + game_state['canTarget']
        #print(state)
        return tuple(state)

    def get_Q(self):
        return self.Q

    def update(self, game_state, a_prime):
        s = self.previous_state
        a = self.previous_action
        s_prime = self.get_state(game_state)

        self.Q[(s, a)] = self.Q[(s, a)] + self.learning_rate * \
            (self.gamma * self.Q[(s_prime, a_prime)] - self.Q[(s, a)])
        self.previous_state = s_prime
        self.previous_action = a_prime

    def end_game(self, game_state, win):
        s = self.previous_state
        a = self.previous_action
        s_prime = self.get_state(game_state)
        if win:
            r = 10
        else:
            r = -10
        self.Q[(s, a)] = self.Q[(s, a)] + self.learning_rate * (r - self.Q[(s, a)])
