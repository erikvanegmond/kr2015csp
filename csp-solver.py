import argparse

print "Hello, this will be a CSP solver!"

def solve_sudokus(fname):
     with open(fname) as f:
        for line in f.readlines():
            print line



class Solver(object):
    """docstring for Solver"""
    def __init__(self, arg):
        self.arg = arg

    def preprocess(self):
        return None

    def constraint_propagation(self):
        return None

    def atomic(self):
        return True

    def split(self):
        return None

    def solve(self):
        cont = True
        solved = False
        while cont and not solved:
            preprocess()
            constraint_propagation()

            if not solved:
                if atomic():
                    cont = False
                else:
                    newSolver = split()
                    newSolver.solve()

solve_sudokus('1000-sudokus.txt')