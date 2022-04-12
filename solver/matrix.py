import os
import numpy as np
import pandas as pd


def get_history_matrix(df_files, df_query):
    table_list = df_files.fileName.unique()
    history_matrix = pd.DataFrame(np.zeros((len(df_query.index), len(table_list))), columns=table_list)

    for i, query in df_query.iterrows():
        for table in query.tables:
            history_matrix[table][i] = query['count']

    return history_matrix


def get_co_occurrence_matrix(history_matrix):
    co_occurrence_matrix = history_matrix.T.dot(history_matrix)
    np.fill_diagonal(co_occurrence_matrix.values, 0)

    if not os.path.exists("FilesLocation"):
        os.mkdir("FilesLocation")

    co_occurrence_matrix.to_csv('FilesLocation' + os.sep + 'co_occurrence_matrix.csv')
    return co_occurrence_matrix
