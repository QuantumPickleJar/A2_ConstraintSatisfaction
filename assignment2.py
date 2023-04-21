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
    if A == B: # row check
        return False
    if a == b: # col check
        return False

    # check adjacent cells
    adj = getAdjacentCells(A, a)
    for x in adj:
        if x == [B, b]:
            return False

    # check same shape


    return True

def getAdjacentCells(row, col):

    # TODO: this can be cleaned up later
    # It would probably be best for these to be made into a list rather than a set because we should be
    # able to have duplicates
    up_cell = [row, col + 1]
    down_cell = [row, col - 1]
    left_cell = [row - 1, col]
    right_cell = [row + 1, col]

    upper_left_cell = [row - 1, col + 1]
    upper_right_cell = [row + 1, col + 1]
    lower_left_cell = [row - 1, col - 1]
    lower_right_cell = [row + 1, col - 1]

    return [up_cell, down_cell, right_cell, left_cell,
            upper_left_cell, upper_right_cell, lower_right_cell, lower_left_cell]

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
        for row in range(len(self.board)):
            self.vars.append(row)
        print(self.vars)

        # Set domain for
        self.domains = {}
        for i in self.vars:
            self.domains[i] = range(len(self.vars))

        # prepare neighbors
        self.neighbors = self.findNeighbors()

        # for row_index, row in enumerate(self.vars):
        #     neighbors[row_index] = {}  #empty dict for this variable
        #     for col_index, cell in enumerate(row):
        #         neighbors[row_index][col_index] = []  # right now, we make a list of cells rather than the row (index)
        #         # itself

        # neighbors = self.findNeighbors()

        CSP.__init__(self, self.vars, self.domains, self.neighbors, star_constraint)

    def findNeighbors(self):
        '''
        consider all other row and column variables, and exclude the cells that already
        have stars placed in them in those variables from the domain of each row variable.
        '''
        all_neighbors = {}
        # loop through all the variables to build each set of neighbors
        for i in range(len(self.vars)):
            if i == 0:
                all_neighbors[0] = {1}
            elif i == len(self.vars) - 1:
                all_neighbors[len(self.vars) - 1] = {len(self.vars) - 2}
            else:
                all_neighbors[i] = {i - 1, i + 1}



        # finds all shape values in a given row
        shape_domains = {}
        for row in range(len(self.vars)):
            shape_domains[row] = set(self.board[row])
        # checks for shape constraints in other rows
        for i in range(len(self.vars)):
            for j in range(len(self.vars)):
                if i != j:
                    if any(x in shape_domains[i] for x in shape_domains[j]):
                        all_neighbors[i].add(j)

        return all_neighbors
def printResult(dict):
    for x in range(len(dict)):
        n = ['-' for x in range(len(dict))]
        n[dict[x]] = '*'
        print(n)


def main():
    sb = StarBattle("puzzles/2.txt")
    print('Board = ' + str(sb.board))
    print('Variables = ' + str(sb.vars))
    print('Domain = ' + str(sb.domains))
    print('Neighbors = ' + str(sb.neighbors))

    result = backtracking_search(sb, select_unassigned_variable=mrv, order_domain_values=lcv,
                                 inference=no_inference)
    print(result)
    printResult(result)

if __name__ == "__main__":
    main()