# kr2015csp

## Constraint Satisfaction Problem Solver with Sudoku-Specific Interface

`sudoku.py` takes five optional arguments.

* `-i INPUT, --input INPUT`, a text file containing sudokus in oneline format, defaults to `1000-sudokus.txt`

*  `-retSolvers`, Return the solvers, default false

*  `-printSolutions`, Print the solution of each sudoku, default false

*  `--val_heur {0,1,2,3}`, value heuristic:: 0:random, 1:first value in list, 2:most limiting value, 3:least limiting value

*  `--var_heur {0,1,2}`, variable heuristic:: 0:random, 1:first variable in list, 2:smallest domain first

You can also call with -h for essentially this message.
