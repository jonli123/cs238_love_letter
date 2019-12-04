from game import Game
from card import Card
from player import Player
from heuristic_player import HeuristicPlayer
from sarsa_player import SarsaPlayer
from collections import defaultdict
import matplotlib.pyplot as plt
import pickle
import os.path

numWinner = 0
numSimulations = int(10)
p1_wins = p0_wins = 0

Q = defaultdict(int)

filename = ''
try:
    if os.path.exists(filename):
        with open(filename, 'rb') as f:
            Q = pickle.load(f)
            print("load pickle")
except:
    Q = defaultdict(int)
    print("new Q")

for i in range(numSimulations):
    if i%1000 == 0:
        print(i)

    deck = Card.shuffle_deck()

    player0 = Player(0,deck[0],2)
    #player1 = HeuristicPlayer(1,deck[1],2)
    player1 = SarsaPlayer(1,deck[1],2, Q)
    deck = deck[2:]
    players = [player0,player1]

    example_game = Game(deck,players)
    result = example_game.simulate()
    if result == 1:
        p1_wins += 1
    elif result == 0:
        p0_wins += 1

    Q = player1.get_Q()

    #print(Q.values())

#with open('Q.pkl', 'wb') as f:
#    pickle.dump(Q, f)

print("Num times player 0 won: ",p0_wins)
print("Num times player 1 won: ",p1_wins)

'''
plt.hist(Q.values())
plt.yscale('log')
plt.show()
'''
