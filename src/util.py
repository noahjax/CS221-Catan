from devcards import *
from random import *
from player import *

# Prompt the user to identify an input
def getResourceInput():
    while True:
        to_get = raw_input("Please type (o, g, wl, b, wd) to choose a resource: ")
        if to_get == 'o':
            return 'Ore'
        elif to_get == 'g':
            return 'Grain'
        elif to_get == 'wl':
            return 'Wool'
        elif to_get == 'b':
            return 'Brick'
        elif to_get == 'wd':
            return 'Wood'
        else:
            print("That was not a valid resource try again")

def get_devcard_prompt():
    while True:
        type = raw_input("Type (k, v, r, m, yp) to choose what you want to play, or hit enter to return: ")
        if type == 'k':
            return 'Knight'
        elif type == 'v':
            return 'Victory Point'
        elif type == 'r':
            return 'Road Building'
        elif type == 'm':
            return 'Monopoly'
        elif type == 'yp':
            return 'Year of Plenty'
        elif type == '':
            return ""
        else:
            print("Sorry this type is not specified")


# Function that defines die roll for the game
def rollDice():
    die1 = randint(1,6)
    die2 = randint(1,6)
    return die1 + die2

# Print the players stats
def print_player_stats(curr_player):
    print ("color: " + curr_player.color + " resources: " + str(curr_player.resources) + " score: " + str(curr_player.score))

# Print a players resources
def printResources(currPlayer):
    print('You have the following resources: ')
    for resource in currPlayer.resources:
        print(resource + ": " + str(currPlayer.resources[resource]))

# Print a players dev cards
def printDevCards(currPlayer):
    print('You have the following development cards: ')
    for devCard in currPlayer.devCards:
        print (devCard + ": " + str(len(currPlayer.devCards[devCard])))