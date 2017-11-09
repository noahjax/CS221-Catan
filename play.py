from game import *
from devcards import *
from board import *
from player import *


class Play:
    def __init__(self):
        """Initialize the board and give values"""
        self.board = Board()
        self.turnNum = 0
        self.num_players = 4
        values = 2*[i for i in range(2, 13)]
        for i in range(self.board.board):
            randIndex = random.randint(0, len(values))
            self.board.board[i] = values.pop(randIndex)

        """Initialize the players"""
        self.players = []
        names = []
        colors = ["blue", "red", "green", "yellow"]
        for i in range(self.num_players):
            names.append(input("Insert name of player:"))

        for i in range(self.num_players):
            new_player = Player(i+1, names[i], colors[i])
            self.players.append(new_player)

        """Initialize the game"""
        self.game = Game(self.players, self.board)


        ##For all pieces in board assign value\

    def main(self):
        self.firstTwoTurns()


    def firstTwoTurns(self):
        for i in range(4):
            currTurn = self.turnNum % self.num_players
            self.turnNum += 1
            player = self.players[currTurn]
            playerName = player.getName()
            print ("It is " + playerName + "\'s turn:")
            
        return True

    def run_first_turns(self):
        return True

    def run_normal_turn(self):

        count = 0
        while (True):
            if (count > 0):
                print("Sorry that was not a valid move, please try again")
            move = input("To buy a structure enter 'b' \n" +
                         "To buy a devcard enter 'd' \n" +
                         "To play a devcard enter 'p'"
                         "To end your turn enter 'e' \n")
            count += 1
            if (move == 'b'):
        return True


