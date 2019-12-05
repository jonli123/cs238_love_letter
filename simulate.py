from game import Game
from card import Card
from player import Player
from heuristic_player import HeuristicPlayer
from sarsa_player import SarsaPlayer
from lambda_player import LambdaPlayer
from collections import defaultdict
import matplotlib.pyplot as plt
import pickle
import os.path
import random


numWinner = 0
numSimulations = int(1.1e5)
train_wins = [0, 0]
q_wins = [0, 0]

Q = defaultdict(int)

'''
filename = ''
try:
    if os.path.exists(filename):
        with open(filename, 'rb') as f:
            Q = pickle.load(f)
            print("load pickle")
except:
    Q = defaultdict(int)
    print("new Q")
'''

# training
for i in range(numSimulations):
    if i%10000 == 0:
        print(i)

    deck = Card.shuffle_deck()

    player0 = Player(0,deck[0],2)
    #to decrease lambda space set all the bs to the same and set p6 to 1
    #lambdas={'g2': 0.55, 'g4': 0.46, 'g5': 0.33, 'g7': 0.65, 'b2': 0.77, 'b4': 0.63, 'b5': 0.44, 'b6': 0.33, 'b7': 0.65, 'p2': 0.34, 'p6': 0.39}
    #player0 = LambdaPlayer(0, deck[0],2, lambdas)
    #player1 = HeuristicPlayer(1,deck[1],2)
    #her = i > 1e4
    if i < 1e5:
        player1 = SarsaPlayer(1,deck[1],2, Q, explore_prob=0.7, lam=True)
        deck = deck[2:]
        players = [player0,player1]

        game = Game(deck,players)
        result = game.simulate()
        train_wins[result] += 1

        Q = player1.get_Q()
    else:
        player1 = SarsaPlayer(1,deck[1],2, Q, explore_prob=0)
        deck = deck[2:]
        players = [player0,player1]

        game = Game(deck,players)
        result = game.simulate()
        q_wins[result] += 1

        Q = player1.get_Q()
    
# testing

    #print(Q.values())

#with open('Q.pkl', 'wb') as f:
#    pickle.dump(Q, f)

print("Num times player 0 won during training: ",train_wins[0])
print("Num times player 1 won during training: ",train_wins[1])
print()
print("Num times player 0 won after: ",q_wins[0])
print("Num times player 1 won after: ",q_wins[1])

plt.hist(Q.values())
plt.yscale('log')
plt.show()

