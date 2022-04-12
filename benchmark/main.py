import os
import solver.read_data as rd
import transfer_time
import execution_time
import cpu_time


path = '..' + os.sep + 'data' + os.sep + '5g-test1'
os.mkdir(path + os.sep + 'benchmark')

df_nodes = rd.get_nodes_data(path)
df_files = rd.get_files_data(path)
df_transfer_time = transfer_time.get_transfer_time(path, df_nodes, df_files)
df_execution_time = execution_time.get_execution_time(path)
df_cpu_time = cpu_time.get_cpu_time(path)

print('')
