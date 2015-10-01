import argparse

print "Hello, this will be a CSP solver!"



class Solver(object):
    """docstring for Solver"""

    variables = {}
    constraints = []

    def __init__(self, variables={}, constraints=[]):
        self.variables.update(variables)
        self.constraints += constraints
        print "init solver"

    def __str__(self):
        return str(self.variables)#+"\n"+str(self.constraints)


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
        for var, domain in self.variables.iteritems():
            if len(domain) > 1:
                return False
        return True

    def split(self):
        return self

    def solved(self):
        if self.atomic():
            return True
        return False

    def solve(self):
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
                    newSolver = self.split()
                    print "did split, now exit :(\ncurrent state:\n",self
                    return
                    # newSolver.solve()
            solved = self.solved()
        print "solution:\n",self



    def addVariable(self, name, domain):
        if name in self.variables:
            print "overriding domain of %s"%(name)

        self.variables[name]=domain
        # self.variables.append(Variable(name, domain))

    def addVariables(self, newvariables):
        # analyze & add vars one at a time via addVariable method
        if isinstance(newvariables, dict):
            for v, d in newvariables.items():
                self.addVariable(self, v, d)
        else:  # i.e., newvariables is a list or set or something
            for v in newvariables:
                self.addVariable(*v)

                
    def addConstraint(self, variables, relation):
        for var in variables:
            if var not in self.variables:
                raise
        self.constraints.append((variables, relation))

    def addConstraints(self, newconstraints):
        for c in newconstraints:
            self.addConstraint(*c)


class Domain(object):

    domain = set()
    """docstring for Domain"""
    def __init__(self, domain):
        self.domain = set(domain)

    def __len__(self):
        return len(self.domain)

    def __repr__(self):
        return str(self.domain)


    def difference(self, inputDomain):
        self.domain.difference(inputDomain.domain)

    def restrict(self, restrictedDomain):
        # ensures restrictedDomain is just a set... 
        if isinstance(restrictedDomain, Domain):    # ..not a Domain object
            restrictedDomain = restrictedDomain.domain
        elif not isinstance(restrictedDomain, set):  # ..convert to set if needed
            restrictedDomain = set(restrictedDomain)
            
        if restrictedDomain.issubset(self.domain):
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


