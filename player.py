from collections import defaultdict
from pieces import *
from game import *
#import all the stuff

class Player(object):
    """
    Class for each player 

    (Add more stuff)
    """
    def __init__(self, turn_num, name, color):
        
        if 3 < turn_num < 0:
            raise Exception("Turn number must be between 1 and 4 inclusive")

        #Lets have turn number start at 0 because it might make coding nicer
        self.turn_num = turn_num
        self.name = name
        self.color = color
        self.score = 0

        #Storing these in dict to make it easy to figure out how many they have. {"item": count}
        self.resources = defaultdict(int)
        self.devCards = {}
        self.roads = []
        self.occupyingNodes = []
        self.cities_and_settlements = []      #Don't necessarily need to keep track of pieces for each player, but could be useful
        self.numKnights = 0
        self.roadLength = 0
        self.numResources = 0
        self.isAi = False



    #Allows you to check if two players are equal...Not sure if we need it, but may come in handy
    def __eq__(self, other):
        if other is None:
            return False
        if other.__class__ != Player:
            return False
        return (self.color == other.color
                and self.name == other.name
                and self.turn_num == other.turn_num
                and self.devCards == other.devCards
                and self.resources == other.resources
                and self.pieces == other.pieces)

    def incrementScore(self, value):
        self.score += value

    def place_settlement(self, positions, player, firstTurn):
        # To define with the AI but for now just pick first available
        # will eventually need to add logic for either it being AI or human click
        node = self.pick_position_settlement(positions)

        settlement_to_add = Settlement(player, node)
        node.set_occupying_piece(settlement_to_add)
        player.cities_and_settlements.append(settlement_to_add)
        player.occupyingNodes.append(node)
        player.score += 1

        if firstTurn:
            for tile in node.touchingTiles:
                player.resources[tile.resource] += 1
                self.numResources += 1
        else:
            game.updateSettlementResources(self.resources)
        return node

    # This will be an AI decision eventually
    def pick_position_settlement(self, positions):
        return positions[0]

    # This will be an AI decision eventually
    def pick_road_position(self, positions):
        return positions[0]

    # This will figure out how to place a road
    # We will need to check that player has the resources before calling this
    def place_road(self, numRoads, firstTurn):
        for i in range(numRoads):
            possible_road_locations = game.getRoadLocations(self)

            # will eventually need to add logic for either it being AI or human click
            position = self.pick_road_position(possible_road_locations)
            self.roads.append(position)
            game.roads.append(position)
            # Add logic for longest road/path stuff
            if not firstTurn:
                game.updateRoadResources(self.resources)

    def getName(self):
        return self.name

    def playDevCard(self, devCardString):
        card = self.devCards[devCardString].pop(0)
        card.play()

    def give_card(self):
        # Need to define this as an AI choice
        if len(self.resources) != 0:
            return self.resources.pop(0)
        return 0

