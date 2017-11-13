from game import *
from pieces import *


"""
Determines how devcards are created in game play, this will create
the given class and then return an instance of it with the correct 
parameters. 
"""


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
    def play(self, position):
        game.set_robber_location(position)
        players_to_give_cards = set()

        # Check all players that need to give a card
        for oppPlayer in self.players:
            if not oppPlayer == self.player:
                for node in self.player.nodes:
                    for tile in node.tiles:
                        if tile == position:
                            players_to_give_cards.add(oppPlayer)

        # For each of those players make them give a card
        for player in players_to_give_cards:
            resource = player.give_card()
            if resource != 0:
                self.player.resources[resource] += 1

        # Increment the current players army
        self.player.numKnights += 1

        # If this gives them largest army update the game state
        if self.player.numKnights >= 3 and self.player.numKnights > Game.currMaxKnights:
            self.player.score += 2
            Game.currMaxKnights = self.player.numKnights


# Defines a default Victory Point dev card from Catan
class VictoryPoint:

    # Initialize the victory point card
    def __init__(self, player):
        self.player = player
        self.value = 1
        self.type = 'Victory Point'

    # Define what happens when the player plays this card
    def play(self):
        self.player.incrementScore(self.value)


# Defines the road building dev card from Catan
class RoadBuilding:

    def __init__(self, player):
        self.player = player
        self.type = 'Road Building'

        # Defines the logic for longest road, needs to be updated when we figure out path logic
        if len(self.player.roads) >= 9 and len(self.player.roads) > Game.currMaxRoad:
            Game.currMaxRoad = self.player.resources['Road']
            self.player.incrementScore(2)

    def play(self, positions):
        # Need to pick the two positions before this point (AI again)
        for position in positions:
            newRoad = Road(self.player, position)
            self.player.roads.append(newRoad)


class Monopoly:
    def __init__(self, player, players):
        self.player = player
        self.players = players
        self.type = 'Monopoly'

    def play(self, resource):
        for player in self.players:
            if not player == self.player:
                if resource in player.resources:
                    numResources = player.resources[resource]
                    self.player.resources[resource] += numResources
                    self.player.numResources += numResources
                    player.resources[resource] = 0

class YearOfPlenty:
    def __init__(self, player, players):
        self.player = player
        self.players = players
        self.type = 'Year of Plenty'

    def play(self, resourceOne, resourceTwo):
        self.player.resources[resourceOne] += 1
        self.player.resources[resourceTwo] += 1
        self.player.numResources += 2




