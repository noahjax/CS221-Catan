import pygame
from pygame.locals import*
# import numpy as np
import board as bd 

class Display:
 
    screen = None
    screenWidth, screenHeight = (640, 480)

    dot = None
    tile = None
    robber = None
    tlbrRoad = None
    trblRoad = None
    lrRoad = None

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
        
        # Load the node png
        self.dot = pygame.image.load('dot.png')
        self.dot = pygame.transform.scale(self.dot, (int(self.screenWidth / 25), int(self.screenHeight / 25)))

        # Load the city and town pngs
        self.city = pygame.image.load('castle.png')
        self.city = pygame.transform.scale(self.city, (self.screenWidth / 25, self.screenHeight / 25))

        self.town = pygame.image.load('town.png')
        self.town = pygame.transform.scale(self.town, (self.screenWidth / 25, self.screenHeight / 25))

        # Load a hexagon to use as a tile
        self.tile = pygame.image.load('hex.png')
        self.tile = pygame.transform.scale(self.tile, (int(self.screenWidth / 8), int(self.screenHeight / 8)))

        # Set some variables to reference later on
        self.tileWidth = self.tile.get_rect().size[0]
        self.tileHeight = self.tile.get_rect().size[1]

        self.dotWidth = self.dot.get_rect().size[0]
        self.dotHeight = self.dot.get_rect().size[1]


        # Load the three different road orientations
        self.tlbrRoad = pygame.image.load('tlbr.png')
        self.tlbrRoad = pygame.transform.scale(self.tile, (self.tileWidth / 2, self.tileHeight / 2))
        
        self.trblRoad = pygame.image.load('trbl.png')
        self.trblRoad = pygame.transform.scale(self.tile, (self.tileWidth / 2, self.tileHeight / 2))
        
        self.lrRoad = pygame.image.load('lr.png')
        self.lrRoad = pygame.transform.scale(self.tile, (self.tileWidth / 2, self.tileHeight / 2))
        # This should happen before loading any temp blits, as tileCenters are initialized here
        self.loadPermanentBlits()

        self.roadWidth = self.lrRoad.get_rect().size[0]
        self.roadHeight = self.lrRoad.get_rect().size[1]

        # Load the robber
        self.robber = pygame.image.load('robber.png')
        self.robber = pygame.transform.scale(self.robber, (int(self.tileWidth / 2), int(self.tileHeight / 2)))
        self.robberWidth = self.robber.get_rect().size[0]
        self.robberHeight = self.robber.get_rect().size[1]

        self.placeRobber(robberTile) 




    def placeRobber(self, tile):
        # Add the robber to tempBlits at the center of the specified tile
        tx, ty = self.tileCenters[tile]
        self.tempBlits['robber'] = (self.robber, (tx - int(self.robberWidth / 2), ty - int(self.robberHeight / 2)))




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
                        nodesToBlit.append((self.dot, (dotX, dotY)))
                        coords = (i, counterJTop) 
                        self.nodeLocs[coords] = (dotX, dotY, dotX + self.dotWidth, dotY + self.dotHeight)
                        counterJTop += 1
                if i >= 2:
                    # Place nodes along the bottom of the corresponding tile
                    for offset in bottomDotOffsets[:dotRange]:
                        dotX = imgX + offset[0]
                        dotY = imgY + offset[1]
                        nodesToBlit.append((self.dot, (dotX, dotY)))
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




    def placeRoad(self, node1, node2):
        # Place something to mark the node here
        # Assumes that the nodes passed in are valid locations
        print('Placing road')
        x11, y11, x12, y12 = self.nodeLocs[(node1.row, node1.col)]
        x21, y21, x22, y22 = self.nodeLocs[(node2.row, node2.col)]
        
        startNodeCenter = ((x11 + x12) / 2, (y11 + y12) / 2)

        roadToBlit = None
        locToBlit = (startNodeCenter[0], startNodeCenter[1] - self.roadWidth / 2)
        # Determine which road we should use
        if node1.col == node2.col and node1.row != node2.row:
            ### | ###
            roadToBlit = self.lrRoad
        elif node1.col < node2.col:
            if y11 < y21:
                ### / ###
                roadToBlit = self.tlbrRoad
            elif y11 > y21:
                ### \ ###
                roadToBlit = self.trblRoad
        assert roadToBlit is not None
        self.permanentBlits.append((roadToBlit, locToBlit))
        self.update()

    def placeSettlement(self, node):
        # Takes in a node object
        x1, y1, x2, y2 = self.nodeLocs[(node.row, node.col)]
        self.permanentBlits.append((self.town, (x1, y1)))
        self.update()




    def placeCity(self, node):
        x1, y1, x2, y2 = self.nodeLocs[node]
        self.permanentBlits.append((self.city, (x1, y1)))
        self.update()




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
                        print('clicked node ' + str(node))
                        return node
        return None 






    # Load some different colored nodes for different player, nodes, etc
    # Four default colors

