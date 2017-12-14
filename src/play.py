from game import *
from board import *
from player import *
from display import *
import time


class Play:

    #############################################################################
    ############################  Initialization ################################
    #############################################################################
    """
    Class for the main game logic

    In this place we will start the game by initializng the board,
    the players, and the resources, and allowing the players to
    allocate their first settlements and roads. After this we will
    run the game until an end state has been found (i.e. a player has
    ten points.)
    """
    # New updates: logs is passed in as a dict from the player number to the current Log containing the weight
    # dicts for each player. At the start, they will contain a placeholder dict, overwritten by the player
    # Each AI player will be passed the log for their weights, which will be updated over time. 
    # This update is assuming that there is a higher level being run in test.py, where the actual log objects are stored.
    # Player types must be constant from one run to the next (e.g. P1 = human, P2 = AI, P3 = AI, P4 = Human for all runs in test.py)
    def __init__(self, players):
        # Initialize the board and give values and resources to tiles
        self.board = Board()
        self.turnNum = 0
        self.num_players = 4
        self.players = players

        # Simulate all possible die rolls and tile types
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
        tile_pool = [tile for tileType in tile_types for tile in tileType]
        tile_vals = [2,3,3,4,4,5,5,6,6,8,8,9,9,10,10,11,11,12]
        random.shuffle(tile_vals)
        for i in range(19):
            # Grab a random value and assign it to the tile
            if i != 9:
                value = tile_vals.pop()
                rand_tile = random.randint(0, len(tile_pool) - 1)
                resource = tile_pool.pop(rand_tile)

                # Create the tile to store its information
                tile = Tile(resource, value, False, self.tileIds[i])

                # Need to figure out how to map tiles to nodes
                self.board.tiles.append(tile)
            else:
                tile = Tile('Desert', 0, True, self.tileIds[i])
                self.board.tiles.append(tile)

            self.board.setTouchingTiles(tile)  

        # # Variables for player initialization
        # self.players = []
        # colors = ["orange", "red", "green", "blue"]

        # 'Modified to see run AI always without asking'
        # # Initialize the players
        # for i in range(self.num_players):
        #     # name = raw_input("Insert name of player or hit Enter to initialize an AI: ")
        #     name = ""
        #     if name != "":
        #         new_player = HumanPlayer(i, name, colors[i])
            
        #     # For each of the AI players, we also pass their corresponding weight log
        #     # elif i == 0:
        #     new_player = qAI(i, "AI"+str(i), colors[i], logs[i])
        #     # else:
        #     #     new_player = AiPlayer(i, "AI" + str(i), colors[i], logs[i])
        #    self.players.append(new_player)

        # Initialize the game 
        init_robber_tile = (2, 5)
        self.game = Game(self.players, self.board, init_robber_tile)
        
        # Initialize the display with the generated tiles
        self.display = Display(self.board, init_robber_tile)

#############################################################################
#################################  Main  ####################################
#############################################################################

    def main(self):
        """
        Main function that manages the majority of the game play.
        """
        # Show the display in its initialized state
        self.display.update()

        # Initialize player resources
        for player in self.players:
            player.resources['Ore'] = 0
            player.resources['Brick'] = 0
            player.resources['Wood'] = 0
            player.resources['Grain'] = 0
            player.resources['Wool'] = 0

        # Run first two turns
        self.first_two_turns()

        while True:
            #Delay so you can watch the game
            # time.sleep(.03)

            # print(str(self.turnNum % self.num_players) + ' ' + str(self.players[self.turnNum % self.num_players].resources))
            if self.turnNum/4 > 50:
                break
            # Check if game is over
            if self.game.currMaxScore >= 10:
                # print self.turnNum
                return self.endGame()
            else:
                curr_turn = self.turnNum
                curr_player = self.players[curr_turn % self.num_players]
                for resource in curr_player.resources:
                    if curr_player.resources[resource] < 0:
                        print curr_player.resources
                        raw_input("Negative Resources")
                #     assert(curr_player.numResources >= 0)
                    assert(curr_player.resources[resource] >= -10)
                    # assert(curr_player.resources[resource] >= 0)
                # print_player_stats(curr_player)

                roll = rollDice()

                # raw_input("")

                # Distribute resources given the last roll
                self.game.distributeResources(roll, self.display, curr_player)
                
                # Play the given turn
                if curr_player.isAI:
                    self.run_AI_turn(curr_player)
                else: 
                    self.run_human_turn(curr_player)

                # Update curMaxScore
                if curr_player.score > self.game.currMaxScore:
                    self.game.currMaxScore = curr_player.score
                
                self.turnNum += 1

                # print "-----End Turn-----"
                

#############################################################################
############################  First Two Turns  ##############################
#############################################################################

    # Main function for first two turns logic
    def first_two_turns(self):
        # Four players place their first settlement
        for i in range(4):
            # print ("It is player " + self.players[i].name + "\'s go")
            self.initial_placements(self.players[i])
            # printResources(self.players[i])

        # Players place second settlement from last to first
        for i in range(3, -1, -1):
            # print ("It is player " + self.players[i].name + "\'s go")
            self.initial_placements(self.players[i])

        # catan_log.log("Ran pregame")

    # Handle placements logic during the first 2 turns
    def initial_placements(self, player):
        # Get all possible options

        if player.isAI:
            # Run first turn logic AI
            self.AI_first_turn(player)
        else:
            # Run first turn logic Human
            possible_settlements = self.game.getSettlementLocations(player, True)
            self.Human_first_turn(player, possible_settlements)

    # Define logic for an AI's first turn
    def AI_first_turn(self, player):
        # Place single settlement
        settlementLoc = player.pick_settlement_position(self.game)
        player.place_settlement(settlementLoc, self.game, True)
        self.display.placeSettlement(settlementLoc, player)
        
        # Place single road
        roadLoc = player.pick_road_position(settlementLoc, self.game)
        player.place_road(roadLoc, self.game, True)
        self.display.placeRoad(roadLoc[0], roadLoc[1], player)

    # Define logic for a Human's first turn
    def Human_first_turn(self, player, possible_settlements):
        self.display.printPlayerStats(player)
        # Place single settlement
        settlementLoc = self.getCitySettlementLoc(possible_settlements, True)
        player.place_settlement(settlementLoc, self.game, True)
        self.display.placeSettlement(settlementLoc, player)

        # Place single road
        possible_roads = [(settlementLoc, neighbor) for neighbor in settlementLoc.neighbours]
        roadLoc = self.getRoadLoc(possible_roads, True)
        player.place_road(roadLoc, self.game, True)
        self.display.placeRoad(roadLoc[0], roadLoc[1], player)

#############################################################################
########################  Functions for AI turns  ###########################
#############################################################################
    """
    This will take an AI player and allow them to pick among all possible moves for a given gamestate
    """
    def run_AI_turn(self, player):
        #Pick and play a devCard. Often won't do anything if no available cards
        devCard = player.pickDevCard()
        # print "devCard: ", devCard
        # print player.devCards
        if devCard: self.play_devcard(devCard, player)
        
        # Get all possible moves player can make and send to AI for decision making
        # time.sleep(0.5)
        resources = player.resources

        # Get move from AI player
        move = player.pickMove(self.game)
        # print('move = ' + str(move))
        '''
        move = player.pickMove(self.game)
        '''

        # Print move for debugging purposes
        if not move:
            # print player.color,  "No move selected"
            return
        
        # print "move:", move
        # raw_input("")

        # Act on move by placing pieces and updating graphics
        for action, locs in move.items():
            piece, count = action

            #Exchange resources
            if isinstance(piece, tuple):
                oldResource, newResource = piece
                player.resources[oldResource] -= count
                player.numResources -= count
                player.resources[newResource] += 1
                player.numResources += 1
                assert player.resources[oldResource] >= 0
            #Buying DevCard
            elif piece == 'buyDevCard':
                self.game.buyDevCard(player)

            #Place piece
            else:
                # Might want to flip structure of for loop and if statements
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

        self.game.updateDevCards(player)

#############################################################################
############ Location finders for city, settlement and road #################
#############################################################################

    # Read node clicks to get settlement/city location
    def getCitySettlementLoc(self, possiblePlacement, firstTurn=False):
        print("Please click on the node where you would like to build")

        # Waits for user to click a node, and then returns location
        while True:
            nc = self.display.getNode()
            
            # Check if node is valid
            if self.board.nodes[nc[0]][nc[1]] in possiblePlacement:
                return self.board.nodes[nc[0]][nc[1]] 
            print('node ' + str(nc) + ' is not a valid location')

            # Give player option to give up selecting a node (if not first turn)
            if not firstTurn:
                try_again = raw_input("Please type \'t\' to try again or enter to exit: ")
                if try_again != 't':
                    return False

    # Read node clicks to get road location, and verify if it is allowed
    def getRoadLoc(self, possiblePlacement, firstTurn=False):
        print("Click on the nodes you would like to build a road on")

        # Wait for clicks which define the road
        while True:
            # Convert from node coordinates used in display to Node objects
            r, c = self.display.getNode()
            node1 = self.board.getNodeFromCoords(r,c)
            r, c = self.display.getNode()
            node2 = self.board.getNodeFromCoords(r,c)

            # Check if valid nodes for a road
            if (node1, node2) in possiblePlacement or (node2, node1) in possiblePlacement:
                print "Leaving get Road Loc"
                return node1, node2
            print('nodes ' + str(node1) + ' ' + str(node2) + ' are not valid')

            # Give player option to give up selecting nodes (if not first turn)
            if not firstTurn:
                try_again = raw_input("Please type \'t\' to try again or enter to exit: ")
                if try_again != 't':
                    break

        return False

#############################################################################
#################### Main function Human Turn  ##############################
#############################################################################
    '''
    Runs a human turn taking user input from both the command line and the graphical interface.
    '''
    def run_human_turn(self, curr_player):
        # Options are to buy something or end turn
        print('It is ' + curr_player.name + '\'s turn \n')

        # Debug print statements
        printResources(curr_player)
        printDevCards(curr_player)
        
        # Loop until user indicates to exit and end turn
        while True:
            self.display.printPlayerStats(curr_player)
            option = raw_input('Type \'b\' to buy something, type \'p\' to play a dev card, or hit enter to end your turn: ')
            if option == 'b':
                
                # Loop until player is done buying things
                while True:
                    self.display.printPlayerStats(curr_player)
                    buyType = raw_input('type (s, c, r, d) to buy something, or hit enter to return: ')

                    # Try and buy a settlement
                    if buyType == 's':
                        self.buy_and_place_settlement(curr_player)

                    # Try and buy a City
                    elif buyType == 'c':
                        self.buy_and_place_city(curr_player)

                    # Try and buy a road
                    elif buyType == 'r':
                        self.buy_and_place_road(curr_player)

                    # Try and buy a dev_card
                    elif buyType == 'd':
                        self.game.buyDevCard(curr_player)

                    # End Turn
                    elif buyType == "":
                        break

            elif option == 'p':
                
                # Loop until player is done playing devCards
                devCardString = get_devcard_prompt()
                
                # Wait until player
                while not self.play_devcard(devCardString, curr_player):
                    if devCardString == '': break
                    devCardString = get_devcard_prompt()
                
            elif option == '':
                break 
        
        # More debug print statements
        self.game.updateDevCards(curr_player)

        printResources(curr_player)
        printDevCards(curr_player)

#############################################################################
################# Buy and place Settlement, City, or Road   #################
#############################################################################

    # Initiates logic to buy and place a settlement
    def buy_and_place_settlement(self, curr_player):
        if self.game.canBuySettlement(curr_player):
            possiblePlacement = self.game.getSettlementLocations(curr_player, False) # array of possible nodes
            if len(possiblePlacement) == 0:
                print("Sorry there are no open settlement locations")
                return
            node = self.getCitySettlementLoc(possiblePlacement)
            if not node:
                return
            curr_player.place_settlement(node, self.game, False)
            self.display.placeSettlement(node, curr_player)
            print(curr_player.score)
        else:
            print("Sorry you do not have the resources to buy a Settlement")

    # Initiates logic to buy and place a city
    def buy_and_place_city(self, curr_player):
        if self.game.canBuyCity(curr_player):
            possiblePlacement = self.game.getCityLocations(curr_player)
            if len(possiblePlacement) == 0:
                print("Sorry there are no valid city locations")
                return
            node = self.getCitySettlementLoc(possiblePlacement)
            if not node:
                return
            curr_player.place_city(node, self.game)
            self.display.placeCity(node, curr_player)
            print(curr_player.score)
        else:
            print("Sorry you do not have the resources to buy a City")

    # Initiates logic to buy and place a road
    def buy_and_place_road(self, curr_player, devCard = False):
        if self.game.canBuyRoad(curr_player) or devCard:
            possiblePlacements = self.game.getRoadLocations(curr_player)
            if len(possiblePlacements) == 0:
                print("Sorry there are no valid road locations")
                return
            if curr_player.isAI:
                roadLoc = curr_player.pick_road_devcard_ai(possiblePlacements)
            else:
                roadLoc = self.getRoadLoc(possiblePlacements)
            if not roadLoc:
                return
            curr_player.place_road(roadLoc, self.game)
            self.display.placeRoad(roadLoc[0], roadLoc[1], curr_player)
        else:
            print("Sorry you do not have the resources to buy a Road")

#############################################################################
###########################   Play and buy Devcard   ########################
#############################################################################

    # Initiate the logic that plays a given devcard
    def play_devcard(self, type, currPlayer):
        #Make sure they have some of this devCard
        if type in currPlayer.devCards and currPlayer.devCards[type]:
            card = currPlayer.devCards[type].pop(0)
            if type == 'Knight':
                card.play(self.display, self.game)
            elif type == 'Road Building':
                currPlayer.devCardsPlayed['Road Building'] += 1
                for i in range(2):
                    self.buy_and_place_road(currPlayer, True)
            else:
                card.play()
        else:
            print("Sorry you do not have that dev card")
            return False

#############################################################################
###########################   End Game  #####################################
#############################################################################
    """
    Ends the game and returns the winner
    """
    def endGame(self):
        # print "game ending"
        for player in self.players:
            #Log for BasicAI Player
            if isinstance(player, BasicStrategy):
                player.update_weights()
                player_log = player.weights_log
                player_log.log_dict(player.resource_weights)

            if player.score >= 10:
                pass
                # print(player.turn_num, player.color + player.name + " has won the game!")
                # catan_log.log(player.color + "," + player.name)

        # stall_end = raw_input("you sure you wanna end right now")

# play = Play()
# play.main()
