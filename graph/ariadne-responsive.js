// ariadne-responsive.js
// Responsive wrapper for ARIADNE

const AriadneResponsive = (function () {
  const MOBILE_BREAKPOINT = 768;
  
  let cyDesktop = null;
  let cyMobile = null;
  let currentMobileSubgraph = 'initial';
  let mobileGraphPath = [];
  let allNodes = [];
  let allEdges = [];

  /* ===========================
     Utility Functions
     =========================== */

  function isMobile() {
    return window.matchMedia(`(max-width: ${MOBILE_BREAKPOINT}px)`).matches;
  }

  function getAccessIcon(openSource) {
    if (openSource === 'TRUE') return '🔓';
    if (openSource === 'HYBRID') return '🔐';
    if (openSource === 'FALSE') return '🔒';
    return '';
  }

  /* ===========================
     Data Loading (Shared)
     =========================== */

  async function fetchDataNodes() {
    try {
      const isLocal = window.location.hostname === 'localhost' || 
                      window.location.hostname === '127.0.0.1' ||
                      window.location.protocol === 'file:';
      
      const githubRawURL = 'https://raw.githubusercontent.com/IGOR-bioDGPs/ARIADNE/master/ariadne/data/data_ariadne_nodes.csv';
      const localURL = '../ariadne/data/data_ariadne_nodes.csv';
      const dataURL = isLocal ? localURL : githubRawURL;
      
      const response = await fetch(dataURL);
      const csvData = await response.text();
      const rows = csvData.split('\n');

      function clean(v) {
        return (v === "NA" || v === "" || v === undefined) ? null : v;
      }

      const nodes = rows.slice(1).filter(row => row.trim()).map(row => {
        const [id, label, shape, bgColor, fontColor, rank, subgraph, subgraphDet, 
               mainGraph, isTerminal, href, tooltip, descr, openSource, keyQuestions, 
               keyLink, path] = row.split(';');
        
        return {
          data: {
            id: clean(id),
            label: clean(label),
            shape: clean(shape),
            background_color: clean(bgColor),
            font_color: clean(fontColor),
            rank: clean(rank),
            subgraph: clean(subgraph),
            subgraphDet: clean(subgraphDet),
            mainGraph: clean(mainGraph),
            is_terminal: clean(isTerminal),
            href: clean(href),
            tooltip: clean(tooltip),
            descr: clean(descr),
            openSource: clean(openSource),
            keyQuestions: clean(keyQuestions),
            keyLink: clean(keyLink),
            path: clean(path),
          }
        };
      });

      return nodes;
    } catch (err) {
      console.error('Error fetching nodes CSV:', err);
      return [];
    }
  }

  async function fetchDataEdges() {
    try {
      const isLocal = window.location.hostname === 'localhost' || 
                      window.location.hostname === '127.0.0.1' ||
                      window.location.protocol === 'file:';
      
      const githubRawURL = 'https://raw.githubusercontent.com/IGOR-bioDGPs/ARIADNE/master/ariadne/data/data_ariadne_edges.csv';
      const localURL = '../ariadne/data/data_ariadne_edges.csv';
      const dataURL = isLocal ? localURL : githubRawURL;
      
      const response = await fetch(dataURL);
      const csvData = await response.text();
      const rows = csvData.split('\n');

      function clean(v) {
        return (v === "NA" || v === "" || v === undefined) ? null : v;
      }

      const edges = rows.slice(1).filter(row => row.trim()).map(row => {
        const [id, source, target, subgraph, label, bgColor] = row.split(';');
        return {
          data: {
            id: clean(id),
            source: clean(source),
            target: clean(target),
            subgraph: clean(subgraph),
            label: clean(label),
            background_color: clean(bgColor),
          }
        };
      });

      return edges;
    } catch (err) {
      console.error('Error fetching edges CSV:', err);
      return [];
    }
  }

  /* ===========================
     Desktop Initialization
     =========================== */

  async function initDesktop() {
    // Load data
    allNodes = await fetchDataNodes();
    allEdges = await fetchDataEdges();

    // Set screen dimensions
    const screenWidth = window.innerWidth * 0.8;
    const screenHeight = window.innerHeight;
    document.documentElement.style.setProperty('--screen-width', screenWidth + 'px');
    document.documentElement.style.setProperty('--screen-height', screenHeight + 'px');

    // Setup buttons
    setupDesktopButtons();

    // Setup info/key boxes
    setupDesktopInfoBoxes();

    // Setup canvas
    setupShapesCanvas();

    // Start the original desktop network
    await createDesktopNetwork('initial', 0, []);
  }

  function setupDesktopButtons() {
    document.getElementById('back-button')?.addEventListener('click', () => {
      window.open('https://igor-biodgps.github.io/ARIADNE/contentpages/intro.html', '_blank');
    });

    document.getElementById('osf-button')?.addEventListener('click', () => {
      window.open('https://osf.io/tqjh8/', '_blank');
    });

    document.getElementById('glos-button')?.addEventListener('click', () => {
      window.open('https://igor-biodgps.github.io/ARIADNE/contentpages/Glossary.html', '_blank');
    });

    document.getElementById('sugg-ghub-button')?.addEventListener('click', () => {
      window.open('https://github.com/IGOR-bioDGPs/ARIADNE/issues/new?assignees=&labels=new+resource&projects=&template=resource-submission-form.md&title=', '_blank');
    });

    document.getElementById('sugg-gdrive-button')?.addEventListener('click', () => {
      window.open('https://docs.google.com/forms/d/1Xqk6MyLYvjdu9cbs1-R40hn9mIZ6KtKL-4LcpI80I_I/', '_blank');
    });

    document.getElementById('bug-ghub-button')?.addEventListener('click', () => {
      window.open('https://github.com/IGOR-bioDGPs/ARIADNE/issues/new?assignees=&labels=&projects=&template=bug_report.md&title=', '_blank');
    });

    document.getElementById('bug-gdrive-button')?.addEventListener('click', () => {
      window.open('https://docs.google.com/forms/d/1sCcvmlokUuWc4EG5mz0vXx-QRkyfqN69ibK5b3PqArA/', '_blank');
    });
  }

  function setupDesktopInfoBoxes() {
    const infoBox = document.getElementById('info-box');
    const infoContent = document.getElementById('infoContent');
    const keyBox = document.getElementById('key-box');
    const keyContent = document.getElementById('keyContent');

    infoBox?.addEventListener('click', () => {
      infoContent.toggleAttribute("hidden");
      if (keyContent) {
        keyContent.style.zIndex = 1;
        infoContent.style.zIndex = 200;
      }
    });

    keyBox?.addEventListener('click', () => {
      keyContent.toggleAttribute("hidden");
      if (infoContent) {
        keyContent.style.zIndex = 200;
        infoContent.style.zIndex = 1;
      }
    });
  }

  function setupShapesCanvas() {
    const canvas = document.getElementById("shapesCanvas");
    if (!canvas) return;
    
    const ctx = canvas.getContext("2d");

    const shapes = [
      { x: 0, y: 20, width: 40, height: 40, color: "#005AB5", rect: true, 
        popupMessage: "Initial node, there are more nodes inside this one!" },
      { x: 130, y: 40, radius: 20, color: "#D41159", 
        popupMessage: "Final node. Click this node to go to the resource's website!" }, 
      { x: 55, y: 20, width: 40, height: 40, color: "#40B0A6", diamond: true, 
        popupMessage: "Decision node, filter the nodes and move deeper!" },
      { x: 0, y: 80, width: 35, height: 35, 
        src: "https://raw.githubusercontent.com/IGOR-bioDGPs/ARIADNE/master/graph/imgs/closed_lock_with_key.png", 
        popupMessage: "Hybrid (partially) open access resource!" },
      { x: 50, y: 80, width: 35, height: 35, 
        src: "https://raw.githubusercontent.com/IGOR-bioDGPs/ARIADNE/master/graph/imgs/lock.png", 
        popupMessage: "Fully closed access resource!" },
      { x: 100, y: 80, width: 35, height: 35, 
        src: "https://raw.githubusercontent.com/IGOR-bioDGPs/ARIADNE/master/graph/imgs/unlock.png", 
        popupMessage: "Fully open access resource!" }
    ];

    let loadedImages = [];
    let imagesToLoad = shapes.filter(shape => shape.src).length;
    let imagesLoaded = 0;

    shapes.forEach((shape, index) => {
      if (shape.src) {
        const img = new Image();
        img.src = shape.src;
        img.onload = () => {
          loadedImages[index] = img;
          imagesLoaded++;
          if (imagesLoaded === imagesToLoad) {
            drawShapes();
          }
        };
      }
    });

    function drawShapes() {
      ctx.clearRect(0, 0, canvas.width, canvas.height);
      shapes.forEach((shape, index) => {
        if (shape.src && loadedImages[index]) {
          ctx.drawImage(loadedImages[index], shape.x, shape.y, shape.width, shape.height);
        } else {
          ctx.fillStyle = shape.color;
          if (shape.radius) {
            ctx.beginPath();
            ctx.arc(shape.x, shape.y, shape.radius, 0, Math.PI * 2);
            ctx.fill();
          } else if (shape.diamond) {
            ctx.beginPath();
            ctx.moveTo(shape.x + shape.width / 2, shape.y);
            ctx.lineTo(shape.x + shape.width, shape.y + shape.height / 2);
            ctx.lineTo(shape.x + shape.width / 2, shape.y + shape.height);
            ctx.lineTo(shape.x, shape.y + shape.height / 2);
            ctx.closePath();
            ctx.fill();
          } else if (shape.rect) {
            ctx.fillRect(shape.x, shape.y, shape.width, shape.height);
          }
        }
      });
    }

    function showPopup(message, x, y) {
      const padding = 10;
      ctx.font = '12px Arial';
      const maxPopupWidth = Math.min(200, canvas.width - 5 * padding);
      const words = message.split(' ');
      const lines = [];
      let currentLine = words[0];

      for (let i = 1; i < words.length; i++) {
        const testLine = currentLine + ' ' + words[i];
        const testWidth = ctx.measureText(testLine).width;
        if (testWidth > 100) {
          lines.push(currentLine);
          currentLine = words[i];
        } else {
          currentLine = testLine;
        }
      }
      lines.push(currentLine);

      const longestWord = lines.reduce((a, b) => a.length > b.length ? a : b, "");
      const lineHeight = 20;
      const popupHeight = lineHeight * lines.length;
      const popupWidth = Math.min(ctx.measureText(longestWord).width + 2 * padding, maxPopupWidth);

      let popupX = x;
      let popupY = y - popupHeight - padding;

      if (popupX + popupWidth > canvas.width) {
        popupX = canvas.width - popupWidth - padding;
      }
      if (popupY < 0) {
        popupY = y + padding;
      }

      ctx.clearRect(0, 0, canvas.width, canvas.height);
      drawShapes();

      ctx.fillStyle = "rgba(255, 255, 255, 0.9)";
      ctx.fillRect(popupX, popupY, popupWidth, popupHeight);

      ctx.fillStyle = "black";
      lines.forEach((line, index) => {
        ctx.fillText(line, popupX + padding, popupY + padding + (index * lineHeight));
      });
    }

    canvas.addEventListener('mousemove', (e) => {
      const mouseX = e.offsetX;
      const mouseY = e.offsetY;
      let popupShown = false;

      shapes.forEach((shape) => {
        if (shape.radius) {
          const dx = mouseX - shape.x;
          const dy = mouseY - shape.y;
          const distance = Math.sqrt(dx * dx + dy * dy);
          if (distance <= shape.radius) {
            showPopup(shape.popupMessage, mouseX, mouseY);
            popupShown = true;
          }
        } else {
          if (mouseX >= shape.x && mouseX <= shape.x + shape.width &&
              mouseY >= shape.y && mouseY <= shape.y + shape.height) {
            showPopup(shape.popupMessage, mouseX, mouseY);
            popupShown = true;
          }
        }
      });

      if (!popupShown) {
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        drawShapes();
      }
    });

    canvas.addEventListener("mouseleave", () => {
      ctx.clearRect(0, 0, canvas.width, canvas.height);
      drawShapes();
    });
  }

  async function createDesktopNetwork(sub_graph, index, graphPathArr) {
    graphPathArr.push(sub_graph);

    const filteredNodes = allNodes.filter(item => 
      item.data?.subgraph?.toLowerCase() === sub_graph?.toLowerCase()
    );
    const filteredEdges = allEdges.filter(item => 
      item.data?.subgraph?.toLowerCase() === sub_graph?.toLowerCase()
    );
    const filteredAll = filteredNodes.concat(filteredEdges);

    const cy = cytoscape({
      container: document.getElementById('cy'),
      elements: filteredAll,
      style: [
        {
          selector: 'node',
          style: {
            'background-color': 'data(background_color)',
            'shape': 'data(shape)',
            'label': 'data(label)',
            'font-size': 24,
            'text-wrap': 'wrap',
            'text-max-width': 150,
            'background-width': '80%',
            'background-height': '80%',
            'background-offset-x': '140%',
            'background-offset-y': '140%',
            'background-clip': 'none',
            'background-image-containment': 'over',
            'bounds-expansion': 4
          }
        },
        {
          selector: 'node[openSource= "TRUE"]',
          style: {
            'background-image': 'url(https://raw.githubusercontent.com/IGOR-bioDGPs/ARIADNE/master/graph/imgs/unlock.png)'
          }
        },
        {
          selector: 'node[openSource= "HYBRID"]',
          style: {
            'background-image': 'url(https://raw.githubusercontent.com/IGOR-bioDGPs/ARIADNE/master/graph/imgs/closed_lock_with_key.png)'
          }
        },
        {
          selector: 'node[openSource= "FALSE"]',
          style: {
            'background-image': 'url(https://raw.githubusercontent.com/IGOR-bioDGPs/ARIADNE/master/graph/imgs/lock.png)'
          }
        },
        {
          selector: 'edge',
          style: {
            'width': 2,
            'font-size': 24,
            'line-color': '#ccc',
            'target-arrow-color': '#ccc',
            'target-arrow-shape': 'triangle',
            'text-wrap': 'wrap',
            'text-max-width': 100,
            'label': 'data(label)'
          }
        }
      ],
      layout: {
        name: 'circle',
        fit: true,
        avoidOverlap: true,
      },
      zoom: 1
    });

    // Apply layout based on node count
    if (filteredNodes.length < 3) {
      const screenWidth = window.innerWidth * 0.8;
      const centerX = screenWidth / 2;
      const centerY = window.innerHeight / 2;

      const positions = {};
      if (filteredNodes[0]) positions[filteredNodes[0].data.id] = { x: centerX - 175, y: centerY - 200 };
      if (filteredNodes[1]) positions[filteredNodes[1].data.id] = { x: centerX - 175, y: centerY + 50 };

      cy.layout({
        name: 'preset',
        fit: false,
        avoidOverlap: true,
        zoom: 0.88,
        positions: positions
      }).run();
    } else if (filteredNodes.length >= 3 && filteredNodes.length < 7) {
      cy.layout({
        name: 'breadthfirst',
        grid: false,
        fit: true,
        avoidOverlap: true,
        spacingFactor: 1.5,
      }).run();
    } else {
      cy.layout({
        name: 'circle',
        fit: true,
        avoidOverlap: true,
        spacingFactor: 1.5,
      }).run();
    }

    setupDesktopCytoscapeEvents(cy, index, graphPathArr);

    // Show/hide key box
    const keyBox = document.getElementById('key-box');
    if (sub_graph !== 'initial') {
      keyBox?.removeAttribute('hidden');
    } else {
      keyBox?.setAttribute('hidden', '');
    }

    cyDesktop = cy;
  }

  function setupDesktopCytoscapeEvents(cy, index, graphPathArr) {
    const minZoom = 0.6;
    const maxZoom = 1.2;
    const cytoCSS = document.body;

    cy.on('click', 'node', (event) => {
      cytoCSS.style.backgroundImage = 'url("")';
      const node = event.target;
      if (node.data('is_terminal') === 'no') {
        createDesktopNetwork(node.data('id').replaceAll(' ', ''), index + 1, graphPathArr);
        if (node.data('mainGraph') === 'initial') {
          updateKeyContent(node, 'left_click');
        }
      } else {
        window.open(node.data('tooltip'), '_blank');
      }
    });

    cy.on('cxttap', (event) => {
      let isNode = false;
      try {
        isNode = event.target.isNode();
      } catch (error) {}

      cytoCSS.style.backgroundImage = 'url("ARIADNE_Logo.png")';
      const tooltips = document.querySelectorAll('.custom-tooltip');
      tooltips.forEach(tooltip => tooltip.remove());
      createDesktopNetwork('initial', 0, []);
      if (!isNode) {
        updateKeyContent('', 'right_click');
      }
      cy.zoom(minZoom);
    });

    cy.on('cxttap', 'node', (event) => {
      const auxElem = graphPathArr[index - 1];
      if (auxElem !== 'initial') {
        cytoCSS.style.backgroundImage = 'url("")';
      } else {
        updateKeyContent('', 'right_click');
      }
      createDesktopNetwork(auxElem.replace(' ', ''), index, graphPathArr.slice(0, -1));
    });

    cy.on('mouseover', 'node', (event) => {
      const node = event.target;
      if (node.data('is_terminal') === 'yes') {
        const tooltip = document.createElement('div');
        tooltip.className = 'custom-tooltip';
        tooltip.textContent = node.data('descr');
        document.body.appendChild(tooltip);

        const nodePosition = node.renderedPosition();
        const nodeHeight = node.height();
        tooltip.style.left = nodePosition.x + 'px';
        tooltip.style.top = nodePosition.y + nodeHeight + 10 + 'px';
      }
    });

    cy.on('mouseout', 'node', () => {
      const tooltips = document.querySelectorAll('.custom-tooltip');
      tooltips.forEach(tooltip => tooltip.remove());
    });

    cy.on('zoom', () => {
      const currentZoom = cy.zoom();
      if (currentZoom < minZoom) {
        cy.zoom(minZoom);
      } else if (currentZoom > maxZoom) {
        cy.zoom(maxZoom);
      }
      cy.center();
    });
  }

  function updateKeyContent(node, clickType) {
    const keyContent = document.getElementById('keyContent');
    if (!keyContent) return;

    keyContent.innerHTML = '';

    if (clickType === 'left_click' && node.data) {
      const keyQuestions = node.data('keyQuestions')?.split('||') || [];
      const ul = document.createElement('ul');
      ul.style.listStylePosition = 'outside';
      keyContent.appendChild(ul);

      keyQuestions.forEach(question => {
        const li = document.createElement('li');
        li.textContent = question.trim();
        ul.appendChild(li);
      });

      if (node.data('keyLink')) {
        const link = document.createElement('a');
        link.href = node.data('keyLink');
        link.target = '_blank';
        link.textContent = "Click here to read the step description";
        keyContent.appendChild(link);
      }
    } else if (clickType === 'right_click') {
      const li = document.createElement('li');
      li.textContent = 'Initial view';
      keyContent.appendChild(li);
    }
  }

  /* ===========================
     Mobile Initialization
     =========================== */

  async function initMobile() {
    // Load data
    allNodes = await fetchDataNodes();
    allEdges = await fetchDataEdges();

    // Setup tabs
    setupMobileTabs();

    // Build step list
    buildMobileStepList();

    // Setup mobile Cytoscape
    await createMobileNetwork('initial');

    // Setup search
    setupMobileSearch();

    // Setup resource sheet
    setupResourceSheet();
  }

  function setupMobileTabs() {
    const tabButtons = document.querySelectorAll("#mobile-tabs button");
    const tabs = document.querySelectorAll(".tab");

    tabButtons.forEach((btn) => {
      btn.addEventListener("click", () => {
        const target = btn.getAttribute("data-tab");

        tabButtons.forEach((b) => b.classList.toggle("active", b === btn));
        tabs.forEach((tab) => {
          tab.classList.toggle("active", tab.id === `tab-${target}`);
        });

        if (target === "map" && cyMobile) {
          setTimeout(() => {
            cyMobile.resize();
            cyMobile.fit();
          }, 100);
        }
      });
    });
  }

  function buildMobileStepList() {
    const stepList = document.getElementById('step-list');
    if (!stepList) return;

    // Get initial nodes (mainGraph === 'initial')
    const initialNodes = allNodes.filter(node => 
      node.data?.mainGraph?.toLowerCase() === 'initial' && 
      node.data?.is_terminal === 'no'
    );

    stepList.innerHTML = '';

    initialNodes.forEach((node, index) => {
      const card = document.createElement('div');
      card.className = 'step-card';
      card.dataset.nodeId = node.data.id;

      const badge = document.createElement('div');
      badge.className = 'step-badge';
      badge.textContent = `Step ${index + 1}`;

      const title = document.createElement('h2');
      title.textContent = node.data.label || node.data.id;

      const desc = document.createElement('p');
      desc.textContent = node.data.descr || node.data.subgraphDet || 'Tap to explore resources';

      card.appendChild(badge);
      card.appendChild(title);
      card.appendChild(desc);

      card.addEventListener('click', () => {
        openResourceSheet(node.data);
      });

      stepList.appendChild(card);
    });
  }

  async function createMobileNetwork(sub_graph) {
    currentMobileSubgraph = sub_graph;
    mobileGraphPath.push(sub_graph);

    const filteredNodes = allNodes.filter(item => 
      item.data?.subgraph?.toLowerCase() === sub_graph?.toLowerCase()
    );
    const filteredEdges = allEdges.filter(item => 
      item.data?.subgraph?.toLowerCase() === sub_graph?.toLowerCase()
    );
    const filteredAll = filteredNodes.concat(filteredEdges);

    const container = document.getElementById('cy-mobile');
    if (!container) return;

    if (cyMobile) {
      cyMobile.destroy();
    }

    cyMobile = cytoscape({
      container: container,
      elements: filteredAll,
      style: [
        {
          selector: 'node',
          style: {
            'background-color': 'data(background_color)',
            'shape': 'data(shape)',
            'label': 'data(label)',
            'font-size': 14,
            'text-wrap': 'wrap',
            'text-max-width': 80,
            'width': 40,
            'height': 40,
          }
        },
        {
          selector: 'edge',
          style: {
            'width': 1.5,
            'line-color': '#ccc',
            'target-arrow-color': '#ccc',
            'target-arrow-shape': 'triangle',
            'curve-style': 'bezier'
          }
        }
      ],
      layout: {
        name: 'circle',
        fit: true,
        avoidOverlap: true,
        spacingFactor: 1.2
      },
      minZoom: 0.3,
      maxZoom: 2,
      wheelSensitivity: 0.2
    });

    cyMobile.on('tap', 'node', (evt) => {
      const node = evt.target.data();
      openResourceSheet(node);
    });

    // Reset button
    const resetBtn = document.getElementById('mobile-reset-view');
    if (resetBtn) {
      resetBtn.onclick = () => {
        cyMobile.fit();
        cyMobile.center();
      };
    }

    // Back button
    const backBtn = document.getElementById('mobile-back');
    if (backBtn) {
      backBtn.onclick = () => {
        if (mobileGraphPath.length > 1) {
          mobileGraphPath.pop();
          const prevGraph = mobileGraphPath[mobileGraphPath.length - 1];
          createMobileNetwork(prevGraph);
        } else {
          createMobileNetwork('initial');
        }
      };
    }
  }

  function openResourceSheet(nodeData) {
    const sheet = document.getElementById('resource-sheet');
    const content = document.getElementById('resource-sheet-content');

    const title = nodeData.label || nodeData.id;
    const description = nodeData.descr || nodeData.subgraphDet || '';
    const url = nodeData.tooltip || nodeData.href || null;
    const isTerminal = nodeData.is_terminal === 'yes';
    const accessIcon = getAccessIcon(nodeData.openSource);

    let html = `<h2>${title}</h2>`;
    
    if (description) {
      html += `<p>${description}</p>`;
    }

    if (accessIcon) {
      html += `<div class="resource-meta">
        <span class="resource-badge">${accessIcon} ${nodeData.openSource === 'TRUE' ? 'Open Access' : nodeData.openSource === 'HYBRID' ? 'Hybrid Access' : 'Closed Access'}</span>
      </div>`;
    }

    if (isTerminal && url) {
      html += `<a href="${url}" target="_blank" rel="noopener noreferrer" class="resource-link">Visit Resource →</a>`;
    } else if (!isTerminal) {
      html += `<p><em>Tap to explore sub-resources in this category.</em></p>`;
      html += `<button onclick="AriadneResponsive.exploreMobileNode('${nodeData.id}')" style="width: 100%; padding: 0.75rem; background: #4CAF50; color: white; border: none; border-radius: 6px; font-size: 1rem; cursor: pointer; margin-top: 0.5rem;">Explore →</button>`;
    }

    content.innerHTML = html;
    sheet.classList.add('visible');
  }

  function exploreMobileNode(nodeId) {
    const sheet = document.getElementById('resource-sheet');
    sheet.classList.remove('visible');
    
    // Switch to map tab
    document.querySelector('#mobile-tabs button[data-tab="map"]')?.click();
    
    // Navigate to that subgraph
    setTimeout(() => {
      createMobileNetwork(nodeId.replaceAll(' ', ''));
    }, 300);
  }

  function setupResourceSheet() {
    const sheet = document.getElementById('resource-sheet');
    const closeBtn = document.getElementById('close-resource-sheet');

    closeBtn?.addEventListener('click', () => {
      sheet.classList.remove('visible');
    });

    // Close on backdrop tap
    sheet?.addEventListener('click', (e) => {
      if (e.target === sheet) {
        sheet.classList.remove('visible');
      }
    });
  }

  function setupMobileSearch() {
    const searchInput = document.getElementById('mobile-search');
    if (!searchInput) return;

    searchInput.addEventListener('input', (e) => {
      const term = e.target.value.toLowerCase().trim();
      filterMobileStepList(term);
    });
  }

  function filterMobileStepList(term) {
    const cards = document.querySelectorAll('.step-card');
    
    if (!term) {
      cards.forEach(card => card.style.display = '');
      return;
    }

    cards.forEach(card => {
      const text = card.textContent.toLowerCase();
      card.style.display = text.includes(term) ? '' : 'none';
    });
  }

  /* ===========================
     App Bootstrap
     =========================== */

  async function init() {
    if (isMobile()) {
      await initMobile();
    } else {
      await initDesktop();
    }

    // Handle resize
    window.addEventListener('resize', () => {
      const nowMobile = isMobile();
      const wasMobile = document.querySelector('.mobile-only')?.style.display !== 'none';
      
      if (nowMobile !== wasMobile) {
        location.reload(); // Simple approach: reload on breakpoint cross
      }
    });
  }

  return { 
    init,
    exploreMobileNode // Expose for button onclick
  };
})();

// Auto-init on DOM ready
document.addEventListener('DOMContentLoaded', () => {
  AriadneResponsive.init();
});