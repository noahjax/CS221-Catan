
class Board:
    
    nodes = {0 : [None] * 7,
             1 : [None] * 9,
             2 : [None] * 11,
             3 : [None] * 11,
             4 : [None] * 9,
             5 : [None] * 7}
  
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
