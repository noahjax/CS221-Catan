#Need a ton of imports
from pieces import *
import random
from collections import deque, defaultdict
from devcards import *
from player import *
from enum import Enum

class Game(object):
    """
    Represents a game of Catan. Each game has players and a board. 

    Currently working on making getter functions so you can get easily get available actions

    (Add more stuff)
    """

    #Need to handle cases where board or players aren't initialized at some point
    # def __init__(self, players=None, board=None):
    def __init__(self, players, board, robber_tile):

        self.currMaxRoad = 0
        self.currMaxKnights = 0
        self.players = players
        self.board = board
        self.turn_num = 0       #Starts at 0 so it can easily access player list
        self.devCards = self.initialize_dev_cards()
        self.gameStart = False
        self.robber_location = robber_tile

    #Function to handle pregame placing of pieces
    # def run_pregame():

    #Rolls dice, returns value
    #Might just make a util.py for this type of stuff
    def rollDice(self):
        die1 = random.randint(1,6)
        die2 = random.randint(1,6)
        return die1 + die2

    #Return possible locations where a piece can be placed. Board and cur_player can be accessed through self
    # def getPossibleLocations(self, piece):

    #Handle buying a piece. cur_player can be accessed through self, and each player should store thier own available resource cards.
    # def buyPiece(self, piece):

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

    #Check to see if you can buy a devCard
    def canBuyDevCard(self, player_num):
        #Make sure there are devCards left 
        if not self.devCards:
            print("No dev cards left sorry")    ###Probably want to handle this better
            return False
        #Get current player
        cur_player = self.players[player_num]
        #Check if you have the resources to buy a devCard
        if cur_player.resources['Ore'] < 1 or cur_player.resources['Wool'] < 1 or cur_player.resources['Wheat'] < 1:
            print("You don't have enough resources to buy a devCard")
            return False
        
        return True

    #Handle buying a devCard. Update player to have this devCard, remove resources from player    
    def buyDevCard(self, player_num):
        if self.canBuyDevCard(player_num):
            cur_player = self.players[player_num]
            #Update player resources
            cur_player.resources['Ore'] -= 1
            cur_player.resources['Wool'] -= 1
            cur_player.resources['Wheat'] -= 1

            #Get devCard and give to player
            dev_card = self.devCards.pop()

            card_to_add = buyDevCard(cur_player, dev_card, self.players)

            if dev_card in self.devCards.keys():
                self.devCards[dev_card].append(card_to_add)
            else:
                self.devCards[dev_card] = [card_to_add]

    #Handle moving the robber
    def set_robber_location(self, location):
        currPosition = self.robber_location
        currPosition.has_robber = False
        self.robber_location = location
        location.has_robber = True



    
    ################################################################
    #######################   Pieces   #############################
    ################################################################
    '''
    Determine how many of each different types of piece you can buy. 
    This is entirely based off of resources and not whether you can place them. 
    '''

    def canBuyRoad(self,resources):
        return resources['Brick'] >= 1 and resources['Wood'] >= 1

    def canBuyCity(self, resources):
        return resources['Ore'] >= 3 and resources['Wheat'] >= 2

    def canBuySettlement(self, resources):
        return resources['Brick'] >= 1 and resources['Wood'] >= 1 \
            and resources['Wool'] >= 1 and resources['Wheat'] >= 1

    def canBuyDevCard(self, resources):
        if not self.devCards: return False
        return resources['Ore'] >= 1 and resources['Wheat'] >= 1 \
            and resources['Wool'] >= 1

    def updateRoadResources(self, resources, add=False):
        i = -1 if add else 1
        resources['Brick'] -= 1 * i
        resources['Wood'] -= 1 * i

    def updateCityResources(self, resources, add=False):
        i = -1 if add else 1
        resources['Ore'] -= 3 * i
        resources['Wheat'] -= 2 * i

    def updateSettlementResources(self, resources, add=False):
        i = -1 if add else 1
        resources['Brick'] -= 1 * i
        resources['Wood'] -= 1 * i
        resources['Wool'] -= 1 * i
        resources['Wheat'] -= 1 * i
    
    def updateDevCardResources(self, resources, add=False):
        i = -1 if add else 1
        resources['Ore'] -= 1 * i
        resources['Wool'] -= 1 * i
        resources['Wheat'] -= 1 * i

    def findResourceCombos(self, resources, pieces, ans):

        #Copy pieces so we don't modify it as we recur
        cur_pieces = pieces.copy()
        
        #Check if you can buy a road, if you can, recurse without road resources
        if self.canBuyRoad(resources):
            cur_pieces['Road'] += 1
            self.updateRoadResources(resources)
            self.findResourceCombos(resources, cur_pieces, ans)
            self.updateRoadResources(resources, add=True)
            cur_pieces['Road'] -= 1
        
        #Check if you can buy a settlement, if you can, recurse 
        if self.canBuySettlement(resources):
            cur_pieces['Settlement'] += 1
            self.updateSettlementResources(resources)
            self.findResourceCombos(resources, cur_pieces, ans)
            self.updateSettlementResources(resources, add=True)
            cur_pieces['Settlement'] -= 1
        
        #Check if you can buy a city, if you can, recurse
        if self.canBuyCity(resources):
            cur_pieces['City'] += 1
            self.updateSettlementResources(resources)
            self.findResourceCombos(resources, cur_pieces, ans)
            self.updateSettlementResources(resources, add=True)
            cur_pieces['City'] -= 1
            
        #Check if you can buy a DevCard, if you can, recurse     
        if self.canBuyDevCard(resources):
            cur_pieces['DevCard'] += 1
            self.updateDevCardResources(resources)
            self.findResourceCombos(resources, cur_pieces, ans)
            self.updateDevCardResources(resources, add=True)
            cur_pieces['DevCard'] -= 1
        
        #Remove 0 values and add to answer
        cur_pieces = defaultdict(int, dict((k,v) for k,v in cur_pieces.items() if v))
        if cur_pieces not in ans:
            ans.append(cur_pieces)

    #Returns list of dictionaries [{Road:1, City:1},{...}]
    def piecesPurchasable(self, player):
        player_resources = player.resources
        ans = []
        pieces = defaultdict(int)
        self.findResourceCombos(player_resources, pieces, ans)
        return ans

    
    def testPiecesPurchasable(self):
        player = Player(1, 'Noah', 'Red')
        player.resources['Wood'] = 1
        player.resources['Brick'] = 1
        player.resources['Ore'] = 1
        # player.resources['Wheat'] = 1
        # player.resources['Wool'] = 1


        x = self.piecesPurchasable(player)
        print(len(x))
        

    


    # #Check if player can buy a particular piece
    # def canBuyPiece(self, player_num, piecetype):
    #     resources_needed = defaultdict(str)
    #     #Put values in resources needed based on the piece type
    #     if piecetype == "Settlement":
    #         resources_needed['Brick'] = 1
    #         resources_needed['Wood'] = 1
    #         resources_needed['Wool'] = 1
    #         resources_needed['Wheat'] = 1
    #     elif piecetype == "City":
    #         resources_needed['Ore'] = 3
    #         resources_needed['Wheat'] = 2
    #     elif piecetype == "Road":
    #         resources_needed['Brick'] = 1
    #         resources_needed['Wood'] = 1
    
    #     #Get resources the player has
    #     cur_resources = self.players[player_num].resources

    #     #Check if player has required resources
    #     for key in resources_needed:
    #         if cur_resources[key] < resources_needed[key]:
    #             return False
        
    #     return True

    # #Buy piece
    # def buyPiece(self, player_num, piecetype):
    #     if not self.canBuyPiece(player_num, piecetype): 
    #         print("You don't have enough resources to buy this piece")
    #         return
    #     resources_needed = defaultdict(str)
    #     #Put values in resources needed based on the piece type
    #     if piecetype == "Settlement":
    #         resources_needed['Brick'] = 1
    #         resources_needed['Wood'] = 1
    #         resources_needed['Wool'] = 1
    #         resources_needed['Wheat'] = 1
    #     elif piecetype == "City":
    #         resources_needed['Ore'] = 3
    #         resources_needed['Wheat'] = 2
    #     elif piecetype == "Road":
    #         resources_needed['Brick'] = 1
    #         resources_needed['Wood'] = 1
    
    #     #Get resources the player has
    #     cur_resources = self.players[player_num].resources

    #     #Update players resources
    #     for key in resources_needed:
    #         cur_resources[key] -= resources_needed[key]

    #     #Give piece to player
    #     self.players[player_num].pieces[piecetype] += 1

    ###Need better understanding of board architecture to implement these
    # def canPlacePiece()
    # def getAvailableLocations()        
    # def placePiece():

    ################################################################
    ######################   Get Actions   ########################
    ################################################################
    '''
    Returns a list of all possible actions for a given game.
    Pretty much all of the information needed should be stored in the game class.
    Makes use of helpers for different types of actions.
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
        -trade (to be implemented later)


        Return format:
        [(piece, location)]
    '''

    '''
    Current thinking: 
        -Create functions that give a list of possible [(piece, location)] assignments for a given gamestate
        -Functions also return number of these assignments you can pick
    '''

    #Get valid road locations
    def getRoadLocations(self, player):
        possible_locations = []
        
        #Loop over all edges, check if edge is empty and one of the neighbors is a valid city/road
            #Add valid edges to the list
        
        return possible_locations
    
    #Get valid bu
    def getSettlementLocations(self, player):
        possible_locations = []
        
        #Loop over all nodes, check if is empty and neighborhoods 
        return possible_locations

    def getCityLocations(self, player):
        possible_locations = []

        #Loop over all nodes, check if node is settlement




    # #Helper that gets the possible pieces that you can buy and place
    # def possiblePieces(self):
    #     return self.possibleRoads() + self.possibleCities() + self.pos


    # def getPossibleActions(self):
    #     cur_player = self.players[self.turn_num]

    #     possibleActions = []
    #     possibleActions += self.possiblePieces()



#############################################################################
#####################   Handle Distributing Resources    ####################
#############################################################################
'''This code is very incomplete'''

    #Can access board through self, so really just need roll
    def distributeResources(self, roll):

        #Check if roll is 7
        if roll == 7:
            print("Move robber. No resources to distribute")
            return

        #Loop over all tiles in game
        for i in range(19):
            tile = self.board.board[i]
            #Get nodes if this tile gives out resources
            if tile == roll:
                nodes = self.board.getPieceCoords(i)
                for piece in nodes:
                    #Check if node has a piece that gives resources
                    if type(piece) is Settlement:
                        piece.player.resources[tile] += 1
                        piece.player.numResources[tile] += 1
                    elif type(piece) is City:
                        piece.player.resources[tile] += 2
                        piece.player.numResources[tile] += 2
                        


#############################################################################
###################################   End    ################################
#############################################################################


#Random test code
game = Game(None,None)
game.testPiecesPurchasable()
