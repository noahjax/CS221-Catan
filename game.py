#Need a ton of imports
import pieces
import random
from collections import deque

class Game(object):
    """
    Represents a game of Catan. Each game has players and a board. 

    (Add more stuff)
    """

    #Need to handle cases where board or players aren't initialized at some point
    # def __init__(self, players=None, board=None):
    def __init__(self, players, board):
        
        self.players = players
        self.board = board
        self.turn_num = 0       #Starts at 0 so it can easily access player list
        self.devCards = self.initialize_dev_cards()
        self.gameStart = False

    #Function to create and shuffle deck of dev cards
    def initialize_dev_cards(self):
        devCards = ['Knight'] * 14
        devCards += ['Victoy Point'] * 5
        devCards += ['Road Building'] * 2
        devCards += ['Monopoly'] * 2
        devCards += ['Year of Plenty'] * 2
        random.shuffle(devCards)
        return deque(devCards)

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

    #Handle buting a devCard. Update player to have this devCard, remove resources from player    
    def buyDevCard(self):
        #Get current player
        cur_player = self.players[self.turn_num]
        
        #Check if player has resources to buy devCard
        if cur_player.resources['Ore'] >= 1 and cur_player.resources['Wool'] >= 1 and cur_player.resources['Grain'] >= 1:
            #Update player resources
            cur_player.resources['Ore'] -= 1
            cur_player.resources['Wool'] -= 1
            cur_player.resources['Grain'] -= 1

            #Make sure there are devCards left
            if not self.devCards:
                print("No dev cards left sorry")    ###Probably want to handle this better
                return
            #Get devCard and give to player
            devCard = self.devCards.pop()
            cur_player.devCards[devCard] += 1

#Random test code
game = Game(None,None)
test = game.initialize_dev_cards()
print(len(test))
test.pop()
print(len(test))