const fs = require('fs');
const path = require('path');

const filePath = path.join(__dirname, '../knowledge.js');
let fileContent = fs.readFileSync(filePath, 'utf-8');

// We want to mock document.body.getAttribute to bypass the outer check
const document = {
  body: {
    getAttribute: () => "knowledge"
  },
  documentElement: {
    getAttribute: () => "en"
  },
  getElementById: () => null,
  querySelectorAll: () => [],
  createElement: () => ({ addEventListener: () => {} }),
  addEventListener: () => {}
};

// We mock window and localstorage
const window = {
  location: { pathname: "/kb-graph.html" },
  addEventListener: () => {}
};
const localStorage = {
  getItem: () => null,
  setItem: () => {}
};
const d3 = {
  select: () => ({ attr: function() { return this; }, call: () => {} }),
  zoom: () => ({ scaleExtent: function() { return this; }, on: function() { return this; } })
};

// Extract the nodes and links array by evaluating the JS file in a simplified environment
// Let's regex extract const nodes = [ ... ] and const links = [ ... ] from knowledge.js
const nodesMatch = fileContent.match(/const\s+nodes\s*=\s*\[([\s\S]*?)\];/);
const linksMatch = fileContent.match(/const\s+links\s*=\s*\[([\s\S]*?)\];/);

if (!nodesMatch || !linksMatch) {
  console.error("Could not find nodes or links arrays in knowledge.js!");
  process.exit(1);
}

// Safely parse arrays by evaluating them
const nodes = eval(`[${nodesMatch[1]}]`);
const links = eval(`[${linksMatch[1]}]`);

console.log(`Found ${nodes.length} nodes and ${links.length} links in knowledge.js.`);

const nodeIds = new Set(nodes.map(n => n.id));
let missingCount = 0;
const missingNodes = new Set();

links.forEach(([src, dst], idx) => {
  if (!nodeIds.has(src)) {
    console.error(`Link index ${idx}: Source node "${src}" does not exist in nodes array!`);
    missingNodes.add(src);
    missingCount++;
  }
  if (!nodeIds.has(dst)) {
    console.error(`Link index ${idx}: Target node "${dst}" does not exist in nodes array!`);
    missingNodes.add(dst);
    missingCount++;
  }
});

if (missingCount > 0) {
  console.error(`\nValidation FAILED: Found ${missingCount} missing node references across ${missingNodes.size} unique invalid node names.`);
  process.exit(1);
} else {
  console.log("Validation PASSED: All links connect valid existing nodes.");
  process.exit(0);
}
