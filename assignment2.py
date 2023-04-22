from csp import *
from timeit import default_timer as timer

'''
A function f(A, a, B, b) that returns true if neighbors
    A, B satisfy the constraint when they have values A=a, B=b
    
    Any variable that shares a row, column, or diagonal with a given variable would be a neighbor,
     as placing a star in the given variable would restrict the placement of stars in its neighbors.
'''
def star_constraint(A, a, B, b):
    if A == B: # row check
        return False
    if a[0] == b[0]: # col check
        return False

    # check adjacent cells
    adj = getAdjacentCells(A, a[0])
    for x in adj:
        if x == [B, b[0]]:
            return False
    # check if same shape
    if a[1] == b[1]:
        return False

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
    # Creates necessary vars
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

        # Set domain for each var
        self.domains = self.findDomains()

        # prepare neighbors
        self.neighbors = self.findNeighbors()

        CSP.__init__(self, self.vars, self.domains, self.neighbors, star_constraint)

    def findDomains(self):
        domains = {}
        for i in range(len(self.vars)):
            domains[i] = []
            for j in range(len(self.vars)):
                domains[i].append(([j, self.board[i][j]]))
        return domains
    def findNeighbors(self):
        '''
        each variable is constrained by every other variable as a star can be in neither the same row nor col
        '''
        all_neighbors = {}
        for i in range(len(self.vars)):
            all_neighbors[i] = list(range(len(self.vars)))
            all_neighbors[i].remove(i)

        return all_neighbors
def printResult(dict):

    for x in range(len(dict)):
        n = ['-' for x in range(len(dict))]
        n[dict[x][0]] = "*"
        print(n)
def run_backtracking(sb,select_unassigned_variable,order_domain_values,inference):
    start = timer()
    result = backtracking_search(sb, select_unassigned_variable, order_domain_values, inference)
    end = timer()
    printResult(result)
    print(result)
    print(f"Time Elapsed: {end - start}")

def main():
    sb = StarBattle("puzzles/5.txt")
    print('Board = ' + str(sb.board))
    print('Variables = ' + str(sb.vars))
    print('Domain = ' + str(sb.domains))
    print('Neighbors = ' + str(sb.neighbors))

    # alter which line is uncommented to compare search times for different search parameters
    '''
    run_backtracking(sb, select_unassigned_variable=first_unassigned_variable, order_domain_values=unordered_domain_values,
                                 inference=no_inference)
    '''
    '''
    '''
    run_backtracking(sb, select_unassigned_variable=mrv, order_domain_values=lcv,
                                 inference=forward_checking)
    run_backtracking(sb, select_unassigned_variable=mrv, order_domain_values=lcv,
                                 inference=mac)
if __name__ == "__main__":
    main()