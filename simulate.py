from game import Game
from card import Card
from player import Player

deck = Card.shuffle_deck()

player0 = Player(0,deck[0])
player1 = Player(1,deck[1])
deck = deck[2:]
players = [player0,player1]

example_game = Game(deck,players)
result = example_game.simulate()
print('Winner: ',result)
