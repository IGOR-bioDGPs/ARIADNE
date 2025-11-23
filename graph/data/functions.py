"""
ARIADNE Graph Data Management Functions
---------------------------------------
This module provides functions for managing nodes and edges in a graph-based network
with multiple layers of subgraphs. The CSV files maintain a hierarchical structure
where nodes represent resources and edges represent connections between them.
"""

import csv
from typing import Optional, List, Dict, Tuple


def load_csv_data(filepath: str, delimiter: str = ';') -> Tuple[List[Dict], List[str]]:
    """
    Load CSV data and return both data rows and headers.
    
    Args:
        filepath: Path to the CSV file
        delimiter: CSV delimiter (default: ';')
        
    Returns:
        Tuple of (data rows as list of dicts, header field names)
    """
    try:
        with open(filepath, mode='r', newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file, delimiter=delimiter)
            headers = reader.fieldnames
            data = list(reader)
        return data, headers
    except FileNotFoundError:
        print(f"Warning: File not found at {filepath}. Returning empty data.")
        return [], []


def save_csv_data(filepath: str, data: List[Dict], headers: List[str], delimiter: str = ';'):
    """
    Save data to CSV file while preserving structure.
    
    Args:
        filepath: Path to the CSV file
        data: List of dictionaries containing row data
        headers: List of column headers
        delimiter: CSV delimiter (default: ';')
    """
    with open(filepath, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=headers, delimiter=delimiter, extrasaction='ignore')
        writer.writeheader()
        writer.writerows(data)


def get_available_subgraphs(nodes_filepath: str = 'data_ariadne_nodes.csv') -> List[str]:
    """
    Get list of all available subgraphs from the nodes file.
    
    Returns:
        List of unique subgraph names
    """
    all_nodes_data, _ = load_csv_data(nodes_filepath)
    subgraphs = sorted(set(node.get('subgraph', '') for node in all_nodes_data if node.get('subgraph')))
    return [sg for sg in subgraphs if sg]


def get_subgraph_details(subgraph_name: str, nodes_filepath: str = 'data_ariadne_nodes.csv') -> Optional[Dict]:
    """
    Get details about a specific subgraph.
    
    Args:
        subgraph_name: Name of the subgraph
        nodes_filepath: Path to nodes CSV file
        
    Returns:
        Dictionary with subgraph details or None if not found
    """
    all_nodes_data, _ = load_csv_data(nodes_filepath)
    
    for node in all_nodes_data:
        if node.get('id') == subgraph_name and node.get('label') == subgraph_name:
            return {
                'name': subgraph_name,
                'rank': node.get('rank'),
                'mainGraph': node.get('mainGraph'),
                'shape': node.get('shape'),
                'bgcolor': node.get('bgcolor')
            }
    return None


def get_nodes_in_subgraph(subgraph_name: str, nodes_filepath: str = 'data_ariadne_nodes.csv') -> List[Dict]:
    """
    Get all nodes that belong to a specific subgraph.
    
    Args:
        subgraph_name: Name of the subgraph
        nodes_filepath: Path to nodes CSV file
        
    Returns:
        List of nodes in the subgraph
    """
    all_nodes_data, _ = load_csv_data(nodes_filepath)
    return [node for node in all_nodes_data if node.get('subgraph') == subgraph_name]


def get_subgraph_effective_rank(subgraph_name: str, all_nodes_data: List[Dict]) -> Optional[str]:
    """
    Finds the rank of the "top node" of a given subgraph.
    The "top node" is identified as the node where both its 'id' and 'label' 
    fields match the subgraph_name.
    
    Args:
        subgraph_name: The name of the subgraph
        all_nodes_data: A list of node dictionaries
        
    Returns:
        The rank of the top node if found, otherwise None
    """
    for node in all_nodes_data:
        if node.get('id') == subgraph_name and node.get('label') == subgraph_name:
            return node.get('rank')
    return None


def get_next_edge_id(all_edges_data: List[Dict]) -> str:
    """
    Returns the next available sequential edge ID based on the max numeric ID found in edges.csv.
    
    Args:
        all_edges_data: List of edge dictionaries
        
    Returns:
        Next available edge ID as string
    """
    try:
        existing_ids = [int(edge['id']) for edge in all_edges_data if edge.get('id', '').isdigit()]
        return str(max(existing_ids) + 1) if existing_ids else "1"
    except Exception as e:
        print(f"Warning: Could not determine next edge ID automatically ({e}). Using '1'.")
        return "1"


def node_exists(node_id: str, nodes_data: List[Dict]) -> bool:
    """
    Check if a node with the given ID already exists.
    
    Args:
        node_id: ID of the node to check
        nodes_data: List of node dictionaries
        
    Returns:
        True if node exists, False otherwise
    """
    return any(node['id'] == node_id for node in nodes_data)


def validate_node_data(new_node_id: str, new_node_rank: str, subgraph_name: str, 
                      target_node_id: str, all_nodes_data: List[Dict]) -> Tuple[bool, str]:
    """
    Validate node data before adding to the graph.
    
    Args:
        new_node_id: ID for the new node
        new_node_rank: Rank for the new node
        subgraph_name: Subgraph the node belongs to
        target_node_id: ID of the target node to connect to
        all_nodes_data: List of all existing nodes
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    # Check if node already exists
    if node_exists(new_node_id, all_nodes_data):
        return False, f"Node with ID '{new_node_id}' already exists."
    
    # Check if target node exists
    if not node_exists(target_node_id, all_nodes_data):
        return False, f"Target node '{target_node_id}' does not exist."
    
    # Validate rank if subgraph exists
    effective_rank = get_subgraph_effective_rank(subgraph_name, all_nodes_data)
    if effective_rank is not None:
        try:
            if int(new_node_rank) < int(effective_rank):
                return False, f"New node rank ({new_node_rank}) must be >= subgraph rank ({effective_rank})."
        except ValueError:
            return False, f"Invalid rank value: {new_node_rank}"
    
    return True, ""


def create_top_node_for_subgraph(subgraph_name: str, rank: str, main_graph: str) -> Dict:
    """
    Create a top node (diamond-shaped category node) for a new subgraph.
    
    Args:
        subgraph_name: Name of the new subgraph
        rank: Rank for the top node
        main_graph: Main graph this subgraph belongs to
        
    Returns:
        Dictionary representing the new top node
    """
    return {
        'id': subgraph_name,
        'label': subgraph_name,
        'shape': 'diamond',
        'bgcolor': '#40B0A6',
        'fontcolor': 'white',
        'rank': rank,
        'subgraph': subgraph_name,
        'subgraphDet': subgraph_name,
        'mainGraph': main_graph,
        'is_terminal': 'no',
        'href': 'NA',
        'tooltip': '',
        'descr': 'NA',
        'openSource': '',
        'keyQuestions': '',
        'keyLink': '',
        'path': ''
    }


def add_graph_entry(new_node_id, new_node_label, new_node_rank, new_node_subgraph, 
                    target_node_id, new_edge_label="", 
                    node_shape="ellipse", node_bgcolor="#D41159", node_fontcolor="white",
                    node_href="NA", node_tooltip="", node_descr="NA", node_openSource="",
                    node_keyQuestions="", node_keyLink="", is_terminal="yes"):
    """
    Add a new node and edge to the ARIADNE graph.
    
    Args:
        new_node_id: Unique identifier for the new node
        new_node_label: Display label for the node
        new_node_rank: Rank/level in the graph hierarchy
        new_node_subgraph: Subgraph the node belongs to
        target_node_id: ID of the parent node to connect to
        new_edge_label: Label for the connecting edge
        node_shape: Visual shape (ellipse/rectangle/diamond)
        node_bgcolor: Background color (hex code)
        node_fontcolor: Font color
        node_href: URL/link for the resource
        node_tooltip: Tooltip text
        node_descr: Description
        node_openSource: Open source status (TRUE/FALSE/HYBRID)
        node_keyQuestions: Key questions
        node_keyLink: Key link
        is_terminal: Whether this is a terminal node (yes/no)
    
    Returns:
        tuple: (success: bool, message: str)
    """

    NODES_FILE = "data_ariadne_nodes.csv"
    EDGES_FILE = "data_ariadne_edges.csv"
    
    # Load existing data
    nodes_data, nodes_file = load_csv_data(NODES_FILE)
    edges_data, edges_file = load_csv_data(EDGES_FILE)
    
    if nodes_data is None or edges_data is None:
        return False, "Failed to load CSV files"
    
    # Validate node doesn't already exist
    if not validate_node_id(new_node_id, nodes_data):
        return False, f"Node ID '{new_node_id}' already exists"
    
    # Validate target node exists
    if not validate_target_node(target_node_id, nodes_data):
        return False, f"Target node '{target_node_id}' does not exist"
    
    # Get subgraphDet and mainGraph from existing nodes in the same subgraph
    subgraphDet = new_node_subgraph  # Default
    mainGraph = new_node_subgraph  # Default
    for node in nodes_data:
        if node.get('subgraph') == new_node_subgraph:
            if node.get('subgraphDet'):
                subgraphDet = node.get('subgraphDet')
            if node.get('mainGraph'):
                mainGraph = node.get('mainGraph')
            if subgraphDet != new_node_subgraph and mainGraph != new_node_subgraph:
                break  # Found both, can stop looking
    
    # Build path from existing nodes
    target_node_data = next((n for n in nodes_data if n.get('id') == target_node_id), None)
    if target_node_data and target_node_data.get('path'):
        path = target_node_data.get('path') + ' > ' + new_node_label
    else:
        path = new_node_label
    
    # Get the next edge ID
    max_edge_id = max([int(e.get('id', 0)) for e in edges_data if e.get('id', '').isdigit()] + [0])
    new_edge_id = max_edge_id + 1
    
    # Create new node entry
    new_node = {
        'id': new_node_id,
        'label': new_node_label,
        'shape': node_shape,
        'bgcolor': node_bgcolor,
        'fontcolor': node_fontcolor,
        'rank': str(new_node_rank),
        'subgraph': new_node_subgraph,
        'subgraphDet': subgraphDet,
        'mainGraph': mainGraph,  # Typically same as subgraph
        'is_terminal': is_terminal,
        'href': node_href,
        'tooltip': node_tooltip,
        'descr': node_descr,
        'openSource': node_openSource,
        'keyQuestions': node_keyQuestions,
        'keyLink': node_keyLink,
        'path': path
    }
    
    # Create new edge entry
    new_edge = {
        'id': str(new_edge_id),
        'source': target_node_id,
        'target': new_node_id,
        'subgraph': new_node_subgraph,
        'label': new_edge_label,
        'background-color': 'black'
    }
    
    # Add to data
    nodes_data.append(new_node)
    edges_data.append(new_edge)

    # Get headers from the original files
    nodes_headers = list(nodes_data[0].keys()) if nodes_data else []
    edges_headers = list(edges_data[0].keys()) if edges_data else []

    save_csv_data(NODES_FILE, nodes_data, nodes_headers)
    save_csv_data(EDGES_FILE, edges_data, edges_headers)

    # # Save updated data
    # if not save_csv_data(NODES_FILE, nodes_data, nodes_headers):
    #     return False, "Failed to save nodes file"

    # if not save_csv_data(EDGES_FILE, edges_data, edges_headers):
    #     return False, "Failed to save edges file"

    return True, f"✓ Successfully added node '{new_node_label}' and connected to '{target_node_id}'"


def get_graph_statistics(nodes_filepath: str = 'data_ariadne_nodes.csv',
                        edges_filepath: str = 'data_ariadne_edges.csv') -> Dict:
    """
    Get statistics about the graph structure.
    
    Returns:
        Dictionary containing graph statistics
    """
    nodes_data, _ = load_csv_data(nodes_filepath)
    edges_data, _ = load_csv_data(edges_filepath)
    
    subgraphs = get_available_subgraphs(nodes_filepath)
    terminal_nodes = [n for n in nodes_data if n.get('is_terminal') == 'yes']
    
    return {
        'total_nodes': len(nodes_data),
        'total_edges': len(edges_data),
        'total_subgraphs': len(subgraphs),
        'terminal_nodes': len(terminal_nodes),
        'subgraphs': subgraphs
    }

def add_resource_interactive():
    """Interactive wizard to add a new resource."""
    print_header("Add New Resource to ARIADNE Graph")
    
    print("  This wizard will guide you through adding a new resource.\n")
    
    # Step 1: Basic Information
    print_section("Step 1: Basic Information")
    
    node_id = get_user_input("  Enter unique Node ID (e.g., 'OpenScience')", required=True)
    node_label = get_user_input("  Enter display label (e.g., 'Open Science')", required=True)
    
    # Step 2: Choose Subgraph
    print_section("Step 2: Choose Subgraph")
    
    subgraphs = get_available_subgraphs()
    print("\n  Would you like to:")
    print("    1. Use an existing subgraph")
    print("    2. Create a new subgraph")
    
    sg_choice = get_user_input("  Enter choice [1]", default="1")
    
    if sg_choice == "1":
        subgraph, _ = select_from_list(
            subgraphs,
            "Select a subgraph",
            lambda x: f"{x:30s} (Rank: {get_subgraph_details(x)['rank'] if get_subgraph_details(x) else 'N/A'})"
        )
        
        if subgraph is None:
            print("\n  ✗ Cancelled.")
            input("\n  Press Enter to continue...")
            return
        
        # Get subgraph rank for validation
        sg_details = get_subgraph_details(subgraph)
        min_rank = int(sg_details['rank']) if sg_details else 1
        print(f"\n  Selected subgraph: {subgraph} (Minimum rank: {min_rank})")
        
    else:
        subgraph = get_user_input("  Enter new subgraph name", required=True)
        min_rank = 1
        print(f"\n  New subgraph '{subgraph}' will be created.")
    
    # Step 3: Node Properties
    print_section("Step 3: Node Properties")
    
    # Show existing nodes in the subgraph with their ranks
    if sg_choice == "1":  # Existing subgraph
        nodes_in_sg = get_nodes_in_subgraph(subgraph)
        if nodes_in_sg:
            print(f"\n  Current nodes in '{subgraph}':")
            # Sort by rank for better visualization
            sorted_nodes = sorted(nodes_in_sg, key=lambda x: int(x.get('rank', 0)))
            for node in sorted_nodes[:10]:  # Show first 10 to avoid clutter
                print(f"    Rank {node.get('rank'):2s}: {node.get('label')}")
            if len(nodes_in_sg) > 10:
                print(f"    ... and {len(nodes_in_sg) - 10} more nodes")
            print()
    
    node_rank = get_user_input(f"  Enter node rank (minimum: {min_rank})", 
                               default=str(min_rank + 1))
    
    # Step 4: Target Node (Connection)
    print_section("Step 4: Connect to Parent Node")
    
    # Get nodes in selected subgraph and parent nodes
    nodes_data, _ = load_csv_data('data_ariadne_nodes.csv')
    relevant_nodes = [n for n in nodes_data if n.get('subgraph') == subgraph or n.get('id') == subgraph]
    
    if not relevant_nodes:
        print(f"\n  ⚠ No existing nodes found in subgraph '{subgraph}'.")
        print(f"  You'll need to specify a parent node manually.")
        target_node = get_user_input("  Enter parent node ID", required=True)
    else:
        print("\n  Available parent nodes:")
        target_node, _ = select_from_list(
            relevant_nodes,
            "Select parent node to connect to",
            lambda x: f"{x.get('label'):40s} (ID: {x.get('id')}, Rank: {x.get('rank')})"
        )
        
        if target_node is None:
            print("\n  ✗ Cancelled.")
            input("\n  Press Enter to continue...")
            return
        
        target_node = target_node.get('id')
    
    # Step 5: Resource Details
    print_section("Step 5: Resource Details")
    
    node_href = get_user_input("  Enter resource URL", required=True)
    node_descr = get_user_input("  Enter description", required=False)
    
    # Open source status
    print("\n  Is this resource open source?")
    print("    1. TRUE (Open source)")
    print("    2. FALSE (Proprietary)")
    print("    3. HYBRID (Freemium/Mixed)")
    
    os_choice = get_user_input("  Enter choice [1]", default="1")
    open_source_map = {"1": "TRUE", "2": "FALSE", "3": "HYBRID"}
    node_openSource = open_source_map.get(os_choice, "TRUE")
    
    # Step 6: Optional Properties
    print_section("Step 6: Optional Properties (press Enter to skip)")
    
    node_shape = get_user_input("  Node shape", default="ellipse", required=False)
    node_bgcolor = get_user_input("  Background color (hex)", default="#D41159", required=False)
    node_tooltip = get_user_input("  Tooltip text", default=node_href, required=False)
    edge_label = get_user_input("  Edge label", required=False)
    
    # Step 7: Confirmation
    print_section("Step 7: Confirmation")
    
    print("\n  Summary:")
    print(f"    Node ID:          {node_id}")
    print(f"    Label:            {node_label}")
    print(f"    Subgraph:         {subgraph}")
    print(f"    Rank:             {node_rank}")
    print(f"    Parent Node:      {target_node}")
    print(f"    URL:              {node_href}")
    print(f"    Description:      {node_descr or '(none)'}")
    print(f"    Open Source:      {node_openSource}")
    
    if not get_yes_no("\n  Proceed with adding this resource?", default=True):
        print("\n  ✗ Cancelled.")
        input("\n  Press Enter to continue...")
        return
    
    # Add the resource
    print("\n  Adding resource...")
    
    success, message = add_graph_entry(
        new_node_id=node_id,
        new_node_label=node_label,
        new_node_rank=node_rank,
        new_node_subgraph=subgraph,
        target_node_id=target_node,
        new_edge_label=edge_label,
        node_shape=node_shape,
        node_bgcolor=node_bgcolor,
        node_href=node_href,
        node_tooltip=node_tooltip,
        node_descr=node_descr,
        node_openSource=node_openSource
    )
    
    if success:
        print(f"\n  {message}")
    else:
        print(f"\n  ✗ Error: {message}")
    
    input("\n  Press Enter to continue...")

def validate_node_id(node_id, nodes_data):
    """
    Check if a node ID is unique (doesn't already exist).

    Args:
        node_id: The node ID to validate
        nodes_data: List of existing node dictionaries

    Returns:
        bool: True if node ID is unique, False if it already exists
    """
    return not any(node.get('id') == node_id for node in nodes_data)


def validate_target_node(target_node_id, nodes_data):
    """
    Check if a target node exists in the graph.

    Args:
        target_node_id: The target node ID to validate
        nodes_data: List of existing node dictionaries

    Returns:
        bool: True if target node exists, False otherwise
    """
    return any(node.get('id') == target_node_id for node in nodes_data)