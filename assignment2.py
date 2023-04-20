from csp import CSP, UniversalDict

"""
Returns True if constraint pass
A = cell1 (string)
B = cell2 (string) 
a = cell1[domain] (where domain = {1} or {0}
b = cell2[domain]
"""


'''
A function f(A, a, B, b) that returns true if neighbors
    A, B satisfy the constraint when they have values A=a, B=b
    
    Any variable that shares a row, column, or diagonal with a given variable would be a neighbor,
     as placing a star in the given variable would restrict the placement of stars in its neighbors.
'''
def star_constraint(A, a, B, b):
    # reject same row
    if A[0] == B[0]:
        return False

    # reject same column
    if A[1] == B[1]:
        return False

    # TOOD: THIS NEEDS TO BE TESTED
    # are A and B at least 1 cell apart?
    # no sqrt fn: we just call a 0.5 exponent
    # this is called the 'Euclidean distance'
    if pow(0.5,
           pow(2,(A[0] - B[0]) + pow(2,A[1] - B[1]))
           ) < 1:
        return False

    return True


# imported from RushHour
def readPuzzleFromFile(fileName):
    infile = open(fileName, "r")
    grid = []
    for line in infile:
        # TODO: ensure the line is safe (only contains A-Z chars)
        dataLine = line
        if dataLine[0] == '#':  # Comment line starts from column 0 with # in that column; skip these lines
            continue
        data = dataLine.split()
        columns = []
        for i in data:
            for n in i:
                columns.append(n)
        grid.append(columns)
    infile.close()
    return grid


class StarBattle(CSP):
    """
    Problem of type CSP
    """

    '''
    From professor:
    'if a row is your variable, then every element of that domain for that variable 
    should specify the row completely; I.e., for a 5 puzzle, something like [-,-,-,-,*]'
    
    this means that instead of removing a value from a domain, we'd mark the entry with 
    '-' (0) or '*' (1) when marking a cell as having a star 
    '''

    vars, board = [], []
    domains = {}
    neighbors = {}

    def __init__(self, fileName):
        """Initialize data structures for n stars"""

        # build the board state so we can set up {vars}
        self.board = readPuzzleFromFile(fileName)
        self.vars = []
        for row in self.board:
            self.vars.append(row)

        # we still have `board` that we can use
        domains = ['-' for x in self.vars]

        # prepare neighbors
        neighbors = {}
        for row_index, row in enumerate(self.vars):
            neighbors[row_index] = {}  #empty dict for this variable

            for col_index, cell in enumerate(row):
                neighbors[row_index][col_index] = []  # create empty list

        neighbors = self.findNeighbors()

        CSP.__init__(self, self.vars, domains, neighbors, star_constraint)

    def findNeighbors(self):
        '''
        consider all other row and column variables, and exclude the cells that already
        have stars placed in them in those variables from the domain of each row variable.
        '''
        all_neighbors = []
        # loop through all the variables to build each set of neighbors

        for row_index, row in enumerate(self.vars):  # for each ['A','B','B','B','C'] in the board:
            # for each cell in this row...
            for cell_index, cell_value in enumerate(row):

                # if a cell contains part of a shape also belonging to a shape in the current 'row':
                if (row_index != cell_index) and any(cell in cell_value for cell in row):
                    all_neighbors.append(row_index)
                #add the current row to the list of neighbors



        '''
        columns relating to A would be:
        column_0 = [row[0] for row in self.board] # may be 'vars' not board?
        newlist = [expression for item in iterable if condition == True]
        '''


        # the neighbors
        # set the KEY in neighbors to be the ROW
        # e.g if on row 1: neighbors[1] = [0, 2]
        for col in self.board[row]:
            # retrieve positions from board
            current_neighbors = self.getAdjacentCells(row, self.board[row])

            # add this row's neighbors to the master list
            all_neighbors.extend(current_neighbors)

        return all_neighbors


    def getAdjacentCells(self, row, col):

        # TODO: this can be cleaned up later
        up_cell = {row, col + 1}
        down_cell = {row, col - 1}
        left_cell = {row - 1, col}
        right_cell = {row + 1, col}

        upper_left_cell = {row - 1, col + 1}
        upper_right_cell = {row + 1, col + 1}
        lower_left_cell = {row - 1, col - 1}
        lower_right_cell = {row + 1, col - 1}

        return {up_cell, down_cell, right_cell, left_cell,
                 upper_left_cell, upper_right_cell, lower_right_cell, lower_left_cell}

def main():
    sb = StarBattle("puzzles/1.txt")

    print(sb)

if __name__ == "__main__":
    main()