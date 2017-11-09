import pygame
from pygame.locals import*

white = (255, 255, 255)
screenWidth = 640
screenHeight = 480

pygame.init()

screen = pygame.display.set_mode((screenWidth, screenHeight))
screen.fill((white))

dot = pygame.image.load('dot.png')
dotSize = dot.get_rect().size
dot = pygame.transform.scale(dot, (dotSize[0] / 25, dotSize[1] / 25))

tile = pygame.image.load('hex.png')
tile = pygame.transform.scale(tile, (screenWidth / 8, screenHeight / 8))

tileWidth = tile.get_rect().size[0]
tileHeight = tile.get_rect().size[1]

dotWidth = dot.get_rect().size[0]
dotHeight = dot.get_rect().size[1]

def loadNodesAndTiles():    
    
    numTiles = [3, 4, 5, 4, 3]

    offsets = [screenWidth / 2 - tileWidth * 3 / 2, \
               screenWidth / 2 - tileWidth * 2, \
               screenWidth / 2 - tileWidth * 5 / 2, \
               screenWidth / 2 - tileWidth * 2, \
               screenWidth / 2 - tileWidth * 3 / 2]

    # Store the locations of the dots relative to each hexagon
    dotOffsets = [(-dotWidth / 2, tileHeight / 5 - dotHeight / 2), \
                  (tileWidth / 2 - dotWidth / 2, -dotHeight / 2), \
                  (tileWidth - dotWidth / 2, tileHeight / 5 - dotHeight / 2)]
    bottomDotOffsets = [(-dotWidth / 2, tileHeight * 4 / 5 - dotHeight / 2), \
                        (tileWidth / 2 - dotWidth / 2, tileHeight - dotHeight / 2), \
                        (tileWidth - dotWidth / 2, tileHeight * 4 / 5 - dotHeight / 2)]

    # Iterate through each row in the board to set the tiles
    # For the first n - 1 rows of dots, we place the dot relative to the top of the hexagon
    for i in range(len(numTiles)):
        for j in range(numTiles[i]):
            imgX = j * tileWidth + offsets[i]
            imgY = i * tileHeight * 4 / 5 + screenWidth / 7
            screen.blit(tile, (imgX, imgY))
            if j == numTiles[i] - 1:
                # We only place all three dots if we are on the last tile
                # Otherwise we will be double counting the dots on intersections
                dotRange = 3 
            else:
                dotRange = 2 
            for offset in dotOffsets[:dotRange]:
                screen.blit(dot, (imgX + offset[0], imgY + offset[1]))
            
            if i == len(numTiles) - 1:
                # For the last row of dots, we also place the dots relative to the bottom of the last hexagons
                for offset in bottomDotOffsets[:dotRange]:
                    screen.blit(dot, (imgX + offset[0], imgY + offset[1]))


def displayAll():
    running = True 
    while running:
        screen.fill((white))
        loadNodesAndTiles()
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False 

def main():
    displayAll()

if __name__ == '__main__':
    main()
