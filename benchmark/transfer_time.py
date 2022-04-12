import glob
import pandas as pd
import os

path = ''


def get_hdfs_read_data(n_nodes, blocks_list):
    n_query = len(glob.glob(path + os.sep + 'Q*_1' + os.sep))
    hdfs_read = []
    for query in range(1, n_query+1):
        hdfs_read.append({'query': query, 'data': check_sub_query(query, n_nodes, blocks_list)})

    return hdfs_read


def check_sub_query(query, n_nodes, blocks_list):
    data = []
    n_sub_query = len(glob.glob(path + os.sep + 'Q' + str(query) + '_' + '*' + os.sep))
    for sub_query in range(1, n_sub_query+1):
        for node in range(1, n_nodes+1):
            file = get_hdfs_read_file_content(query, sub_query, node)
            for line in file:
                if 'NONMAPREDUCE' not in line:
                    block = get_block(line, blocks_list)
                    if block is not None:
                        if block['src'] != block['dest']:
                            data.append(block)

    return data


def get_hdfs_read_file_content(query, sub_query, node):
    file_to_open = '' + path + os.sep + 'Q' + str(query) + '_' + str(sub_query) + os.sep + 'nodes_results' + os.sep +\
                   'node-' + str(node) + os.sep + 'q' + str(sub_query) + os.sep + 'hdfs_read.log' + ''
    with open(file_to_open) as file:
        file = file.readlines()

    return file


def get_block(line, blocks_list):
    fields = line.split(',')
    block = fields[-2].split(':')[2]
    if block in blocks_list:
        return {
            'src': fields[0].split(':')[1].strip(),
            'dest': fields[1].split(':')[1].strip(),
            'bytes': fields[2].split(':')[1].strip(),
            'block': block.strip(),
            'duration': fields[-1].split(':')[1].strip(),
        }
    else:
        return None


def print_transfer_time(hdfs_read):
    transfer_time = []
    for read in hdfs_read:
        bytes_sum = 0
        duration_sum = 0
        count = 0

        for move in read['data']:
            bytes_sum += int(move['bytes'])
            duration_sum += int(move['duration'])
            count += 1

        data = {
            "query": read['query'],
            "bytes": bytes_sum,
            "duration": duration_sum,
            "n_moved_blocks": count
        }
        transfer_time.append(pd.json_normalize(data))

    return pd.concat(transfer_time, axis=0, ignore_index=True)


def get_transfer_time(data_path, df_nodes, df_files):
    global path
    path = data_path

    n_nodes = int(len(df_nodes.index))
    blocks_list = df_files.blockId.to_list()
    hdfs_read = get_hdfs_read_data(n_nodes, blocks_list)
    df_transfer_time = print_transfer_time(hdfs_read)
    df_transfer_time.set_index('query', inplace=True)
    df_transfer_time.to_csv(path + os.sep + 'benchmark' + os.sep + 'transfer_time.csv', sep=',', encoding='utf-8')
    return df_transfer_time
