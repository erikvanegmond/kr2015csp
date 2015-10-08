import random
from pprint import *
from collections import Counter
import sys
import time

class Solver(object):
    """docstring for Solver"""

    # variables = {}
    # constraints = []

    instance = 0

    def __init__(self, variables={}, constraints=[]):
        self.variables = {}
        self.constraints = []
        self.variables.update(variables)
        self.constraints += constraints
        self.instance += 1

    def __str__(self):
        return str(self.variables)#+"\n"+str(self.constraints)

    def preprocess(self):
        # print "preprocessing..."
        return None

    def constraint_propagation(self):
        # print "propagating..."
        change = True
        sTime = time.time()
        while change:
            change = False
            for constraint in self.constraints:
                unaries = self.get_unary_values(constraint[0])

                unariesSet = set([list(x[1])[0] for x in unaries])

                if unariesSet and len(unariesSet) != 9:
                    variables = [(x,self.variables[x]) for x in constraint[0]]
                    if constraint[1] == 1: #all different and has unary variables
                        for i,var in enumerate(variables):
                            if len(var[1])>1:
                                preVar = var[1].copy()
                                var[1].difference_update(unariesSet)
                                if preVar != var[1]:
                                    change = True


                            # for unary in unaries:
                            #     if unary[0] != var[0]:
                            #         preVar = var[1].copy()
                            #         var[1].difference_update(unary[1])
                            #         if preVar != var[1]:
                            #             change = True
        # print time.time() - sTime
    def atomic(self):
        # print "atomic?"
        for var, domain in self.variables.iteritems():
            if len(domain) > 1:
                return False
        return True

    def pick_variable(self, heuristic=0):
        # print "picking var"
        if heuristic==0:#random
            while True:
                var = random.choice(self.variables.keys())
                if len(self.variables[var])>1:
                    return var
        elif heuristic==1:#pick first one
            for var in self.variables:
                if len(self.variables[var])>1:
                    return var
        elif heuristic==2:#pick the one with the smallest domains
            smallestLen = 0
            smallest = set()
            for var, domain in self.variables.iteritems():
                if len(domain)>1 and (not smallestLen or len(domain)<smallestLen  ):
                    smallest = var
                    smallestLen = len(domain)
                    if smallestLen == 2:
                        return var
            # print smallestLen, self.variables[smallest]
            return smallest

    def pick_value(self, var, heuristic=0):
        if heuristic==0:#random
            return random.choice(list(self.variables[var]))
        elif heuristic==1:#pick first one
            return list(self.variables[var])[0]
        elif heuristic==2:#most limiting value
            # print self.variables[var]
            allValues = []
            for constraint in self.constraints:
                if var in constraint[0]:
                    if constraint[1] == 1: #all different constraint
                        for constVar in constraint[0]:
                            allValues+=list(self.variables[constVar].intersection(self.variables[var]))
            return Counter(allValues).most_common(1)[0][0] #most common value
        elif heuristic==3:#least limiting value
            # print self.variables[var]
            allValues = []
            for constraint in self.constraints:
                if var in constraint[0]:
                    if constraint[1] == 1: #all different constraint
                        for constVar in constraint[0]:
                            allValues+=list(self.variables[constVar].intersection(self.variables[var]))
            return Counter(allValues).most_common()[-1][0] #most common value
        else:
            exit()

    def split(self):
        var = self.pick_variable(heuristic=2)
        value = self.pick_value(var, heuristic=3)
        vars1 = set([value])
        vars2 = self.variables[var] - set([value])

        problem1 = self.duplicate_variables()
        problem1[var] = vars1
        problem2 = self.duplicate_variables()

        problem2[var] = vars2

        solver1 = Solver(problem1, self.constraints)
        solver2 = Solver(problem2, self.constraints)

        # print "|",solver1,"\n|",solver2,"\n"
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
        # sys.stdout.write('.'),
        cont = True
        solved = self.solved()
        while cont and not solved:
            self.preprocess()
            self.constraint_propagation()
            solved = self.solved()

            if not solved:
                if self.atomic():
                    cont = False
                else:
                    newSolver1, newSolver2 = self.split()
                    if newSolver1.solved():
                        self = newSolver1
                        return ("solved", self)
                    elif newSolver2.solved():
                        self = newSolver2
                        return ("solved", self)
                    (message, result) = newSolver1.solve()

                    if message == "unsolvable":
                        (message, result) = newSolver2.solve()
                        if message == "unsolvable":
                            return (message, result)
                    if message == "solved":
                        return (message, result)
            solved = self.solved()
        solved = self.solved()
        if self.unsolvable():
            return ("unsolvable", None)
        if solved:
            return ("solved",self)
        # print "??", solved, self.unsolvable(), self
        return (None, None)

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

    def constraint_contains_unary(self, constraint):
        for var in constraint:
            if len(self.variables[var])==1:
                return True
        return False

    def get_unary_values(self, constraint):
        unaries = []
        for var in constraint:
            if len(self.variables[var])==1:
                unaries.append([var, self.variables[var]])
        return unaries

    def duplicate_variables(self):
        newVariables = {}
        for var in self.variables:
            newVariables[var] = set(list(self.variables[var]))
        return newVariables

class Constraint(object):
    """docstring for Constraint"""

    variables = [] #list of Variable
    relation = 1# = all different

    def __init__(self, variables, relation):
        self.variables = variables
        self.relation = relation
    def __repr__(self):
        return "Constraint("+repr(self.variables)+", "+str(self.relation)+")"
