
# script(s) to test/run cspsolver


from cspsolver import *
from sudoku import *


## ==============================================



def solve_sudokus(fname):
     with open(fname) as f:
        for line in f.readlines():
            print line


# solve_sudokus('1000-sudokus.txt')



## ==============================================



solver = Solver()
solver.addVariable("a", Domain([1,2,4]))
solver.addVariable("b", Domain([2]))
solver.addVariable("c", Domain([1,2]))
solver.addConstraint(["b","a","c"], 1)
print solver
solver.solve()

