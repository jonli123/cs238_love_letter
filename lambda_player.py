from player import Player, PlayerAction
from card import Card # map of total count
from collections import namedtuple
import numpy as np
import random
import copy


#let's implement this for just two players
class LambdaPlayer(Player):
    def __init__(self, player, starting_hand, num_players, \
        lambdas={'g2': 0.79, 'g4': 0.85, 'g5': 0.53, 'g7': 0.46, 'b2': 0.77, 'b4': 0.54, 'b5': 0.67, 'b6': 0.34, 'b7': 0.45, 'p2': 0.52, 'p6': 0.54}):
        self.id = player

        #Private Knowledge
        self.knowledge = [Card.noCard for player in range(num_players)]
        self.my_hand = starting_hand
        self.new_card = Card.noCard
        self.am_known = 0
        self.lambdas = lambdas 
        #lambdas is dictionary where keys are g2, g4, g5, g7, b2, b4, b5, b6, b7, p2, p5

    def take_turn(self,game_state,player_ids):
        opponent = int(not self.id)
        hand = self.get_hand()

        #if I have an 8, play the other card
        if Card.princess in hand:
            card = list(filter(lambda c: c != Card.princess, hand))[0]
            if card in {Card.prince, Card.priest, Card.baron}:
                self.discard(card)
                return PlayerAction(card, opponent, Card.noCard)
            if card == Card.guard:
                distr = self.opponent_distribution(game_state)
                return self.play_guard(distr)
            if card == Card.handmaid:
                self.discard(card)
                return PlayerAction(card, self.id, Card.noCard)
            self.discard(card)
            return PlayerAction(card, None, Card.noCard)

        #play 7 if necessary
        if Card.countess in hand:
            other = list(filter(lambda c: c != Card.countess, hand))[0]
            if other in {Card.king, Card.prince}:
                self.discard(Card.countess)
                return PlayerAction(Card.countess, None, Card.noCard)
            if other == Card.priest: #if 2 and 7 play 2
                self.discard(Card.priest)
                return PlayerAction(Card.priest, opponent, Card.noCard)
        
        #play 4 if not paired with 1 or 3
        if Card.handmaid in hand and not (Card.guard in hand or Card.baron in hand):
            self.discard(Card.handmaid)
            return PlayerAction(Card.handmaid, self.id, Card.noCard)

        #if 6 and 2 play 6
        if Card.priest in hand and Card.king in hand:
            self.discard(Card.king)
            return PlayerAction(Card.king, None, Card.noCard)
        
        distr = self.opponent_distribution(game_state)
        #if I have a 1
        if Card.guard in hand:
            if self.knowledge[opponent] not in (Card.guard, 0):
                self.discard(Card.guard)
                return PlayerAction(Card.guard, opponent, self.knowledge[opponent])
            other = list(filter(lambda c: c != Card.guard, hand))
            if len(other) == 0 or other[0] in {Card.king, Card.baron}:
                return self.play_guard(distr)
            other = other[0]
            key = 'g{}'.format(other)
            lambd = self.lambdas[key]
            if not self.knowledge[opponent] == Card.guard or max(distr[1:]) > lambd:
                return self.play_guard(distr)
            elif other == Card.priest:
                self.discard(Card.priest)
                return PlayerAction(Card.priest, opponent, Card.noCard)
            elif other == Card.handmaid:
                self.discard(Card.handmaid)
                return PlayerAction(Card.handmaid, self.id, Card.noCard)
            elif other == Card.prince:
                return self.play_prince()
            self.discard(other)
            return PlayerAction(other, None, Card.noCard)

        #if I can make them discard an 8
        if Card.prince in hand and self.knowledge[opponent] == 8:
            self.discard(Card.prince)
            return PlayerAction(Card.prince, opponent, Card.noCard)

        #if I have a 3
        if Card.baron in hand:
            other = list(filter(lambda c: c != Card.baron, hand))
            if len(other) == 0:
                self.discard(Card.baron)
                return PlayerAction(Card.baron, opponent, Card.noCard)
            other = other[0]
            if self.knowledge[opponent] != 0:
                if self.knowledge[opponent] < other:
                    self.discard(Card.baron)
                    return PlayerAction(Card.guard, opponent, Card.noCard)
            key = 'b{}'.format(other)
            lambd = self.lambdas[key]
            if self.knowledge[opponent] == 0 and sum(distr[:other - 1]) > lambd:
                self.discard(Card.baron)
                return PlayerAction(Card.baron, opponent, Card.noCard)
            elif other == Card.priest:
                self.discard(Card.priest)
                return PlayerAction(Card.priest, opponent, Card.noCard)
            elif other == Card.handmaid:
                self.discard(Card.handmaid)
                return PlayerAction(Card.handmaid, self.id, Card.noCard)
            elif other == Card.prince:
                return self.play_prince()
            self.discard(other)
            return PlayerAction(other, None, Card.noCard)
        
        if hand[0] == 2 and hand[1] == 2:
            self.discard(2)
            return PlayerAction(2, opponent, 0)

        #I have a prince
        if self.am_known:
            return self.play_prince()
        other = list(filter(lambda c: c != Card.prince, hand))
        if len(other) == 0:
            return self.play_prince()
        other = other[0]
        key = 'p{}'.format(other)
        lambd = self.lambdas[key]
        if random.random() < lambd:
            return self.play_prince()
        self.discard(other)
        if other == Card.priest:
            return PlayerAction(Card.priest, opponent, Card.noCard)
        return PlayerAction(other, None, Card.noCard)
        
    def play_prince(self):
        #assumes the other card isn't an 8
        opp = int(not self.id)
        #if I'm known, or I know what they have, discard myself
        self.discard(Card.prince)
        if (self.am_known and self.new_card == Card.prince) or self.knowledge[opp]:
            return PlayerAction(Card.prince, self.id, Card.noCard)
        return PlayerAction(Card.prince, opp, Card.noCard)

    def play_guard(self, distr):
        guess = len(distr[1:]) - 1 - distr[1:][::-1].index(max(distr[1:]))
        self.discard(Card.guard)
        opp = int(not self.id)
        return PlayerAction(Card.guard, opp, guess)

    def opponent_distribution(self, game_state):
        hand = self.get_hand()
        seen = copy.copy(game_state['allSeenCards'])
        for c in hand:
            seen[c - 1] += 1
        avail = [0 for i in range(len(Card.counts))]
        for i in range(len(Card.counts)):
            avail[i] = Card.counts[i] - seen[i]
        total_avail = sum(avail)
        return [c / total_avail for c in avail]