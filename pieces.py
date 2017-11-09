from enum import Enum
from collections import defaultdict

#Not sure if this enum is even useful now that we have classes for each piece
# class PieceType(Enum):
#     settlement = "Settlement"
#     road = "Road"
#     city = "City"
#     robber = "Robber"

#Also not sure how useful this will be. Haven't used it down below yet but easily could
#by calling Resource.Ore instead of 'Ore'. Does allow you to loop through resources thought which is nice.
class Resource(Enum):
    Ore = 'Ore'
    Wood = 'Wood'
    Brick = 'Brick'
    Grain = 'Grain'


class Piece:
    """
    Superclass for pieces settlement, road, and robber. Holds functions shared across pieces.
    """
    def __init__(self, player, location):
        self.pieceType = "Piece"
        self.player = player
        self.location = location
        self.resources_needed = defaultdict(str)

    #To string for all subclasses
    def __str__(self):
        printStr = self.pieceType
        printStr += "\nPlayer: " + str(self.player)
        printStr += "\nLocation: " + str(self.location)
        printStr += "\nResources Needed: " + str(dict(self.resources_needed))
        return printStr
        

class Settlement(Piece):
    """
    Represents the settlement piece
    """
    def __init__(self, player, location):
        Piece.__init__(self, player, location)
        self.pieceType = 'Settlement'
        #Define resources needed to buy this piece
        self.resources_needed['Brick'] = 1
        self.resources_needed['Wood'] = 1
        self.resources_needed['Wool'] = 1
        self.resources_needed['Grain'] = 1


class Road(Piece):
    """
    Represents the road piece
    """
    def __init__(self, player, location):
        Piece.__init__(self, player, location)
        self.pieceType = 'Road'
        #Define resources needed to buy this piece
        self.resources_needed['Brick'] = 1
        self.resources_needed['Wood'] = 1


class City(Piece):
    """
    Represents the city piece
    """
    def __init__(self, player, location):
        Piece.__init__(self, player, location)
        self.pieceType = 'City'
        #Define resources needed to buy this piece
        self.resources_needed['Ore'] = 2
        self.resources_needed['Grain'] = 1

class Robber:
    """
    Represents the robber piece

    My thinking is that we initialize the Robber piece with only a position. We don't 
    need to do much but keep track of where the robber is. All of the heavy logic can be handled in
    game when a  7 is rolled. May not need robber class at all.
    """
    def __init__(self, location):
    # def __init__(self, board, player, players, location):
        #Not sure if we need these
        # self.board = board    
        # self.player = player
        # self.players = players
        self.location = location

    #May not even need this function if we handle the logic in game
    def move(self, board, position):
        if not position == self.location:
            ##set location on board for robber
            ##if position on board
            self.location = position
            return True
        else:
            #May want to handle printing in function that calls this, idk
            print("This location is invalid, please choose again.")  
            return False

    def __str__(self):
        return "Robber \nLocation: " + str(self.location)

# test = City("noah", 2)
# print(test)
# test = Robber(3)
# print(test)
