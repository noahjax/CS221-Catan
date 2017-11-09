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
        # Initialize the board and give values and resources to tiles
        self.board = Board()
        self.turnNum = 0
        self.num_players = 4

        # Simulate all possible die rolls and tile types
        values = 2*[i for i in range(2, 13)]
        tile_types = [['Ore'] * 3,
                      ['Brick'] * 3,
                      ['Wood'] * 4,
                      ['Grain'] * 4,
                      ['Wool'] * 4]

        # Select random values and resource for each tile and create it
        for i in range(20):
            # Grab a random value and assign it to the tile
            if i != 10:
                rand_value = random.randint(0, len(values))
                rand_tile = random.randint(0, len(values))

                value = values.pop(rand_value)
                resource = tile_types.pop(rand_tile)

                tile = Tile(resource, value, False, i)

                # Need to figure out how to map tiles to nodes
                self.board.tiles.append(tile)
            else:
                tile = Tile('Desert', 0, True, i)
                self.board.tiles.append(tile)

        # Initialize the players
        self.players = []
        names = []
        colors = ["blue", "red", "green", "yellow"]

        # Will need to comment out if we use AI
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

    # Defines logic for the first two turns where players select their settlements
    def firstTwoTurns(self):
        for i in range(4):
            self.initial_settlement_placements(i)

        for i in range(3, 0, -1):
            self.initial_settlement_placements(i)
        return True

    # This will place the initial settlement given the current player
    def initial_settlement_placements(self, playerIndex):
        player = self.players[playerIndex]
        playerName = player.getName()
        print("It is " + playerName + "\'s turn:")
        possible_placement = self.game.getSettlementLocations(player, True)
        # May want to decompose this into "get location" using AI and then place afterwards
        player.place_settlement(possible_placement, player)

    def run_AI_turn(self, curr_player):
        """
        This will take a given player and allow them to pick all of their options
        regardless of whether they are an AI or not.
        :param curr_player:
        :return:
        """
        curr_player_poss_moves = self.game.getPossibleActions(curr_player)

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




