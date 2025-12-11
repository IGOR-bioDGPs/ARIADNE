import csv

# Load the CSV file
data = []
with open('data_ariadne_nodes.csv', 'r', encoding='latin-1') as csvfile:
    reader = csv.DictReader(csvfile, delimiter=';')
    for row in reader:
        data.append(row)

# Create a dictionary to store the paths
paths = {}

# Traverse the data and build the paths
for row in data:
    node_label = row['id']
    subgraph = row['subgraphDet']
    is_terminal = row['is_terminal'].strip().lower()
    rank_from_csv = int(row['rank'])

    if is_terminal == 'yes':
        path = []
        current_node = node_label

        while current_node:
            path.append(current_node)
            node_info = next((r for r in data if r['id'] == current_node), None)
            if node_info is None or node_info['subgraphDet'] == 'initial':
                break
            current_node = node_info['subgraphDet']

        paths[node_label] = {
            'path': path[::-1],  # Reverse path to show from 'initial' to node
            'subgraph': subgraph,
        }

# Add paths to each row in data
for row in data:
    node_label = row['id']
    if node_label in paths:
        row['path'] = ' > '.join(paths[node_label]['path'])
    else:
        row['path'] = ''  # Empty path for non-terminal nodes

# Determine the output fieldnames
fieldnames = list(data[0].keys()) + ['path']

# Write the updated data to a new CSV
with open('data_ariadne_nodes.csv', 'w', encoding='latin-1', newline='') as csvfile:
    writer = csv.DictWriter(csvfile, delimiter=';', fieldnames=fieldnames)
    writer.writeheader()
    for row in data:
        writer.writerow(row)

print("Original CSV file 'data_ariadne_nodes.csv' updated with paths successfully.")
