import pandas as pd
import numpy as np
import os


def get_cluster_setting(df_nodes, df_files):
    nodes_len = int(len(df_nodes.index))
    blocks_len = int(len(df_files.index))

    nodes_capacity = (df_nodes.capacity.div(2.5))[0:nodes_len].astype(int).to_list()
    blocks_size = df_files.length[0:blocks_len].astype(int).to_list()
    return nodes_len, blocks_len, nodes_capacity, blocks_size


def compute_weights(df_files, blocks_len, co_occurrence_matrix):
    # compute weights
    df_weight = pd.DataFrame(data={'fileName': df_files.fileName[0:blocks_len], 'weight': np.zeros(blocks_len)})
    for table in df_files[0:blocks_len].fileName.unique():
        df_weight.loc[df_weight['fileName'] == table, 'weight'] = sum(co_occurrence_matrix[table])

    return df_weight.weight.astype(int).to_numpy()


def print_solution(model, df_nodes, df_files, sol):
    if not os.path.exists("FilesLocation"):
        os.mkdir("FilesLocation")

    df_sol = pd.DataFrame(sol, columns=df_nodes.name)
    df_sol.insert(loc=0, column='block_table', value=df_files.fileName + '.tbl')
    
    df_sol.to_csv('FilesLocation' + os.sep + 'sol_' + model + '.csv')

    df_sol = df_sol.where(df_sol != 1, df_sol.columns.to_series(), axis=1)

    df_str = df_sol.to_string(header=False, index=False).split('\n')
    if model == 'cplex':
        df_str_sep = [','.join(e.replace(' 0', '').replace('0 ', '').split()) for e in df_str]
    else:
        df_str_sep = [','.join(e.replace(' 0.0', '').replace('0.0 ', '').split()) for e in df_str]

    file = open('FilesLocation' + os.sep + 'FilesLocation_' + model + '.txt', 'w')
    for e in df_str_sep:
        file.write(e + '\n')

    file.close()


def print_tmp(df_nodes, df_files, sol):
    df_sol = pd.DataFrame(sol, columns=df_nodes.name)
    df_sol.insert(loc=0, column='block_id', value=df_files.blockId)
    df_sol.insert(loc=1, column='block_size', value=df_files.length)
    df_sol.insert(loc=2, column='block_table', value=df_files.fileName + '.tbl')
    df_sol.set_index('block_id', inplace=True)
    print(df_sol)
