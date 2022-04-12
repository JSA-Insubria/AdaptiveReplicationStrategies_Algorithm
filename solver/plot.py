import os
import pandas as pd
import plotly.express as px


def generate_default_map(df_nodes, df_files, df_blocks_loc, name):
    if name != 'default':
        df_blocks_loc = pd.DataFrame(df_blocks_loc, columns=df_nodes.name)
        df_blocks_loc.insert(loc=0, column='fileName', value=df_files.fileName + '.tbl')

    df_actual = df_blocks_loc.groupby("fileName").sum()
    fig = px.imshow(df_actual.T, labels=dict(x="File", y="Nodes"), x=df_actual.index, y=df_actual.columns)

    if not os.path.exists("images"):
        os.mkdir("images")

    fig.write_html('images' + os.sep + name + '.html')
