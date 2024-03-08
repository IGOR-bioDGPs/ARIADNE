# -*- coding: utf-8 -*-
"""
Created on Fri Mar  8 11:45:28 2024

@author: Cagatay.Guersoy
"""

import pandas as pd
url="https://raw.githubusercontent.com/IGOR-bioDGPs/ARIADNE/master/testbook/data/data_ariadne_nodes.csv"
df_csv = pd.read_csv(url, on_bad_lines='skip', delimiter=';')
# Select four columns
selected_columns = df_csv.loc[:, ['id', 'mainGraph', 'subgraph', 'href', 'descr']]
selected_columns.dropna(inplace=True)
selected_columns.reset_index(inplace=True)
selected_columns.drop(labels='index', axis=1, inplace=True)
# Save to XLSX
selected_columns.to_excel('ARIADNE_Resources.xlsx', index=False)