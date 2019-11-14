from game import Game
from card import Card
from player import Player

player0 = Player(0)
player1 = Player(1)

deck = Card.shuffle_deck()

players = [player0,player1]

example_game = Game(deck,players)
result = example_game.simulate()
