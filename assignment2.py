from csp import CSP, UniversalDict

"""
Returns True if constraint pass
A = cell1 (string)
B = cell2 (string) 
a = cell1[domain] (where domain = {1} or {0}
b = cell2[domain]
"""
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


"""
Rules:
Max 20 shapes per puzzle

"""
class StarBattle(CSP):
    '''
    Problem of type CSP
    '''
    def __init__(self, fileName):
        """Initialize data structures for n stars"""

        # build the board state
        board = readPuzzleFromFile(fileName)

        shape_set = set()

        # since the board shows ALL shapes, that can't be our vars:
        for row in board:
            # split out all the letters in the row
            # convert the row into a set to remove duplicates, cutting down our work
            converted_row = set(row)
            if any(converted_row) not in shape_set:
                for char in converted_row:
                    shape_set.add(char)

        vars = list(shape_set)
        vars.sort()     # for readability, sort A-Z

        # since we aren't passing n as a param (like in NQueens), n = column width
        n = len(vars[0])

        CSP.__init__(self, range(n), UniversalDict(range(n)),
                     UniversalDict(range(n)), star_constraint)

    # Since the variable is what will change, stars are the variables
    vars = []

    """Likewise, since domains represent all possible values for a variable,
        we can just say (0,1) to represent star status"""
    domains = {}

    neighbors = {}



def main():
    sb = StarBattle("puzzles/1.txt")

    print(sb)

if __name__ == "__main__":
    main()
