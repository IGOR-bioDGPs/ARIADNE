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

# Placeholder for the new unified function
def add_graph_entry(new_node_id: str,
                    new_node_label: str,
                    new_node_rank: str,
                    new_node_subgraph: str,
                    target_node_id: str,
                    new_edge_id: str, # Will be used in next step
                    new_edge_label: str = '', # Will be used in next step
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
                    node_mainGraph: str = '', # Added as per detailed plan
                    edge_background_color: str = 'black' # for signature, used in next step
                    ):
    """
    Adds a new node and potentially an edge to the Ariadne graph data.
    Currently, only node addition logic is fully implemented.
    """
    nodes_filepath = 'ariadne/data/data_ariadne_nodes.csv'
    all_nodes_data = []
    original_headers_nodes = ['id', 'label', 'shape', 'bgcolor', 'fontcolor', 'rank', 'subgraph', 'mainGraph', 'is_terminal', 'href', 'tooltip', 'descr', 'openSource', 'keyQuestions', 'keyLink']

    # 3. Read Nodes Data
    try:
        with open(nodes_filepath, mode='r', newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file, delimiter=';')
            if reader.fieldnames:
                original_headers_nodes = reader.fieldnames
            all_nodes_data = list(reader)
    except FileNotFoundError:
        print(f"Error: Nodes file not found at {nodes_filepath}. Cannot add new node.")
        # If the file doesn't exist, we might allow creating it, 
        # but for now, let's assume it must exist if target_node_id is specified.
        # If target_node_id is also meant to be optional for an initial graph, this needs adjustment.
        return
    except Exception as e:
        print(f"Error reading {nodes_filepath}: {e}")
        return

    # 4. Target Node Validation
    target_node_exists = any(node['id'] == target_node_id for node in all_nodes_data)
    if not target_node_exists and target_node_id is not None: # Assuming target_node_id can be None if no edge is to be created
        print(f"Error: Target node with ID '{target_node_id}' not found. Cannot create edge.")
        # If only adding a node without an edge, this check might be skipped or target_node_id could be optional.
        # For now, assuming if target_node_id is provided, it must exist for a potential future edge.
        # If the primary goal is just to add a node, this error might be too strict.
        # Let's proceed with node addition even if target is not found, but print a warning.
        # This will be revisited when edge logic is added.
        print(f"Warning: Target node ID '{target_node_id}' provided but not found. Proceeding with node addition only.")


    # 5. Subgraph and Top Node Handling
    effective_rank_of_subgraph = get_subgraph_effective_rank(new_node_subgraph, all_nodes_data)
    subgraph_exists = effective_rank_of_subgraph is not None
    new_top_node_dict = None

    if new_node_subgraph and not subgraph_exists: # Ensure new_node_subgraph is not empty
        print(f"Subgraph '{new_node_subgraph}' does not exist. Creating a new top node for it.")
        new_top_node_dict = {
            'id': new_node_subgraph,
            'label': new_node_subgraph,
            'shape': 'diamond',
            'bgcolor': '#40B0A6',
            'fontcolor': 'white',
            'rank': new_node_rank, # Use the rank of the new node being added
            'subgraph': new_node_subgraph, # Top node belongs to its own subgraph name
            'mainGraph': node_mainGraph if node_mainGraph else '', # Or determine based on context
            'is_terminal': 'no',
            'href': 'NA',
            'tooltip': f"Top node for subgraph {new_node_subgraph}",
            'descr': 'NA',
            'openSource': 'TRUE',
            'keyQuestions': '',
            'keyLink': 'NA'
        }
        effective_rank_of_subgraph = new_node_rank # For validation against the actual new node
    
    # 6. Rank Validation for the New Actual Node
    if new_node_subgraph: # Only validate rank if subgraph is specified
        try:
            if int(new_node_rank) < int(effective_rank_of_subgraph):
                print(f"Error: New node rank ({new_node_rank}) cannot be less than the subgraph's effective rank ({effective_rank_of_subgraph}).")
                return
        except ValueError:
            print("Error: Node rank and subgraph effective rank must be integers for comparison.")
            return

    # 7. New Node Dictionary Creation
    new_node_dict = {
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

    # 8. Node Insertion Strategy
    if new_top_node_dict:
        all_nodes_data.append(new_top_node_dict) # Simple append for now

    insert_index_node = len(all_nodes_data) # Default to appending at the end
    if new_node_subgraph: # Only try to insert intelligently if a subgraph is specified
        # Iterate to find the last node of the same subgraph to insert after
        for i in range(len(all_nodes_data) -1, -1, -1): # Iterate backwards
            if all_nodes_data[i].get('subgraph') == new_node_subgraph:
                # If we find the new top node we just added, insert the actual new node after it
                if new_top_node_dict and all_nodes_data[i]['id'] == new_top_node_dict['id']:
                    insert_index_node = i + 1
                    break
                # If it's another node in the same subgraph, insert after it
                elif not new_top_node_dict or (new_top_node_dict and all_nodes_data[i]['id'] != new_top_node_dict['id']):
                    insert_index_node = i + 1
                    break
        # If the only node of this subgraph is the new top node, this logic correctly inserts after it.
        # If no nodes of this subgraph are found (e.g. new_top_node_dict was None and subgraph didn't exist before)
        # it will append to the end, which is acceptable for now.
    
    all_nodes_data.insert(insert_index_node, new_node_dict)


    # 9. Rewrite Nodes CSV
    try:
        with open(nodes_filepath, mode='w', newline='', encoding='utf-8') as file:
            # Ensure all keys present in any dictionary in all_nodes_data are in headers
            # This handles cases where new_top_node_dict or new_node_dict might have keys not in original_headers_nodes
            # However, for consistency, it's better to stick to a predefined set of headers.
            # Let's use original_headers_nodes, assuming they cover all necessary fields.
            # If new fields were dynamically added, original_headers_nodes should be updated.
            
            # Re-evaluate headers: take all keys from all dicts to be safe for DictWriter
            # This is safer if nodes can have variable fields.
            # However, the prompt implies a fixed structure for nodes.csv.
            # Let's stick to the defined headers and ensure all dicts conform.
            current_headers = original_headers_nodes[:] # Make a copy

            # Check if all dicts have all necessary keys, fill with default if not, or ensure they do before writing.
            # For simplicity, assume all_nodes_data dictionaries will conform to original_headers_nodes.
            # If a new key was added (e.g. 'mainGraph' if it wasn't there), it should be in original_headers_nodes.

            writer = csv.DictWriter(file, fieldnames=current_headers, delimiter=';', extrasaction='ignore')
            writer.writeheader()
            writer.writerows(all_nodes_data)
        print(f"Node '{new_node_id}' (and potentially top node for subgraph '{new_node_subgraph}') added successfully to {nodes_filepath}.")
    except Exception as e:
        print(f"Error writing to {nodes_filepath}: {e}")
        return
    print("Node handling complete.")

    # 1. File Path for Edges
    edges_filepath = 'ariadne/data/data_ariadne_edges.csv'
    all_edges_data = []
    # Define headers for edges CSV
    original_headers_edges = ['id', 'source', 'target', 'subgraph', 'label', 'background-color']

    # 2. Read Edges Data
    if target_node_id and new_edge_id: # Only proceed if an edge is intended
        try:
            with open(edges_filepath, mode='r', newline='', encoding='utf-8') as file:
                reader = csv.DictReader(file, delimiter=';')
                if reader.fieldnames: # Check if file is not empty and has headers
                    original_headers_edges = reader.fieldnames
                all_edges_data = list(reader)
        except FileNotFoundError:
            print(f"Info: Edges file not found at {edges_filepath}. Will create a new one.")
            # If the file doesn't exist, all_edges_data remains empty, and a new file will be created.
        except Exception as e:
            print(f"Error reading {edges_filepath}: {e}")
            return # Stop if there's an error reading existing edges

        # 3. New Edge Dictionary Creation
        new_edge_dict = {
            'id': new_edge_id,
            'source': new_node_id,
            'target': target_node_id,
            'subgraph': new_node_subgraph, # Edge belongs to the same subgraph as the new node
            'label': new_edge_label,
            'background-color': edge_background_color
        }

        # 4. Edge Insertion Strategy
        insert_index_edge = len(all_edges_data) # Default to appending
        if new_node_subgraph: # Only try to insert intelligently if a subgraph is specified for the edge
            for i in range(len(all_edges_data) -1, -1, -1): # Iterate backwards
                if all_edges_data[i].get('subgraph') == new_node_subgraph:
                    insert_index_edge = i + 1
                    break 
        all_edges_data.insert(insert_index_edge, new_edge_dict)

        # 5. Rewrite Edges CSV
        try:
            with open(edges_filepath, mode='w', newline='', encoding='utf-8') as file:
                # Use the dynamically read or default headers
                current_edge_headers = original_headers_edges[:]
                # Ensure all keys from new_edge_dict are in headers if they were not in the original file.
                # This is important if the file was empty or had fewer columns.
                for key in new_edge_dict.keys():
                    if key not in current_edge_headers:
                        current_edge_headers.append(key)
                
                writer = csv.DictWriter(file, fieldnames=current_edge_headers, delimiter=';', extrasaction='ignore')
                writer.writeheader()
                writer.writerows(all_edges_data)
            print(f"Edge '{new_edge_id}' added successfully to {edges_filepath}.")
        except Exception as e:
            print(f"Error writing to {edges_filepath}: {e}")
            return
    elif not target_node_id or not new_edge_id:
        print("Skipping edge creation as target_node_id or new_edge_id was not provided.")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Add a new graph entry (node and connecting edge) to Ariadne CSV data files.')

    # Required arguments
    parser.add_argument('new_node_id', help="ID for the new node")
    parser.add_argument('new_node_label', help="Label for the new node")
    parser.add_argument('new_node_rank', help="Rank for the new node")
    parser.add_argument('new_node_subgraph', help="Subgraph for the new node and its edge")
    parser.add_argument('target_node_id', help="ID of the existing node to connect the new node to")
    parser.add_argument('new_edge_id', help="ID for the new edge")

    # Optional arguments for the node
    parser.add_argument('--node-shape', default='ellipse', help="Shape for the new node (default: 'ellipse')")
    parser.add_argument('--node-bgcolor', default='#D41159', help="Background color for the new node (default: '#D41159')")
    parser.add_argument('--node-fontcolor', default='white', help="Font color for the new node (default: 'white')")
    parser.add_argument('--node-mainGraph', default='', help="MainGraph for the new node (default: '')")
    parser.add_argument('--node-is_terminal', default='no', help="Is the new node terminal? (yes/no) (default: 'no')")
    parser.add_argument('--node-href', default='NA', help="Hyperlink for the new node (default: 'NA')")
    parser.add_argument('--node-tooltip', default='', help="Tooltip for the new node (default: '')")
    parser.add_argument('--node-descr', default='NA', help="Description for the new node (default: 'NA')")
    parser.add_argument('--node-openSource', default='TRUE', help="Open source status for the new node (TRUE/FALSE/HYBRID/NA) (default: 'TRUE')")
    parser.add_argument('--node-keyQuestions', default='', help="Key questions for the new node (default: '')")
    parser.add_argument('--node-keyLink', default='NA', help="Key questions link for the new node (default: 'NA')")

    # Optional arguments for the edge
    parser.add_argument('--edge-label', default='', help="Label for the new edge (default: '')")
    parser.add_argument('--edge-background-color', default='black', help="Background color for the new edge (default: 'black')")

    args = parser.parse_args()

    add_graph_entry(
        new_node_id=args.new_node_id,
        new_node_label=args.new_node_label,
        new_node_rank=args.new_node_rank,
        new_node_subgraph=args.new_node_subgraph,
        target_node_id=args.target_node_id,
        new_edge_id=args.new_edge_id,
        new_edge_label=args.edge_label,
        node_shape=args.node_shape,
        node_bgcolor=args.node_bgcolor,
        node_fontcolor=args.node_fontcolor,
        node_is_terminal=args.node_is_terminal,
        node_href=args.node_href,
        node_tooltip=args.node_tooltip,
        node_descr=args.node_descr,
        node_openSource=args.node_openSource,
        node_keyQuestions=args.node_keyQuestions,
        node_keyLink=args.node_keyLink,
        node_mainGraph=args.node_mainGraph,
        edge_background_color=args.edge_background_color
    )

    print(f"Graph entry for node '{args.new_node_id}' and edge '{args.new_edge_id}' processed.")
