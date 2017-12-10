import numpy as np
import pygame
from pygame.locals import *

# Turn off when training
DISPLAY_ON = True

class Display:
    
    colors = {'green': (16, 124, 16), 'blue': (0, 0, 231), 'orange': (243, 87, 40), 'red': (241, 0, 0)}

    screen = None
    screenWidth, screenHeight = (640, 480)
    # screenWidth, screenHeight = (1280, 960)

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
    # 'name' : (img, (blitAtX, blitAtY))
    tempBlits = {}

    # Store the x, y tuples of each tile center
    # In order of tile index (0-18)
    tileCenters = []
    
    # The font in which text should be displayed
    font = None
    
    def __init__(self, board, robberTile):
        if not DISPLAY_ON: return None

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
        self.displayOn = False
        
        self.font = pygame.font.SysFont('../res/Comic Sans MS', 80)

        self.screen = pygame.display.set_mode((self.screenWidth, self.screenHeight))
        self.roadsToDraw = [] 

        # Dots on dots on dots on dots on dots on ... 
        self.redDot = pygame.image.load('../res/red_dot.png')
        self.redDot = pygame.transform.scale(self.redDot, (int(self.screenWidth / 25), int(self.screenHeight / 25)))
        
        self.blueDot = pygame.image.load('../res/blue_dot.png')
        self.blueDot = pygame.transform.scale(self.blueDot, (int(self.screenWidth / 25), int(self.screenHeight / 25)))
        
        self.greenDot = pygame.image.load('../res/green_dot.png')
        self.greenDot = pygame.transform.scale(self.greenDot, (int(self.screenWidth / 25), int(self.screenHeight / 25)))
        
        self.orangeDot = pygame.image.load('../res/orange_dot.png')
        self.orangeDot = pygame.transform.scale(self.orangeDot, (int(self.screenWidth / 25), int(self.screenHeight / 25)))
        
        self.blackDot = pygame.image.load('../res/black_dot.png')
        self.blackDot = pygame.transform.scale(self.blackDot, (int(self.screenWidth / 25), int(self.screenHeight / 25)))

        self.whiteDot= pygame.image.load('../res/white_dot.png')
        self.whiteDot = pygame.transform.scale(self.whiteDot, (int(self.screenWidth / 25), int(self.screenHeight / 25)))

        # Load the city and town pngs
        self.city = pygame.image.load('../res/city.png')
        self.city = pygame.transform.scale(self.city, (self.screenWidth / 38, self.screenHeight / 38))

        # self.town = pygame.image.load('../res/town.png')
        # self.town = pygame.transform.scale(self.town, (self.screenWidth / 25, self.screenHeight / 25))

        # self.tile = pygame.image.load('../res/hex.png')
        # self.tile = pygame.transform.scale(self.tile, (int(self.screenWidth / 8), int(self.screenHeight / 8)))
        self.resourceTiles = {}
        self.resourceTiles['Wood'] = pygame.image.load('../res/wood.png')
        self.resourceTiles['Grain'] = pygame.image.load('../res/grain.png')
        self.resourceTiles['Ore'] = pygame.image.load('../res/ore.png')
        self.resourceTiles['Wool'] = pygame.image.load('../res/wool.png')
        self.resourceTiles['Brick'] = pygame.image.load('../res/brick.png')
        self.resourceTiles['Desert'] = pygame.image.load('../res/desert.png')

        for resource, unscaled in self.resourceTiles.items():
            self.resourceTiles[resource] = pygame.transform.scale(unscaled, (int(self.screenWidth / 8), int(self.screenHeight / 8)))
 
        # Set some variables to reference later on
        self.tileWidth = int(self.screenWidth / 8) 
        self.tileHeight = int(self.screenHeight / 8) 
        self.background = pygame.image.load('../res/water.png')
        self.background = pygame.transform.scale(self.background, (self.screenWidth, self.screenHeight))
      
        self.dotWidth = self.redDot.get_rect().size[0]
        self.dotHeight = self.redDot.get_rect().size[1]

        # This should happen before loading any temp blits, as tileCenters are initialized here
        self.loadPermanentBlits()

        # Load the robber
        self.robber = pygame.image.load('../res/robber.png')
        self.robber = pygame.transform.scale(self.robber, (int(self.tileWidth / 2), int(self.tileHeight / 2)))
        self.robberWidth = self.robber.get_rect().size[0]
        self.robberHeight = self.robber.get_rect().size[1]

        self.placeRobber(robberTile) 

    def placeRobber(self, node):
        if not DISPLAY_ON: return
        # Add the robber to tempBlits at the center of the specified tile
        x, y, z, w = self.nodeLocs[node]
        self.tempBlits['Robber'] = (self.robber, (x - self.dotWidth / 2, y + int(self.tileHeight / 2) - self.dotHeight / 2))
        self.update()


    def getTileTextSurface(self, tile):
        if not DISPLAY_ON: return
        # Returns a surface containing the resource, value string of the given tile
        # text = str(tile.resource) + ' ' + str(tile.value)
        text = str(tile.value)
        textSurface = self.font.render(text, False, (255, 255, 255))
        # Scale according to the size of the tiles
        textSurface = pygame.transform.scale(textSurface, (int(self.tileWidth * 2 / 5), int(self.tileWidth / 4)))
        return textSurface
    
    def getResourceTile(self, tile):
        if not DISPLAY_ON: return
        return self.resourceTiles[tile.resource]

    def getStatsTextSurface(self, player):
        text = 'Wood: %s - Grain: %s - Brick: %s - Ore: %s - Wool: %s' % \
                (player.resources['Wood'],
                 player.resources['Grain'],
                 player.resources['Brick'],
                 player.resources['Ore'],
                 player.resources['Wool'])
        textSurface = self.font.render(text, False, (0, 0, 0))
        textSurface = pygame.transform.scale(textSurface, (int(self.screenWidth), int(self.screenHeight / 15)))
        return textSurface

    
    def loadPermanentBlits(self):    
        if not DISPLAY_ON: return

        # Add the background first, so that it appears behind everything else
        self.permanentBlits.append((self.background, (0, 0)))

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
                # self.permanentBlits.append((self.tile, (imgX, imgY)))
    
                # Display the type of the tile inside the hexagon
                tile = self.board.tiles[counterTile]
                self.permanentBlits.append((self.getResourceTile(tile), (imgX, imgY)))

                text = self.getTileTextSurface(tile)
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
                        nodesToBlit.append((self.whiteDot, (dotX, dotY)))
                        coords = (i, counterJTop) 
                        self.nodeLocs[coords] = (dotX, dotY, dotX + self.dotWidth, dotY + self.dotHeight)
                        counterJTop += 1
                if i >= 2:
                    # Place nodes along the bottom of the corresponding tile
                    for offset in bottomDotOffsets[:dotRange]:
                        dotX = imgX + offset[0]
                        dotY = imgY + offset[1]
                        nodesToBlit.append((self.whiteDot, (dotX, dotY)))
                        coords = (i + 1, counterJBot)
                        self.nodeLocs[coords] = (dotX, dotY, dotX + self.dotWidth, dotY + self.dotHeight)
                        counterJBot += 1
                
        # Now we add the nodes to self.permanentBlits, so that they will appear after the tiles
        for n in nodesToBlit:
            self.permanentBlits.append(n)
       
        # print('done in init')


    def getNodeAtXY(self, x, y):
        if not DISPLAY_ON: return
        # If a node is at the coordinates x, y, return the coordinates of the node in the game logic
        # Return None if no node is at the specified coords
        for coords, minmaxTuple in self.nodeLocs.iteritems():
            if minmaxTuple[0] <= x <= minmaxTuple[2] and minmaxTuple[1] <= y <= minmaxTuple[3]:
                return coords
        return None


    def blitAll(self):
        if not DISPLAY_ON: return
        # Blit all available objects to the screen
        # Currently blits all objects in 
        # - permanentBlits
        # - tempBlits 
        # for rd in self.roadsToDraw:
        #    pygame.draw.line(rd[0], rd[1], rd[2], rd[3], rd[4])
        for blit in (self.permanentBlits + list(self.tempBlits.values())):
            self.screen.blit(blit[0], blit[1])


    def getUserAction(self):
        if not DISPLAY_ON: return
        # Put some kinds of possible commands in here at the moment
        # I'm guessing that this kind of thing will be moved elsewhere long-term 
        print('Possible commands:\ngetNode (gn) moveRobber (mr)')
        return raw_input('')

    def update(self):
        if not DISPLAY_ON: return
        # Update the display
        white = (255, 255, 255)
        self.screen.fill((white))
        self.blitAll()
        for rd in self.roadsToDraw:
            pygame.draw.line(rd[0], rd[1], rd[2], rd[3], rd[4])

        # Hacky workaround to get cities to show up on top
        for blit in self.permanentBlits:
            if blit[0] == self.city:
                self.screen.blit(blit[0], blit[1])
        pygame.display.flip()


    def placeRoad(self, node1, node2, curPlayer):
        if not DISPLAY_ON: return
        # Place something to mark the node here
        # Assumes that the nodes passed in are valid locations
        # x <=> screen width
        # y <=> screen height
        x11, y11, x12, y12 = self.nodeLocs[(node1.row, node1.col)]
        x21, y21, x22, y22 = self.nodeLocs[(node2.row, node2.col)]
        self.roadsToDraw.append((self.screen, self.colors[curPlayer.color], \
                                (x11 + self.dotWidth / 2, y11 + self.dotHeight / 2), (x21 + self.dotWidth / 2, y21 + self.dotHeight / 2), 5))
        self.update()

    def placeSettlement(self, node, player):
        if not DISPLAY_ON: return
        # Takes in a node object
        # print('placing settlement')
        x1, y1, x2, y2 = self.nodeLocs[(node.row, node.col)]
        self.permanentBlits.append((self.getDotForPlayer(player), (x1, y1)))
        self.update()



    def placeCity(self, node, player):
        if not DISPLAY_ON: return
        x1, y1, x2, y2 = self.nodeLocs[(node.row, node.col)]
        self.permanentBlits.append((self.city, (x1 + self.city.get_rect().size[0] / 4, y1 + self.city.get_rect().size[1] / 4)))
        # self.permanentBlits.append((self.city, (x1, y1)))
        self.update()

    def getTile(self):
        if not DISPLAY_ON: return
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
        if not DISPLAY_ON: return
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
        if not DISPLAY_ON: return
        # Get the dot corresponding to the player's color
        if player.color == 'red':
            return self.redDot
        elif player.color == 'green':
            return self.greenDot
        elif player.color == 'blue':
            return self.blueDot
        else:
            return self.orangeDot 

    def printPlayerStats(self, player):
        if not DISPLAY_ON: return
        print('ppstats')
        stats = self.getStatsTextSurface(player)         
        self.tempBlits['Player stats'] = stats, (0, int(self.screenHeight - (self.screenHeight / 15)))
        self.update()

