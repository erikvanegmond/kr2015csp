import argparse

print "Hello, this will be a CSP solver!"

def solve_sudokus(fname):
     with open(fname) as f:
        for line in f.readlines():
            print line



class Solver(object):
    """docstring for Solver"""

    variables = {}
    constraints = []

    def __init__(self):
        print "init solver"

    def preprocess(self):
        return None

    def constraint_propagation(self):
        change = True

        while change:
            change = False
            for constraint in self.constraints:
                variables = [self.variables[x] for x in constraint[0]]
                if constraint[1] == 1: #all different
                    unaryConstraints = [x for x in variables if len(x)==1]
                    for var in variables:
                        for unaryConstraint in unaryConstraints:
                            if var != unaryConstraint:
                                preVar = var.copy()
                                var.difference_update(unaryConstraint)
                                if preVar != var:
                                    change = True

        return None

    def atomic(self):
        return True

    def split(self):
        return None

    def solve(self):
        cont = True
        solved = False
        while cont and not solved:
            self.preprocess()
            self.constraint_propagation()

            if not solved:
                if self.atomic():
                    cont = False
                else:
                    newSolver = self.split()
                    newSolver.solve()



    def addVariable(self, name, domain):
        if name in self.variables:
            print "overriding domain of %s"%(name)

        self.variables[name]=domain
        # self.variables.append(Variable(name, domain))


    def addConstraint(self, variables, relation):
        for var in variables:
            if var not in self.variables:
                raise
        self.constraints.append((variables, relation))



    def __str__(self):
        return str(self.variables)#+"\n"+str(self.constraints)

class Domain(object):

    domain = set()
    """docstring for Domain"""
    def __init__(self, domain):
        self.domain = set(domain)

    def difference(self, inputDomain):
        self.domain.difference(inputDomain.domain)

    def __len__(self):
        return len(self.domain)

    def __repr__(self):
        return str(self.domain)


class Constraint(object):
    """docstring for Constraint"""

    variables = [] #list of Variable
    relation = 1# = all different

    def __init__(self, variables, relation):
        self.variables = variables
        self.relation = relation


# solve_sudokus('1000-sudokus.txt')

solver = Solver()
solver.addVariable("a", set([1,2,4]))
solver.addVariable("b", set([2]))
solver.addVariable("c", set([1,2]))
solver.addConstraint(["b","a","c"], 1)
print solver
solver.solve()
print solver

