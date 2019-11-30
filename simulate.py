from game import Game
from card import Card
from player import Player
from heuristic_player import HeuristicPlayer

numWinner = 0
numSimulations = 10000
p1_wins = p0_wins = 0
for i in range(numSimulations):
    deck = Card.shuffle_deck()

    player0 = Player(0,deck[0],2)
    player1 = HeuristicPlayer(1,deck[1],2)
    deck = deck[2:]
    players = [player0,player1]

    example_game = Game(deck,players)
    result = example_game.simulate()
    if result == 1:
        p1_wins += 1
    elif result == 0:
        p0_wins += 1

print("Num times player 0 won: ",p0_wins)
print("Num times player 1 won: ",p1_wins)
