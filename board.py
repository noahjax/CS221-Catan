from node import *

class Board:
    
    nodes = {0 : [Node(0, i) for i in range(7)],
             1 : [Node(1, i) for i in range(9)],
             2 : [Node(2, i) for i in range(11)],
             3 : [Node(3, i) for i in range(11)],
             4 : [Node(4, i) for i in range(9)],
             5 : [Node(5, i) for i in range(7)]}
  
    def inBounds(self, tup):
        return tup[0] >= 0 and tup[0] < len(self.nodes.keys()) and tup[1] >= 0 and tup[1] < len(self.nodes[tup[0]])

    def getNode(self, r, c):
        return self.nodes[r][c]

    def getNeighborNodes(self, r, c):
        if c % 2 == 0:
            neighbors = [(r, c - 1), (r, c + 1), (r + 1, c + 1)]
        else:
            neighbors = [(r - 1, c - 1), (r, c - 1), (r, c + 1)] 
        inBoundsNeighbors = []
        for n in neighbors:
            if self.inBounds(n):
                inBoundsNeighbors.append(n)
        return inBoundsNeighbors
        
    def __init__(self):
        pass

class Tile:

    def __init__(self, resource, value, has_robber):
        self.resource = resource
        self.value = value
        self.hasRobber = has_robber



