import argparse

print "Hello, this will be a CSP solver!"

def solve_sudokus(fname):
     with open(fname) as f:
        for line in f.readlines():
            print line



class Solver(object):
    """docstring for Solver"""

    variables = {}

    def __init__(self):
        print "init solver"

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


    def addVariable(self, name, domain):
        if name in self.variables:
            print "overriding domain of %s"%(name)

        self.variables[name]=domain

        # self.variables.append(Variable(name, domain))


    def addConstraint(self, variables, relation):
        for var in variables:
            if var not in self.variables:
                raise Exeption( "ERROR unknown variable!" )



    def __str__(self):
        return str(self.variables)


class Constraint(object):
    """docstring for Constraint"""

    variables = [] #list of Variable
    relation = 1# = all different

    def __init__(self, variables, relation):
        self.variables = variables
        self.relation = relation


# solve_sudokus('1000-sudokus.txt')

solver = Solver()
solver.addVariable("a", [1,2,4])
solver.addVariable("a", [1,2,4,5])
solver.addVariable("b", [2,3])
solver.addConstraint(["a","b"], 1)
solver.addConstraint(["a","c"], 1)
print solver
