
class Board:
    
    '''
    class Board:
    ------------
    Our board is a pointy-topped hexagonal grid with rows of size [3, 4, 5, 4, 3]
    Coordinates are defined by x, y, z axis.
    Moving in the Northeast or Southwest directions holds y constant,
    moving in the Northwest or Southeast directions holds x constant,
    moving in the East or West directions holds z constant.
    '''

    # We define the cumulative indices stored in each row for easy access by tile index
    rowMaxIndices = [3, 7, 12, 16, 19]

    def __init__(self):
        self.board = {0 : [None] * 3,
                      1 : [None] * 4,
                      2 : [None] * 5,
                      3 : [None] * 4,
                      4 : [None] * 3}

        self.intersections = {0 : [None] * 2,
                              1 : [None] * 7,
                              2 : [None] * 9,
                              3 : [None] * 9,
                              4 : [None] * 7,
                              5 : [None] * 2}


        # Note that edges are stored in separate dictionaries depending on their orientation.
        # They will likely be most useful in finding the edges between two tiles, rather than 
        # referencing them explicitly.
        self.verticalEdges = {0 : [None] * 2,
                              1 : [None] * 3,
                              2 : [None] * 4,
                              3 : [None] * 3,
                              4 : [None] * 2}
        
        self.horizontalEdges = {0 : [None] * 6,
                                1 : [None] * 8,
                                2 : [None] * 8,
                                3 : [None] * 6}

    def setAllEdges(self, val):
        '''
        Method: setAllEdges
        -------------------
        Sets all horizontal and vertical edges to a single value.
        Primarily for initialization and testing, as we will update single
        edges within the game.
        '''
        for key in self.verticalEdges.keys():
            for i in range(len(self.verticalEdges[key])):
                self.verticalEdges[key][i] = val
        for key in self.horizontalEdges.keys():
            for i in range(len(self.horizontalEdges[key])):
                self.horizontalEdges[key][i] = val

    
    def printEdges(self):
        '''
        Method: printEdges
        ------------------
        Print all vertical edges, followed by all horizontal edges.
        '''
        for key in self.verticalEdges.keys():
            s = ''
            for elem in self.verticalEdges[key]:
                s += (str(elem) + ' ')
            print(s)
       
        for key in self.horizontalEdges.keys():
            s = ''
            for elem in self.horizontalEdges[key]:
                s += (str(elem) + ' ')
            print(s)


    def printBoard(self):
        '''
        Method: printBoard
        ------------------
        Helper for debugging. Prints the value stored at each tile index.
        '''
        for i in range(19):
            r, c = self.getPieceCoords(i)
            if self.inBounds(r, c):
                print(self.board[r][c])
                pass

    def setPiece(self, index, val):
        '''
        Method: setPiece
        ----------------
        Set the piece at the given index equal to val.
        '''
        r, c = self.getPieceCoords(index)
        if self.inBounds(r, c):
            self.board[r][c] = val
        else:
            raise Exception('Index ' + str(index) + ' to set is not in bounds')
  

    def setEdgeBetween(self, indexOne, indexTwo, val):
        '''
        Method: setEdgeBetween
        ----------------------
        Set the edge between the specified indices, or raise an exception if no such
        edge exists.
        '''
        coordsOne = self.getPieceCoords(indexOne)
        coordsTwo = self.getPieceCoords(indexTwo)
        if coordsOne[0] == coordsTwo[0]:
            if abs(coordsOne[1] - coordsTwo[1]) != 1:
                raise Exception('Pieces are not adjoining')
            else:
                self.verticalEdges[coordsOne[0], min(coordsOne[1], coordsTwo[1])] = val
        elif abs(coordsOne[0] - coordsTwo[0]) == 1:
            if abs(coordsOne[1] - coordsTwo[1]) > 1:
                raise Exception('Pieces are not adjoining')
            else:   
                self.horizontalEdges[min(coordsOne[0], coordsTwo[0]), max(coordsOne[1], coordsTwo[1])] = val
        else:
            raise Exception('Edge could not be set') 


    def getEdgeBetween(self, indexOne, indexTwo):
        '''
        Method: getEdgeBetween
        ----------------------
        Returns an edge object between two tiles, specified by their indices, or raise an 
        exception if no such edge exists.
        '''
        coordsOne = getPieceCoords(indexOne)
        coordsTwo = getPieceCoords(indexTwo)
        if coordsOne[0] == coordsTwo[0]:
            # The tiles are in the same row, so the edge will be vertical
            if abs(coordsOne[1] - coordsTwo[1]) != 1:
                raise Exception('Pieces are not adjoining')
            else:
                return self.verticalEdges[coordsOne[0], min(coordsOne[1], coordsTwo[1])]
        elif abs(coordsOne[0] - coordsTwo[0]) == 1:
            # They are in adjoining rows, so the edges will be horizontal
            if abs(coordsOne[1] - coordsTwo[1]) > 1:
                raise Exception('Pieces are not adjoining')
            else:
                return self.horizontalEdge[min(coordsOne[0], coordsTwo[0]), max(coordsOne[1], coordsTwo[1])]

        else:   
            return None


    def inBounds(self, r, c):
        return r >= 0 and c >= 0 \
               and r < len(self.board.keys()) \
               and c < len(self.board[r])


    def getNeighbors(self, index):
        '''
        Method: getNeighbors
        --------------------
        Return a list of all objects stored at point neighboring the given tile index.
        '''
        neighborCoords = self.getNeighborCoords(index)
        neighbors = []
        for r, c in neighborCoords:
            neighbors.append(self.board[r][c])
        return neighbors


    def getNeighborCoords(self, index):
        '''
        Method: getNeighborCoords
        -------------------------
        Returns a list of all coordinates of objects stored at neighboring points in 
        self.board (according to the layout of a Catan board). Ports are not included at the moment.
        '''
        
        # All possible modifications we could make to our coordinates to get neighboring coordinates
        # Many of these may be out of bounds
        deltas = [(0, 1), (1, 0), (1, -1), (0, -1), (-1, -1), (-1, 1)]
        
        r, c = self.getPieceCoords(index)
        neighborCoords = [] 
        for delta in deltas:
            dr = r + delta[0]
            dc = c + delta[1]
            if self.inBounds(dr, dc):
               neighborCoords.append((dr, dc)) 
        
        return neighborCoords


    def getPiece(self, index):
        '''
        Method: getPiece
        ----------------
        The primary access method for a player trying reference a piece on the board.
        We define indices to be [0, 19), starting in the top left and proceeding down
        row by row on the game board.

        Returns the element stored at that position in the board, assumably of type Tile 
        '''
        row = self.__getRow__(index)
        rowPos = self.__getRowPos__(index, row)
        return self.board[row][rowPos]

    def getPieceCoords(self, index):
        '''
        Method: getPieceCoords
        ----------------------
        Use to get the coordinates for a piece index in the board. Probably will primarily be
        a helper method for other code.
        '''
        row = self.__getRow__(index)
        rowPos = self.__getRowPos__(index, row)
        return row, rowPos


    def __getRow__(self, index):
        for i in range(5):
            if index < self.rowMaxIndices[i]: 
                return i 
        return -1

    def __getRowPos__(self, index, row):
        if row - 1 >= 0:
            return index - self.rowMaxIndices[row - 1]
        else:
            return index 
