'''
    Test adding an entry where the subgraph is new (verify top node creation for nodes, correct node and edge placement).
    Test adding an entry to an existing subgraph (verify correct node and edge placement).
    Test rank validation:
    Valid rank (new_node_rank >= subgraph_effective_rank).
    Invalid rank (new_node_rank < subgraph_effective_rank).
    Test target node validation (target_node_id does not exist).
    Check CSV files manually for correct structure, quoting, and delimiter.
'''
import csv
import argparse

def get_subgraph_effective_rank(subgraph_name: str, all_nodes_data: list) -> str | None:
    """
    Finds the rank of the "top node" of a given subgraph.

    The "top node" is identified as the node where both its 'id' and 'label' 
    fields match the subgraph_name.

    Args:
        subgraph_name (str): The name of the subgraph.
        all_nodes_data (list of dicts): A list of node dictionaries, 
                                         each representing a node.

    Returns:
        str | None: The rank of the top node if found, otherwise None.
    """
    for node in all_nodes_data:
        if node.get('id') == subgraph_name and node.get('label') == subgraph_name:
            return node.get('rank')
    return None

def get_next_edge_id(all_edges_data: list) -> str:
    """
    Returns the next available sequential edge ID
    based on the max numeric ID found in edges.csv.
    Assumes that 'id' column is numeric or can be cast to int.
    """
    try:
        existing_ids = [int(edge['id']) for edge in all_edges_data if edge.get('id', '').isdigit()]
        return str(max(existing_ids) + 1) if existing_ids else "1"
    except Exception as e:
        print(f"Warning: Could not determine next edge ID automatically ({e}). Using '1'.")
        return "1"

def add_graph_entry(new_node_id: str,
                    new_node_label: str,
                    new_node_rank: str,
                    new_node_subgraph: str,
                    target_node_id: str,
                    new_edge_label: str = '',
                    node_shape: str = 'ellipse',
                    node_bgcolor: str = '#D41159',
                    node_fontcolor: str = 'white',
                    node_is_terminal: str = 'no',
                    node_href: str = 'NA',
                    node_tooltip: str = '',
                    node_descr: str = 'NA',
                    node_openSource: str = 'TRUE',
                    node_keyQuestions: str = '',
                    node_keyLink: str = 'NA',
                    node_mainGraph: str = '',
                    edge_background_color: str = 'black'):
    """
    Adds a new node and potentially an edge to the Ariadne graph data.
    """
    nodes_filepath = 'data_ariadne_nodes.csv'
    edges_filepath = 'data_ariadne_edges.csv'

    # Read nodes
    all_nodes_data = []
    original_headers_nodes = []
    try:
        with open(nodes_filepath, mode='r', newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file, delimiter=';')
            original_headers_nodes = reader.fieldnames  # Preserve original column order
            all_nodes_data = list(reader)
    except FileNotFoundError:
        print(f"Error: Nodes file not found at {nodes_filepath}. Cannot add new node.")
        return

    # Check if node already exists
    if any(node['id'] == new_node_id for node in all_nodes_data):
        print(f"Node with ID '{new_node_id}' already exists. Skipping addition.")
        return

    # Handle subgraph
    effective_rank_of_subgraph = get_subgraph_effective_rank(new_node_subgraph, all_nodes_data)
    if new_node_subgraph and effective_rank_of_subgraph is None:
        print(f"Subgraph '{new_node_subgraph}' does not exist. Creating a new top node for it.")
        if not any(node['id'] == new_node_subgraph for node in all_nodes_data):
            new_top_node = {
                'id': new_node_subgraph,
                'label': new_node_subgraph,
                'shape': 'diamond',
                'bgcolor': '#40B0A6',
                'fontcolor': 'white',
                'rank': new_node_rank,
                'subgraph': new_node_subgraph,
                'mainGraph': node_mainGraph,
                'is_terminal': 'no',
                'href': 'NA',
                'tooltip': f"Top node for subgraph {new_node_subgraph}",
                'descr': 'NA',
                'openSource': 'TRUE',
                'keyQuestions': '',
                'keyLink': 'NA'
            }
            all_nodes_data.append(new_top_node)

    # Add new node
    new_node = {
        'id': new_node_id,
        'label': new_node_label,
        'rank': new_node_rank,
        'subgraph': new_node_subgraph,
        'shape': node_shape,
        'bgcolor': node_bgcolor,
        'fontcolor': node_fontcolor,
        'mainGraph': node_mainGraph,
        'is_terminal': node_is_terminal,
        'href': node_href,
        'tooltip': node_tooltip,
        'descr': node_descr,
        'openSource': node_openSource,
        'keyQuestions': node_keyQuestions,
        'keyLink': node_keyLink
    }
    all_nodes_data.append(new_node)

    # Write nodes to CSV
    with open(nodes_filepath, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=original_headers_nodes, delimiter=';', extrasaction='ignore')
        writer.writeheader()
        writer.writerows(all_nodes_data)

    # Read edges
    all_edges_data = []
    original_headers_edges = []
    try:
        with open(edges_filepath, mode='r', newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file, delimiter=';')
            original_headers_edges = reader.fieldnames  # Preserve original column order
            all_edges_data = list(reader)
    except FileNotFoundError:
        print(f"Info: Edges file not found at {edges_filepath}. Will create a new one.")

    # Add edge
    if not any(edge['source'] == new_node_id and edge['target'] == target_node_id for edge in all_edges_data):
        new_edge_id = get_next_edge_id(all_edges_data)
        new_edge = {
            'id': new_edge_id,
            'source': new_node_id,
            'target': target_node_id,
            'subgraph': new_node_subgraph,
            'label': new_edge_label,
            'background-color': edge_background_color
        }
        all_edges_data.append(new_edge)

    # Write edges to CSV
    with open(edges_filepath, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=original_headers_edges, delimiter=';', extrasaction='ignore')
        writer.writeheader()
        writer.writerows(all_edges_data)

    print(f"Node '{new_node_id}' and edge added successfully.")