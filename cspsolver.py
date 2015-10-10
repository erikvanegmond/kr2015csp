import random
from pprint import *
from collections import Counter
from copy import deepcopy
import sys
import time

class Solver(object):
    """docstring for Solver"""

    # variables = {}
    # constraints = []

    instance = 0

    def __init__(self, variables={}, constraints=[], propagated_variables=set()):
        self.variables = {}
        self.constraints = []
        self.variables.update(variables)
        self.constraints += constraints
        self.instance += 1
        self.variables_initial = None
        self.propagated_variables = propagated_variables

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

                # unariesSet = set([list(x[1])[0] for x in unaries if not x[0] in self.propagated_variables])
                unariesSet = set([list(x[1])[0] for x in unaries])
                # unaryVars = set([x[0] for x in unaries])
                # self.propagated_variables = self.propagated_variables.union(unaryVars)

                # print self.propagated_variables
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
        else:
            exit()

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

    def split(self, var_heur=0, val_heur=0):
        var = self.pick_variable(heuristic=var_heur)
        value = self.pick_value(var, heuristic=val_heur)
        vars1 = set([value])
        vars2 = self.variables[var] - set([value])

        problem1 = self.duplicate_variables()
        problem1[var] = vars1
        problem2 = self.duplicate_variables()

        problem2[var] = vars2

        solver1 = Solver(problem1, self.constraints, propagated_variables=self.propagated_variables)
        solver2 = Solver(problem2, self.constraints, propagated_variables=self.propagated_variables)

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

    def solve(self, var_heur=0, val_heur=0): #remember_initial_state
        # freeze a copy of self.variables right before solving

        ## COMMENTED OUT, I could not find it being used and it took half of the solving time!
        # self.variables_initial = deepcopy(self.variables)
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
                    newSolver1, newSolver2 = self.split(var_heur, val_heur)
                    if newSolver1.solved():
                        self = newSolver1
                        return ("solved", self)
                    elif newSolver2.solved():
                        self = newSolver2
                        return ("solved", self)
                    (message, result) = newSolver1.solve(var_heur, val_heur)

                    if message == "unsolvable":
                        (message, result) = newSolver2.solve(var_heur, val_heur)
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
            if len(self.variables[var])==1 and not var in self.propagated_variables:
                self.propagated_variables.add(var)
                unaries.append([var, self.variables[var]])
        return unaries

    def get_unary_variables(self, constraint):
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


    def clone_from_initial(self):
        # returns brand new solver with same initial variable-setup as self
        if self.variables_initial is None:
            raise
        return Solver( deepcopy(self.variables_initial), deepcopy(self.constraints) )

    def reset_to_initial(self):
        # similar but resets state of preexisting solver
        if self.variables_initial is None:
            raise
        self.variables = deepcopy(self.variables_initial)
        # (and self.constraints stay where they are)
        self.variables_initial = None
        # self.instance?





class Constraint(object):
    """docstring for Constraint"""

    variables = [] #list of Variable
    relation = 1# = all different

    def __init__(self, variables, relation):
        self.variables = variables
        self.relation = relation
    def __repr__(self):
        return "Constraint("+repr(self.variables)+", "+str(self.relation)+")"
