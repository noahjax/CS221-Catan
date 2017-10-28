from enum import Enum

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
    def __init__(self, type, player, location):
        self.type = type
        self.player = player
        self.location = location    #Not sure if individual pieces need to keep track of location
        self.pieces = set()         #Don't necessarily need to keep track of pieces for each player, but could be useful