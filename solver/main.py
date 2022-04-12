import read_data
import matrix
import model_cplex
import model_gurobi
import model_pulp
import plot
import os

path = '..' + os.sep + 'data' + os.sep + '5g-test1'

df_nodes = read_data.get_nodes_data(path)
df_files = read_data.get_files_data(path)
df_query = read_data.get_queries_data(path)

df_blocks_loc = read_data.get_default_blocks_locations(path, df_nodes)
plot.generate_default_map(df_nodes, df_files, df_blocks_loc, 'default')

history_matrix = matrix.get_history_matrix(df_files, df_query)
co_occurrence_matrix = matrix.get_co_occurrence_matrix(history_matrix)

model_cplex.build_model(df_nodes, df_files, co_occurrence_matrix)
model_gurobi.build_model(df_nodes, df_files, co_occurrence_matrix)
model_pulp.build_model(df_nodes, df_files, co_occurrence_matrix)
