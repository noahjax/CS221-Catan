
class Board:
    
    nodes = {0 : [None] * 7,
             1 : [None] * 9,
             2 : [None] * 11,
             3 : [None] * 11,
             4 : [None] * 9,
             5 : [None] * 7}
  
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
        pass
