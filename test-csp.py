import cspsolver as csp

solver = csp.Solver()
solver.addVariable("a", set([1,2,3]))
solver.addVariable("b", set([2,3]))
solver.addVariable("c", set([1,2]))
solver.addConstraint(["b","a","c"], 1)
print solver
solver.solve()