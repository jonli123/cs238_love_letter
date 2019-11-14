from game import Game
from card import Card
from player import Player

<<<<<<< HEAD
deck = Card.shuffle_deck()


player0 = Player(0,deck[0])
player1 = Player(1,deck[1])
deck = deck[2:]
=======
player0 = Player(0)
player1 = Player(1)

deck = Card.shuffle_deck()

>>>>>>> e9e591490cbe0094e2a9d12092916754a04d349c
players = [player0,player1]

example_game = Game(deck,players)
result = example_game.simulate()
