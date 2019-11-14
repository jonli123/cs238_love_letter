PlayerAction = namedtuple('PlayerAction', 'discard player_target guess revealed_card')
# have to import Card object somehow
from Card import counts # map of total count

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
        # Game perform card drawing such that self.my_hand now has 2 cards
        all_actions=[]
        current_hand=self.my_hand        
        game=self.game
        # might want to make a method to return all players instead of direcly accessing it
        all_players=game._players 
        another_player=list(set(all_players) - set(self.player))
        # find possible cards to guess given the known state
        '''
        stateMap looks like 
        {allSeenCards:{guard:1,...,princess:0}, canTarget:True ,knowledge: {p0:king, p1:priest}}
        '''
        stateMap=game.getGameState()
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
            
        
                         
                         
                         
        
        
        








