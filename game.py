#Need a ton of imports
import pieces

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
        self.turn = 1
        self.devCards = initialize_dev_cards()

    #Function to create and shuffle deck of dev cards
    def initialize_dev_cards():


    #Function to handle pregame placing of pieces
    def run_pregame():
