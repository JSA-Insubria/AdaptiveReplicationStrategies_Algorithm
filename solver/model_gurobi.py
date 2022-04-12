import util
import plot
import numpy as np
import gurobipy as gp
from gurobipy import GRB


def build_model(df_nodes, df_files, co_occurrence_matrix):
    nodes_len, blocks_len, nodes_capacity, blocks_size = util.get_cluster_setting(df_nodes, df_files)

    model = gp.Model(name='Algorithm')
    x = model.addMVar((blocks_len, nodes_len), vtype=GRB.BINARY, name='x')

    # rep factor >= 3
    for r in range(blocks_len):
        model.addConstr(gp.quicksum(x[r][c] for c in range(nodes_len)) >= 3, name='rep_factor')

    tmp = df_files.groupby('fileName', sort=False)['fileName'].count()
    i = 0
    for index, row in tmp.iteritems():
        if row == 1:
            i += row
        else:
            for r in range(0, row-1):
                model.addConstr((gp.quicksum(x[i+r][c] for c in range(nodes_len)) ==
                                 gp.quicksum(x[i+r+1][c] for c in range(nodes_len))), name='rep_sum')
            i += row

    # sum < node capacity
    for c in range(nodes_len):
        model.addConstr(gp.quicksum(x[r][c] * blocks_size[r] for r in range(blocks_len)) <= nodes_capacity[c], name='sum_node_cap')

    blocks_weight = util.compute_weights(df_files, blocks_len, co_occurrence_matrix)

    z_tmp = []
    for c in range(nodes_len):
        z_tmp.append(gp.quicksum(x[r][c] * blocks_weight[r] for r in range(blocks_len)))

    z_0 = sum(z_tmp)
    model.setObjective(z_0, GRB.MAXIMIZE)

    z = sum((z_i - np.mean(z_tmp)) ** 2 for z_i in z_tmp) / len(z_tmp)
    model.setObjective(z, GRB.MINIMIZE)
    #model.setObjective(z, GRB.MAXIMIZE)

    # Solve model
    print("\nSolving model...")
    model.Params.TimeLimit = 7200
    #model.Params.SolutionLimit = 1
    model.optimize()

    #if model.status == GRB.Status.OPTIMAL:
    print(x.X)
    util.print_solution('gurobi', df_nodes, df_files, x.X)
    util.print_tmp(df_nodes, df_files, x.X)
    plot.generate_default_map(df_nodes, df_files, x.X, 'gurobi')

