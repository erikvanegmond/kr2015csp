from cspsolver import *
import pprint as pp
import sys

digits1to9 = [1, 2, 3, 4, 5, 6, 7, 8, 9]
digits1to9str = [str(n) for n in digits1to9]
sudokuvars = [ i+j for i in digits1to9str for j in digits1to9str ]

def generate_sudoku_constraints():
    # generates a list of 27 Constraints representing the rules of sudoku.

    scs = []
    ns = digits1to9str

    #rows
    for r in ns:
        scs.append( Constraint([r+i for i in ns], 1) )

    #columns
    for c in ns:
        scs.append( Constraint([i+c for i in ns], 1) )

    #blocks
    for bx in range(3):
        for by in range(3):
            scs.append( Constraint( [str(br+1+(3*by))+str(bc+1+(3*bx)) for br in range(3) for bc in range(3)],1 ))

    return scs

def parse_givens_to_unaries( boardstring ):
    # given 81-character str representing a sudoku instance,
    # returns list of tuples (var,dom) representing unary constraints:
    # the domain of var is to be restricted to the singleton set dom

    rows = [list(boardstring[i:i+9]) for i in range(0,81,9)]

    return [ (str(r+1)+str(c+1), {rows[r][c]}) \
             for c in range(9) for r in range(9) \
             if rows[r][c] != '.' ]

    # I'm not sure how you want to feed this into the solver.

def initialize_sudoku_solver( boardstring, constraints ):

    # initialize a solver with 81 variables '11','12',...,'98','99'
    # each with corresponding domain {1,...,9}
    ss = Solver()
    ss.addVariables(dict([(v, set(digits1to9str)) for v in sudokuvars]))
    # add the generic sudoku constraints to the solver
    ss.addConstraints( constraints )
    # originally I had the following line when I was representing givens as
    # unary constraints but maybe you just want to take the list given by
    # the parse_givens_to_unaries and feed it to the solver directly somehow...
    #
    # ss.addConstraints( parse_givens_to_unaries(boardstring) )
    givens = parse_givens_to_unaries( boardstring )
    for given in givens:
        ss.addVariable(given[0], given[1])
    return ss

def solve_sudokus(fname):
    # constraints = generate_sudoku_constraints()
    with open(fname) as f:
        c = 0
        for line in f.readlines():
            print c
            c+=1
            ss = initialize_sudoku_solver(line.strip(), generate_sudoku_constraints())
            ss.solve()

            # break



def solution_to_oneline(s):
    sl = list(s.items())
    sl.sort()
    return ''.join([str(i[1].pop()) for i in sl])
    

       


            

solve_sudokus('1000-sudokus.txt')


