from game import *
from pieces import *
import display
import board
from util import *

"""
Determines how devcards are created in game play, this will create
the given class and then return an instance of it with the correct 
parameters. 
"""
# Allow user to buy a devcard
def buyDevCard(player, type, players):
    if type == 'Knight':
        return Knight(player, players)
    elif type == 'Victory Point':
        return VictoryPoint(player)
    elif type == 'Monopoly':
        return Monopoly(player, players)
    elif type == 'Road Building':
        return RoadBuilding(player)
    elif type == 'Year of Plenty':
        return YearOfPlenty(player, players)

# Defines the Knight dev card from Catan
class Knight:

    # Initialization of the class
    def __init__(self, player, players):
        self.player = player
        self.players = players
        self.player.numKnights += 1
        self.type = 'Knight'

    # Plays the Knight card given a new position for the Robber
    def play(self, display, game):
        self.player.devCardsPlayed[self.type] += 1
        if not self.player.isAi:
            moveRobber(game, display)
        else:
            self.player.moveRobber(game, display)

        players_to_give_cards = set()

        # Check all players that need to give a card
        for oppPlayer in self.players:
            if not oppPlayer == self.player:
                for node in self.player.occupyingNodes:
                    for tile in node.touchingTiles:
                        if tile.hasRobber:
                            players_to_give_cards.add(oppPlayer)

        if len(players_to_give_cards) == 0:
            print("No players need to give cards")

        # For each of those players make them give a card
        for player in players_to_give_cards:
            player.give_card(self.player)

        # Increment the current players army
        self.player.numKnights += 1

        # If this gives them largest army update the game state
        if self.player.numKnights >= 3 and self.player.numKnights > game.currMaxKnights:
            if game.playerWithLargestArmy is not None:
                game.playerWithLargestArmy.hasLargestArmy = False

            self.player.score += 2
            game.currMaxKnights = self.player.numKnights
            game.playerWithLargestArmy = self.player
            self.player.hasLargestArmy = True


# Defines a default Victory Point dev card from Catan
class VictoryPoint:

    # Initialize the victory point card
    def __init__(self, player):
        self.player = player
        self.value = 1
        self.type = 'Victory Point'

    # Define what happens when the player plays this card
    def play(self):
        self.player.devCardsPlayed[self.type] += 1
        self.player.incrementScore(self.value)


# Defines the road building dev card from Catan
class RoadBuilding:

    def __init__(self, player):
        self.player = player
        self.type = 'Road Building'


class Monopoly:
    def __init__(self, player, players):
        self.player = player
        self.players = players
        self.type = 'Monopoly'

    def play(self):
        self.player.devCardsPlayed[self.type] += 1
        resource = getResourceInput()
        total = 0
        for player in self.players:
            if not player == self.player:
                if resource in player.resources:
                    numResources = player.resources[resource]
                    self.player.resources[resource] += numResources
                    self.player.numResources += numResources
                    player.resources[resource] = 0
                    total += numResources
        print("You stole a total of " + str(total) + " " + resource + " from the other players")

class YearOfPlenty:
    def __init__(self, player, players):
        self.player = player
        self.players = players
        self.type = 'Year of Plenty'

    def play(self):
        self.player.devCardsPlayed[self.type] += 1
        for i in range(2):
            resource = getResourceInput()
            self.player.resources[resource] += 1
            self.player.numResources += 1



