# cs238_love_letter

API Interface:

Game Class:
  Provides the framework for playing the game.
  * init(players,deck) - Initializes a game with a given deck and players
  * simulate - simulates an entire game with the deck provided
  * turn - Calls Player functions such as draw and discard; uses the action returned to takeAction.
  * getGameState - Returns info about the current state of the game that is available to all players
  * takeAction(player,action) - Makes the player take the action that the player decided to take. This function manipulates the state of the game and the state of the player
  
  
Player Class:
  Stores the state of a Player. Contains all the intelligence involved in player decision making.
  * init - initializes a Player; should start with no cards
  * draw(card) - Player adds card to their hand
  * discard(game_state) - Player discards a card from their hand and returns which card they discard and what action they are taking
  * possible_actions(game_state) - Returns all possible actions a player has.
  
  
Card Class:
  Provides a description of what a card is (integer)
  * shuffle_deck - generates a random deck
