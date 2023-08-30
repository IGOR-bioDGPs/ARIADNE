```html
<script src="https://cdnjs.cloudflare.com/ajax/libs/require.js/2.3.4/require.min.js"></script>

<script type="text/x-thebe-config">
  {
    requestKernel: true,
    binderOptions: {
      repo: "QuantStack/ipycytoscape",
      ref: "1.2.0",
      repoProvider: "github",
    },
  }
</script>
<script src="https://unpkg.com/thebe@latest/lib/index.js"></script>

<button id="activateButton" style="width: 120px; height: 40px; font-size: 1.5em;">
  Activate
</button>
<script>
var bootstrapThebe = function() {
    thebelab.bootstrap();
}
document.querySelector("#activateButton").addEventListener('click', bootstrapThebe)
</script>
<style>
pre{
    display: none;
    height: 75%;
    width: 75%;
}
</style>
<html>
  <pre hidden data-executable="true" data-language="python" data-readonly="true">
# Some more prerequisites, just run this
import networkx as nx
import pandas as pd
import json
from ipycytoscape import *
from pathlib import Path


df_nodes = pd.read_csv(str('https://raw.githubusercontent.com/caggursoy/thebetest/main/data/data_ariadne_nodes.csv'), sep=';')
df_edges = pd.read_csv(str('https://raw.githubusercontent.com/caggursoy/thebetest/main/data/data_ariadne_edges.csv'), sep=';')

df_nodes = df_nodes.fillna('')
df_edges = df_edges.fillna('')

# Import stuff to dynamically update the graph
from ipywidgets import Output
from IPython.display import display, HTML

# graph constructor function
def const_graph(nodes_df, edges_df, init):
    # convert df to dicts
    nodes_dict = nodes_df.to_dict('records')
    edges_dict = edges_df.to_dict('records')
    # start building nodes
    data_keys = ['id', 'label'] # cyto logic
    rest_keys = ['score', 'idInt', 'name', 'score', 'group', 'removed', 'selected',
                 'selectable', 'locked', 'grabbed', 'grabbable'] # cyto extra logic
    nodes_graph_list = []
    # now loop over nodes
    for node in nodes_dict:
        dict_node = {}
        data_sub_dict = {'data':{el:node[el] for el in data_keys}} # get MUST data info
        rest_sub_dict = {el:node[el] for el in node.keys() if el in rest_keys} # get extra data info
        dict_node = {**data_sub_dict,**rest_sub_dict} # zip them
        nodes_graph_list.append(dict_node) # add to the list
    # start building edges
    data_keys  = ['id', 'source', 'target'] # cyto logic
    data_keys2 = ['label', 'classes'] # cyto logic
    rest_keys  = ['score', 'weight', 'group', 'networkId', 'networkGroupId', 'intn',
                  'rIntnId', 'group', 'removed', 'selected', 'selectable', 'locked',
                  'grabbed', 'gra bbable', 'classes'] # cyto extra logic
    edges_graph_list = []
    # now loop over edges
    for edge in edges_dict:
        dict_edge = {}
        data_sub_dict = {el:edge[el] for el in data_keys} # get MUST data info
        data_sub_dict2 = {el:edge[el] for el in edge.keys() if el in data_keys2} # get MUST_2 data info
        rest_sub_dict = {el:edge[el] for el in edge.keys() if el in rest_keys} # get extra data info
        dict_edge = {'data':{**data_sub_dict,**data_sub_dict},**rest_sub_dict} # zip them
        edges_graph_list.append(dict_edge) # add to the list
    # create the combined edge+node dictionary
    total_graph_dict = {'nodes': nodes_graph_list, 'edges':edges_graph_list}
    # building the style
    all_node_style = ['background-color', 'background-opacity',
                     'font-family', 'font-size', 'label', 'width',
                     'shape', 'height', 'width', 'text-valign', 'text-halign', 'underlay-color' ,'underlay-shape']
    all_edge_style = ['background-color', 'background-opacity',
                     'font-family', 'font-size', 'label', 'width', 'line-color', 'arrow', 'type', 'target-arrow-shape']
    total_style_dict = {}
    style_elements = []
    # now construct the node styles
    for node in nodes_dict:
        node_dict = {'selector': f'node[id = \"{node["id"]}\"]'}
        style_dict ={"style": { el:node[el] for el in node.keys() if el in all_node_style}}
        node_dict.update(style_dict)
        style_elements.append(node_dict)
    # now construct the edge styles
    for edge in edges_dict:
        edge_dict = {'selector': f'edge[id = \"{edge["id"]}\"]'}
        style_dict = {"style": { el:edge[el] for el in edge.keys() if el in all_edge_style}}
        edge_dict.update(style_dict)
        style_elements.append(edge_dict)
    # now create the graph
    data_graph = json.dumps(total_graph_dict)
    json_to_python = json.loads(data_graph)
    # result_cyto = CytoscapeWidget()
    # for some reason ipycytoscape's function is not callable, so calling it manually
    cyto_graph.graph.nodes.clear()
    cyto_graph.graph.edges.clear()
    cyto_graph.graph._adj.clear()
    cyto_graph.graph.add_graph_from_json(json_to_python)
    cyto_graph.set_style(style_elements)
    # also save the initial json to a file
    if init:
        json_filename = 'init_config.json'
        style_filename = 'init_style.json'
        cyto_graph.set_layout(name = 'circle')
    else:
        json_filename = 'curr_config.json'
        style_filename = 'curr_style.json'
        cyto_graph.set_layout(name = 'breadthfirst')
    with open(json_filename, 'w') as outfile:
        json.dump(json_to_python, outfile)
    with open(style_filename, 'w') as outfile:
        json.dump(json_to_python, outfile)
    # and return it
    #return result_cyto

# reset the graph
def res_graph(node):
    with out:
        # for some reason ipycytoscape's function is not callable, so calling it manually
        cyto_graph.graph.nodes.clear()
        cyto_graph.graph.edges.clear()
        cyto_graph.graph._adj.clear()
        const_graph(df_nodes[df_nodes['subgraph'] == 'initial'], df_edges[df_nodes['subgraph'] == 'initial'], init=True)

def log_clicks(node):
    with out:
        new_nodes = df_nodes['subgraph'] == node['data']['id'].replace(' ','')
        const_graph(df_nodes[new_nodes], df_edges[new_nodes], init=False)
        if len(df_edges[new_nodes]) == 0 or len(df_nodes[new_nodes]) == 0:
            print('Empty subgraph, resetting view...')
            res_graph(node)


# instantiate an jupyternotebook output
out = Output()
out.layout.height = '500px'
# instantiate a graph
cyto_graph = CytoscapeWidget() # ok now create the cytoscape object
const_graph(df_nodes[df_nodes['subgraph'] == 'initial'], df_edges[df_nodes['subgraph'] == 'initial'], init=True)

cyto_graph.on('node', 'click', log_clicks) # dynamically listen to left clicks
cyto_graph.on('node', 'cxttap', res_graph) # dynamically listen to right clicks
cyto_graph.on('node', 'click', log_clicks)

display(cyto_graph) # display the object
display(out) # display the output

  </pre>
</html>
```
