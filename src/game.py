from pieces import *
import random
from collections import deque, defaultdict
from devcards import *
from player import *
# from enum import Enum
from log import *
from util import *

class Game(object):
    """
    Represents a game of Catan. Each game has players and a board. 

    Currently working on making getter functions so you can get easily get available actions

    (Add more stuff)
    """

    # Need to handle cases where board or players aren't initialized at some point
    # def __init__(self, players=None, board=None):
    def __init__(self, players, board, robber_tile):

        self.currMaxRoad = 0
        self.currMaxKnights = 0
        self.players = players
        self.currMaxScore = 0
        self.longestRoad = 0
        self.currPlayerWithLongestRoad = None
        self.playerWithLargestArmy = None
        self.board = board
        self.turn_num = 0 #TODO: Remove fields that aren't used, like turn_num here
        self.devCards = self.initialize_dev_cards()
        self.gameStart = False
        self.robber_location = robber_tile
        self.roads = []

        '''Set up dicts for the resources in typical game purchases'''
        self.settlement_cost = defaultdict(int)
        self.city_cost = defaultdict(int)
        self.road_cost = defaultdict(int)
        self.devCard_cost = defaultdict(int)
        self.initialize_resource_dicts()

        # catan_log.log("Game class intitialized")

    ################################################################
    ##################   Initialize Cost Dicts   ###################
    ################################################################
    def initialize_resource_dicts(self):
        #Settlements
        self.settlement_cost['Brick'] = 1
        self.settlement_cost['Wool'] = 1
        self.settlement_cost['Grain'] = 1
        self.settlement_cost['Wool'] = 1

        #Cities
        self.city_cost['Ore'] = 3
        self.city_cost['Grain'] = 2

        #Roads
        self.road_cost['Brick'] = 1
        self.road_cost['Wood'] = 1

        #DevCards
        self.devCard_cost['Ore'] = 1
        self.devCard_cost['Wool'] = 1
        self.devCard_cost['Grain'] = 1

    ################################################################
    #######################   Dev Cards   ##########################
    ################################################################
    
    #Function to create and shuffle deck of dev cards
    def initialize_dev_cards(self):
        devCards = ['Knight'] * 14
        devCards += ['Victory Point'] * 5
        devCards += ['Road Building'] * 2
        devCards += ['Monopoly'] * 2
        devCards += ['Year of Plenty'] * 2
        random.shuffle(devCards)
        return deque(devCards)

    # #Check to see if you can buy a devCard
    # def canBuyDevCard(self, player):
    #     # Make sure there are devCards left
    #     if not self.devCards:
    #         return False

    #     # Check if player has the resources to buy a devCard
    #     if player.resources['Ore'] < 1 or player.resources['Wool'] < 1 or player.resources['Grain'] < 1:
    #         return False
        
    #     return True

    # Handle buying a devCard. Update player to have this devCard, remove resources from player
    def buyDevCard(self, cur_player):
        can_buy = self.canBuyDevCard(cur_player)
        if can_buy:
            # Update player resources
            self.updateDevCardResources(cur_player)

            # Get devCard and give to player
            dev_card = self.devCards.pop()
            # print("You got a " + dev_card.type)

            card_to_add = buyDevCard(cur_player, dev_card, self.players)
            cur_player.prevDevCards.append(card_to_add)

            # Checks if you already have devCard, may be redundant with defaultdict()
            if dev_card in cur_player.newDevCards.keys():
                cur_player.newDevCards[dev_card].append(card_to_add)
            else:
                cur_player.newDevCards[dev_card] = [card_to_add]

            # printDevCards(cur_player)

            # Log purchase
            name = cur_player.name
            # catan_log.log(name + " bought " + dev_card)

        else:
            if not self.devCards:
                print("Sorry there are no devcards left to buy")
            else:
                print("You don't have enough resources to buy a devCard")

            # catan_log.log("Couldn't buy devCard")
    
    #Return a devCard
    def returnDevCard(self, cur_player):
        self.updateDevCardResources(cur_player, True)
        cards = cur_player.devCards   
        return_card = cur_player.prevDevCards[-1]   
        del cards[return_card][-1]
        del cur_player.prevDevCards[-1]

    #TODO: Maybe we should move this to game so that we can model successor states actually having playable 
    #Devcards
    def updateDevCards(self, currPlayer):
        for type_card in currPlayer.newDevCards.keys():
            for num_cards in range(len(currPlayer.newDevCards[type_card])):
                card_to_add = currPlayer.newDevCards[type_card].pop(0)
                if type_card in currPlayer.devCards.keys():
                    currPlayer.devCards[type_card].append(card_to_add)
                else:
                    currPlayer.devCards[type_card] = [card_to_add]    

    #Handle moving the robber
    def set_robber_location(self, location, display):
        currPosition = self.board.getTileForNode(self.robber_location[0], self.robber_location[1])
        currPosition.has_robber = False
        self.robber_location = location
        newRobberTile = self.board.getTileForNode(self.robber_location[0], self.robber_location[1])
        # location.has_robber = True
        newRobberTile.has_robber = True

        display.placeRobber(location)
        # catan_log.log("Robber location moved to " + str(location))
      

    ################################################################
    ######################   Get Actions   #########################
    ################################################################
    '''
    Possible action types:
        -buyPiece: 
            -Road
            -Settlement
            -City
        -buyDevCard
        -playDevCard
            -Knight
            -Victory Point
            -etc
        -end turn
        -trade (to be implemented later)

    Implementation: 
        -function piecesPurchasable(self,player) returns all possible things you can purchase
        -function getLocations returns possible placements for each piece
    '''
    
    
    # First group of helpers to determine if you can buy an item
    def canBuyRoad(self, player):
        return player.resources['Brick'] >= 1 and player.resources['Wood'] >= 1

    def canBuyCity(self, player):
        return player.resources['Ore'] >= 3 and player.resources['Grain'] >= 2

    def canBuySettlement(self, player):
        return player.resources['Brick'] >= 1 and player.resources['Wood'] >= 1 \
            and player.resources['Wool'] >= 1 and player.resources['Grain'] >= 1

    def canBuyDevCard(self, player):
        if len(self.devCards) == 0: return False
        return player.resources['Ore'] >= 1 and player.resources['Grain'] >= 1 \
            and player.resources['Wool'] >= 1

    # Second group of helpers to update resources if you buy an item
    def updateRoadResources(self, player, add=False):
        i = -1 if add else 1
        player.resources['Brick'] -= 1 * i
        player.resources['Wood'] -= 1 * i
        player.numResources -= 2 * i

    def updateCityResources(self, player, add=False):
        i = -1 if add else 1
        player.resources['Ore'] -= 3 * i
        player.resources['Grain'] -= 2 * i
        player.numResources -= 5 * i

    def updateSettlementResources(self, player, add=False):
        i = -1 if add else 1
        player.resources['Brick'] -= 1 * i
        player.resources['Wood'] -= 1 * i
        player.resources['Wool'] -= 1 * i
        player.resources['Grain'] -= 1 * i
        player.numResources -= 4 * i

    def updateDevCardResources(self, player, add=False):
        i = -1 if add else 1
        player.resources['Ore'] -= 1 * i
        player.resources['Wool'] -= 1 * i
        player.resources['Grain'] -= 1 * i
        player.numResources -= 3 * i

    #Handles recursion to explore items you can buy
    def findResourceCombos(self, pieces, ans, curr_player, depth=3):

        if not areValidResources(curr_player.resources):
            print curr_player.resources
            print "depth: ", depth
            raw_input("Resource combos failure")

        #Only recurse 5 levels to limit running time
        if depth <= 0:
        #     for r,c in curr_player.resources.items():
        #         if c <0 : print "fuck you", depth
            return

        #Copy pieces so we don't modify it as we recurse
        cur_pieces = copy.deepcopy(pieces)

        #Check if you can buy a road, if you can, recurse without road resources
        if self.canBuyRoad(curr_player):
            cur_pieces['Road'] += 1
            self.updateRoadResources(curr_player)
            if not areValidResources(curr_player.resources):
                print "Road invalid resources"
                raw_input("")
            # print "road before s ", curr_player.turn_num, curr_player.resources
            # subtractResources(curr_player, self.road_cost)
            # print "road after s ", curr_player.turn_num, curr_player.resources
            self.findResourceCombos(cur_pieces, ans, curr_player, depth-1)
            # print "road before a ", curr_player.turn_num, curr_player.resources
            # addResources(curr_player, self.road_cost)
            # print "road after a ", curr_player.turn_num, curr_player.resources
            self.updateRoadResources(curr_player, add=True)
            cur_pieces['Road'] -= 1

        #Check if you can buy a settlement, if you can, recurse
        if self.canBuySettlement(curr_player):
            cur_pieces['Settlement'] += 1
            self.updateSettlementResources(curr_player)
            if not areValidResources(curr_player.resources):
                print "Settlement invalid resources"
                raw_input("")
            # print "settlement before s", curr_player.turn_num, curr_player.resources
            # subtractResources(curr_player, self.settlement_cost)
            # print "settlement after s", curr_player.turn_num, curr_player.resources
            self.findResourceCombos(cur_pieces, ans, curr_player, depth-1)
            # print "settlement before a", curr_player.turn_num, curr_player.resources
            # addResources(curr_player, self.settlement_cost)
            # print "settlement after a", curr_player.turn_num, curr_player.resources
            self.updateSettlementResources(curr_player, add=True)
            cur_pieces['Settlement'] -= 1

        #Check if you can buy a city, if you can, recurse
        if self.canBuyCity(curr_player):
            cur_pieces['City'] += 1
            self.updateCityResources(curr_player)
            
            if not areValidResources(curr_player.resources):
                print "City invalid resources"
                print curr_player.resources
                raw_input("")
            
            self.findResourceCombos(cur_pieces, ans, curr_player, depth-1)
            self.updateCityResources(curr_player, add=True)
            cur_pieces['City'] -= 1

        #Check if you can buy a DevCard, if you can, recurse
        if self.canBuyDevCard(curr_player):
            cur_pieces['buyDevCard'] += 1
            self.updateDevCardResources(curr_player)
            
            if not areValidResources(curr_player.resources):
                print "Devcard invalid resources"
                print curr_player.resources
                raw_input("")
            
            self.findResourceCombos(cur_pieces, ans, curr_player, depth-1)
            self.updateDevCardResources(curr_player, add=True)
            cur_pieces['buyDevCard'] -= 1

        # Check if you can exchange any of your resources
        for resource, count in curr_player.resources.items():
            if count >= curr_player.exchangeRates[resource]:
                curr_player.resources[resource] -= curr_player.exchangeRates[resource]
                #Add a new resource
                for addResource in curr_player.resources:
                    if addResource != resource:
                        curr_player.resources[addResource] += 1
                        # Store exchanges in form (trade in, recieve): exchange rate
                        cur_pieces[(resource, addResource)] = curr_player.exchangeRates[resource]
                        self.findResourceCombos(cur_pieces, ans, curr_player, depth-2)
                        del cur_pieces[(resource, addResource)]
                        curr_player.resources[addResource] -= 1

                curr_player.resources[resource] += curr_player.exchangeRates[resource]

        #Remove 0 values and add to answer
        cur_pieces = defaultdict(int, dict((k, v) for k, v in cur_pieces.items() if v))
        if cur_pieces not in ans:
            ans.append(cur_pieces)
        # print "ans: ", ans

    #Returns list of dictionaries [{Road:1, City:1},{...}] representing possible pieces
    #you can buy given a player with some resources
    def piecesPurchasable(self, player):
        # player_resources = player.resources
        # for r in player_resources:
        #     assert r >= 0

        #Look at trades the person could make to get different resources
        # possible_resources = self.resource_exchanges(player_resources, exchange_rates)
        
        ans = []
        pieces = defaultdict(int)
        self.findResourceCombos(pieces, ans, player)
        # print "possible purchases: ", ans
        # for move, newResources in possible_resources:
        #     newAns = []
        #     newPieces = {}
        #     self.findResourceCombos(newResources, newPieces, newAns, 4)
        #     newAns 

        # catan_log.log("Found pieces purchasable for " + player.name)

        return ans

    '''
    Returns dicts of resources you could have if you traded in your resources at the given exchange rate
        -return format is a tuple [((traded_resource, count), [{resource: count, resource:count}, {res..}]), ...]
    '''
    # def resource_exchanges(self, resources, exchange_rates):
    #     q = deque(resources)
    #     seen = [resources]
    #     ans = []

    #     #Number of loops determines recursive depth...shouldn't need to be high
    #     for _ in range(3):
    #         #Check if there are any options left to consider
    #         if not q: break
    #         #Get resources and make sure we haven't explored them before
    #         cur_resources = q.pop()
    #         if resources in seen: continue
            
    #         #Find resources we could exchange
    #         for resource, count in cur_resources.items():
    #             if count >= exchange_rates[resource]:
    #                 left = (resource, exchange_rates[resource])
    #                 right = []
    #                 #Explore possible new resources to give yourself
    #                 for new_resource, new_count in cur_resources:
    #                     #Don't trade in for the resource you just had
    #                     if new_resource != resource:
    #                         appendRes = cur_resources.copy()
    #                         appendRes[new_resource] += 1
    #                         appendRes[resource] -= exchange_rates[resource]
    #                         #Append to 
    #                         right.append(appendRes)
    #                         if appendRes not in q:
    #                             q.appendleft(appendRes)

    #                 ans.append((left, right))

    #Simple test
    def testPiecesPurchasable(self):
        player = Player(1, 'Noah', 'Red')
        player.resources['Wood'] = 1
        player.resources['Brick'] = 1
        player.resources['Ore'] = 1
        # player.resources['Grain'] = 1
        # player.resources['Wool'] = 1

        x = self.piecesPurchasable(player)
        print(len(x))
        
    ################################################################
    ######################   Get Actions   ########################
    ################################################################
    '''
    Returns valid locations for settlements, roads, and cities, as well as 
    a full list of the possible actions that an AI could take.
    Possible action types:
        -buyPiece: (placing a piece is incorporated as part of buying a piece)
            -Road
            -Settlement
            -City
        -buyDevCard
        -playDevCard
            -Knight
            -Victory Point
            -etc
        -end turn
        -Exchange resources
            -Not quite trading because set exchange rates
        -trade (to be implemented later)

        Return format:
        List dicts of [{(piece, count): [loc1, loc2]},{(piece,location): [loc1]}, ...]
            -dict entries can be in form:
                -(piece, count): [locs,...]
                # Liable to change
                -(resource, amount) : newResource (amount can be assumed to be 1)

        TODO: DevCard related actions
    '''

    #Returns a list lists of [{(piece, count): [loc1, loc2]},{(piece,location): [loc1]}, ...]
    #that represent buying and placing pieces. 
    '''Note: Does not handle playing DevCards. This logic is handled in player'''
    def getPossibleActions(self, player):
        #Get possible purchases
        possiblePurchases = self.piecesPurchasable(player)

        actions = [None]
        #Loop over each purchase and define the locations for each piece in the purchase
        for purchase in possiblePurchases:
            #Dict to store {(piece,count) : [locations]} pairs
            cur_action = {}
            locations = []
            #Get locations for each piece

            for piece, count in purchase.items():
                if piece == 'City':
                    locations = self.getCityLocations(player)
                elif piece == 'Road':
                    locations = self.getRoadLocations(player)
                elif piece == 'Settlement':
                    locations = self.getSettlementLocations(player)

                #Add to dict if there are enough valid locations
                if len(locations) < count and piece != buyDevCard:
                    continue
                cur_action[(piece, count)] = locations
            #Add this dict to the list of possible actions
            if cur_action:
                actions.append(cur_action)

        # catan_log.log("Found possible actions for " + player.name)

        return actions
    
    # Get valid road locations
    def getRoadLocations(self, player):
        possible_locations = []

        #Check the ends of existing roads as a place to put new roads
        for road in player.roads:
            first_node = road[0]
            second_node = road[1]
            for neighbour in second_node.neighbours:
                if not (second_node, neighbour) in self.roads and not (neighbour, second_node) in self.roads \
                    and self.isValidRoadNode(neighbour, player):
                    possible_locations.append((second_node, neighbour))

            for neighbour in first_node.neighbours:
                if not (first_node, neighbour) in self.roads and not (neighbour, first_node) in self.roads \
                    and self.isValidRoadNode(neighbour, player):
                    possible_locations.append((first_node, neighbour))

        for node in player.occupyingNodes:
            for neighbour in node.neighbours:
                if not (node, neighbour) in self.roads and not (neighbour, node) in self.roads:
                    possible_locations.append((node, neighbour))

        return possible_locations
    
    def isValidRoadNode(self, node, player):
        empty = not node.isOccupied
        if empty: return True
        mine = node.occupyingPiece.player.turn_num == player.turn_num
        return mine


    '''Missing test for settlement being at end of road'''
    #Helper to test if node is valid for a settlment. 
    def isValidSettlement(self, node, player, firstTurn):
        # If node is occupied we can't place anything there
        if node.isOccupied:
            return False

        # If neighbour is occupied we can't place anything there
        for neighbor in node.neighbours:
            if neighbor.isOccupied:
                return False

        # Check if the node is currently on a players road
        if not firstTurn:
            for (node_one, node_two) in player.roads:
                if node_one == node or node_two == node:
                    return True
            return False

        return True

        # If we get here we can not use the given node
        # return False

    #Get all possible locations to place a settlement
    def getSettlementLocations(self, player, firstTurn=False):
        possible_locations = []
        
        #Loop over all nodes, check if is empty and neighbors are appropriate
        for li in self.board.nodes.values():
            for node in li:
                if self.isValidSettlement(node, player, firstTurn):
                    possible_locations.append(node)

        return possible_locations

    def getCityLocations(self, player):
        possible_locations = []

        # Loop over all nodes, check if there is already a Settlement there with the right owner
        for node in player.occupyingNodes:
            # print('n = ' + str(node.occupyingPiece))
            if isinstance(node.occupyingPiece, Settlement):
                possible_locations.append(node)

        return possible_locations

   


#############################################################################
#####################   Handle Distributing Resources    ####################
#############################################################################
    """
    Function to distribute resources after every roll
    """
    # Can access board through self, so really just need roll
    def distributeResources(self, roll, display, curr_player):
        for player in self.players:
            if player.numResources > 7:
                player.numTimesOverSeven += 1

        if roll == 7:
            # return  #Don't want to do this for now
            curr_player.moveRobber(self, display)
            for player in self.players:
                if player.numResources > 7:
                    player.over_seven()

        # Loop over nodes and see if they are touching a tile with the rolled value
        for row in self.board.nodes.values():
            for node in row:
                if node.isOccupied:
                    # Look at all tiles touching node
                    for tile in node.touchingTiles:
                        # If tile value was rolled and its not blocked, give out resources
                        if tile.value == roll and not tile.hasRobber and tile.resource != 'Desert':
                            resourceNum = 2 if node.occupyingPiece == City else 1
                            node.occupyingPiece.player.resources[tile.resource] += resourceNum
                            node.occupyingPiece.player.numResources += resourceNum

                    
        # catan_log.log("Distributed resources to players")
                        

#############################################################################
###################################   End    ################################
#############################################################################


#Random test code
# game = Game(None,None,None)
