from collections import defaultdict
from pieces import *
from game import *
#import all the stuff

'''
Player superclass for shared functionality across human and AI players. Should be 
mostly useful for initialization and establishing values that the player stores.
'''
class Player:
    def __init__(self, turn_num, name, color):

        if 3 < turn_num < 0:
            raise Exception("Turn number must be between 0 and 3 inclusive")

        self.turn_num = turn_num
        self.name = name
        self.color = color
        self.score = 0

        #Storing these in dict to make it easy to figure out how many they have. {"item": count}
        self.resources = defaultdict(int)
        self.devCards = defaultdict(int)
        self.roads = []
        self.occupyingNodes = []
        # Don't necessarily need to keep track of pieces for each player, but could be useful
        self.cities_and_settlements = []
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
        if other.__class__ != self.__class__:
            return False
        return (self.color == other.color
                and self.name == other.name
                and self.turn_num == other.turn_num
                and self.devCards == other.devCards
                and self.resources == other.resources)

    def incrementScore(self, value):
        self.score += value

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

    #roadLoc should be a pair of node objects
    def place_road(self, roadLoc, game, firstTurn=False):
        self.roads.append(roadLoc)
        game.roads.append(roadLoc)
        if not firstTurn:
            game.updateRoadResources(self.resources)
        # TODO: Check longest road logic

    def place_settlement(self, node, game, firstTurn=False):
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

    def place_city(self, node, game):
        prev_settlement = node.get_occupying_piece()
        self.cities_and_settlements.remove(prev_settlement)
        city_to_add = City(self, node)
        node.set_occupying_piece(city_to_add)
        self.cities_and_settlements.append(city_to_add)
        self.incrementScore(1)
        game.updateCityResources(self.resources)
    
    


#############################################################################
#############################   Human Player    #############################
#############################################################################


class HumanPlayer(Player):
    """
    Class for each player 

    (Add more stuff)
    """
    def __init__(self, turn_num, name, color):
        Player.__init__(self, turn_num, name, color)
        self.isAI = False

    '''
    Shouldn't need much code here because human actions are much more limited than the AI,
    which needs to know all possible actions and respond
    '''
    # def place_settlement_human(self, node, game, firstTurn):
    #     settlement_to_add = Settlement(self, node)
    #     node.set_occupying_piece(settlement_to_add)
    #     self.cities_and_settlements.append(settlement_to_add)
    #     self.occupyingNodes.append(node)
    #     self.incrementScore(1)

    #     if firstTurn:
    #         for tile in node.touchingTiles:
    #             self.resources[tile.resource] += 1
    #             self.numResources += 1
    #     else:
    #         game.updateSettlementResources(self.resources)


    # def place_city_human(self, node, player, game):
    #     prev_settlement = node.get_occupying_piece()
    #     player.cities_and_settlements.remove(prev_settlement)
    #     city_to_add = City(player, node)
    #     node.set_occupying_piece(city_to_add)
    #     player.cities_and_settlements.append(city_to_add)
    #     self.incrementScore(1)
    #     game.updateCityResources(player.resources)

    # # This will be an AI decision eventually
    # def pick_position_settlement(self, positions):
    #     return positions[0]

    # # This will be an AI decision eventually
    # def pick_road_position(self, positions):
    #     return positions[0]

    
                       
    # def place_road_human(self, roadLoc, firstTurn):
    #     self.roads.append(roadLoc)
    #     game.roads.append(roadLoc)
    #     if not firstTurn:
    #         game.updateRoadResources(self.resources)
    #     # TODO: Check longest road logic

    #Not sure when we would use this
    # def give_card(self):
    #     # Need to define this as an AI choice
    #     if len(self.resources) != 0:
    #         return self.resources.pop(0)
    #     return 0


#############################################################################
#############################   AI Player    ################################
#############################################################################


class AiPlayer(Player):
    """
    Class for AI Player

    (Add more stuff)
    """

    def __init__(self, turn_num, name, color):
        Player.__init__(self, turn_num, name, color)
        self.isAI = True

    '''
    Start of actual logic
    '''

    #Handles picking a road and building it. Assumes possible road locations isn't empty
    def pick_road_position(self, possible_locations):
        return possible_locations[0]
        #AI stuff
        #return roadLoc
   
    def pick_settlement_position(self, possible_locations):
        return possible_locations[0]
        #AI stuff
        #return settlementLoc

    def pick_city_position(self, possible_locations):
        return possible_locations[0]
        #AI stuff
        #return settlementLoc
    
    # This will figure out how to place a road
    # We will need to check that player has the resources before calling this
    def place_road_AI(self, numRoads, firstTurn):
        for i in range(numRoads):
            possible_road_locations = game.getRoadLocations(self)
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
'''
class AiPlayer(object):
    """
    Class for each player

    (Add more stuff)
    """
    def __init__(self, turn_num, name, color):
        pass

    def place_settlement(self, positions, firstTurn):
        # To define with the AI but for now just pick first available
        # will eventually need to add logic for either it being AI or human click
        node = self.pick_settlement_position(positions)

        settlement_to_add = Settlement(self, node)
        node.set_occupying_piece(settlement_to_add)
        self.cities_and_settlements.append(settlement_to_add)
        self.occupyingNodes.append(node)
        self.score += 1

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
        
        if firstTurn:
            for tile in node.touchingTiles:
                self.resources[tile.resource] += 1
                self.numResources += 1
        else:
            game.updateSettlementResources(self.resources)
        return node
'''
