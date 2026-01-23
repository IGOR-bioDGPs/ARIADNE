# -*- coding: utf-8 -*-
"""
Created on Fri Mar  8 11:45:28 2024

@author: Cagatay.Guersoy
"""
import os
from osfclient import OSF
import pandas as pd

## First convert CSV to XLSX
url="https://raw.githubusercontent.com/IGOR-bioDGPs/ARIADNE/master/ariadne/data/data_ariadne_nodes.csv"
df_csv = pd.read_csv(url, on_bad_lines='skip', delimiter=';', encoding = "ISO-8859-1")
# Select four columns
selected_columns = df_csv.loc[:, ['id', 'mainGraph', 'subgraph', 'href', 'descr']]
selected_columns.dropna(inplace=True)
selected_columns.reset_index(inplace=True)
selected_columns.drop(labels='index', axis=1, inplace=True)
# Save to XLSX
selected_columns.to_excel('ARIADNE_Resources.xlsx', index=False)

## Now the OSF stuff
# Get token from environment variable
token = os.environ.get('OSF_TOKEN')
if not token:
    raise ValueError("OSF_TOKEN environment variable not set")

# Initialize OSF client with token
osf = OSF(token=token)

# Configuration
PROJECT_ID = 'tqjh8'
LOCAL_FILE = 'ARIADNE_Resources.xlsx'
REMOTE_PATH = '2023 ARIADNE/ARIADNE Resources.xlsx'

# Get your project
project = osf.project(PROJECT_ID)

# Get the storage (osfstorage is the default)
storage = project.storage('Osfstorage')

# Upload/update the file (creates new version automatically)
print(f"Uploading {LOCAL_FILE} to {REMOTE_PATH}...")
with open(LOCAL_FILE, 'rb') as fp:
    # Pass the local file path, not the remote path
    storage.create_file(REMOTE_PATH, fp, update=True, force=True)

print("Upload successful! New version created.")
