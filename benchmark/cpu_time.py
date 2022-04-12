import glob
import numpy as np
import pandas as pd
import os

path = ''


def get_query_cpu_time():
    n_query = len(glob.glob(path + os.sep + 'Q*_1' + os.sep))
    cpu_time = []
    for query in range(1, n_query+1):
        cpu_time.append(pd.json_normalize({'query': query, 'time': get_sub_query_time(query)}))

    return cpu_time


def get_sub_query_time(query):
    n_sub_query = len(glob.glob(path + os.sep + 'Q' + str(query) + '_' + '*' + os.sep))
    data = []
    for sub_query in range(1, n_sub_query+1):
        file = get_query_cpu_time_file_content(query, sub_query)
        for line in file:
            if 'CPU:' in line:
                data.append(float(line.split(',')[0].split(':')[1]))

    return np.mean(data)


def get_query_cpu_time_file_content(query, sub_query):
    file_to_open = '' + path + os.sep + 'Q' + str(query) + '_' + str(sub_query) +\
                   os.sep + 'results' + os.sep + 'namenode' + os.sep + 'QueryCPUTime.log' + ''
    with open(file_to_open) as file:
        file = file.readlines()

    return file


def get_cpu_time(data_path):
    global path
    path = data_path

    cpu_time = get_query_cpu_time()
    df_cpu_time = pd.concat(cpu_time, axis=0, ignore_index=True)
    df_cpu_time.set_index('query', inplace=True)
    df_cpu_time.to_csv(path + os.sep + 'benchmark' + os.sep + 'cpu_time.csv', sep=',', encoding='utf-8')
    return df_cpu_time
