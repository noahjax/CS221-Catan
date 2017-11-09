
class Board:
  
    def inBounds(self, node):
        return node[0] >= 0 and node[0] < len(self.nodes.keys()) and node[1] >= 0 and node[1] < len(self.nodes[node[0]])

    def getNode(self, node):
        r, c = node
        return self.nodes[r][c]

    def getNeighborNodes(self, node):
        r, c = node
        if c % 2 == 0:
            neighbors = [(r, c - 1), (r, c + 1), (r + 1, c + 1)]
        else:
            neighbors = [(r - 1, c - 1), (r, c - 1), (r, c + 1)] 
        inBoundsNeighbors = []
        for n in neighbors:
            if self.inBounds(n):
                inBoundsNeighbors.append(n)
        return inBoundsNeighbors

    def getNeighborEdges(self, edge):
        one = edge[0]
        two = edge[1]
        nOne = self.getNeighborNodes(one)
        nTwo = self.getNeighborNodes(two)
        nEdgesOne = [(one, n) for n in nOne]
        nEdgesTwo = [(two, n) for n in nTwo]
        return nEdgesOne + nEdgesTwo 

    def __init__(self):
        self.nodes = {0: [Node(0, i) for i in range(7)],
                       1: [Node(1, i) for i in range(9)],
                       2: [Node(2, i) for i in range(11)],
                       3: [Node(3, i) for i in range(11)],
                       4: [Node(4, i) for i in range(9)],
                       5: [Node(5, i) for i in range(7)]}


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
        self.neighbours = board.getNeighborNodes(self.row, self.col)



