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
    def __init__(self, players, board):

        self.currMaxRoad = 0
        self.currMaxKnights = 0
        self.players = players
        self.board = board
        self.turn_num = 0       #Starts at 0 so it can easily access player list
        self.devCards = self.initialize_dev_cards()
        self.gameStart = False

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
        if cur_player.resources['Ore'] < 1 or cur_player.resources['Wool'] < 1 or cur_player.resources['Grain'] < 1:
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
            cur_player.resources['Grain'] -= 1

            #Get devCard and give to player
            devCard = self.devCards.pop()

            card_to_add = createDevCard(cur_player, devCard, self.players)

            if devCard in self.devCards.keys():
                self.devCards[devCard].append(card_to_add)
            else:
                self.devCards[devCard] = [card_to_add]


    
    ################################################################
    #######################   Pieces   #############################
    ################################################################

    ###AT some point I think it makes sense to store piece costs as a part of the game so you only
    ###calculate resources needed once at the start

    #Check if player can buy a particular piece
    def canBuyPiece(self, player_num, piecetype):
        resources_needed = defaultdict(str)
        #Put values in resources needed based on the piece type
        if piecetype == "Settlement":
            resources_needed['Brick'] = 1
            resources_needed['Wood'] = 1
            resources_needed['Wool'] = 1
            resources_needed['Grain'] = 1
        elif piecetype == "City":
            resources_needed['Ore'] = 3
            resources_needed['Grain'] = 2
        elif piecetype == "Road":
            resources_needed['Brick'] = 1
            resources_needed['Wood'] = 1
    
        #Get resources the player has
        cur_resources = self.players[player_num].resources

        #Check if player has required resources
        for key in resources_needed:
            if cur_resources[key] < resources_needed[key]:
                return False
        
        return True

    #Buy piece
    def buyPiece(self, player_num, piecetype):
        if not self.canBuyPiece(player_num, piecetype): 
            print("You don't have enough resources to buy this piece")
            return
        resources_needed = defaultdict(str)
        #Put values in resources needed based on the piece type
        if piecetype == "Settlement":
            resources_needed['Brick'] = 1
            resources_needed['Wood'] = 1
            resources_needed['Wool'] = 1
            resources_needed['Grain'] = 1
        elif piecetype == "City":
            resources_needed['Ore'] = 3
            resources_needed['Grain'] = 2
        elif piecetype == "Road":
            resources_needed['Brick'] = 1
            resources_needed['Wood'] = 1
    
        #Get resources the player has
        cur_resources = self.players[player_num].resources

        #Update players resources
        for key in resources_needed:
            cur_resources[key] -= resources_needed[key]

        #Give piece to player
        self.players[player_num].pieces[piecetype] += 1

    ###Need better understanding of board architecture to implement these
    # def canPlacePiece()
    # def getAvailableLocations()        
    # def placePiece():


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
test = game.initialize_dev_cards()
print(len(test))
test.pop()
print(len(test))
