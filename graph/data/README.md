# ARIADNE Resource Manager

This application provides an interactive command-line interface for managing resources in the ARIADNE graph database.

## Overview

The ARIADNE project uses a graph-based structure to organize research resources, tools, and workflows. The graph consists of:
- **Nodes**: Individual resources or steps in the research workflow
- **Edges**: Connections between nodes showing relationships and flow

## Files

The application comes bundled with the following data files:
- `data_ariadne_nodes.csv` - Node data storage
- `data_ariadne_edges.csv` - Edge data storage

**Important:** Keep these CSV files in the same directory as the executable.

## Installation

No installation required! The application is bundled as a standalone executable with all dependencies included.

## Usage

Simply double-click the executable file or run it from the command line:

**Windows:**
```bash
ARIADNE_manager.exe
```

**macOS/Linux:**
```bash
./ARIADNE_manager
```

The application will launch an interactive menu in your terminal/command prompt.

## Main Menu Options

1. **Add new resource (node + edge)** - Add a new node and edge to the graph
2. **View available subgraphs** - Display all subgraphs in the system
3. **View subgraph details** - See detailed information about a specific subgraph
4. **View statistics** - Display overall graph statistics 
5. **Regenerate all node paths** - Regenerate the auto-generated node paths 
6. **Exit** - Close the application

## Adding a New Resource

When you select option 1 (Add new resource), the script guides you through the following steps:

### Step 1: Select Subgraph
Choose the subgraph where you want to add the resource. Available options include:
- ProjectStart
- Literature
- Communities
- Data Management
- And more...

### Step 2: Select Target Node
Choose the parent node that will connect to your new resource. The script displays:
- All nodes in the selected subgraph
- Node IDs and labels
- Current rank information

### Step 3: Select Node Type
Choose the type of node you're creating:
- **Terminal node** (ellipse, red background) - End points or final resources
- **Initial node** (rectangle, blue background) - Starting points or entry nodes
- **Intermediate node** (diamond, teal background) - Middle steps or decision points

### Step 4: Enter Node Details

You'll be prompted to provide:

#### Required Fields:
- **Node ID**: Unique identifier (e.g., "Unpaywall", "Research Rabbit")
- **Label**: Display name for the node
- **Tooltip**: Brief description shown on hover
- **Description**: Detailed explanation of the resource

#### Optional Fields:
- **URL (href)**: Link to the resource (press Enter to skip)
- **Open Source**: Whether the resource is open source (yes/no)
- **Key Questions**: Important questions related to this resource (use || as separator)
- **Key Link**: Additional reference link

### Step 5: Confirmation
Review all entered information and confirm to add the resource to the graph.

## Data Structure

### Node Fields
- `id` - Unique identifier
- `label` - Display name
- `shape` - Visual shape (rectangle/diamond/ellipse)
- `bgcolor` - Background color
- `fontcolor` - Text color (typically white)
- `rank` - Hierarchical level
- `subgraph` - Subgraph identifier
- `subgraphDet` - Subgraph display name
- `mainGraph` - Main graph identifier
- `is_terminal` - Terminal node flag (yes/no)
- `href` - URL link
- `tooltip` - Hover text
- `descr` - Description
- `openSource` - Open source flag
- `keyQuestions` - Key questions (|| separated)
- `keyLink` - Reference link
- `path` - Hierarchical path (e.g., "Project Start > Literature > Unpaywall")

### Edge Fields
- `id` - Unique edge identifier
- `source` - Source node ID
- `target` - Target node ID
- `subgraph` - Subgraph identifier
- `label` - Edge label (typically empty)
- `background-color` - Edge color (typically black)

## Node Types and Visual Styling

| Node Type | Shape | Background Color | Use Case |
|-----------|-------|------------------|----------|
| Terminal | Ellipse | Red (#D41159) | Final resources, tools, endpoints |
| Initial | Rectangle | Blue (#005AB5) | Starting points, entry nodes |
| Intermediate | Diamond | Teal (#40B0A6) | Decision points, intermediate steps |

## Path Hierarchy

The `path` field automatically builds a hierarchical structure:
- Connects to target node's path
- Appends new node's label
- Uses " > " as separator
- Example: `Project Start > Literature > Unpaywall`

## Tips

- Use descriptive node IDs that are easy to reference
- Keep tooltips concise (one sentence)
- Provide detailed descriptions for better documentation
- Include URLs when available to link to external resources
- Use the || separator for multiple key questions
- Review the subgraph structure before adding nodes to ensure proper placement

## Example Workflow

1. Launch the ARIADNE Manager executable
2. Select option 4 (Add new resource)
3. Choose subgraph: "Literature"
4. Select target node: "Literature" (the main node)
5. Choose node type: "Terminal node"
6. Enter details:
   - ID: "Zotero"
   - Label: "Zotero"
   - Tooltip: "Free reference management software"
   - Description: "Zotero is a free, easy-to-use tool to help you collect, organize, cite, and share research."
   - URL: "https://www.zotero.org/"
   - Open Source: "yes"
7. Confirm and save

## Data Backup

The script automatically saves changes to the CSV files. Consider backing up your data files before making significant changes.

## Troubleshooting

- **Invalid node ID**: Ensure the ID doesn't already exist
- **Missing target node**: Verify the target node exists in the selected subgraph
- **CSV errors**: Check that CSV files are properly formatted and not corrupted

## Support

For questions or issues, refer to the ARIADNE project documentation or contact the project maintainers.