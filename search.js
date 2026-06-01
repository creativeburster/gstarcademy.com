// CAD Learn Hub — Unified Instant Trie Search Engine (search.js)

class TrieNode {
  constructor() {
    this.children = {};
    this.isWord = false;
    this.nodes = []; // Store actual nodes that map to this prefix
  }
}

class CADPrefixTrie {
  constructor() {
    this.root = new TrieNode();
  }

  // Insert a node mapping into the Trie (indexes multiple tokens)
  insert(word, nodeData) {
    if (!word) return;
    const cleanWord = word.toLowerCase().trim();
    if (!cleanWord) return;

    // Index the full string
    this._addPhrase(cleanWord, nodeData);

    // Index individual tokens (words) so users can search multi-word terms by any word
    const tokens = cleanWord.split(/[\s\-_/]+/).filter(t => t.length > 1);
    tokens.forEach(tok => {
      this._addPhrase(tok, nodeData);
    });
  }

  _addPhrase(phrase, nodeData) {
    let current = this.root;
    for (let char of phrase) {
      if (!current.children[char]) {
        current.children[char] = new TrieNode();
      }
      current = current.children[char];
    }
    current.isWord = true;
    // Prevent duplicate node entries under the same word
    if (!current.nodes.some(n => n.id === nodeData.id)) {
      current.nodes.push(nodeData);
    }
  }

  // Search the Trie for matched nodes under the prefix
  search(prefix) {
    if (!prefix) return [];
    const cleanPrefix = prefix.toLowerCase().trim();
    let current = this.root;
    for (let char of cleanPrefix) {
      if (!current.children[char]) {
        return []; // No matches
      }
      current = current.children[char];
    }
    const results = [];
    this._collectAll(current, results);
    return results;
  }

  _collectAll(node, results) {
    if (node.isWord) {
      node.nodes.forEach(n => {
        if (!results.some(r => r.id === n.id)) {
          results.push(n);
        }
      });
    }
    for (let key in node.children) {
      this._collectAll(node.children[key], results);
    }
  }
}

// Global Search State
const CADSearch = {
  trie: new CADPrefixTrie(),
  initialized: false,

  // Load compiled nodes database and initialize search handlers
  async init() {
    if (this.initialized) return;
    
    // Resolve absolute path to data/search_nodes.json depending on subdirectory depth
    const dataPath = this.resolvePath("./data/search_nodes.json");

    try {
      const resp = await fetch(dataPath);
      if (!resp.ok) throw new Error("Search index fetch failed");
      const nodes = await resp.json();
      
      // Populate Trie Index
      nodes.forEach(node => {
        // Index by ID
        this.trie.insert(node.id, node);
        // Index by tags
        if (node.tags && Array.isArray(node.tags)) {
          node.tags.forEach(tag => this.trie.insert(tag, node));
        }
      });

      this.initialized = true;
      console.log(`[Search Engine] Prefix Trie built with ${nodes.length} nodes successfully.`);
      
      // Bind to all visible search inputs on the page
      this.bindInputs();
    } catch (err) {
      console.warn("[Search Engine] Falling back to dynamic search bindings: ", err);
    }
  },

  // Helper method to insert tag prefixes specifically
  trieNodeInsert(term, node) {
    this.trie.insert(term, node);
  },

  // Resolve file paths correctly for root files and subdirectory files (kb/concepts/ etc.)
  resolvePath(originalUrl) {
    const pathname = window.location.pathname;
    const isSubdir = pathname.includes("/kb/concepts/") || pathname.includes("/kb/software/") || pathname.includes("/kb/vendors/");
    
    if (isSubdir) {
      // If we are inside /kb/concepts/, /kb/software/, or /kb/vendors/
      if (originalUrl.startsWith("./data/")) {
        return "../../" + originalUrl.replace("./", "");
      }
      if (originalUrl.startsWith("./kb/concepts/")) {
        if (pathname.includes("/kb/concepts/")) {
          return originalUrl.replace("./kb/concepts/", "./");
        } else {
          return originalUrl.replace("./kb/concepts/", "../concepts/");
        }
      }
      if (originalUrl.startsWith("./kb/software/")) {
        if (pathname.includes("/kb/software/")) {
          return originalUrl.replace("./kb/software/", "./");
        } else {
          return originalUrl.replace("./kb/software/", "../software/");
        }
      }
      if (originalUrl.startsWith("./kb/vendors/")) {
        if (pathname.includes("/kb/vendors/")) {
          return originalUrl.replace("./kb/vendors/", "./");
        } else {
          return originalUrl.replace("./kb/vendors/", "../vendors/");
        }
      }
      if (originalUrl.startsWith("./")) {
        return "../../" + originalUrl.replace("./", "");
      }
    }
    return originalUrl;
  },

  // Find all search inputs and bind handlers
  bindInputs() {
    // 1. Sidebar Search (Wiki pages)
    const sidebarSearch = document.getElementById("kb-sidebar-search");
    if (sidebarSearch) {
      this.attachDropdown(sidebarSearch);
      if (document.activeElement === sidebarSearch && sidebarSearch.value.trim()) {
        sidebarSearch.dispatchEvent(new Event("input"));
      }
    }

    // 2. Homepage Hero Search
    const heroSearchRow = document.querySelector(".hero-search-shell input");
    if (heroSearchRow) {
      this.attachDropdown(heroSearchRow);
      if (document.activeElement === heroSearchRow && heroSearchRow.value.trim()) {
        heroSearchRow.dispatchEvent(new Event("input"));
      }
      // Bind home search button as well
      const heroSearchBtn = document.querySelector(".hero-search-shell button");
      if (heroSearchBtn) {
        heroSearchBtn.addEventListener("click", () => {
          this.triggerGeneralSearch(heroSearchRow.value);
        });
      }
    }

    // 3. Tutorials search input
    const tutorialSearch = document.querySelector(".search-row input");
    // Only bind autocomplete if NOT on the tutorials page (to avoid conflict with dynamic filter)
    if (tutorialSearch && document.body.getAttribute("data-page") !== "tutorials") {
      this.attachDropdown(tutorialSearch);
      if (document.activeElement === tutorialSearch && tutorialSearch.value.trim()) {
        tutorialSearch.dispatchEvent(new Event("input"));
      }
    }

    // 4. Offline Page Search
    const offlineSearchRow = document.querySelector(".offline-search-shell input");
    if (offlineSearchRow) {
      this.attachDropdown(offlineSearchRow);
      if (document.activeElement === offlineSearchRow && offlineSearchRow.value.trim()) {
        offlineSearchRow.dispatchEvent(new Event("input"));
      }
    }
  },

  // Redirect to full terms index or closest match on manual search triggers
  triggerGeneralSearch(query) {
    if (!query.trim()) return;
    const matches = this.trie.search(query);
    if (matches.length > 0) {
      // Navigate to the first best match
      window.location.href = this.resolvePath(matches[0].url);
    } else {
      // Fallback: search on kb-terms index
      const termsIndex = this.resolvePath("./kb-terms.html");
      window.location.href = `${termsIndex}?q=${encodeURIComponent(query)}`;
    }
  },

  // Attach a floating suggestions dropdown to an input element
  attachDropdown(inputEl) {
    // Prevent default browser autocomplete behaviors
    inputEl.setAttribute("autocomplete", "off");
    inputEl.setAttribute("aria-haspopup", "listbox");

    // Create unique suggestions list container
    const dropdown = document.createElement("div");
    dropdown.className = "search-suggestions-dropdown";
    dropdown.setAttribute("role", "listbox");
    dropdown.hidden = true;
    
    // Position dropdown below input
    inputEl.parentNode.appendChild(dropdown);

    let activeIndex = -1;
    let currentMatches = [];

    const renderSuggestions = (query) => {
      dropdown.innerHTML = "";
      activeIndex = -1;

      if (!query.trim()) {
        dropdown.hidden = true;
        return;
      }

      currentMatches = this.trie.search(query).slice(0, 8); // Top 8 matches max

      if (currentMatches.length === 0) {
        const noRes = document.createElement("div");
        noRes.className = "suggestion-no-results";
        noRes.textContent = "No matching concepts found.";
        dropdown.appendChild(noRes);
        dropdown.hidden = false;
        return;
      }

      currentMatches.forEach((node, index) => {
        const item = document.createElement("div");
        item.className = "suggestion-item";
        item.setAttribute("role", "option");
        item.setAttribute("id", `suggestion-opt-${index}`);

        // Category Badge Color
        let badgeClass = "badge-concept";
        if (node.type === "product") badgeClass = "badge-product";
        else if (node.type === "vendor") badgeClass = "badge-vendor";
        else if (node.type === "domain") badgeClass = "badge-domain";

        // Highlight matching text in title
        const titleText = node.id;
        const qIndex = titleText.toLowerCase().indexOf(query.toLowerCase());
        let highlightedTitle = titleText;
        if (qIndex >= 0) {
          const prefix = titleText.substring(0, qIndex);
          const matchText = titleText.substring(qIndex, qIndex + query.length);
          const suffix = titleText.substring(qIndex + query.length);
          highlightedTitle = `${prefix}<strong class="search-highlight">${matchText}</strong>${suffix}`;
        }

        item.innerHTML = `
          <span class="suggestion-badge ${badgeClass}">${node.type.toUpperCase()}</span>
          <div class="suggestion-info">
            <span class="suggestion-title">${highlightedTitle}</span>
            <span class="suggestion-hint">${node.hint || "Explore related CAD documentation"}</span>
          </div>
          <span class="suggestion-arrow" aria-hidden="true">›</span>
        `;

        item.addEventListener("click", () => {
          window.location.href = this.resolvePath(node.url);
        });

        dropdown.appendChild(item);
      });

      dropdown.hidden = false;
    };

    // Event: Input
    inputEl.addEventListener("input", (e) => {
      renderSuggestions(e.target.value);
    });

    // Event: Focus
    inputEl.addEventListener("focus", () => {
      if (inputEl.value.trim()) renderSuggestions(inputEl.value);
    });

    // Event: Keyboard Navigation
    inputEl.addEventListener("keydown", (e) => {
      if (dropdown.hidden) return;

      const items = dropdown.querySelectorAll(".suggestion-item");

      if (e.key === "ArrowDown") {
        e.preventDefault();
        activeIndex = (activeIndex + 1) % items.length;
        this.updateActiveItem(items, activeIndex, inputEl);
      } else if (e.key === "ArrowUp") {
        e.preventDefault();
        activeIndex = (activeIndex - 1 + items.length) % items.length;
        this.updateActiveItem(items, activeIndex, inputEl);
      } else if (e.key === "Enter") {
        if (activeIndex >= 0 && activeIndex < currentMatches.length) {
          e.preventDefault();
          window.location.href = this.resolvePath(currentMatches[activeIndex].url);
        } else {
          // Full search query redirect
          e.preventDefault();
          this.triggerGeneralSearch(inputEl.value);
        }
      } else if (e.key === "Escape") {
        dropdown.hidden = true;
        inputEl.blur();
      }
    });

    // Close dropdown on click outside
    document.addEventListener("click", (e) => {
      if (!inputEl.contains(e.target) && !dropdown.contains(e.target)) {
        dropdown.hidden = true;
      }
    });
  },

  // Highlight active element and sync aria-active descendant
  updateActiveItem(items, activeIndex, inputEl) {
    items.forEach((item, idx) => {
      if (idx === activeIndex) {
        item.classList.add("active");
        item.setAttribute("aria-selected", "true");
        inputEl.setAttribute("aria-activedescendant", item.id);
        
        // Scroll into view if needed
        item.scrollIntoView({ block: "nearest" });
      } else {
        item.classList.remove("active");
        item.setAttribute("aria-selected", "false");
      }
    });
  }
};

// Initialize search engine lazily on input interaction to boost page load speed
document.addEventListener("DOMContentLoaded", () => {
  const searchInputs = [
    document.getElementById("kb-sidebar-search"),
    document.querySelector(".hero-search-shell input"),
    document.querySelector(".search-row input"),
    document.querySelector(".offline-search-shell input")
  ].filter(Boolean);

  if (searchInputs.length === 0) {
    // Fallback: in case inputs are loaded dynamically, bind focus handler to body
    document.body.addEventListener("focusin", (e) => {
      if (e.target && (e.target.id === "kb-sidebar-search" || e.target.type === "search" || e.target.placeholder?.toLowerCase().includes("search"))) {
        CADSearch.init();
      }
    }, { once: true });
    return;
  }

  const triggerInit = () => {
    CADSearch.init();
    // Remove listeners once initialized
    searchInputs.forEach(input => {
      input.removeEventListener("focus", triggerInit);
      input.removeEventListener("input", triggerInit);
      input.removeEventListener("mouseenter", triggerInit);
    });
  };

  searchInputs.forEach(input => {
    input.addEventListener("focus", triggerInit, { once: true });
    input.addEventListener("input", triggerInit, { once: true });
    input.addEventListener("mouseenter", triggerInit, { once: true }); // pre-fetch on hover
  });
});
