import util
import plot
import pulp as pl


def build_model(df_nodes, df_files, co_occurrence_matrix):
    nodes_len, blocks_len, nodes_capacity, blocks_size = util.get_cluster_setting(df_nodes, df_files)

    model = pl.LpProblem(name="Algorithm", sense=pl.LpMaximize)

    x = pl.LpVariable.matrix(name='x', indices=(range(blocks_len), range(nodes_len)), lowBound=0, upBound=1,
                             cat=pl.LpBinary)

    # rep factor >= 3
    for r in range(blocks_len):
        model += pl.lpSum(x[r][c] for c in range(nodes_len)) >= 3

    tmp = df_files.groupby('fileName', sort=False)['fileName'].count()
    i = 0
    for index, row in tmp.iteritems():
        if row == 1:
            i += row
        else:
            for r in range(0, row-1):
                model += (pl.lpSum(x[i+r][c] for c in range(nodes_len)) ==
                          pl.lpSum(x[i+r+1][c] for c in range(nodes_len)))
            i += row

    # sum < node capacity
    for c in range(nodes_len):
        model += pl.lpSum(x[r][c] * blocks_size[r] for r in range(blocks_len)) <= nodes_capacity[c]

    blocks_weight = util.compute_weights(df_files, blocks_len, co_occurrence_matrix)

    z_tmp = []
    for c in range(nodes_len):
        z_tmp.append(sum(x[r][c] * blocks_weight[r] for r in range(blocks_len)))

    model += pl.lpSum(z_tmp)

    # Solve model
    print("\nSolving model...")
    model.solve(pl.COIN(timeLimit=7200))

    sol = [[x[r][c].varValue for c in range(nodes_len)] for r in range(blocks_len)]
    util.print_solution('pulp', df_nodes, df_files, sol)
    util.print_tmp(df_nodes, df_files, sol)
    plot.generate_default_map(df_nodes, df_files, sol, 'pulp')
