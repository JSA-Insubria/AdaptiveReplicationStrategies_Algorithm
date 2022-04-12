import numpy as np
import pandas as pd
import json
import glob
import os


# Nodes_ Fields: ipAddr - hostName - name - datanodeUuid - networkLocation - capacity - dfsUsed - nonDfsUsed - remaining
def get_nodes_data(path):
    to_read = glob.glob(path + os.sep + 'system-info' + os.sep + 'results' + os.sep + 'namenode' + os.sep +
                        'ClusterInfo' + os.sep + '*.json')
    node_json = []
    for i in to_read:
        tmp = json.load(open(i))
        data = {
            'ipAddr': tmp['ipAddr'], 'hostName': tmp['hostName'], 'name': tmp['name'],
            'datanodeUuid': tmp['datanodeUuid'], 'networkLocation': tmp['networkLocation'],
            'capacity': (tmp['capacity']/(1024**2)), 'dfsUsed': tmp['dfsUsed'],
            'nonDfsUsed': tmp['nonDfsUsed'], 'remaining': tmp['remaining']
        }
        node_json.append(pd.json_normalize(data))

    return pd.concat(node_json, axis=0, ignore_index=True)


def get_files_data(path):
    # Files_ Fields: fileName - filePath - fileSize - blockLocations(blockId) - blockLocations(blockLocation(hosts)) -
    # blockLocations(blockLocation(names)) - blockLocations(blockLocation(length))
    to_read = glob.glob(path + os.sep + 'system-info' + os.sep + 'results' + os.sep + 'namenode' + os.sep +
                        'FilesInfo' + os.sep + '*.json')
    file_json = []
    for i in to_read:
        tmp = json.load(open(i))
        block_locations = tmp['blockLocations']
        block_list = []
        for block in block_locations:
            block_data = {
                'fileName': tmp['fileName'],
                'filePath': tmp['filePath'],
                'fileSize': tmp['fileSize'],
                'blockId': block['blockId'],
                'hosts': block['blockLocation']['hosts'],
                'names': block['blockLocation']['names'],
                'length': (block['blockLocation']['length']/(1024**2))
            }
            block_list.append(block_data)

        file_json.append(pd.json_normalize(block_list))

    return pd.concat(file_json, axis=0, ignore_index=True)


def get_default_blocks_locations(path, df_nodes):
    columns = df_nodes.name.to_list()
    to_read = glob.glob(path + os.sep + 'system-info' + os.sep + 'results' + os.sep + 'namenode' + os.sep +
                        'FilesInfo' + os.sep + '*.json')
    df = pd.DataFrame(columns=['fileName'] + columns)
    for i in to_read:
        tmp = json.load(open(i))
        block_locations = tmp['blockLocations']
        for block in block_locations:
            node_list = [tmp['fileName'] + '.tbl']
            for node in columns:
                if node in block['blockLocation']['names']:
                    node = 1
                else:
                    node = 0
                node_list.append(node)

            df = pd.concat([df, pd.DataFrame([node_list], columns=['fileName'] + columns)])

    return df


def get_queries_data(path):
    query_json = []
    n_query = len(glob.glob(path + os.sep + 'Q*_1' + os.sep))
    for i in range(1, n_query+1):
        tmp = json.load(open(glob.glob(path + os.sep + 'Q' + str(i) + '_' + '1' + os.sep + 'results' + os.sep +
                                       'namenode' + os.sep + 'QueryDataBlocks' + os.sep + '*.json')[0]))
        query_table_list = []
        for table in tmp['tableList']:
            query_table_list.append(table['tableName'].split('.')[-1])

        query_data = {
            'query': tmp['query'],
            'count': len(glob.glob(path + os.sep + 'Q' + str(i) + '_' + '*' + os.sep)),
            'tables': query_table_list
        }
        query_json.append(pd.json_normalize(query_data))

    return pd.concat(query_json, axis=0, ignore_index=True)
