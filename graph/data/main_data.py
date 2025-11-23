"""
ARIADNE Graph Resource Adder - Interactive UI
---------------------------------------------
A user-friendly command-line interface for adding resources (nodes and edges)
to the ARIADNE graph network while maintaining the CSV structure.
"""

import os
import sys
from functions import (
    add_graph_entry,
    get_available_subgraphs,
    get_subgraph_details,
    get_nodes_in_subgraph,
    get_graph_statistics,
    load_csv_data
)


def clear_screen():
    """Clear the terminal screen."""
    os.system('cls' if os.name == 'nt' else 'clear')


def print_header(title: str):
    """Print a formatted header."""
    print("\n" + "=" * 70)
    print(f"  {title}")
    print("=" * 70 + "\n")


def print_section(title: str):
    """Print a section divider."""
    print(f"\n--- {title} ---")


def get_user_input(prompt: str, default: str = None, required: bool = True) -> str:
    """
    Get input from user with optional default value.
    
    Args:
        prompt: The prompt to display
        default: Default value if user presses Enter
        required: Whether input is required
        
    Returns:
        User input or default value
    """
    if default:
        full_prompt = f"{prompt} [{default}]: "
    else:
        full_prompt = f"{prompt}: "
    
    while True:
        value = input(full_prompt).strip()
        
        if value:
            return value
        elif default:
            return default
        elif not required:
            return ""
        else:
            print("  ⚠ This field is required. Please enter a value.")


def get_yes_no(prompt: str, default: bool = True) -> bool:
    """Get yes/no input from user."""
    default_str = "Y/n" if default else "y/N"
    response = input(f"{prompt} [{default_str}]: ").strip().lower()
    
    if not response:
        return default
    return response in ['y', 'yes']


def display_menu():
    """Display the main menu."""
    print("\n┌─────────────────────────────────────────────────┐")
    print("│         ARIADNE Resource Adder Menu             │")
    print("├─────────────────────────────────────────────────┤")
    print("│  1. Add a new resource (node + edge)           │")
    print("│  2. View available subgraphs                    │")
    print("│  3. View subgraph details                       │")
    print("│  4. View graph statistics                       │")
    print("│  5. Exit                                        │")
    print("└─────────────────────────────────────────────────┘")


def view_subgraphs():
    """Display all available subgraphs."""
    print_header("Available Subgraphs")
    
    subgraphs = get_available_subgraphs()
    
    if not subgraphs:
        print("  No subgraphs found.")
        return
    
    print(f"  Total subgraphs: {len(subgraphs)}\n")
    
    for i, sg in enumerate(subgraphs, 1):
        details = get_subgraph_details(sg)
        if details:
            print(f"  {i:3d}. {sg:30s} (Rank: {details['rank']}, MainGraph: {details['mainGraph']})")
        else:
            print(f"  {i:3d}. {sg}")
    
    input("\n  Press Enter to continue...")


def view_subgraph_detail():
    """Display details of a specific subgraph."""
    print_header("Subgraph Details")
    
    subgraphs = get_available_subgraphs()
    
    if not subgraphs:
        print("  No subgraphs found.")
        input("\n  Press Enter to continue...")
        return
    
    print("  Available subgraphs:")
    for i, sg in enumerate(subgraphs, 1):
        print(f"    {i}. {sg}")
    
    choice = get_user_input("\n  Enter subgraph number or name", required=True)
    
    # Try to parse as number
    try:
        idx = int(choice) - 1
        if 0 <= idx < len(subgraphs):
            subgraph_name = subgraphs[idx]
        else:
            print(f"  ⚠ Invalid selection.")
            input("\n  Press Enter to continue...")
            return
    except ValueError:
        subgraph_name = choice
    
    details = get_subgraph_details(subgraph_name)
    
    if not details:
        print(f"\n  ⚠ Subgraph '{subgraph_name}' not found.")
    else:
        print(f"\n  Subgraph: {details['name']}")
        print(f"  Rank: {details['rank']}")
        print(f"  Main Graph: {details['mainGraph']}")
        print(f"  Shape: {details['shape']}")
        print(f"  Background Color: {details['bgcolor']}")
        
        nodes = get_nodes_in_subgraph(subgraph_name)
        print(f"\n  Total nodes in this subgraph: {len(nodes)}")
        
        if get_yes_no("\n  Show all nodes in this subgraph?", default=False):
            print()
            for node in nodes:
                print(f"    - {node.get('label')} (ID: {node.get('id')}, Rank: {node.get('rank')})")
    
    input("\n  Press Enter to continue...")


def view_statistics():
    """Display graph statistics."""
    print_header("Graph Statistics")
    
    stats = get_graph_statistics()
    
    print(f"  Total Nodes:        {stats['total_nodes']}")
    print(f"  Total Edges:        {stats['total_edges']}")
    print(f"  Total Subgraphs:    {stats['total_subgraphs']}")
    print(f"  Terminal Nodes:     {stats['terminal_nodes']}")
    
    if get_yes_no("\n  Show all subgraphs?", default=False):
        print("\n  Subgraphs:")
        for sg in stats['subgraphs']:
            print(f"    - {sg}")
    
    input("\n  Press Enter to continue...")


def select_from_list(items: list, title: str, display_func=None) -> tuple:
    """
    Display a list and let user select an item.
    
    Args:
        items: List of items to display
        title: Title for the selection
        display_func: Optional function to format item display
        
    Returns:
        Tuple of (selected_item, index) or (None, -1) if cancelled
    """
    print(f"\n  {title}:")
    print()
    
    for i, item in enumerate(items, 1):
        if display_func:
            print(f"    {i:3d}. {display_func(item)}")
        else:
            print(f"    {i:3d}. {item}")
    
    print(f"    {len(items) + 1:3d}. Cancel")
    
    while True:
        try:
            choice = int(get_user_input("\n  Select a number", required=True))
            if 1 <= choice <= len(items):
                return items[choice - 1], choice - 1
            elif choice == len(items) + 1:
                return None, -1
            else:
                print(f"  ⚠ Please enter a number between 1 and {len(items) + 1}")
        except ValueError:
            print("  ⚠ Please enter a valid number")


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
    
    # Node type (determines shape and color)
    print("\n  What type of node is this?")
    print("    1. Terminal/Final node (ellipse, red)")
    print("    2. Initial/Starting node (rectangle, blue)")
    print("    3. Intermediate/Parent node (diamond, teal)")
    
    node_type_choice = get_user_input("  Enter choice [1]", default="1")
    
    if node_type_choice == "2":
        node_shape = "rectangle"
        node_bgcolor = "#005AB5"
        is_terminal = "no"
    elif node_type_choice == "3":
        node_shape = "diamond"
        node_bgcolor = "#40B0A6"
        is_terminal = "no"
    else:  # Default to terminal
        node_shape = "ellipse"
        node_bgcolor = "#D41159"
        is_terminal = "yes"
    
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


def main():
    """Main application loop."""
    while True:
        clear_screen()
        print_header("ARIADNE Graph Resource Manager")
        print("  Manage resources in the ARIADNE graph network")
        
        display_menu()
        
        choice = get_user_input("\n  Enter your choice", default="1")
        
        if choice == "1":
            add_resource_interactive()
        elif choice == "2":
            view_subgraphs()
        elif choice == "3":
            view_subgraph_detail()
        elif choice == "4":
            view_statistics()
        elif choice == "5":
            print("\n  Goodbye! 👋\n")
            sys.exit(0)
        else:
            print("\n  ⚠ Invalid choice. Please try again.")
            input("\n  Press Enter to continue...")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n  Interrupted by user. Goodbye! 👋\n")
        sys.exit(0)
    except Exception as e:
        print(f"\n  ✗ An error occurred: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)