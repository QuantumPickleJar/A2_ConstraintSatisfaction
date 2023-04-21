
from search import Problem
from csp import backtracking_search, no_inference, forward_checking, mac
from csp import first_unassigned_variable,mrv,num_legal_values,unordered_domain_values,lcv
from csp import CSP,UniversalDict
from timeit import default_timer as timer
from utils import DefaultDict,update,argmin_random_tie

#______________________________________________________________________________
# Map-Coloring Problems
def different_values_constraint(A, a, B, b):
    "A constraint saying two neighboring variables must differ in value."
    return a != b

def MapColoringCSP(colors, neighbors):
    """Make a CSP for the problem of coloring a map with different colors
    for any two adjacent regions.  Arguments are a list of colors, and a
    dict of {region: [neighbor,...]} entries.  This dict may also be
    specified as a string of the form defined by parse_neighbors."""
    if isinstance(neighbors, str):
        neighbors = parse_neighbors(neighbors)
    return CSP(neighbors.keys(), UniversalDict(colors), neighbors,
               different_values_constraint)

def parse_neighbors(neighbors, vars=[]):
    """Convert a string of the form 'X: Y Z; Y: Z' into a dict mapping
    regions to neighbors.  The syntax is a region name followed by a ':'
    followed by zero or more region names, followed by ';', repeated for
    each region name.  If you say 'X: Y' you don't need 'Y: X'.
    >>> parse_neighbors('X: Y Z; Y: Z')
    {'Y': ['X', 'Z'], 'X': ['Y', 'Z'], 'Z': ['X', 'Y']}
    """
    dict = DefaultDict([])
    for var in vars:
        dict[var] = []
    specs = [spec.split(':') for spec in neighbors.split(';')]
    for (A, Aneighbors) in specs:
        A = A.strip()
        dict.setdefault(A, [])
        for B in Aneighbors.split():
            dict[A].append(B)
            dict[B].append(A)
    return dict

australia = MapColoringCSP(list('RGB'),
                           'SA: WA NT Q NSW V; NT: WA Q; NSW: Q V; T: ')

usa = MapColoringCSP(list('RGBY'),
        """WA: OR ID; OR: ID NV CA; CA: NV AZ; NV: ID UT AZ; ID: MT WY UT;
        UT: WY CO AZ; MT: ND SD WY; WY: SD NE CO; CO: NE KA OK NM; NM: OK TX;
        ND: MN SD; SD: MN IA NE; NE: IA MO KA; KA: MO OK; OK: MO AR TX;
        TX: AR LA; MN: WI IA; IA: WI IL MO; MO: IL KY TN AR; AR: MS TN LA;
        LA: MS; WI: MI IL; IL: IN KY; IN: OH KY; MS: TN AL; AL: TN GA FL;
        MI: OH IN; OH: PA WV KY; KY: WV VA TN; TN: VA NC GA; GA: NC SC FL;
        PA: NY NJ DE MD WV; WV: MD VA; VA: MD DC NC; NC: SC; NY: VT MA CT NJ;
        NJ: DE; DE: MD; MD: DC; VT: NH MA; MA: NH RI CT; CT: RI; ME: NH;
        HI: ; AK: """)

france = MapColoringCSP(list('RGBY'),
        """AL: LO FC; AQ: MP LI PC; AU: LI CE BO RA LR MP; BO: CE IF CA FC RA
        AU; BR: NB PL; CA: IF PI LO FC BO; CE: PL NB NH IF BO AU LI PC; FC: BO
        CA LO AL RA; IF: NH PI CA BO CE; LI: PC CE AU MP AQ; LO: CA AL FC; LR:
        MP AU RA PA; MP: AQ LI AU LR; NB: NH CE PL BR; NH: PI IF CE NB; NO:
        PI; PA: LR RA; PC: PL CE LI AQ; PI: NH NO CA IF; PL: BR NB CE PC; RA:
        AU BO FC PA LR""")

#______________________________________________________________________________
# n-Queens Problem

def queen_constraint(A, a, B, b):
    """Constraint is satisfied (true) if A, B are really the same variable,
    or if they are not in the same row, down diagonal, or up diagonal."""
    return A == B or (a != b and A + a != B + b and A - a != B - b)

class NQueen(CSP):
    '''
    Think of placing queens one per column, from left to right.
    That means position (x, y) represents (var, val) in the CSP.
    '''
    def __init__(self, n):
        """Initialize data structures for n Queens."""
        CSP.__init__(self, range(n), UniversalDict(range(n)),
                     UniversalDict(range(n)), queen_constraint)

#______________________________________________________________________________
#An implementation of the example in the CSP class notes 
vars = ['A','B','C','D']
neighbors = {'A': ['B','D'], 'B': ['A','C','D'], 'C': ['B','D'],
             'D': ['A','B','C']} 
domains = {'A': [1,2,3,4],'B': [1,2,3,4],'C': [2,4],'D': [1,2,3,4]} 
#If they all had the same domain, we could use the line below instead
#domains = UniversalDict(range(1,5))  
           
def AC3Example_constraints(A, a, B, b):
    #A <= B
    if (A=='A' and B=='B'): return (a<=b)
    if (A=='B' and B=='A'): return (a >= b)
    
    #A <> D
    if ((A=='A' and B=='D') or (A=='D' and B=='A')): return (a != b) 

    #B < C
    if (A=='B' and B=='C'): return (a < b)
    if (A=='C' and B=='B'): return (a > b)

    #C <= D
    if (A=='C' and B=='D'): return (a<=b)
    if (A=='D' and B=='C'): return (a >= b)

    #D = 2*B
    if (A=='D' and B=='B'):
        return ((2*b)==a)
    if (A=='B' and B=='D'):
        return ((2*a)==b)  
                         
#______________________________________________________________________________
#Options for CSP:
## select_unassigned_variable: = [first_unassigned_variable,  mrv,  num_legal_values]
## order_domain_values = [unordered_domain_values, lcv]
## inference = [no_inference, forward_checking, mac]
start = timer()

#Test Class example
# problem = CSP(vars, domains, neighbors, AC3Example_constraints)
# result = backtracking_search(problem,select_unassigned_variable=mrv,order_domain_values=lcv,inference=no_inference)

#Test map coloring problems
problem = NQueen(4)
result = backtracking_search(problem,select_unassigned_variable=mrv,order_domain_values=lcv,inference=forward_checking) #no_inference forward_checking mac

#Test map coloring problems
#problem = usa  #usa france australia
#result = backtracking_search(problem,select_unassigned_variable=mrv,order_domain_values=lcv,inference=mac) #no_inference forward_checking mac

end = timer()
print(result)
print()
print("Time elapsed:",end - start)
