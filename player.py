class player():
    #player is a number?
    def __init__(self, player, game):
        #self.my_discards = []
        #self.opponent_discards = []
        #self.pool_discards = []
        self.discards = []
        self.other_hand = 0 #or it can be a number, which is the other persons hand
        self.player = player
        self.my_hand = None
        self.win = None
        self.game = game

    def get_hand(self):
        return self.my_hand

    def discard(self, card):
        #learning!!!
        pass

    def targeted(self, action):
        pass

    def possible_actions(self):
        pass
