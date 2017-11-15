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
        for i in range(2, 9, 2): self.tileIds.append((3, i))
        for i in range(2, 7, 2): self.tileIds.append((4, i))
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

            self.board.setTouchingTiles(tile)  
            

        # Initialize the players
        self.players = []
        names = []
        colors = ["blue", "red", "green", "orange"]

        # Will need to comment out if we use AI
        for i in range(self.num_players):
            name = raw_input("Insert name of player or hit Enter to initialize an AI: ")
            if name != "":
                new_player = HumanPlayer(i, name, colors[i])
            else:
                new_player = AiPlayer(i, "AI"+str(i), colors[i])
            self.players.append(new_player)
        
        # # Add the current player to players array
        # for i in range(self.num_players):
        #     new_player = Player(i+1, names[i], colors[i])
        #     self.players.append(new_player)

        # Initialize the game 
        initRobberTile = 9
        self.game = Game(self.players, self.board, initRobberTile)
        
        # Initialize the display with the generated tiles
        self.display = Display(self.board, initRobberTile) 

#############################################################################
#################################  Main  ####################################
#############################################################################

    def main(self):
        """
        Main function that manages the majority of the game play.
        """
        self.display.update() # Show the display in its initialized state

        for player in self.players:
            player.resources['Ore'] = 3
            player.resources['Brick'] = 3
            player.resources['Wood'] = 3
            player.resources['Grain'] = 3
            player.resources['Wool'] = 3

        # self.firstTwoTurns()

        while True:
            # game.currMaxScore is not implemented
            if self.game.currMaxScore >= 5:
                self.endGame()
            else:
                curr_turn = self.turnNum
                curr_player = self.players[curr_turn % self.num_players]
                roll = 7
                while roll == 7:
                    roll = self.game.rollDice()
                    print("the roll was a " + str(roll))
                self.game.distributeResources(roll, curr_player)
                
                # Working on the display functionality, so only run human turns for now
                if curr_player.isAI:
                    print "Running AI turn"
                    print curr_player
                    self.run_AI_turn(curr_player)
                else: 
                    print "Why tho"
                    self.run_human_turn(curr_player)

                self.printResources(curr_player)
                option = raw_input("Press a key to continue")

                #if curr_player.isAi:
                #    self.run_human_turn(curr_player)
                #else:
                #    self.run_AI_turn(curr_player)
                if curr_player.score > self.game.currMaxScore:
                    self.game.currMaxScore = curr_player.score
                self.turnNum += 1

#############################################################################
############################  Pregame Logic  ################################
#############################################################################

    #Handle placements during the first 2 turns
    def initial_placements(self, player):
        #Get all possible options (should be same for human or AI)
        possible_settlements = self.game.getSettlementLocations(player, True)
        # print('possible settlements = ' + str(possible_settlements))
        if player.isAI:
            #Get possible locations and place at a location
            settlementLoc = player.pick_settlement_position(possible_settlements)
            player.place_settlement(settlementLoc, self.game, True)
            self.display.placeSettlement(settlementLoc, player)

            # #Get road locations and place (road locations must be adjacent to respective settlement)
            possible_roads = [(settlementLoc, neighbor) for neighbor in settlementLoc.neighbours]
            roadLoc = player.pick_road_position(possible_roads)
            player.place_road(roadLoc, self.game, True)
            self.display.placeRoad(roadLoc[0], roadLoc[1], player)
        else:
            #Find where the human wants to place the settlement
            settlementLoc = self.getCitySettlementLoc(possible_settlements, True)
            # for neighbour in settlementLoc.neighbours:
            #     print neighbour.row, neighbour.col
            player.place_settlement(settlementLoc, self.game, True)
            self.display.placeSettlement(settlementLoc, player)

            #Find where human wants to place road
            possible_roads = [(settlementLoc, neighbor) for neighbor in settlementLoc.neighbours]
            roadLoc = self.getRoadLoc(possible_roads, True)
            player.place_road(roadLoc, self.game, True)
            self.display.placeRoad(roadLoc[0], roadLoc[1], player)
    
    #Defines logic for the first two turns where players select their settlements
    def firstTwoTurns(self):
        #Snake forwards through players
        for i in range(4):
            print ("It is player " + self.players[i].name + "\'s go")
            self.initial_placements(self.players[i])
            self.printResources(self.players[i])

        #Snake backwards through players
        for i in range(3, -1, -1):
            print ("It is player " + self.players[i].name + "\'s go")
            self.initial_placements(self.players[i])

        catan_log.log("Ran pregame")

#############################################################################
########################  Functions for AI turns  ###########################
#############################################################################
    """
    This will take an AI player and allow them to pick among all possible moves for a give gamestate
    """
    def run_AI_turn(self, player):
        
        #Get all possible moves player can make and send to AI for decision making
        possible_moves = self.game.getPossibleActions(player)

        #Get move from AI player
        move = player.pickMove(possible_moves)
        if not move:
            print player.name,  "No move selected"
            return
        
        print "move:",move
        #Act on move by placing pieces and updating graphics
        for action, locs in move.items():
            piece, count = action
            #Might want to flip structure of for loop and if statements
            for loc in locs:
                if piece == 'Settlement':
                    player.place_settlement(loc, self.game)
                    self.display.placeSettlement(loc, player)
                elif piece == 'City':
                    player.place_city(loc, self.game)
                    self.display.placeCity(loc, player)
                elif piece == 'Road':
                    player.place_road(loc, self.game)
                    self.display.placeRoad(loc[0], loc[1], player)

        
        # # Get all the moves that the player can play and pass to AI to select a move
        # moves = [[possible_move.keys()] for possible_moves in possible_moves]
        # positions = possible_moves[1]

        # # This is where the AI would come in to choose best move
        # chosenMove = curr_player.pickMove(moves)
        # for key, val in chosenMove:
        #     if not key == 'dev card':
        #         curr_player.pickPosition(key, val, positions)
        #     else:
        #         curr_player.pickDevCard(key, val)

#############################################################################
###########################   Random Utils   ################################
#############################################################################

    def printResources(self, currPlayer):
        print('You have the following resources: ')
        for resource in currPlayer.resources:
            print(resource + ": " + str(currPlayer.resources[resource]))

    def printDevCards(self, currPlayer):
        print('You have the following development cards: ')
        for devCard in currPlayer.devCards:
            print (devCard + ": " + str(len(currPlayer.devCards[devCard])))

    def get_and_play_devcard(self, type, currPlayer):
        if type in currPlayer.devCards:
            card = currPlayer.devCards[type].pop(0)
            if type == 'Knight':
                card.play(self.display, self.game)
            else:
                card.play()
        else:
            print("Sorry you do not have that dev card")



#############################################################################
######################   Functions for Human Turns   ########################
#############################################################################

    #Read node clicks to get settlement/city location
    def getCitySettlementLoc(self, possiblePlacement, firstTurn=False):
        print("Please click on the node where you would like to build")
        while True:
            nc = self.display.getNode()
            if self.board.nodes[nc[0]][nc[1]] in possiblePlacement:
                return self.board.nodes[nc[0]][nc[1]] 
            print('node ' + str(nc) + ' is not a valid location')
            if not firstTurn:
                try_again = raw_input("Please type \'t\' to try again or enter to exit: ")
                if try_again != 't':
                    return False

    #Read node clicks to get road location
    def getRoadLoc(self, possiblePlacement, firstTurn=False):
        # For the human player to select the location of a road they want to build 
        print("Click on the nodes you would like to build a road on")
        while True:
            #Convert from node coordinates used in display to Node objects
            r,c = self.display.getNode()
            node1 = self.board.getNodeFromCoords(r,c)
            r, c = self.display.getNode()
            node2 = self.board.getNodeFromCoords(r,c)
            print(possiblePlacement)
            print(node1,node2)
            if (node1, node2) in possiblePlacement or (node2, node1) in possiblePlacement:
                print "Leaving get Road Loc"
                return node1, node2 
            print('nodes ' + str(node1) + ' ' + str(node2) + ' are not valid')
            if not firstTurn:
                try_again = raw_input("Please type \'t\' to try again or enter to exit: ")
                if try_again != 't':
                    break
        return False

    '''
    Runs a hunan turn taking user input from both the command line and the graphical interface.
    '''
    def run_human_turn(self, curr_player):
        # Options are to buy something or end turn
        print('It is ' + curr_player.name + '\'s turn \n')

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
                            curr_player.place_settlement(node, self.game, False)
                            self.display.placeSettlement(node, curr_player)
                            print(curr_player.score)
                        else:
                            print("Sorry you do not have the resources to buy a Settlement")

                    elif buyType == 'c':
                        if self.game.canBuyCity(curr_player.resources):
                            possiblePlacement = self.game.getCityLocations(curr_player)
                            if len(possiblePlacement) == 0:
                                print("Sorry there are no valid city locations")
                                continue
                            node = self.getCitySettlementLoc(possiblePlacement)
                            if not node: continue
                            curr_player.place_city(node, self.game)
                            self.display.placeCity(node, curr_player)
                            print(curr_player.score)
                        else:
                            print("Sorry you do not have the resources to buy a City")

                    elif buyType == 'r':
                        if self.game.canBuyRoad(curr_player.resources):
                            possiblePlacements = self.game.getRoadLocations(curr_player)
                            if len(possiblePlacements) == 0:
                                print("Sorry there are no valid road locations")
                                continue
                            roadLoc = self.getRoadLoc(possiblePlacements)
                            if not roadLoc: continue
                            curr_player.place_road(roadLoc, self.game)
                            self.display.placeRoad(roadLoc[0], roadLoc[1], curr_player)
                        else:
                            print("Sorry you do not have the resources to buy a Road")

                    elif buyType == 'd':
                        self.game.buyDevCard(curr_player)

                    elif buyType == "":
                        break

            elif option == 'p':
                while True:
                    if len(curr_player.devCards) != 0:
                        print ("You have the following development cards: ")
                        self.printDevCards(curr_player)
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
                break 
        print('exited')
        self.printResources(curr_player)
        self.printDevCards(curr_player)

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

    # def main2(self):
    #     self.display.update() # Show the display in its initialized state
    #     while True:
    #         r, c = self.display.getNode()
    #         node = self.board.nodes[r][c]
    #         for tile in node.touchingTiles:
    #             print(tile.value, tile.resource)


play = Play()
play.main()
