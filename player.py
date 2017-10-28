import pieces
#import all the stuff

class Player(object):
    """
    Class for each player 

    (Add more stuff)
    """
    def __init__(self, turn_num, name, color):
        
        if turn_num < 1 or turn_num > 4:
            raise Exception("Turn number must be between 1 and 4 inclusive")

        self.turn_num = turn_num
        self.name = name
        self.color = color
        self.pieces = set()         #Don't necessarily need to keep track of pieces for each player, but could be useful
