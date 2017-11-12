import pygame
from pygame.locals import*

class Display:
 
    screen = None
    screenWidth, screenHeight = (640, 480)

    dot = None
    tile = None

    dotWidth, dotHeight = (None, None) 
    tileWidth, tileHeight = (None, None)
    
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
    tempBlits = []

    def __init__(self):
        # Load the screen, dot, and tile pngs
        # Set the member variables storing their sizes.
        pygame.init()

        self.screen = pygame.display.set_mode((self.screenWidth, self.screenHeight))
        self.dot = pygame.image.load('dot.png')
        dotSize = self.dot.get_rect().size
        self.dot = pygame.transform.scale(self.dot, (dotSize[0] / 25, dotSize[1] / 25))
        
        self.tile = pygame.image.load('hex.png')
        self.tile = pygame.transform.scale(self.tile, (self.screenWidth / 8, self.screenHeight / 8))

        self.tileWidth = self.tile.get_rect().size[0]
        self.tileHeight = self.tile.get_rect().size[1]

        self.dotWidth = self.dot.get_rect().size[0]
        self.dotHeight = self.dot.get_rect().size[1]

        self.loadPermanentBlits()
        
    def loadPermanentBlits(self):    
        # Compute the location to blit each tile and each node
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
                
        for s in sorted(self.nodeLocs.keys()):
            print(s)
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

    def handleClick(self, event):
        if event.button == 1:
            # The left button was clicked
            mouseX, mouseY = event.pos
            node = self.getNodeAtXY(mouseX, mouseY)
            
            if node != None:
                print('clicked node ' + str(node))
                #TODO: what do we want to do once we have the node?

            else:
                raise Exception('No node clicked. Unspecified behaviour')

    def blitAll(self):
        # Blit all available objects to the screen
        # Currently blits all objects in 
        # - permanentBlits
        # - tempBlits 
        for blit in (self.permanentBlits + self.tempBlits):
            self.screen.blit(blit[0], blit[1])

    def run(self):
        white = (255, 255, 255)
        running = True 
        while running:
            # Not sure if this saves any processing time, but I think we want some way to
            # pause this loop while the AI players are executing their turns. Otherwise, there
            # could be a lot of extra iterations that don't do anything
            # raw_input('Press enter on user\'s turn') 
            self.screen.fill((white))
            self.blitAll()
            pygame.display.flip()
           
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False 
                elif event.type == MOUSEBUTTONDOWN:
                    self.handleClick(event)

            # raw_input('Press enter when turn is ended')


# Test the Display class
# display = Display()
# display.run()



