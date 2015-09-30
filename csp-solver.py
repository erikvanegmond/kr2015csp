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


    def addConstraint(self, variables, relation):
        for var in variables:
            if var not in self.variables:
                raise
        self.constraints.append((variables, relation))



    def __str__(self):
        return str(self.variables)#+"\n"+str(self.constraints)

class Constraint(object):
    """docstring for Constraint"""

    variables = [] #list of Variable
    relation = 1# = all different

    def __init__(self, variables, relation):
        self.variables = variables
        self.relation = relation