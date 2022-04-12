from docplex.mp.model import Model
from docplex.cp.model import *


def build_sudoku_model():
    sudoku = (
        (0, 0, 0, 0, 0, 8, 0, 0, 0),
        (0, 5, 9, 0, 0, 0, 0, 0, 8),
        (2, 0, 0, 0, 0, 6, 0, 0, 0),
        (0, 4, 5, 0, 0, 0, 0, 0, 0),
        (0, 0, 3, 0, 0, 0, 0, 0, 0),
        (0, 0, 6, 0, 0, 3, 0, 5, 4),
        (0, 0, 0, 3, 2, 5, 0, 0, 6),
        (0, 0, 0, 0, 0, 0, 0, 0, 0),
        (0, 0, 0, 0, 0, 0, 0, 0, 0)
    )

    model = CpoModel(name='sudoku')
    grid = [[integer_var(min=1, max=9, name='C' + str(r) + str(c)) for r in range(9)] for c in range(9)]
    for r in range(9):
        model.add(all_diff([grid[r][c] for c in range(9)]))
    for c in range(9):
        model.add(all_diff([grid[r][c] for r in range(9)]))

    for sr in range(0, 9, 3):
        for sc in range(0, 9, 3):
            model.add(all_diff([grid[r][c] for r in range(sr, sr + 3) for c in range(sc, sc + 3)]))

    for r in range(9):
        for c in range(9):
            v = sudoku[r][c]
            if v > 0:
                grid[r][c].set_domain((v, v))

    print("\nSolving model...")
    msol = model.solve(TimeLimit=10)

    if msol:
        sol = [[msol[grid[r][c]] for c in range(9)] for r in range(9)]
        print('Solve Time: ' + str(msol.get_solve_time()))
        print('Solution: ', sol)
    else:
        print('No solution found.')


def build_knapsack_model():
    w = [4, 2, 5, 4, 5, 1, 3, 5]
    v = [10, 5, 18, 12, 15, 1, 2, 8]
    C = 15
    N = len(w)

    model = Model(name='knapsack_problem')
    x = model.binary_var_list(N, name='x')
    model.add_constraint(sum(w[i] * x[i] for i in range(N)) <= C)
    obj_fn = sum(v[i] * x[i] for i in range(N))
    model.set_objective('max', obj_fn)
    model.print_information()
    sol = model.solve()
    model.print_solution()
    if sol is None:
        print('Infeasible')


build_knapsack_model()