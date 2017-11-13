# from enum import Enum
#
# class PieceType(Enum):
#     settlement = "Settlement"
#     road = "Road"
#     city = "City"
#     robber = "Robber"
#
#
# class Resource(Enum):
#     Ore = 'Ore'
#     Wood = 'Wood'
#     Brick = 'Brick'
#     Grain = 'Grain'


class Settlement:
    """
    Represents the settlement piece
    """
    def __init__(self, player, location):
        self.pieceType = 'Settlement'
        self.player = player
        self.location = location
        # Define resources needed to buy this piece
        self.resources_needed = {'Brick': 1, 'Wood': 1, 'Wool': 1, 'Grain': 1}

    def __str__(self):
        print_str = self.pieceType
        print_str += "\nPlayer: " + str(self.player)
        print_str += "\nLocation: " + str(self.location)
        print_str += "\nResources Needed: " + str(dict(self.resources_needed))
        return print_str


class Road:
    """
    Represents the road piece
    """
    def __init__(self, player, location):
        self.pieceType = 'Road'
        self.location = location
        self.player = player
        # Define resources needed to buy this piece
        self.resources_needed = {'Brick': 1, 'Wood': 1}

    def __str__(self):
        print_str = self.pieceType
        print_str += "\nPlayer: " + str(self.player)
        print_str += "\nLocation: " + str(self.location)
        print_str += "\nResources Needed: " + str(dict(self.resources_needed))
        return print_str


class City:
    """
    Represents the city piece
    """
    def __init__(self, player, location):
        self.pieceType = 'City'
        self.location = location
        self.player = player
        # Define resources needed to buy this piece
        self.resources_needed = {'Ore': 1, 'Grain': 1}

    def __str__(self):
        print_str = self.pieceType
        print_str += "\nPlayer: " + str(self.player)
        print_str += "\nLocation: " + str(self.location)
        print_str += "\nResources Needed: " + str(dict(self.resources_needed))
        return print_str


# test = City("noah", 2)
# print(test)
# test = Robber(3)
# print(test)
