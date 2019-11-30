from player import Player

class HeuristicPlayer(Player):
    def take_turn(self,game_state,players):
        A = self.possible_actions(game_state,players)
        if not A:
            for card in self.get_hand():
                A.append(PlayerAction(card,None,Card.noCard))
            a = random.choice(A) #tuple of (card, target, guess)
        else:
            a = heuristic(A,game_state,players)
        #print(a)
        self.discard(a.card)
        return a

    def heuristic(self, A, game_state, players):
        #Given list of possible actions and game_state, return an action
        allSeenCards=game_state['allSeenCards']
        canTarget=game_state['canTarget']
        current_hand=self.get_hand()
        opponents=list(set(players) - set([players[self.id]]))
        #action: card player_target guess
        #If we know the opponent card and we have a 1, play it and guess the card
        #If we know the opponent card is less than ours and we have a baron, play it
        for opponent in opponents:
            if self.other_hand != Card.noCard:
                if self.other_hand != Card.guard and Card.guard in current_hand:
                    return PlayerAction(Card.guard,opponent.player,self.knowledge[opponent.player])
                if current_hand[0] == Card.baron and current_hand[1] > self.knowledge[opponent.player]:
                    return PlayerAction(Card.baron,opponent.player,Card.noCard)
                if current_hand[1] == Card.baron and current_hand[0] > self.knowledge[opponent.player]:
                    return PlayerAction(Card.baron,opponent.player,Card.noCard)
        #If we have a 4, play the 4

        #If we have a 2, play the 2

        #Never play an 8
        A_safe = A
        #random play
        a = random.choice(A_safe)
        return a
