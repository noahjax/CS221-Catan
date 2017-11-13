from game import *
from board import *
from player import *
from display import *

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
    
        # Set the tile ids
        # Each tile is defined by the coordinates of its peak node (0, 1), (0, 3), etc
        # tileIds contains the coordinates of each tile 0-18 in the above specified form
        self.tileIds = []
        for i in range(1, 7, 2): self.tileIds.append((0, i))
        for i in range(1, 9, 2): self.tileIds.append((1, i))
        for i in range(1, 11, 2): self.tileIds.append((2, i))
        for i in range(1, 9, 2): self.tileIds.append((3, i))
        for i in range(1, 7, 2): self.tileIds.append((4, i))
        assert len(self.tileIds) == 19
        
        # Select random values and resource for each tile and create it
        # Flatten the tile_types list so that popping works
        tilePool = [tile for tileType in tile_types for tile in tileType]
        tileCounter = 0
        for i in range(19):
            # Grab a random value and assign it to the tile
            if i != 9:
                rand_value = random.randint(0, len(values) - 1)
                rand_tile = random.randint(0, len(tilePool) - 1)
                value = values.pop(rand_value)
                resource = tilePool.pop(rand_tile)
        
                tile = Tile(resource, value, False, self.tileIds[i])

                # Need to figure out how to map tiles to nodes
                self.board.tiles.append(tile)
            else:
                tile = Tile('Desert', 0, True, self.tileIds[i])
                self.board.tiles.append(tile)
        
        # Initialize the players
        self.players = []
        names = []
        colors = ["blue", "red", "green", "yellow"]

        # Will need to comment out if we use AI
        for i in range(self.num_players):
            names.append(raw_input("Insert name of player:"))

        # Add the current player to players array
        for i in range(self.num_players):
            new_player = Player(i+1, names[i], colors[i])
            self.players.append(new_player)

        # Initialize the game 
        initRobberTile = 9
        self.game = Game(self.players, self.board, initRobberTile)
        
        # Initialize the display with the generated tiles
        self.display = Display(self.board, initRobberTile) 
        
    def main(self):
        """
        Main function that manages the majority of the game play.
        """
        self.display.update() # Show the display in its initialized state

        # self.firstTwoTurns()
        while True:
            # game.currMaxScore is not implemented
            if game.currMaxScore >= 10:
                self.endGame()
            else:
                curr_turn = self.turnNum
                curr_player = self.players[curr_turn % self.num_players]
                
                # Working on the display functionality, so only run human turns for now
                self.run_human_turn(curr_player)

                #if curr_player.isAi:
                #    self.run_human_turn(curr_player)
                #else:
                #    self.run_AI_turn(curr_player)
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
        player.place_settlement(possible_placement, player, True)
        player.place_road(2, True)

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

    def printResources(self, currPlayer):
        print('You have the following resources: \n')
        for resource in currPlayer.resources:
            print(resource + ": " + currPlayer.resources[resource] + "\n")

    def printDevCards(self, currPlayer):
        for devCard in currPlayer.devCards:
            print (devCard.type + ": " + currPlayer.devCards[devCard] + "\n")

    def getCitySettlementLoc(self, possiblePlacement):
        print("Please click on the node where you would like to build")
        while True:
            nc = self.display.getNode()
            if self.board.nodes[nc[0]][nc[1]] in possiblePlacement:
                return self.board.nodes[nc[0]][nc[1]] 
            print('node ' + str(nc) + ' is not a valid location')
            try_again = raw_input("Please type \'t\' to try again or enter to exit")
            if try_again != 't':
                return False

    def getRoadLoc(self, possiblePlacement):
        # For the human player to select the location of a road they want to build 
        while True:
            node1 = self.display.getNode()
            node2 = self.display.getNode()
            if (node1, node2) in possiblePlacement or (node2, node1) in possiblePlacement:
                return node1, node2 
            print('nodes ' + str(node1) + ' ' + str(node2) + ' are not valid')
            try_again = raw_input("Please type \'t\' to try again or enter to exit")
            if try_again != 't':
                break
        return False

    def get_and_play_devcard(self, type, currPlayer):
        if type in currPlayer.devCards:
            card = currPlayer.devCards[type].pop(0)
            card.play()

    def run_human_turn(self, curr_player):
        """
        This will run a humans turn, not yet implemented will deal with this when we
        have a graphical interface
        """
        # Options are to buy something or end turn
        print('It is ' + curr_player.name + '\s turn \n')

        self.printResources(curr_player)
        self.printDevCards(curr_player)
        while True:
            option = raw_input('Type \'b\' to buy something, type \'p\' to play a dev card, or hit enter to end your turn: ')
            if option == 'b':
                while True:
                    buyType = raw_input('type (s, c, r, d) to buy something, or hit enter to return: ')

                    if buyType == 's':
                        if self.game.canBuySettlement(curr_player.resources):
                            possiblePlacement = self.game.getSettlementLocations(curr_player, False) # array of possible nodes
                            if len(possiblePlacement) == 0:
                                print("Sorry there are no open settlement locations")
                                continue
                            node = self.getCitySettlementLoc(possiblePlacement)
                            if not node: continue
                            curr_player.place_settlement_human(node, self.game, False)
                            self.display.placeSettlement(node)
                            print(curr_player.score)
                        else:
                            print("Sorry you do not have the resources to buy a settlement")

                    elif buyType == 'c':
                        if self.game.canBuyCity(curr_player.resources):
                            possiblePlacement = self.game.getCityLocations(curr_player)
                            if len(possiblePlacement) == 0:
                                print("Sorry there are no valid city locations")
                                continue
                            node = self.getCitySettlementLoc(possiblePlacement)
                            if not node: continue
                            curr_player.place_city_human(node, self.game)
                            self.display.placeCity(node)
                            print(curr_player.score)

                    elif buyType == 'r':
                        if self.game.canBuyRoad(curr_player.resources):
                            possiblePlacements = self.game.getRoadLocations(curr_player)
                            if len(possiblePlacements) == 0:
                                print("Sorry there are no valid road locations")
                                continue
                            roadLoc = self.getRoadLoc(possiblePlacements)
                            if not roadLoc: continue
                            curr_player.place_road_human(roadLoc, False)
                            self.display.placeRoad(roadLoc[0], roadLoc[1])

                    elif buyType == 'd':
                        if self.game.canBuyDevCard(curr_player.resources):
                            if len(game.devCards) > 0:
                                curr_player.get_dev_card()
                            else:
                                print("Sorry there are no devcards left to buy")

            elif option == 'p':
                while True:
                    if len(curr_player.devCards) != 0:
                        type = raw_input("Type (k, v, r, m, yp) to choose what you want to play, or hit enter to return: ")
                        if type == 'k':
                            self.get_and_play_devcard('Knight', curr_player)
                        elif type == 'v':
                            self.get_and_play_devcard('Victory Point', curr_player)
                        elif type == 'r':
                            self.get_and_play_devcard('Road Building', curr_player)
                        elif type == 'm':
                            self.get_and_play_devcard('Monopoly', curr_player)
                        elif type == 'yp':
                            self.get_and_play_devcard('Year of Plenty', curr_player)
                        elif type == '':
                            break
                        else:
                            print("Sorry this type is not specified")
                    else:
                        print("You have no devcards left to play")
                        break
            elif option == '':
                return




        # print('run human turn')
        # # curPlayerPossMoves = self.game.getPossibleActions(curr_player)
        # curPlayerPossMoves = ['gn', 'mr'] # Testing only. Should be replaced with getPossibleActions
        # while True:
        #     # Loop until the user enters a valid action
        #     action = self.display.getUserAction()
        #     print('action = ' + str(action))
        #     if action in curPlayerPossMoves:
        #         break
        #     print('I\'m sorry Dave, I\'m afraid I can\'t do that')
        # self.display.execute(action)

    def endGame(self):
        """
        Ends the game and returns the winner
        """
        for player in self.players:
            if player.score >= 10:
                print (player.name + " has won the game!")
                print(player.name + " has won the game!")
play = Play()
play.main()
