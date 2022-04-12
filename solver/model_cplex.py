import util
import plot
from docplex.cp.model import *


def build_model(df_nodes, df_files, co_occurrence_matrix):
    nodes_len, blocks_len, nodes_capacity, blocks_size = util.get_cluster_setting(df_nodes, df_files)

    model = CpoModel(name='Algorithm')

    x = [[integer_var(min=0, max=1, name="X" + str(r) + "_" + str(c)) for c in range(nodes_len)]
         for r in range(blocks_len)]

    # rep factor >= 3
    for r in range(blocks_len):
        model.add_constraint(modeler.sum(x[r][c] for c in range(nodes_len)) >= 3)

    tmp = df_files.groupby('fileName', sort=False)['fileName'].count()
    i = 0
    for index, row in tmp.iteritems():
        if row == 1:
            i += row
        else:
            for r in range(0, row-1):
                model.add_constraint(modeler.equal(
                    modeler.sum(x[i+r][c] for c in range(nodes_len)),
                    modeler.sum(x[i+r+1][c] for c in range(nodes_len))))
            i += row

    # sum < node capacity
    for c in range(nodes_len):
        model.add_constraint(modeler.sum(x[r][c] * blocks_size[r] for r in range(blocks_len)) < nodes_capacity[c])

    blocks_weight = util.compute_weights(df_files, blocks_len, co_occurrence_matrix)

    z_tmp = []
    for c in range(nodes_len):
        z_tmp.append(modeler.sum(x[r][c] * blocks_weight[r] for r in range(blocks_len)))

    #z_0 = modeler.sum(z_tmp)
    #model.add(maximize(z_0))

    z = modeler.power(modeler.standard_deviation(z_tmp), 2)
    model.add(minimize(z))
    #model.add(maximize(z))

    # Solve model
    print("\nSolving model...")
    solve = model.solve(TimeLimit=7200)
    #solve = model.solve(SolutionLimit=10)

    if solve:
        sol = [[solve[x[r][c]] for c in range(nodes_len)] for r in range(blocks_len)]
        print('Solve Time: ' + str(solve.get_solve_time()))
        util.print_solution('cplex', df_nodes[0:nodes_len], df_files[0:blocks_len], sol)
        util.print_tmp(df_nodes[0:nodes_len], df_files[0:blocks_len], sol)
        plot.generate_default_map(df_nodes, df_files, sol, 'cplex')
    else:
        print('No solution found.')
