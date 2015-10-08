import cspsolver as csp

solver = csp.Solver()

### simple ###

solver.addVariable("a", set([1,2,3]))
solver.addVariable("b", set([1,2,3]))
solver.addVariable("c", set([1,2,3]))
solver.addVariable("d", set([1,2,3,4]))
solver.addConstraint(["b","a","c","d"], 1)

### 2x2 sudoku ###
# solver.addVariable("11",set([2]))
# solver.addVariable("12",set([1,2]))
# solver.addVariable("21",set([1,2]))
# solver.addVariable("22",set([1,2]))

# solver.addConstraint(['11','12'],1)
# solver.addConstraint(['11','21'],1)
# solver.addConstraint(['22','12'],1)
# solver.addConstraint(['22','21'],1)

print solver
(message, result) = solver.solve()
print message, result