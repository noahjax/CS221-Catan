from game import *
from board import *
from player import *


class Play:
    """
    Class for the main game logic

    In this place we will start the game by initializng the board,
    the players, and the resources, and allowing the players to
    allocate their first settlements and roads. After this we will
    run the game until an end state has been found (i.e. a player has
    ten points.)
    """
    def __init__(self):
        # Initialize the board and give values
        self.board = Board()
        self.turnNum = 0
        self.num_players = 4
        values = 2*[i for i in range(2, 13)]

        for i in range(self.board.board):
            # Grab a random value and assign it to the tile
            randIndex = random.randint(0, len(values))
            currTile = self.board.board[i]
            currTile.setValue(values.pop(randIndex))
            # If its the desert tile set the robber to true
            if currTile.resource == 'desert':
                currTile.robber = True

        # Initialize the players
        self.players = []
        names = []
        colors = ["blue", "red", "green", "yellow"]
        for i in range(self.num_players):
            names.append(input("Insert name of player:"))

        # Add the current player to players array
        for i in range(self.num_players):
            new_player = Player(i+1, names[i], colors[i])
            self.players.append(new_player)

        # Initialize the game
        self.game = Game(self.players, self.board)


    def main(self):
        """
        Main function that manages the majority of the game play.
        """
        self.firstTwoTurns()
        while True:
            if game.currMaxScore >= 10:
                self.endGame()
            else:

                curr_turn = self.turnNum
                curr_player = self.players[curr_turn]
                if curr_player.isAi:
                    self.run_human_turn(curr_player)
                else:
                    self.run_AI_turn(curr_player)
                self.turnNum += 1


    def firstTwoTurns(self):
        for i in range(4):
            currTurn = self.turnNum % self.num_players
            self.turnNum += 1
            player = self.players[currTurn]
            playerName = player.getName()
            print("It is " + playerName + "\'s turn:")
            
        return True

    def run_AI_turn(self, curr_player):
        """
        This will take a given player and allow them to pick all of their options
        regardless of whether they are an AI or not.
        :param curr_player:
        :return:
        """
        curr_player_poss_moves = curr_player.getPossibleMoves()

        # Get all the moves that the player can play, with the positions for each piece
        moves = curr_player_poss_moves[0]
        positions = curr_player_poss_moves[1]

        # This is where the AI would come in to choose best move
        chosenMove = curr_player.pickMove(moves)
        for key, val in chosenMove:
            if not key == 'dev card':
                curr_player.pickPosition(key, val, positions)
            else:
                curr_player.pickDevCard(key, val)



    def run_human_turn(self, curr_player):
        """
        This will run a humans turn, not yet implemented will deal with this when we
        have a graphical interface
        """
        return True



    def endGame(self):
        """
        Ends the game and returns the winner
        """
        for player in self.players:
            if player.score >= 10:
                print (player.name + " has won the game!")




