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

# Prompt user to identify a devcard
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
def printDevCards(currPlayer, endTurn = False):
    print('You recently purchased the following development cards: ')
    if not endTurn:
        for devCard in currPlayer.newDevCards:
            print(devCard + ": " + str(len(currPlayer.newDevCards[devCard])))

    print('You can play the following development cards: ')
    for devCard in currPlayer.devCards:
        print (devCard + ": " + str(len(currPlayer.devCards[devCard])))

# Helper function to add resources. Assumes use of defaultdicts
def addResources(resources, toAdd):
    for resource, count in toAdd.items():
        resources[resource] += count

# Helper function to subtract resources. Assumes use of defaultdicts
def subtractResources(resources, toSub):
    for resource, count in toSub.items():
        resources[resource] -= count

# Helper function to check if resource amounts are valid. Helpful for canBuy(x)
### May not be useful ###
def areValidResources(resources):
    for count in resources.values():
        if count < 0: return False
    return True

# Move the robber
def moveRobber(game, display):
    print("Please click on the top central node of the tile where you would like to place the robber")
    while True:
        position = display.getNode()
        isValid = True
        for tile in position.get_tiles:
            for node_coordinates in game.board.getNodesForTile(tile):
                node = game.board.getNodeFromCoords(node_coordinates[0], node_coordinates[1])
                if node is not None and node.isOccupied:
                    if node.occupyingPiece.player.score <= 3:
                        print("Sorry this is an invalid robber location")
                        isValid = False
        if isValid:
            break

    display.placeRobber(position)
    game.set_robber_location(position, display)

#Gets the probability of a certain roll
def rollProb(roll):
            dist = abs(roll - 7)
            num = float(6 - dist)
            return num / 36

# Pulled from sentiment assignment to do an efficient dot product
def dotProduct(d1, d2):
    if len(d1) < len(d2):
        return dotProduct(d2, d1)
    else:
        return sum(d1.get(f, 0) * v for f, v in d2.items())

