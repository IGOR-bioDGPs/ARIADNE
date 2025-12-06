"""
ARIADNE Graph Resource Adder - Interactive UI
---------------------------------------------
A user-friendly command-line interface for adding resources (nodes and edges)
to the ARIADNE graph network while maintaining the CSV structure.
"""

import sys
from functions import (
    add_graph_entry,
    get_available_subgraphs,
    get_subgraph_details,
    get_nodes_in_subgraph,
    get_graph_statistics,
    load_csv_data,
    clear_screen,
    print_header,
    print_section,
    get_user_input,
    get_yes_no,
    display_menu,
    view_subgraphs,
    view_subgraph_detail,
    view_statistics,
    select_from_list,
    add_resource_interactive,
    regenerate_all_paths,
    regenerate_paths_interactive
)

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
        elif choice == '5':
            regenerate_paths_interactive()
        elif choice == "6":
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