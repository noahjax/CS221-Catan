import pygame
from pygame.locals import*
import numpy as np

class Display:
 
    screen = None
    screenWidth, screenHeight = (640, 480)

    dot = None
    tile = None
    robber = None
    
    dotWidth, dotHeight = (None, None) 
    tileWidth, tileHeight = (None, None)
    robberWidth, robberHeight = (None, None)

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
    
    # Store the tempBlits as a dict, since the order etc will be changing
    # As such, these should not need to be printed in any particular order
    tempBlits = {}

    # Store the x, y tuples of each tile center
    # In order of tile index (0-18)
    tileCenters = []

    def __init__(self):
        # Loads:
        # - tiles
        # - nodes
        # - robber
        # Set the member variables storing their sizes.
        pygame.init()

        self.screen = pygame.display.set_mode((self.screenWidth, self.screenHeight))
        self.dot = pygame.image.load('dot.png')
        self.dot = pygame.transform.scale(self.dot, (self.screenWidth / 30, self.screenHeight / 30))
        
        self.tile = pygame.image.load('hex.png')
        self.tile = pygame.transform.scale(self.tile, (self.screenWidth / 8, self.screenHeight / 8))

        self.tileWidth = self.tile.get_rect().size[0]
        self.tileHeight = self.tile.get_rect().size[1]

        self.dotWidth = self.dot.get_rect().size[0]
        self.dotHeight = self.dot.get_rect().size[1]

        # This should happen before loading any temp blits, as tileCenters are initialized here
        self.loadPermanentBlits()
 
        self.robber = pygame.image.load('robber.png')
        self.robber = pygame.transform.scale(self.robber, (self.tileWidth / 2, self.tileHeight / 2))
        self.robberWidth = self.robber.get_rect().size[0]
        self.robberHeight = self.robber.get_rect().size[1]

        self.placeRobber(5) # Just initializing the robber to the 5th tile for now 

    def placeRobber(self, tile):
        # Add the robber to tempBlits at the center of the specified tile
        tx, ty = self.tileCenters[tile]
        self.tempBlits['robber'] = (self.robber, (tx - self.robberWidth / 2, ty - self.robberHeight / 2))

    def loadPermanentBlits(self):    
        # Compute the blit locations of each node and tile
        numTiles = [3, 4, 5, 4, 3]

        offsets = [self.screenWidth / 2 - self.tileWidth * 3 / 2, \
                   self.screenWidth / 2 - self.tileWidth * 2, \
                   self.screenWidth / 2 - self.tileWidth * 5 / 2, \
                   self.screenWidth / 2 - self.tileWidth * 2, \
                   self.screenWidth / 2 - self.tileWidth * 3 / 2]

        # Store the locations of the dots relative to each hexagon
        topDotOffsets = [(-self.dotWidth / 2, self.tileHeight / 5 - self.dotHeight / 2), \
                      (self.tileWidth / 2 - self.dotWidth / 2, -self.dotHeight / 2), \
                      (self.tileWidth - self.dotWidth / 2, self.tileHeight / 5 - self.dotHeight / 2)]
        bottomDotOffsets = [(-self.dotWidth / 2, self.tileHeight * 4 / 5 - self.dotHeight / 2), \
                            (self.tileWidth / 2 - self.dotWidth / 2, self.tileHeight - self.dotHeight / 2), \
                            (self.tileWidth - self.dotWidth / 2, self.tileHeight * 4 / 5 - self.dotHeight / 2)]

        # Store all of the nodes to blit in this list, and add them last so
        # that they will appear in the foreground
        nodesToBlit = []

        for i in range(len(numTiles)):
            
            # We use two counterJ's so that the double-layer of nodes in the middle tiles can be 
            # handled at the same time
            counterJTop = 0
            counterJBot = 0
            for j in range(numTiles[i]):
                # Place the j tiles
                imgX = j * self.tileWidth + offsets[i]
                imgY = i * self.tileHeight * 4 / 5 + self.screenWidth / 7
                self.tileCenters.append((imgX + self.tileWidth / 2, imgY + self.tileHeight / 2)) 
                self.permanentBlits.append((self.tile, (imgX, imgY)))
                
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

        
    def getNodeAtXY(self, x, y):
        # If a node is at the coordinates x, y, return the coordinates of the node in the game logic
        # Return None if no node is at the specified coords
        for coords, minmaxTuple in self.nodeLocs.iteritems():
            if minmaxTuple[0] <= x <= minmaxTuple[2] and minmaxTuple[1] <= y <= minmaxTuple[3]:
                return coords
        return None

    def handleClick(self, event, playerCommand):
        if event.button == 1:
            if playerCommand == 'getNode':
                mouseX, mouseY = event.pos
                node = self.getNodeAtXY(mouseX, mouseY)
                
                if node != None:
                    print('clicked node ' + str(node))
                    #TODO: what do we want to do once we have the node?

                else:
                    raise Exception('No node clicked. Unspecified behaviour')
            elif playerCommand == 'moveRobber':
                # Get the nearest tile to the clicked point, and send the robber there
                destTile = np.argmin([np.linalg.norm(np.subtract(event.pos, tc)) for tc in self.tileCenters])
                self.placeRobber(destTile)
        
    def blitAll(self):
        # Blit all available objects to the screen
        # Currently blits all objects in 
        # - permanentBlits
        # - tempBlits 
        for blit in (self.permanentBlits + self.tempBlits.values()):
            self.screen.blit(blit[0], blit[1])

    def getUserCommand(self):
        # Put some kinds of possible commands in here at the moment
        # I'm guessing that this kind of thing will be moved elsewhere long-term 
        print('Possible commands:\ngetNode\nmoveRobber')
        return raw_input('')

    def run(self):
        white = (255, 255, 255)
        running = True 
        while running:
            self.screen.fill((white))
            self.blitAll()
            pygame.display.flip()
            
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False 
                elif event.type == MOUSEBUTTONDOWN:
                    command = self.getUserCommand()
                    self.handleClick(event, command)

# Test the Display class
display = Display()
display.run()



