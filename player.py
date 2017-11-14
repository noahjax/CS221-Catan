from collections import defaultdict
from pieces import *
from game import *
#import all the stuff

class HumanPlayer(object):
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
        self.devCards = defaultdict(int)
        self.roads = []
        self.occupyingNodes = []
        self.cities_and_settlements = []      #Don't necessarily need to keep track of pieces for each player, but could be useful
        self.numKnights = 0
        self.roadLength = 0
        self.numResources = 0
        self.isAi = False
       
        # Store the two tuples of coordinates where the initial settlements are placed
        self.initialSettlementCoords = [] 


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

    def place_settlement_human(self, node, game, firstTurn):
        settlement_to_add = Settlement(self, node)
        node.set_occupying_piece(settlement_to_add)
        self.cities_and_settlements.append(settlement_to_add)
        self.occupyingNodes.append(node)
        self.incrementScore(1)

        if firstTurn:
            for tile in node.touchingTiles:
                self.resources[tile.resource] += 1
                self.numResources += 1
        else:
            game.updateSettlementResources(self.resources)


    def place_city_human(self, node, player, game):
        prev_settlement = node.get_occupying_piece()
        player.cities_and_settlements.remove(prev_settlement)
        city_to_add = City(player, node)
        node.set_occupying_piece(city_to_add)
        player.cities_and_settlements.append(city_to_add)
        self.incrementScore(1)
        game.updateCityResources(player.resources)


    def place_settlement(self, positions, firstTurn):
        # To define with the AI but for now just pick first available
        # will eventually need to add logic for either it being AI or human click
        node = self.pick_position_settlement(positions)

        settlement_to_add = Settlement(self, node)
        node.set_occupying_piece(settlement_to_add)
        self.cities_and_settlements.append(settlement_to_add)
        self.occupyingNodes.append(node)
        self.score += 1

        if firstTurn:
            for tile in node.touchingTiles:
                self.resources[tile.resource] += 1
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
    def place_road_AI(self, numRoads, firstTurn):
        for i in range(numRoads):
            possible_road_locations = game.getRoadLocations(self)

            # will eventually need to add logic for either it being AI or human click
            position = self.pick_road_position(possible_road_locations)
            self.roads.append(position)
            game.roads.append(position)
            # Add logic for longest road/path stuff
            if not firstTurn:
                game.updateRoadResources(self.resources)
            self.updateLongestRoad(position)

    def place_road_human(self, roadLoc, firstTurn):
        self.roads.append(roadLoc)
        game.roads.append(roadLoc)
        if not firstTurn:
            game.updateRoadResources(self.resources)
        self.updateLongestRoad(roadLoc)
    
    def getName(self):
        return self.name

    def get_dev_card(self):
        card = game.devCards.pop(0)
        print "You got a " + card.type
        if card in self.devCards:
            self.devCards[card] += 1
        else:
            self.devCards[card] = 1

    def playDevCard(self, devCardString):
        card = self.devCards[devCardString].pop(0)
        card.play()

    def give_card(self):
        # Need to define this as an AI choice
        if len(self.resources) != 0:
            return self.resources.pop(0)
        return 0

    def updateLongestRoad(self):
        # Get the maximum two paths leading away from the starting point
        # return their sum
        roadNodes = []
        for road in self.roads:
            roadNodes.append(road.location[0])
            roadNodes.append(road.location[1])
        roadNodes = list(set(roadNodes))

        finLongestPaths = [] # Store the longest path length from each settlement

        for startPoint in self.initialSettlementCoords: 
            # Starting from each settlement, compute the 0-3 path lengths
            pathLens = []
            
            for neighbor in board.getNodeNeighbors(startPoint): 
                if neighbor in roadNodes:
                    alreadySearched = [startPoint]

                    def recurse(node):
                        nextToSearch = [n for n in self.board.getNeighborNodes(node) if n not in alreadySearched]
                        if len(nextToSearch) == 0:
                            return 0
                        else:
                            for n in nextToSearch:
                                alreadySearched.append(n)
                                return recurse(n) + 1

                    pathLens.append(recurse(neighbor))

            assert len(pathLens) <= 3
            if len(pathLens) == 0:
                finLongestPaths.append(0)
            elif len(pathLens) == 1:
                finLongestPaths.append(pathLens[0])
            elif len(pathLens) == 2:
                finLongestPaths.append(sum(pathLens))
            else:
                finLongestPaths.append(sum(sorted(pathLens)[1:3]))
        assert len(finLongestPaths) == 2
        self.roadLength = max(finLongestPaths)
        print('new longest path has length = ' + str(self.roadLength))

class AiPlayer(object):
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
        self.devCards = defaultdict(int)
        self.roads = []
        self.occupyingNodes = []
        self.cities_and_settlements = []      #Don't necessarily need to keep track of pieces for each player, but could be useful
        self.numKnights = 0
        self.roadLength = 0
        self.numResources = 0
        self.isAi = False
