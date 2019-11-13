from game import Game
from card import Card
from player import Player

player1 = Player()
player2 = Player()

deck = Card.shuffle_deck()

players = [player1,player2]

example_game = Game(deck,players)
result = example_game.simulate()
