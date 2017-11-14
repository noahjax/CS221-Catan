"""
This is the node class which deals with the intersections
of any tile in the board. It will be the primary point
for functionality in the game.
"""
class Node:
    def __init__(self, row, col):
        self.row = row
        self.col = col
        self.touchingTiles = []
        self.neighbours = []
        self.isOccupied = False
        self.occupyingPiece = None


    def get_occupying_piece(self):
        return self.occupyingPiece

    def is_occupied(self):
        return self.isOccupied

    def get_tiles(self):
        return self.touchingTiles

    def set_occupying_piece(self, piece):
        self.isOccupied = True
        self.occupyingPiece = piece

    def set_neighbours(self, board):
        neighbours = board.getNeighborNodes(self.row, self.col)
        toSet = []
        for coord in neighbours:
            toSet.append(board.nodes[coord[0]][coord[1]])
        self.neighbours = toSet
        