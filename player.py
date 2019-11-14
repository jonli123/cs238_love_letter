# have to import Card object somehow
from card import Card # map of total count
from collections import namedtuple
import numpy as np


PlayerAction = namedtuple('PlayerAction', 'discard player_target guess')


class Player():
    def __init__(self, player, starting_hand):
        #self.my_discards = []
        #self.opponent_discards = []
        #self.pool_discards = []
        self.discards = []
        self.player = player
        self.other_hand = Card.noCard #or it can be a number, which is the other persons hand
        self.my_hand = starting_hand
        self.new_card = None
        self.am_known = False
        self.protected = False
        self.other_protected = False
        self.win = None

    def get_hand(self):
        return self.my_hand

    def draw(self,card):
        if self.new_card != None:
            raise RuntimeError("already holding two cards {} and {}".format(self.my_hand, self.new_card))
        self.new_card = card

    def discard(self):
        self.discards.append(self.my_hand)
        return self.my_hand

    def take_turn(self,game_state,players):
        self.protected = False
        A = self.possible_actions(game_state,players)
        a = np.sample(A) #tuple of (card, target, guess)
        #a = self.heuristic(A)
        if a[0] == self.my_hand:
            self.my_hand = self.new_card
        self.new_card = None
        self.discards.append(a[0])
        return a

    def possible_actions(self,game_state,players):
        # Game perform card drawing such that self.my_hand now has 2 cards
        all_actions=[]
        current_hand=self.my_hand
        # might want to make a method to return all players instead of direcly accessing it
        all_players=players
        another_player=list(set(all_players) - set(self.player))
        # find possible cards to guess given the known state
        '''
        stateMap looks like
        {allSeenCards:{guard:1,...,princess:0}, canTarget:True ,knowledge: {p0:king, p1:priest}}
        '''
        stateMap=game_state
        allSeenCards=stateMap['stateMap']
        canTarget=stateMap['canTarget']
        knowledge=stateMap['knowledge']

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

    def heuristic(self, A):
        #Eventually we can implement the heuristic here
        return A[0]
