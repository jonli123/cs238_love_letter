from player import Player, PlayerAction
from card import Card # map of total count
from collections import namedtuple
import numpy as np
import random

class SarsaPlayer(Player):
    def __init__(self, player, starting_hand, num_players, Q, explore_prob=0.0, learning_rate=0.9, gamma=0.95):
        super().__init__(player, starting_hand, num_players)
        self.Q = Q
        self.explore_prob = explore_prob
        self.learning_rate = learning_rate
        self.gamma = gamma
        self.previous_state = ()
        self.previous_action = ()

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
            if random.random() < self.explore_prob:
                a = random.choice(A)
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
        print(state)
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
