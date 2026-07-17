async function fetchData(url) {
  try {
    const response = await fetch(url);
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    const csvData = await response.text();
    const rows = csvData.split("\n").filter((row) => row.trim() !== "");
    const nodes = rows.map((row) => {
      const fields = row.split(";");
      return {
        data: {
          id: fields[0],
          label: fields[1],
          shape: fields[2],
          background_color: fields[3],
          font_color: fields[4],
          rank: fields[5],
          subgraph: fields[6],
          mainGraph: fields[7],
          is_terminal: fields[8],
          href: fields[9],
          tooltip: fields[10],
          descr: fields[11],
          openSource: fields[12],
          keyQuestions: fields[13],
          keyLink: fields[14],
        },
      };
    });
    if (nodes[0] && Object.keys(nodes[0].data).length === 0) {
      nodes.shift();
    } // Remove empty node created from header row if present
    return nodes;
  } catch (error) {
    console.error(`Error fetching data:`, error);
    return null;
  }
}

async function createCytoscapeGraph() {
  const githubNodesURL =
    "https://raw.githubusercontent.com/IGOR-bioDGPs/ARIADNE/master/ariadne/data/data_ariadne_nodes.csv";
  const nodes = await fetchData(githubNodesURL);

  if (!nodes) {
    console.error("Failed to fetch data. Cannot create graph.");
    return;
  }

  const cy = cytoscape({
    container: document.getElementById("cy"),
    elements: nodes, // Directly use the fetched nodes
    style: [
      // ... your Cytoscape style configuration
      {
        selector: "node",
        style: {
          "background-color": "data(background_color)",
          label: "data(label)",
          color: "data(font_color)",
          shape: "data(shape)",
        },
      },
    ],
  });

  cy.on("tap", "node", function (evt) {
    const node = evt.target;
    if (node.data("href")) {
      window.open(node.data("href"), "_blank");
    }
  });
}

createCytoscapeGraph();
