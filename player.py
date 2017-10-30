import pieces
from collections import defaultdict
#import all the stuff

class Player(object):
    """
    Class for each player 

    (Add more stuff)
    """
    def __init__(self, turn_num, name, color):
        
        if turn_num < 1 or turn_num > 4:
            raise Exception("Turn number must be between 1 and 4 inclusive")

        #Lets have turn number start at 0 because it might make coding nicer
        self.turn_num = turn_num
        self.name = name
        self.color = color

        #Storing these in dict to make it easy to figure out how many they have. {"item": count}
        self.resources = defaultdict(str)
        self.devCards = defaultdict(str)
        self.pieces = defaultdict(str)         #Don't necessarily need to keep track of pieces for each player, but could be useful

    #Allows you to check if two players are equal...Not sure if we need it, but may come in handy
    def __eq__(self, other):
        if other is None:
            return False
        if other.__class__ != Player:
            return False
        return (self.color == other.color
                and self.name == other.name
                and self.turn_num == other.turn_num
                and self.devCards == other.devCards
                and self.resources == other.resources
                and self.pieces == other.pieces)