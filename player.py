# have to import Card object somehow
from card import Card # map of total count
from collections import namedtuple
import numpy as np


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
        idx = np.random.choice(len(A)) #tuple of (card, target, guess)
        a = A[idx]
        self.discard(a.card)
        return a

    def possible_actions(self,game_state,players):
        # Game perform card drawing such that self.my_hand now has 2 cards
        all_actions=[]
        current_hand=self.get_hand()
        print("current_hand ",current_hand)
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
        '''
        # special scenario when need to play countess
        pool={self.player.get_hand(),another_player.get_hand()}
        if Card.countess in pool:
            if (Card.king in pool) or (Card.prince in pool):
                all_actions=all_actions.append(PlayerAction(Card.countess,Card.noCard,Card.noCard,Card.noCard))
            else:

                current_card=current_hand[0]
                # play guard
                if current_card == Card.guard:
                    if not another_player.pretected:
                        # if know what the other peroson has then call and the game is over
                        if knowledge[self.player.get_hand()] != Card.noCard:
                            knownCard=knowledge[self.player.get_hand()]
                            all_actions=all_actions.append(PlayerAction(Card.guard,another_player,knownCard,Card.noCard))
                        # if no prior knowledge then have no guess
                        else:
                            for (key,value) in allSeenCards:
                                # if reveled less than total number of that specific card and not a gueard itself
                                if (value < counts[key]) and (key != Card.guard):
                                    all_actions=all_actions.append(PlayerAction(Card.guard,another_player,key,Card.noCard))
                    else:
                        # discard with no effect
                        all_actions=all_actions.append(PlayerAction(Card.guard,None,Card.noCard,Card.noCard))
                # play priest
                elif current_card == Card.priest:
                    if not another_player.pretected:
                        all_actions=all_actions.append(PlayerAction(Card.priest,another_player,Card.noCard,another_player.get_hand()))
                        # update knowledge in Game class
                        game.getGameState()['knowledge'][self.player.get_hand()]=another_player.get_hand()
                    else:
                        # discard with no effect
                        all_actions=all_actions.append(PlayerAction(Card.guard,None,Card.noCard,Card.noCard))
                # play baron
                elif current_card == Card.baron:
                    if not another_player.pretected:
                        all_actions=all_actions.append(PlayerAction(Card.baron,another_player,Card.noCard,Card.noCard))
                    else:
                        all_actions=all_actions.append(PlayerAction(Card.baron,None,Card.noCard,Card.noCard))
                # play handmaid
                elif current_card == Card.handmaid:
                    all_actions=all_actions.append(PlayerAction(Card.handmaid,self.player,Card.noCard,Card.noCard))
                # play prince
                elif current_card == Card.prince:
                    # can always target yourself
                    all_actions=all_actions.append(PlayerAction(Card.baron,self.player,Card.noCard,Card.noCard))
                    if not another_player.pretected:
                        all_actions=all_actions.append(PlayerAction(Card.baron,another_player,Card.noCard,Card.noCard))
                # play king
                elif current_card == Card.king:
                    if not another_player.pretected:
                        all_actions=all_actions.append(PlayerAction(Card.king,another_player,Card.noCard,Card.noCard))
                    else:
                        # discard with no effect
                        all_actions=all_actions.append(PlayerAction(Card.king,None,Card.noCard,Card.noCard))
                # play countess
                elif current_card == Card.countess:
                    all_actions=all_actions.append(PlayerAction(Card.countess,None,Card.noCard,Card.noCard))
                # play princess
                elif current_card == Card.countess:
                    all_actions=all_actions.append(PlayerAction(Card.princess,None,Card.noCard,Card.noCard))
                    '''

    def heuristic(self, A):
        #Eventually we can implement the heuristic here
        return A[0]
