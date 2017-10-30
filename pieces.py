from enum import Enum
from collections import defaultdict

#Not sure if this enum is even useful...might as well use strings
class PieceType(Enum):
    settlement = "Settlement"
    road = "Road"
    city = "City"
    robber = "Robber"

class Piece(object):
    """
    Represents one of four possible pieces
        -Settlement
        -Road
        -City
        -Robber
    """
    def __init__(self, piecetype, player, location):
        self.type = type
        self.player = player
        self.location = location    #Not sure if individual pieces need to keep track of location
        
        #Not sure if pieces should store thier costs...What do you guys think about storing here vs elsewhere
        #Ideal location may be in game so it's only calculated once
        self.resources_needed = defaultdict(str)
        #Put values in resources needed based on the piece type
        if piecetype == "Settlement":
            self.resources_needed['Brick'] = 1
            self.resources_needed['Wood'] = 1
            self.resources_needed['Wool'] = 1
            self.resources_needed['Grain'] = 1
        elif piecetype == "City":
            self.resources_needed['Ore'] = 3
            self.resources_needed['Grain'] = 2
        elif piecetype == "Road":
            self.resources_needed['Brick'] = 1
            self.resources_needed['Wood'] = 1