import glob
import numpy as np
import pandas as pd
import os

path = ''


def get_query_execution_time():
    n_query = len(glob.glob(path + os.sep + 'Q*_1' + os.sep))
    execution_time = []
    for query in range(1, n_query+1):
        execution_time.append(pd.json_normalize({'query': query, 'time': get_sub_query_time(query)}))

    return execution_time


def get_sub_query_time(query):
    n_sub_query = len(glob.glob(path + os.sep + 'Q' + str(query) + '_' + '*' + os.sep))
    data = []
    for sub_query in range(1, n_sub_query+1):
        file = get_query_execution_time_file_content(query, sub_query)
        for line in file:
            if 'hadoop' in line:
                data.append(float(line.split()[1]))

    return np.mean(data)


def get_query_execution_time_file_content(query, sub_query):
    file_to_open = '' + path + os.sep + 'Q' + str(query) + '_' + str(sub_query) +\
                   os.sep + 'results' + os.sep + 'namenode' + os.sep + 'QueryExecutionTime.log' + ''
    with open(file_to_open) as file:
        file = file.readlines()

    return file


def get_execution_time(data_path):
    global path
    path = data_path

    execution_time = get_query_execution_time()
    df_execution_time = pd.concat(execution_time, axis=0, ignore_index=True)
    df_execution_time.set_index('query', inplace=True)
    df_execution_time.to_csv(path + os.sep + 'benchmark' + os.sep + 'execution_time.csv', sep=',', encoding='utf-8')
    return df_execution_time
