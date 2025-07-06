import csv

def load_nodes(filename='data_ariadne_nodes.csv'):
    data = []
    with open(filename, 'r', encoding='latin-1') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=';')
        for row in reader:
            data.append(row)
    return data

def load_edges(filename='data_ariadne_edges.csv'):
    data = []
    with open(filename, 'r', encoding='latin-1') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=';')
        for row in reader:
            data.append(row)
    return data

def add_node_to_subgraph(data, new_node_info, target_subgraph):
    target_nodes = [row for row in data if row['subgraphDet'] == target_subgraph]
    if not target_nodes:
        print(f"Subgraph '{target_subgraph}' not found!")
        return data, None

    max_rank = max(int(row['rank']) for row in target_nodes)
    new_rank = max_rank + 1

    new_node = {
        'id': new_node_info.get('id', ''),
        'label': new_node_info.get('label', new_node_info.get('id', '')),
        'shape': new_node_info.get('shape', 'ellipse'),
        'bgcolor': new_node_info.get('bgcolor', '#D41159'),
        'fontcolor': new_node_info.get('fontcolor', 'white'),
        'rank': str(new_rank),
        'subgraph': target_subgraph,
        'subgraphDet': target_subgraph,
        'mainGraph': target_nodes[0]['mainGraph'],
        'is_terminal': new_node_info.get('is_terminal', 'yes'),
        'href': new_node_info.get('href', 'NA'),
        'tooltip': new_node_info.get('tooltip', ''),
        'descr': new_node_info.get('descr', ''),
        'openSource': new_node_info.get('openSource', ''),
        'keyQuestions': new_node_info.get('keyQuestions', ''),
        'keyLink': new_node_info.get('keyLink', '')
    }

    data.append(new_node)
    return data, new_node

def add_edge(edges, source, target, subgraph, label='', color='black'):
    # Find the max id and increment
    max_id = max(int(row['id']) for row in edges) if edges else 0
    new_edge = {
        'id': str(max_id + 1),
        'source': source,
        'target': target,
        'subgraph': subgraph,
        'label': label,
        'background-color': color
    }
    edges.append(new_edge)
    return edges

def save_nodes(data, filename='data_ariadne_nodes_updated.csv'):
    if not data:
        return
    fieldnames = list(data[0].keys())
    with open(filename, 'w', encoding='latin-1', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, delimiter=';', fieldnames=fieldnames)
        writer.writeheader()
        for row in data:
            writer.writerow(row)

def save_edges(edges, filename='data_ariadne_edges_updated.csv'):
    if not edges:
        return
    fieldnames = list(edges[0].keys())
    with open(filename, 'w', encoding='latin-1', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, delimiter=';', fieldnames=fieldnames)
        writer.writeheader()
        for row in edges:
            writer.writerow(row)

# Usage example:
def main():
    nodes = load_nodes()
    edges = load_edges()

    # Define new node
    new_tool = {
        'id': 'ResearchGate',
        'label': 'ResearchGate',
        'href': 'https://www.researchgate.net/',
        'tooltip': 'Academic social network for researchers',
        'descr': 'Platform to find and share research papers',
        'openSource': 'FALSE',
        'is_terminal': 'yes'
    }

    # Add node to Literature subgraph
    nodes, new_node = add_node_to_subgraph(nodes, new_tool, 'Literature')

    # Add edge from parent to new node
    if new_node:
        # Find a parent node in the subgraph (e.g., the main node for the subgraph)
        parent_candidates = [row for row in nodes if row['subgraph'] == 'Literature' and row['rank'] == '2']
        parent_id = parent_candidates[0]['id'] if parent_candidates else 'Literature'
        edges = add_edge(edges, parent_id, new_node['id'], 'Literature')

    # Save updated files
    save_nodes(nodes)
    save_edges(edges)
    print("Node and edge added successfully!")

if __name__ == "__main__":
    main()