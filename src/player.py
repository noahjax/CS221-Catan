from collections import defaultdict
from pieces import *
from game import *
import random
import copy
import util
from log import *
import copy
import numpy as np

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

        # Storing these in dict to make it easy to figure out how many they have. {"item": [obj,obj,...]}
        self.resources = defaultdict(int)
        self.devCards = defaultdict(int)
        self.devCardsPlayed = defaultdict(int)
        self.newDevCards = defaultdict(int)
        self.roads = []
        self.numTimesOverSeven = 0
        self.numCardsDiscarded = 0
        self.holdsLongestRoad = False
        self.hasLargestArmy = False
        self.features = {"Has largest army": 0, "Num roads": 0, "Resource spread": 0,
                         "Num cities": 0, "Has longest road": 0, "Num turns with more than 7 cards": 0,
                         "Num cards discarded": 0, "Devcards played": 0, "Grain": 0,
                         "Brick": 0, "Ore": 0, "Wood": 0, "Wool": 0, "Longest Road": 0, "Num settlements": 0,
                         "Knight": 0, "Monopoly": 0, "Year of Plenty": 0, "Victory Point": 0,
                         "Road Building": 0, "Desert": 0, "Score": 0, "Has Won": 0,
                         'Ratio roads to settlements': 0, 'Ratio cities to settlements': 0,
                         'Squared distance to end': 0, 'Num accesible resources': 0}

        # Map each node to a list of other road nodes it is touching
        # This is used for computing the longest path
        self.touching = defaultdict(list)

        self.occupyingNodes = []

        #Rates that you can swap cards in at. Currently 4 for all cards but can change as we introduce ports
        #At some point we should make it so desert doesn't get distributed to people at all
        self.exchangeRates = {'Ore':4, 'Brick':4, 'Wood':4, 'Wool':4, 'Grain':4, 'Desert':1000000000}

        # Don't necessarily need to keep track of pieces for each player, but could be useful
        self.cities_and_settlements = []
        self.numKnights = 0
        self.longestRoadLength = 0
        self.numResources = 0
        self.isAI = False
       
        # Store the two tuples of coordinates where the initial settlements are placed
        self.initialSettlementCoords = [] 

    # Allows you to check if two players are equal...Not sure if we need it, but may come in handy
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

    # Increment a players score by a certain amount
    def incrementScore(self, value):
        self.score += value

    # Places road in desired location, updates necessary data structures
    # roadLoc should be a tuple of node objects
    def place_road(self, roadLoc, game, firstTurn=False, future=False):
        self.roads.append(roadLoc)
        game.roads.append(roadLoc)
        
        if not firstTurn:
            game.updateRoadResources(self)

        if future: return

        self.updateLongestRoad(roadLoc)


        # Update game longest road and players score
        if self.longestRoadLength > game.longestRoad:
            game.longestRoad = self.longestRoadLength
            if self.longestRoadLength >= 5:
                if game.currPlayerWithLongestRoad == None:
                    self.score += 2
                    self.holdsLongestRoad = True
                    game.currPlayerWithLongestRoad = self
                if not game.currPlayerWithLongestRoad is None and not game.currPlayerWithLongestRoad == self:
                    game.currPlayerWithLongestRoad.score -= 2
                    game.currPlayerWithLongestRoad.holdsLongestRoad = False
                    self.score += 2
                    game.currPlayerWithLongestRoad = self
                    self.holdsLongestRoad = True


    # Places settlement in desired location, updates necessary data structures
    def place_settlement(self, node, game, firstTurn=False):
        # print "placing settlement", node.row, node.col
        settlement_to_add = Settlement(self, node)
        node.set_occupying_piece(settlement_to_add)
        self.cities_and_settlements.append(settlement_to_add)
        self.occupyingNodes.append(node)
        self.incrementScore(1)

        if firstTurn:
            self.initialSettlementCoords.append((node.row, node.col))
            for tile in node.touchingTiles:
                if tile.resource is not 'Desert':
                    self.resources[tile.resource] += 1
                    self.numResources += 1
        else:
            game.updateSettlementResources(self)

    # Places city in desired location, updates necessary data structures
    def place_city(self, node, game):
        # Update: modified how settlements are removed. When the duplicate player object was passed out of get_successor,
        # it was located at a different memory address than the original owner of the city, and so list.remove(x) would throw and error
        prev_settlement = node.get_occupying_piece()
        origLen = len(self.cities_and_settlements)
        self.cities_and_settlements = [c_or_s for c_or_s in self.cities_and_settlements if str(c_or_s.location) != str(node)]
        # self.cities_and_settlements.remove(prev_settlement)
        city_to_add = City(self, node)
        node.set_occupying_piece(city_to_add)
        self.cities_and_settlements.append(city_to_add)
        self.incrementScore(1)
        game.updateCityResources(self)

    # Allows a player to discard a resource
    def discard_resource(self, resource):
        if resource in self.resources and self.resources[resource] > 0:
            self.resources[resource] -= 1
            self.numResources -= 1
        else:
            print("Sorry you do not have any of these to discard")

    # Should be called whenever a road is built.
    def updateLongestRoad(self, road):
        # Update the 'touching' dict (self.touching)
        roadNodes = list(set(list(sum(self.roads, ())))) # Flatten the roads into a (unique) list of nodes 
        nn1, nn2 = road # new node 1, 2 (for the new node)
        for node in roadNodes:
            # If a road exists between the two, they are touching
            if (nn1, node) in self.roads or (node, nn1) in self.roads:
                self.touching[nn1].append(node)
                self.touching[node].append(nn1)
            if (nn2, node) in self.roads or (node, nn2) in self.roads:
                self.touching[nn2].append(node)
                self.touching[node].append(nn2)
        
        # Use the touching dict to get the longest path
        longestPaths = []
        for startNode in roadNodes:
            visited = []
            
            def longestPath(node, length, last, path):
                toVisit = [n for n in self.touching[node] if n != last]
                if node in visited or len(toVisit) == 0:
                    return length
                visited.append(node)
                return max(longestPath(neighbor, length + 1, node, path + [neighbor]) for neighbor in toVisit) 

            longestPaths.append(longestPath(startNode, 0, None, [startNode]))

        self.longestRoadLength = max(longestPaths)

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
    # Deals with a player having more than 7 cards when a seven is rolled
    def over_seven(self):
        numResources = self.numResources
        while self.numResources > (numResources / 2):
            print("You have more than 7 resources, they are as follows: ")
            for resource in self.resources:
                print(resource + ": " + str(self.resources[resource]))
            to_discard = util.getResourceInput()
            self.discard_resource(to_discard)

    def give_card(self, oppPlayer):
        print("You need to give a card to your opponent, please select one")
        resource = util.getResourceInput()
        self.resources[resource] -= 1
        self.numResources -= 1
        oppPlayer.resources[resource] += 1
        oppPlayer.numResources += 1
        print(self.name + " gave one " + resource + " to " + oppPlayer.name)

    def moveRobber(self, game, display):
        util.moveRobber(game, display)


#############################################################################
#############################   AI Player    ################################
#############################################################################


class AiPlayer(Player):
    """
    Class for AI Player

    Ideally we can create multiple subclasses of this with different ways of picking
    moves to test what features work better in different scenarios. This class operates
    as a random AI, and subsequent classes will need much more sophisticated implementations
    of pick_*_position and other methods using real features
    """

    def __init__(self, turn_num, name, color, weightsLog=None):
        Player.__init__(self, turn_num, name, color)
        self.isAI = True

        #Used for unchoosing a devCard
        self.prevDevCards = []
       
    '''
    These functions are used for pregame positions

    Picking positions mostly useful for pregame when possible moves are limited and it's 
    easier to simply pick a random position. Full gameplay uses more extensive methods
    defined later.
        -Leave these as seperate functions because subclasses may want to use different 
         implementations even though this class doesn't. 
    '''
    #Handles picking a road and building it. Assumes possible road locations isn't empty
    #Including game in case we want to get more information about road locations
    def pick_road_position(self, settlementLoc, game):
        possible_roads = [(settlementLoc, neighbor) for neighbor in settlementLoc.neighbours]
        return random.choice(possible_roads)

    def pick_road_devcard_ai(self, possRoads):
        return random.choice(possRoads)
   
    def pick_settlement_position(self, game):
        possible_settlements = game.getSettlementLocations(self, True)
        return random.choice(possible_settlements)
    
    '''Functions for the robber logic'''

    def moveRobber(self, game, display):
        positions = self.getPossibleRobberPositions(game)
        if not positions:
            return
        maxNum, bestTile = -1, None
        for tile in positions:
            currNum = 0
            for node_coordinates in game.board.getNodesForTile(tile):
                node = game.board.getNodeFromCoords(node_coordinates[0], node_coordinates[1])
                if node is not None and node.isOccupied:
                    if isinstance(node.occupyingPiece, Settlement):
                        currNum += 1
                    if isinstance(node.occupyingPiece, City):
                        currNum += 2
            if currNum > maxNum:
                maxNum, bestTile = currNum, tile

        if display is not None:
            display.placeRobber(bestTile.id)
        game.set_robber_location(bestTile.id, display)

    def getPossibleRobberPositions(self, game):
        possTiles = []
        # For every tile check if it has a piece on it with a score less than three
        for tile in game.board.tiles:
            if tile.hasRobber:
                continue
            isValid = True
            for node_coordinates in game.board.getNodesForTile(tile):
                node = game.board.getNodeFromCoords(node_coordinates[0], node_coordinates[1])
                if node is not None and node.isOccupied:
                    if node.occupyingPiece.player.score <= 3 or node.occupyingPiece.player is self:
                        # print("Sorry this is an invalid robber location")
                        isValid = False
            if isValid:
                possTiles.append(tile)

        return possTiles

    # If the AI has over seven cards currently just discard all until you get a
    def over_seven(self):
        numResources = self.numResources
        while self.numResources > (numResources/2):
            resource = self.getFavResource()
            self.resources[resource] -= 1
            self.numResources -= 1
            self.numCardsDiscarded += 1

    #Don't think we need this considering that this is probably for pregame
    # def pick_city_position(self, possible_locations):
    #     return possible_locations[0]
    #     #AI stuff
    #     #return settlementLoc

    '''
    Given a list of all possible moves, pick a move. This simple implementation picks 
    a random move and returns it. 
        -possible_moves in format [{(piece, count): [loc1, loc2]},{(piece,count): [loc1]}, ...]
        -Move should be in dict format {(Piece, count): loc, (Piece, count): loc}
        -Not sure how we will update this with devCards 
        -Probably need check to make sure that you don't try to place two pieces in the same
         location
    '''

    def pickMove(self, game):
        #Always buy a devCard if you can

        possible_moves = game.getPossibleActions(self)

        for move in possible_moves:
            if not move: continue
            for action, location in move.items():
                piece, count = action
                if piece == 'buyDevCard':
                    move[action] = None
                    return move
        
        #Get a random move 
        move = random.choice(possible_moves)
        if not move: return move

        for action, locations in move.items():
            piece, count = action

            #Handle case where you exchange resource cards
            if isinstance(piece, tuple):
                move[action] = None
            #Handle selecting a random move
            else:
                random.shuffle(move[action])
                move[action] = move[action][:count]

        return move 

    #Randomly pick and play a devCard
    def pickDevCard(self):
        options = []
        for devType, cards in self.devCards.items():
            if cards:
                options.append(devType)
        if not options:
            return None
        return random.choice(options)
        
    #Function used for the monopoly devcard to get the resource you want
    def getFavResource(self):
        resources = [resource for resource in self.resources if self.resources[resource] > 0]
        if not resources:
            return 'Grain'
        return random.choice(resources)
    
    #Random AI should still be able to do this at some point, even if not yet
    # TODO: Currently gives away a random card. At some point would be nice to 
    # give away more optimally
    def give_card(self, oppPlayer):
        if self.numResources > 0:
            #Randomly select a resource to give up
            resource = random.choice(self.resources.keys())
            while(not self.resources[resource]):
                resource = random.choice(self.resources.keys())
            
            self.resources[resource] -= 1
            self.numResources -= 1
            oppPlayer.resources[resource] += 1
            oppPlayer.numResources += 1

    '''
    Given a state and an move, returns the successor state. 
    Used by eval function to determine what move to take from a given state
    Make sure to delete the successor state after using it so we don't have a million copies
    floating around
    '''

    #Updates a game after a move so the new gamestate s' can be used in Eval(s')
    def do_move(self, game, move, firstTurn=False):
        
        # for action, loc in move.items(): <- again, we're only considering single locations at this point, so 
        # this loop is not needed at the moment
        # print "move: ", move
        action, loc = move
        piece, count = action

        #Exchange resources
        if isinstance(piece[0], tuple):
            oldResource, newResource = piece
            self.resources[oldResource] -= count
            self.resources[newResource] += 1
            self.numResources -= count
            self.numResources += 1
                
        #Place piece
        else:
            if piece == 'Settlement':
                self.place_settlement(loc, game, firstTurn)
            elif piece == 'City':
                self.place_city(loc, game)
            elif piece == 'Road':
                self.place_road(loc, game, firstTurn, True)
            elif piece == 'DevCard':
                game.buyDevCard(self)
        
        return game
    
    #TODO: Potential issue: What happens when we run this at a depth > 1 and we want to 
    #Undoes a move, return s' to state s. Assumes move you are undoing was the last move made.
    def undo_move(self, game, move, firstTurn=False):
        piece, count = move[0]
        loc = move[1]

        #Exchange resources
        if isinstance(piece, tuple):
            oldResource, newResource = piece
            self.resources[oldResource] += count
            self.resources[newResource] -= 1
            self.numResources += count
            self.numResources -= 1
                
        #Place piece
        else:
            if piece == 'Settlement':
                self.remove_settlement(loc, game)
            elif piece == 'City':
                self.remove_city(loc, game)
            elif piece == 'Road':
                self.remove_road(loc, game)
            elif piece == 'DevCard':
                game.returnDevCard(self)
        
        return game

    #Helper to remove roads
    #TODO: handle undoing longest road
    def remove_road(self, roadLoc, game, firstTurn=False):
        del self.roads[-1]
        del game.roads[-1]

        if not firstTurn:
            game.updateRoadResources(self, True)

        #Longest road stuff
        #TODO TODO TODO
        

    #Helper to remove settlements
    def remove_settlement(self, node, game, firstTurn=False):
        node.occupyingPiece = None
        node.isOccupied = False
        del self.cities_and_settlements[-1]
        del self.occupyingNodes[-1]
        self.score -= 1

        if firstTurn:
            self.initialSettlementCoords.append((node.row, node.col))
            for tile in node.touchingTiles:
                if tile.resource is not 'Desert':
                    self.resources[tile.resource] -= 1
                    self.numResources -= 1
        else:
            game.updateSettlementResources(self, True)

    #Helper to remove cities
    def remove_city(self, node, game):
        del node.occupyingPiece
        node.occupyingPiece = Settlement(self, node)
        del self.cities_and_settlements[-1]
        self.occupyingNodes.append(node)
        self.score -= 1

        game.updateCityResources(self, True)

    #Returns the successor state after a move has been taken
    def get_successor(self, game, move):

        #Do each indivdual move one at a time
        # for move in moves:
        game = self.do_move(game, move)
        return game

    #Update weights now that game is over and we know the outcome
    def update_weights(self, bestFeatures, bestWeights, scoreDiff):
        for feature, count in bestFeatures.items():
            bestWeight = bestWeights[feature]
            weightdiff = bestWeight - self.weights[feature]
            self.weights[feature] += 0.01 * scoreDiff * weightdiff
        return self.weights

    #Returns to starting state from a successor state
    def undo_successor(self, game, moves):
        actions = moves.items()

        #Loop backwards to undo moves in the correct order
        for i in range(len(actions), -1, -1):
            move = actions[i]
            game = self.undo_move(game, move)

        return game


    # def get_successor(self, game, move):
    #     new_game = copy.deepcopy(game) # Exceeds max recursive depth
    #     player = new_game.players[self.turn_num]
        
    #     # for action, loc in move.items(): <- again, we're only considering single locations at this point, so 
    #     # this loop is not needed at the moment
    #     piece, count = move[0]
    #     loc = move[1]

    #     #Exchange resources
    #     if isinstance(piece, tuple):
    #         oldResource, newResource = piece
    #         player.resources[oldResource] -= count
    #         player.resources[newResource] += 1
                
    #     #Place piece
    #     else:
    #         # Might want to flip structure of for loop and if statements
    #         # Updated this to only take in a single location. In evaluateMoveValue, we're only 
    #         # considering the value of moves made in isolation, which reduces the number of permutations
    #         # that could be made of different moves. May be a less intelligent approach for the AI but
    #         # might save some complexity. 
    #         if piece == 'Settlement':
    #             player.place_settlement(loc, new_game)
    #         elif piece == 'City':
    #             player.place_city(loc, new_game)
    #         elif piece == 'Road':
    #             player.place_road(loc, new_game)
    #         elif piece == 'DevCard':
    #             new_game.buyDevCard(player)
        
    #     #Pick and play a devCard. Often won't do anything
    #     devCard = player.pickDevCard()
    #     #Had to copy devCard logic because it relied on the play class to 
    #     #handle road building. 
    #     if devCard: 
    #         if type in player.devCards and player.devCards[type] >= 0:
    #             card = player.devCards[type].pop(0)
    #         if type == 'Knight':
    #             card.play(self.display, new_game) 
    #         elif type == 'Road Building':
    #             for i in range(2):
    #                 possible_locations = new_game.getRoadLocations(player)
    #                 loc = self.pick_road_position(possible_locations)
    #                 self.place_road(loc, new_game, True)
    #         else:
    #             card.play()
    #     # else:
    #     #     print("Sorry you do not have that dev card")

    #     return new_game



    '''Random AI doesn't have a feature extractor, but we want it to be compatible with test'''
    def feature_extractor(self):
        pass

      
class WeightedAI(AiPlayer):
  
    def __init__(self, turn_num, name, color, weightsLog):
        AiPlayer.__init__(self, turn_num, name, color, weightsLog)
        self.weightsLog = weightsLog
        self.weights = defaultdict(float, weightsLog.readDict())
        if 'DELETE ME' in self.weights.keys():
            # The weights log has not been initialized
            weights = self.features # Get the list of features
            for k in weights:
                # Initialize each feature to a random weight
                weights[k] = random.randint(-3, 3)
            weights['Score'] = abs(weights['Score'])
            weights['Has Won'] = 1000
            weights['Ratio roads to settlements'] = random.randint(-5, -3)
            weights['Squared distance to end'] = random.randint(-1, 1)


            self.weights = weights
            # Overwrite the log with the randomized weights dict
            weightsLog.log_dict(self.weights)

    # Use the weights to determine the value of a given roll
    def evaluateMoveValue(self, game, move):
        if not move:
            return -1
        future = self.do_move(game, move) 
        futureFeatures = future.players[self.turn_num].feature_extractor()
        score = util.dotProduct(futureFeatures, self.weights)
        self.undo_move(game, move)
        return score
    
    # Figure out how many of each resource we would expect per roll
    def expected_resources_per_roll(self):
        possibleRolls = [a+b for a in range(1, 7) for b in range(1, 7)]
        def prob(num):
            return len([a for a in possibleRolls if a == num]) / 36.0

        expected_resources = defaultdict(float)
        multiplier = 1
        for settlement in self.cities_and_settlements:
            if isinstance(settlement, City):
                multiplier = 2
            for tile in settlement.location.get_tiles():
                expected_resources[tile.resource] += prob(tile.value) * multiplier

        if not expected_resources:
            for resource in self.resources:
                expected_resources[resource] = 0
        return expected_resources

    def getNumSettlementsAndCities(self):
        city, settlement = (0, 0)
        for city_or_settlement in self.cities_and_settlements:
            if isinstance(city_or_settlement, City):
                city += 1
            else:
                settlement += 1

        return city, settlement

    def pick_settlement_position(self, game):
        possible_settlements = game.getSettlementLocations(self, True)
        maxScore, maxLocation = float('-inf'), None
        for settlement in possible_settlements:
            action = ('Settlement', 1)
            location = settlement
            score = self.evaluateMoveValue(game, (action, location))
            # print score
            if score > maxScore:
                maxScore = score
                maxLocation = location
        return maxLocation

    def getAccessibleResources(self, expectedResources):
        score = 0
        for resource in expectedResources:
            if expectedResources[resource] > 0:
                score += 1
        return score

    def feature_extractor(self):
        expectedResources = self.expected_resources_per_roll() 
        features = expectedResources 
        features['Devcards played'] = len(self.devCardsPlayed.values())
        features.update(self.devCardsPlayed)
        features['Num roads'] = len(self.roads)
        features['Longest Road'] = self.longestRoadLength
        numCities, numSettlements = self.getNumSettlementsAndCities()
        features['Num cities'] = numCities
        features['Num settlements'] = numSettlements
        features['Num turns with more than 7 cards'] = self.numTimesOverSeven
        features['Resource spread'] = np.std([expectedResources[k] for k in expectedResources.keys()])
        features['Has longest road'] = 1 if self.holdsLongestRoad else 0
        features['Has largest army'] = 1 if self.hasLargestArmy else 0
        features['Num cards discarded'] = self.numCardsDiscarded
        features['Score'] = self.score
        features['Has Won'] = self.score == 10
        features['Ratio roads to settlements'] = (len(self.roads) / numSettlements) if numSettlements > 0 else 1
        features['Ratio cities to settlements'] = (numCities/ numSettlements) if numSettlements > 0 else 1 if numCities > 0 else 0
        features['Squared distance to end'] = (10 - self.score)**2
        features['Num accesible resources'] = self.getAccessibleResources(expectedResources)
        return features    
      
    
    def pickMove(self, game):
        # TODO: Optimize this. Try to avoid using get_successor for cheap/uncomplicated moves
        possible_moves = game.getPossibleActions(self)
        # print "In pick move :", self.resources
        bestMoveScore, bestMove = float('-inf'), None
        for possibleMove in possible_moves:
            if not possibleMove: continue
            scoreForMove = 0
            tempMove = {}
            for action in possibleMove:
                piece, count = action
                mostValuableActions = [(action, location, self.evaluateMoveValue(game, (action, location))) for location in possibleMove[action]]
                mostValuableActions.sort(key = lambda a: a[2], reverse = True) # Sort by value
                totalValueOfAction = sum([mva[2] for mva in mostValuableActions[:count]])
                scoreForMove += totalValueOfAction
                tempMove[action] = [mva[1] for mva in mostValuableActions[:count]]
            if scoreForMove > bestMoveScore:
                bestMoveScore, bestMove = scoreForMove, tempMove
            # print(bestMoveScore)

        # Returns a dict of {(piece, count) : [most valuable 'count' locations] for each key (piece, count)}
        # print('best move = ' + str(bestMove))

        return bestMove

'''
My attempt to build an AI that updates its weights every turn. We will see if it works. Eval(s) represents predicted end
score of gamestate s.

    Q-Learning Basis:
        Prediction: Eval(s) (or 10 if you can win)
        Target: Eval(s') when you get to state s'
        Don't have access to game before first few turns, so weights won't update at the start
'''

class qAI(WeightedAI):

    def __init__(self,turn_num, name, color, weightsLog):
        AiPlayer.__init__(self, turn_num, name, color, weightsLog)
        self.weightsLog = weightsLog

        self.weights = defaultdict(float, weightsLog.readDict())
        if 'DELETE ME' in self.weights.keys():
            self.weights = defaultdict(float)
                    
        #Need to keep track of previous score and features to update them        
        self.prevScore = None
        self.prevFeatures = None
        self.eta = .00000005

    #Same as superclass feature extractor, but adding some more adversarial features
    def feature_extractor(self, game):
        expectedResources = self.expected_resources_per_roll() 
        features = expectedResources 
        features['Devcards played'] = len(self.devCardsPlayed.values())
        features.update(self.devCardsPlayed)
        features['Num roads'] = len(self.roads)
        features['Longest Road'] = self.longestRoadLength
        numCities, numSettlements = self.getNumSettlementsAndCities()
        features['Num cities'] = numCities
        features['Num settlements'] = numSettlements
        features['Num turns with more than 7 cards'] = self.numTimesOverSeven
        features['Resource spread'] = np.std([expectedResources[k] for k in expectedResources.keys()])
        features['Has longest road'] = 1 if self.holdsLongestRoad else 0
        features['Has largest army'] = 1 if self.hasLargestArmy else 0
        features['Num cards discarded'] = self.numCardsDiscarded
        features['Score'] = self.score
        features['Has Won'] = self.score == 10
        features['Ratio roads to settlements'] = (len(self.roads) / numSettlements) if numSettlements > 0 else 1
        features['Ratio cities to settlements'] = (numCities/ numSettlements) if numSettlements > 0 else 1 if numCities > 0 else 0
        features['Squared distance to end'] = (10 - self.score)**2
        features['Num accesible resources'] = self.getAccessibleResources(expectedResources)

        #Features for other players number of each piece and total score
        #TODO: Feature for longest road or expected resources per turn?
        if game:
            for player in game.players:
                if player.turn_num != self.turn_num:
                    features["Score " + str(player.turn_num)] = player.score
                    features["Player "+ str(player.turn_num) + " DevCards"] = len(player.devCards) + len(player.devCardsPlayed)
                    features["Player "+ str(player.turn_num) + " Roads"] = len(player.roads)
                    features["Player "+ str(player.turn_num) + " Settlements"] = sum([int(i.pieceType=='Settlement') for i in player.cities_and_settlements])
                    features["Player "+ str(player.turn_num) + " Cities"] = sum([int(i.pieceType=='City') for i in player.cities_and_settlements])

        return features    

    #Helper function to evaluate a gamestate
    def eval(self,game):
        features = self.feature_extractor(game)
        return util.dotProduct(features, self.weights)

    #Update the weights of your features after a given turn. Different from update_weights used in other AI's
    def updateWeights(self, game):
        # print game
        #Get current score
        cur_features = self.feature_extractor(game)
        target = util.dotProduct(cur_features, self.weights)
        pred = self.prevScore
        
        # print "fuck" , cur_features["Player "+ str(1) + " Settlements"]

        #If there are no previous features you can't update
        if self.prevFeatures: 

            #Update weights
            diff = pred - target
            for feature, val in self.prevFeatures.items():
                # print diff, val
                self.weights[feature] -= self.eta * diff * val
        
        self.prevFeatures = cur_features
        self.prevScore = target


    #Same as superclass, but it updates weights before picking the move and stores prediction at the end of the turn
    def pickMove(self, game):

        #Update weights
        self.updateWeights(game)

        #Pick a move as normal
        possible_moves = game.getPossibleActions(self)
        bestMoveScore, bestMove = -10000, None
        for possibleMove in possible_moves:
            if not possibleMove: continue
            scoreForMove = 0
            tempMove = {}
            for action in possibleMove:
                piece, count = action
                mostValuableActions = [(action, location, self.evaluateMoveValue(game, (action, location))) for location in possibleMove[action]]
                mostValuableActions.sort(key = lambda a: a[2], reverse = True) # Sort by value
                totalValueOfAction = sum([mva[2] for mva in mostValuableActions[:count]])
                scoreForMove += totalValueOfAction
                tempMove[action] = [mva[1] for mva in mostValuableActions[:count]]
            if scoreForMove > bestMoveScore:
                bestMoveScore, bestMove = scoreForMove, tempMove

        return bestMove

    #Does the end game update for each player
    def endGameUpdate(self, game, target, eta = .000003):
        # target = self.score
        pred = self.prevScore
        features = self.prevFeatures

        #Get current score
        # features = self.feature_extractor(game)
        # pred = util.dotProduct(features, self.weights)
    
        # print "pred: ", pred
        # print "features: ", features

        diff = pred - target
        print self.turn_num, " pred: ", pred, "target: ", target, "diff: ", diff
        for feature, val in features.items():
            # print feature, val,  diff
            self.weights[feature] -= eta * diff * val

        # print(self.weights)
        # raw_input("")
        if abs(pred) > 100: raw_input("FUCK")
        self.weightsLog.log_dict(self.weights)

        return diff
        





'''
This is a class I wrote when I was high that fucks around with an simple way ot use weights
to improve initial settlement and road locations. Basically it uses the probability of a tile
and the weight of that resource to predict end game score or whether or not you won. Weights are
written to and read from a file.


Notes on how to go forward:

    -TODO: feature extractor functions
        -I am thinking we do feature extraction differently for the pregame than the full game
        -We should implement pregame first because it will be easier and give us a better idea of 
            how to do it
        -How will we update weights? Should we update every turn or just at the end of the game?

    -Pregame:

        -Currently writes weights to a file at the end of the game and then reads them back in at the start
            -TODO: update so doing this works with a blank file and the file doesn't have to already have an entry
        -Need dedicated feature extractor
            -Would be nice if somehow worked for roads and settlements
                -Since feature names don't matter, we could just define features with 'Road' appended to the name and then 
                    only look at weights that begin with road
                -Also could define seperate extractors for road and settlement placement
                    -Issue is that we may need a TON of feature extractors for the main game if we do this

    -Potential Issues:
    
        -At first we will probably build an AI that considers its moves and the board and stuff, but later on we would want
         our AI to incorporate the states of other players. 
            -To do this, we need access to the game in general, or at the very least other player objects
            -Could require rethinking how we implemented the Player class so that it takes in the game 

'''

class BasicStrategy(AiPlayer):
    
    def __init__(self, turn_num, name, color, log):
        AiPlayer.__init__(self, turn_num, name, color, log)

        #These keep track of weights for each resource in the pregame setup
        self.weights_log = Log("../logs/win_test_log_" + str(self.turn_num) +".txt")
        self.resource_weights = self.load_weights()
        self.resource_weights['Desert'] = 0
        # print self.resource_weights
        self.eta = .01

        #Keep track of features chosen. Need a better way to do this eventually
        self.pre_game_features = defaultdict(int)
        self.pre_game_score = 0

    def load_weights(self):
        return defaultdict(float)
        weights = self.weights_log.readDict()
        if weights:
            return defaultdict(int, weights)
        else:
            return defaultdict(float)

    #Randomly picks a road. For now only the Settlement location will be optimized.
    #TODO: Add more features for evaluating a good road
    def pick_road_position(self, possible_locations):
        '''
        Current heuristic:
            -Takes a look at the settlements that could be placed if you added another 
             to the end of it
        '''
        best_road = None
        best_score = float('-inf')

        for start, end in possible_locations:
            cur_score = 0
            neighbors = end.neighbours
            for neighbor in neighbors:
                #Make sure nieghbor is empty
                if not neighbor.isOccupied:
                    cur_score += self.getLocScore(neighbor)[0]
            if cur_score >= best_score:
                best_score = cur_score
                best_road = (start, end)

        return best_road

    def pick_settlement_position(self, possible_locations):
        max_location = None
        max_score = float("-inf")
        best_types = None

        for loc in possible_locations:
            score, tileTypes = self.getLocScore(loc)
            if score > max_score:
                max_location = loc
                max_score = score
                best_types = tileTypes

        #Add selected features to features
        for tileType, count in best_types.items():
            self.pre_game_features[tileType] += count

        self.pre_game_score += max_score

        return max_location

    #Gets the value of all three tiles boardering a location and sums them
    def getLocScore(self, node):
        tileTypes = defaultdict(int)
        score = 0
        for tile in node.touchingTiles:
            # tile_weight = 1
            tile_weight = self.resource_weights[tile.resource]
            tile_prob = util.rollProb(tile.value)
            score += tile_prob * tile_weight
            tileTypes[tile.resource] += 1
        
        return score, tileTypes
