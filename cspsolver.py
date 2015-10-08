import random
from pprint import *

class Solver(object):
    """docstring for Solver"""

    # variables = {}
    # constraints = []

    def __init__(self, variables={}, constraints=[]):
        self.variables = {}
        self.constraints = []
        self.variables.update(variables)
        self.constraints += constraints

    def __str__(self):
        return str(self.variables)#+"\n"+str(self.constraints)

    def preprocess(self):
        # print "preprocessing..."
        return None

    def constraint_propagation(self):
        # print "propagating..."
        change = True

        while change:
            change = False
            for constraint in self.constraints:
                variables = [self.variables[x] for x in constraint[0]]
                if constraint[1] == 1: #all different
                    for i,var in enumerate(variables):
                        for j, otherVar in enumerate(variables):
                            if i!=j and len(otherVar)==1:
                                preVar = var.copy()
                                var.difference_update(otherVar)
                                if preVar != var:
                                    change = True
        return None

    def atomic(self):
        # print "atomic?"
        for var, domain in self.variables.iteritems():
            if len(domain) > 1:
                return False
        return True

    def pick_variable(self, heuristic=0):
        # print "picking var"
        while True:
            var = random.choice(self.variables.keys())
            if len(self.variables[var])>1:
                return var

    def pick_value(self, var, heuristic=0):
        return random.choice(list(self.variables[var]))

    def split(self):
        var = self.pick_variable()
        value = self.pick_value(var)

        vars1 = self.variables[var] - set([value])
        vars2 = set([value])
        problem1 = self.variables.copy()
        problem1[var] = vars1
        problem2 = self.variables.copy()
        problem2[var] = vars2
        solver1 = Solver(problem1, self.constraints)
        solver2 = Solver(problem2, self.constraints)
        return solver1, solver2

    def solved(self):
        if not self.unsolvable() and self.atomic():
            return True
        return False

    def unsolvable(self):
        for var, domain in self.variables.iteritems():
            if len(domain) == 0:
                return True
        return False

    def solve(self):
        # print "solving:",self
        cont = True
        solved = self.solved()
        # print "solved",solved
        while cont and not solved:
            # print "looping..."
            self.preprocess()
            self.constraint_propagation()
            # print "solved2,",solved
            solved = self.solved()
            # print "solved3,",solved

            if not solved:
                if self.atomic():
                    cont = False
                else:
                    # print "presplit:",self
                    newSolver1, newSolver2 = self.split()
                    # print "problem1:", newSolver1
                    # print "problem2:", newSolver2
                    newSolver1.solve()
                    if newSolver1.unsolvable():
                        return
                    if newSolver1.solved():
                        self = newSolver1
                        break
                    newSolver2.solve()
                    if newSolver2.unsolvable():
                        return

                    if newSolver2.solved():
                        self = newSolver2
                        break
                    # print "did split, now exit :(\ncurrent state:\n",self
                    return
                    # newSolver.solve()
            solved = self.solved()
        print "solved:\n",self

    def addVariable(self, name, domain):
        # if name in self.variables:
        #     print "overriding domain of %s to %s"%(name, domain)

        self.variables[name]=domain
        # self.variables.append(Variable(name, domain))

    def addVariables(self, newvariables):
        # analyze & add vars one at a time via addVariable method
        if isinstance(newvariables, dict):
            for v, d in newvariables.items():
                self.addVariable(v, d)
        else:  # i.e., newvariables is a list or set or something
            for v in newvariables:
                self.addVariable(*v)


    def addConstraint(self, variables, relation):
        for var in variables:
            if var not in self.variables:
                raise

        if (variables, relation) in self.constraints:
            return

        self.constraints.append((variables, relation))

    def addConstraints(self, newconstraints):
        for c in newconstraints:
            self.addConstraint(c.variables, c.relation)

    def restrict(self, var, restrictedDomain):
        # restricts domain of variable var to restrictedDomain;
        # var must be in self.variables and its domain must be
        # superset of restrictedDomain
        if not isinstance(restrictedDomain, set):  # convert to set if needed
            restrictedDomain = set(restrictedDomain)
        if restrictedDomain.issubset(self.variables[var]):
            self.domain = restrictedDomain
        else:
            #print "cannot restrict"
            raise ValueError("Domain restriction is not subset of original Domain")



class Constraint(object):
    """docstring for Constraint"""

    variables = [] #list of Variable
    relation = 1# = all different

    def __init__(self, variables, relation):
        self.variables = variables
        self.relation = relation
    def __repr__(self):
        return "Constraint("+repr(self.variables)+", "+str(self.relation)+")"
