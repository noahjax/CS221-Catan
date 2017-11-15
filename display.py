import pygame
from pygame.locals import*
import numpy as np
import board as bd 

class Display:
 
    screen = None
    screenWidth, screenHeight = (640, 480)

    redDot, blueDot, greenDot, orangeDot, blackDot = (None, None, None, None, None)
    redRoad, blueRoad, greenRoad, orangeRoad, blackRoad = (None, None, None, None, None)
    
    tile = None
    robber = None

    dotWidth, dotHeight = (None, None) 
    tileWidth, tileHeight = (None, None)
    robberWidth, robberHeight = (None, None)
    roadWidth, roadHeight = (None, None)

    # Store the location that the image for each node occupies
    # Each location is mapped to by a key equivalent to the coordinate of the node in the
    # game logic (e.g. (0, 1) : (xmin, ymin, xmax, ymax))
    nodeLocs = {}
    
    # Load all constant objects to blit exactly once, so we don't have to do a lot of tedious
    # computation each time we want to refresh the screen. 
    # If we want to make changes to the screen, roads, etc, we will do that elsewhere, in a fluid list
    # Each element in permanent blits is a tuple containing an image, and the x, y coordinate to blit at
    # (img, (blitAtX, blitAtY))
    permanentBlits = []
   
    # Store the type of each tile. This is set upon intialization of the board, when an initial
    # arrangement should be passed in
    tileValues = []

    # Store the tempBlits as a dict, since the order etc will be changing
    # As such, these should not need to be printed in any particular order
    tempBlits = {}

    # Store the x, y tuples of each tile center
    # In order of tile index (0-18)
    tileCenters = []
    
    # The font in which text should be displayed
    font = None
    
    def __init__(self, board, robberTile):
        # Loads:
        # - tiles
        # - nodes
        # - robber
        # Set the member variables storing their sizes.
        pygame.init()
        pygame.font.init()
       
        # Not sure this is the best way to do this, as we will have to keep updating the
        # local board, as well as the board stored elsewhere. Should really discuss this
        self.board = board
        
        self.font = pygame.font.SysFont('Comic Sans MS', 10)

        self.screen = pygame.display.set_mode((self.screenWidth, self.screenHeight))
        
        # Dots on dots on dots on dots on dots on ... 
        self.redDot = pygame.image.load('red_dot.png')
        self.redDot = pygame.transform.scale(self.redDot, (int(self.screenWidth / 25), int(self.screenHeight / 25)))
        
        self.blueDot = pygame.image.load('blue_dot.png')
        self.blueDot = pygame.transform.scale(self.blueDot, (int(self.screenWidth / 25), int(self.screenHeight / 25)))
        
        self.greenDot = pygame.image.load('green_dot.png')
        self.greenDot = pygame.transform.scale(self.greenDot, (int(self.screenWidth / 25), int(self.screenHeight / 25)))
        
        self.orangeDot = pygame.image.load('orange_dot.png')
        self.orangeDot = pygame.transform.scale(self.orangeDot, (int(self.screenWidth / 25), int(self.screenHeight / 25)))
        
        self.blackDot = pygame.image.load('black_dot.png')
        self.blackDot = pygame.transform.scale(self.blackDot, (int(self.screenWidth / 25), int(self.screenHeight / 25)))

        # Load the city and town pngs
        self.city = pygame.image.load('castle.png')
        self.city = pygame.transform.scale(self.city, (self.screenWidth / 25, self.screenHeight / 25))

        self.town = pygame.image.load('town.png')
        self.town = pygame.transform.scale(self.town, (self.screenWidth / 25, self.screenHeight / 25))

        # Load a hexagon to use as a tile
        self.tile = pygame.image.load('hex.png')
        self.tile = pygame.transform.scale(self.tile, (int(self.screenWidth / 8), int(self.screenHeight / 8)))

        # Load triangles to use as roads
        self.redRoad = pygame.image.load('red_triangle.png')
        self.redRoad = pygame.transform.scale(self.redRoad, (self.screenWidth / 25, self.screenHeight / 25))
        
        self.blueRoad = pygame.image.load('blue_triangle.png')
        self.blueRoad = pygame.transform.scale(self.blueRoad, (self.screenWidth / 25, self.screenHeight / 25))

        self.greenRoad = pygame.image.load('green_triangle.png')
        self.greenRoad = pygame.transform.scale(self.greenRoad, (self.screenWidth / 25, self.screenHeight / 25))
        
        self.orangeRoad = pygame.image.load('orange_triangle.png')
        self.orangeRoad = pygame.transform.scale(self.orangeRoad, (self.screenWidth / 25, self.screenHeight / 25))
        
        # Set some variables to reference later on
        self.tileWidth = self.tile.get_rect().size[0]
        self.tileHeight = self.tile.get_rect().size[1]

        self.dotWidth = self.redDot.get_rect().size[0]
        self.dotHeight = self.redDot.get_rect().size[1]

        self.roadWidth = self.redRoad.get_rect().size[0]
        self.roadHeight = self.redRoad.get_rect().size[1]

        # This should happen before loading any temp blits, as tileCenters are initialized here
        self.loadPermanentBlits()

        # Load the robber
        self.robber = pygame.image.load('robber.png')
        self.robber = pygame.transform.scale(self.robber, (int(self.tileWidth / 2), int(self.tileHeight / 2)))
        self.robberWidth = self.robber.get_rect().size[0]
        self.robberHeight = self.robber.get_rect().size[1]

        self.placeRobber(robberTile) 



    def placeRobber(self, node):
        # Add the robber to tempBlits at the center of the specified tile
        x, y, z, w = self.nodeLocs[node]
        self.tempBlits['robber'] = (self.robber, (x, y + int(self.tileHeight / 2)))


    def getTextSurface(self, tile):
        # Returns a surface containing the resource, value string of the given tile
        text = str(tile.resource) + ' ' + str(tile.value)
        textSurface = self.font.render(text, False, (0, 0, 0))
        # Scale according to the size of the tiles
        textSurface = pygame.transform.scale(textSurface, (int(self.tileWidth * 4 / 5), int(self.tileWidth / 4)))
        return textSurface




    def loadPermanentBlits(self):    
        # Compute the blit locations of each node and tile
        numTiles = [3, 4, 5, 4, 3]

        offsets = [int(self.screenWidth / 2) - int(self.tileWidth * 3 / 2), \
                   int(self.screenWidth / 2) - int(self.tileWidth * 2), \
                   int(self.screenWidth / 2) - int(self.tileWidth * 5 / 2), \
                   int(self.screenWidth / 2) - int(self.tileWidth * 2), \
                   int(self.screenWidth / 2) - int(self.tileWidth * 3 / 2)]

        # Store the locations of the dots relative to each hexagon
        topDotOffsets = [(int(-self.dotWidth / 2), int(self.tileHeight / 5) - int(self.dotHeight / 2)), \
                      (int(self.tileWidth / 2) - int(self.dotWidth / 2), int(-self.dotHeight / 2)), \
                      (self.tileWidth - int(self.dotWidth / 2), int(self.tileHeight / 5) - int(self.dotHeight / 2))]
        bottomDotOffsets = [(int(-self.dotWidth / 2), int(self.tileHeight * 4 / 5) - int(self.dotHeight / 2)), \
                            (int(self.tileWidth / 2) - int(self.dotWidth / 2), self.tileHeight - int(self.dotHeight / 2)), \
                            (self.tileWidth - int(self.dotWidth / 2), int(self.tileHeight * 4 / 5) - int(self.dotHeight / 2))]

        # Store all of the nodes to blit in this list, and add them last so
        # that they will appear in the foreground
        nodesToBlit = []

        # Since we are setting up the tiles in order, we can set the type of each tile at the same time
        # Use this counter to keep track of the tile index to be set
        counterTile = 0

        for i in range(len(numTiles)):
            
            # We use two counterJ's so that the double-layer of nodes in the middle tiles can be 
            # handled at the same time
            counterJTop = 0
            counterJBot = 0
            for j in range(numTiles[i]):
                imgX = j * self.tileWidth + offsets[i]
                imgY = i * int(self.tileHeight * 4 / 5) + int(self.screenWidth / 7)
                self.tileCenters.append((imgX + int(self.tileWidth / 2), imgY + int(self.tileHeight / 2))) 
                self.permanentBlits.append((self.tile, (imgX, imgY)))
    
                # Display the type of the tile inside the hexagon
                tile = self.board.tiles[counterTile]
                text = self.getTextSurface(tile)
                self.permanentBlits.append((text, (imgX + int(self.tileWidth / 8), imgY + int(self.tileHeight / 2) - int(self.tileHeight / 8))))
                counterTile += 1

                if j == numTiles[i] - 1:
                    # We only place all three dots if we are on the last tile
                    # Otherwise we will be double counting the dots on intersections
                    dotRange = 3 
                else:
                    dotRange = 2 
                
                if i <= 2:
                    # Place nodes along the top of the corresponding tile

                    for offset in topDotOffsets[:dotRange]:
                        # Use i, j, and dotRange to compute the coordinate for this dot in the
                        # nodeLocs dict (and the game logic)
                        # Both blit the dot to the game screen, and add it to nodeLocs
                        dotX = imgX + offset[0]
                        dotY = imgY + offset[1]
                        nodesToBlit.append((self.blackDot, (dotX, dotY)))
                        coords = (i, counterJTop) 
                        self.nodeLocs[coords] = (dotX, dotY, dotX + self.dotWidth, dotY + self.dotHeight)
                        counterJTop += 1
                if i >= 2:
                    # Place nodes along the bottom of the corresponding tile
                    for offset in bottomDotOffsets[:dotRange]:
                        dotX = imgX + offset[0]
                        dotY = imgY + offset[1]
                        nodesToBlit.append((self.blackDot, (dotX, dotY)))
                        coords = (i + 1, counterJBot)
                        self.nodeLocs[coords] = (dotX, dotY, dotX + self.dotWidth, dotY + self.dotHeight)
                        counterJBot += 1
                
        # Now we add the nodes to self.permanentBlits, so that they will appear after the tiles
        for n in nodesToBlit:
            self.permanentBlits.append(n)
       
        print('done in init')




    def getNodeAtXY(self, x, y):
        # If a node is at the coordinates x, y, return the coordinates of the node in the game logic
        # Return None if no node is at the specified coords
        for coords, minmaxTuple in self.nodeLocs.iteritems():
            if minmaxTuple[0] <= x <= minmaxTuple[2] and minmaxTuple[1] <= y <= minmaxTuple[3]:
                return coords
        return None




    def blitAll(self):
        # Blit all available objects to the screen
        # Currently blits all objects in 
        # - permanentBlits
        # - tempBlits 
        for blit in (self.permanentBlits + list(self.tempBlits.values())):
            self.screen.blit(blit[0], blit[1])


    def getUserAction(self):
        # Put some kinds of possible commands in here at the moment
        # I'm guessing that this kind of thing will be moved elsewhere long-term 
        print('Possible commands:\ngetNode (gn) moveRobber (mr)')
        return raw_input('')


    def update(self):
        # Update the display
        white = (255, 255, 255)
        self.screen.fill((white))
        self.blitAll()
        pygame.display.flip()


    def placeRoad(self, node1, node2, curPlayer):
        # Place something to mark the node here
        # Assumes that the nodes passed in are valid locations
        # x <=> screen width
        # y <=> screen height
        x11, y11, x12, y12 = self.nodeLocs[(node1.row, node1.col)]
        x21, y21, x22, y22 = self.nodeLocs[(node2.row, node2.col)]
        
        roadToBlit = None
        locToBlit = ((x11 + x21) / 2, (y11 + y21) / 2) 
        if curPlayer.color == 'red':
            roadToBlit = self.redRoad
        elif curPlayer.color == 'orange':
            roadToBlit = self.orangeRoad
        elif curPlayer.color == 'green':
            roadToBlit = self.greenRoad
        else:
            roadToBlit = self.blueRoad
        self.permanentBlits.append((roadToBlit, locToBlit))
        self.update()


    def placeSettlement(self, node, player):
        # Takes in a node object
        print('placing settlement')
        x1, y1, x2, y2 = self.nodeLocs[(node.row, node.col)]
        self.permanentBlits.append((self.getDotForPlayer(player), (x1, y1)))
        self.update()



    def placeCity(self, node, player):
        x1, y1, x2, y2 = self.nodeLocs[(node.row, node.col)]
        self.permanentBlits.append((self.city, (x1, y1)))
        self.update()

    def getTile(self):
        # Returns the (tuple) tile ID of the nearest tile clicked
        tileFound = False
        while True:
            for event in pygame.event.get():
                if event.type == MOUSEBUTTONDOWN:
                    mouseX, mouseY = event.pos
                    tileIndex = np.argmin(np.linalg.norm(np.subtract(tc, (mouseX, mouseY))) for tc in self.tileCenters)
                    return self.board.tileIds[tileIndex] 
        return None

    def getNode(self):
        # Takes in an action and updates the display accordingly
        nodeFound = False
        while True:
            # Loop until they click a node
            for event in pygame.event.get():
                if event.type == MOUSEBUTTONDOWN:
                    mouseX, mouseY = event.pos
                    node = self.getNodeAtXY(mouseX, mouseY)
                
                    if node != None:
                        print('Clicked node ' + str(node))
                        return node
        return None 

    def getDotForPlayer(self, player):
        # Get the dot corresponding to the player's color
        if player.color == 'red':
            return self.redDot
        elif player.color == 'green':
            return self.greenDot
        elif player.color == 'blue':
            return self.blueDot
        else:
            return self.orangeDot 


    # Load some different colored nodes for different player, nodes, etc
    # Four default colors

