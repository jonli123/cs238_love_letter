import numpy as np

class player():
    #player is a number?
    def __init__(self, player, game, starting_hand):
        #self.my_discards = []
        #self.opponent_discards = []
        #self.pool_discards = []
        self.discards = [] 
        self.player = player
        self.other_hand = 0 #or it can be a number, which is the other persons hand
        self.my_hand = starting_hand
        self.new_card = None
        self.am_known = False
        self.protected = False
        self.other_protected = False
        self.win = None

    def get_hand(self):
        return self.my_hand

    def draw(card):
        if(self.new_card != None):
            return "already holding two cards {} and {}".format(self.my_hand, self.new_card) 
        self.new_card = card

    def discard():
        self.discards.append(self.my_hand)
        return self.my_hand

    def take_turn(self):
        self.protected = False
        A = self.possible_actions()
        a = np.sample(A) #tuple of (card, target, guess)
        #a = self.heuristic(A)
        if a[0] == self.my_hand:
            self.my_hand = self.new_card
        self.new_card = None
        self.discards.append(a[0])
        return a

    def possible_actions(self):
        pass

    def heuristic(self, A):
        #Eventually we can implement the heuristic here
        return A[0]








