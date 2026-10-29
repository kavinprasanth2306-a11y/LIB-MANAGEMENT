/**
 * DSA-Powered Library Management System
 * Frontend Client & Interactive State Visualizer
 */

const API_BASE = "http://127.0.0.1:8000/api";

// Current active state
let currentBooks = [];
let selectedBookForIssue = null;
let currentDsaTab = "unit1";

// Document ready bootstrap
document.addEventListener("DOMContentLoaded", () => {
  if (window.lucide) {
    lucide.createIcons();
  }
  loadInitialData();
  // Poll periodic buffer updates
  setInterval(refreshActiveBuffers, 5000);
});

async function loadInitialData() {
  await fetchBooks();
  await refreshFeaturedCarousel();
  await refreshActiveBuffers();
  await refreshVisualizerState();
}

// ==========================================
// Toast Notifications
// ==========================================

function showToast(message, type = "info") {
  const container = document.getElementById("toast-container");
  const toast = document.createElement("div");
  const bgColors = {
    info: "bg-indigo-900/90 border-indigo-500 text-indigo-100",
    success: "bg-emerald-900/90 border-emerald-500 text-emerald-100",
    error: "bg-rose-900/90 border-rose-500 text-rose-100",
    warning: "bg-amber-900/90 border-amber-500 text-amber-100",
  };
  toast.className = `p-3 rounded-xl border shadow-xl text-xs flex items-center space-x-2 transition-all duration-300 transform translate-y-2 pointer-events-auto ${bgColors[type] || bgColors.info}`;
  toast.innerHTML = `<span>${message}</span>`;
  container.appendChild(toast);

  setTimeout(() => {
    toast.classList.add("opacity-0", "translate-y-4");
    setTimeout(() => toast.remove(), 300);
  }, 3500);
}

// ==========================================
// Tab Switching
// ==========================================

function switchMainTab(tab) {
  const portalView = document.getElementById("view-portal");
  const visualizerView = document.getElementById("view-visualizer");
  const portalBtn = document.getElementById("tab-portal-btn");
  const visualizerBtn = document.getElementById("tab-visualizer-btn");

  if (tab === "portal") {
    portalView.classList.remove("hidden");
    visualizerView.classList.add("hidden");
    portalBtn.className = "px-4 py-1.5 rounded-lg text-sm font-medium transition-all bg-indigo-600 text-white shadow-sm flex items-center space-x-2";
    visualizerBtn.className = "px-4 py-1.5 rounded-lg text-sm font-medium transition-all text-slate-400 hover:text-white flex items-center space-x-2";
  } else {
    portalView.classList.add("hidden");
    visualizerView.classList.remove("hidden");
    visualizerBtn.className = "px-4 py-1.5 rounded-lg text-sm font-medium transition-all bg-indigo-600 text-white shadow-sm flex items-center space-x-2";
    portalBtn.className = "px-4 py-1.5 rounded-lg text-sm font-medium transition-all text-slate-400 hover:text-white flex items-center space-x-2";
    refreshVisualizerState();
  }
  if (window.lucide) lucide.createIcons();
}

function switchDsaSection(unit) {
  currentDsaTab = unit;
  const units = ["unit1", "unit2", "unit3", "unit4", "unit5"];
  units.forEach(u => {
    const sec = document.getElementById(`dsa-sec-${u}`);
    const btn = document.getElementById(`nav-dsa-${u}`);
    if (u === unit) {
      sec.classList.remove("hidden");
      btn.className = "dsa-nav-btn px-4 py-2 rounded-lg text-xs font-semibold bg-indigo-600 text-white transition";
    } else {
      sec.classList.add("hidden");
      btn.className = "dsa-nav-btn px-4 py-2 rounded-lg text-xs font-semibold text-slate-400 hover:text-slate-200 transition";
    }
  });
  refreshVisualizerState();
  if (window.lucide) lucide.createIcons();
}

// ==========================================
// API Operations: Books
// ==========================================

async function fetchBooks() {
  try {
    const res = await fetch(`${API_BASE}/books`);
    const data = await res.json();
    currentBooks = data.books || [];
    renderBooksGrid(currentBooks);
    document.getElementById("catalog-count-badge").innerText = currentBooks.length;
  } catch (err) {
    console.error("fetchBooks error:", err);
  }
}

function renderBooksGrid(books) {
  const container = document.getElementById("books-grid");
  if (!books || books.length === 0) {
    container.innerHTML = `<div class="col-span-2 text-center py-8 text-slate-500 text-xs">No books available in the catalog.</div>`;
    return;
  }

  container.innerHTML = books.map(book => {
    const isAvailable = book.available_copies > 0;
    return `
      <div class="p-4 bg-slate-900/70 border border-slate-800 rounded-xl hover:border-slate-700 transition flex flex-col justify-between space-y-3">
        <div>
          <div class="flex items-start justify-between gap-2">
            <span class="text-[10px] font-mono px-2 py-0.5 rounded bg-indigo-500/10 text-indigo-400 border border-indigo-500/20">
              ID #${book.id}
            </span>
            <span class="text-[10px] font-semibold px-2 py-0.5 rounded ${isAvailable ? 'bg-emerald-500/10 text-emerald-400 border border-emerald-500/20' : 'bg-rose-500/10 text-rose-400 border border-rose-500/20'}">
              ${isAvailable ? `${book.available_copies} of ${book.total_copies} Available` : 'Waitlist Active'}
            </span>
          </div>
          <h4 class="font-bold text-sm text-slate-100 mt-2 line-clamp-1" title="${book.title}">${book.title}</h4>
          <p class="text-xs text-slate-400">${book.author} (${book.year})</p>
          <div class="flex items-center space-x-2 mt-2 text-[11px] text-slate-500 font-mono">
            <span>ISBN: ${book.isbn}</span>
            <span>•</span>
            <span>Borrows: ${book.borrow_count}</span>
          </div>
        </div>
        <div class="pt-2 border-t border-slate-800 flex items-center justify-between">
          <span class="text-[11px] text-indigo-400">${book.category}</span>
          <div class="flex items-center space-x-1.5">
            <button onclick="promptReturnBook(${book.id})" class="px-2.5 py-1 bg-slate-800 hover:bg-slate-700 text-slate-300 text-xs rounded transition">
              Return
            </button>
            <button onclick="openIssueModal(${book.id}, '${escapeQuotes(book.title)}')" class="px-3 py-1 bg-indigo-600 hover:bg-indigo-500 text-white text-xs font-semibold rounded shadow transition">
              ${isAvailable ? 'Issue' : 'Enqueue'}
            </button>
          </div>
        </div>
      </div>
    `;
  }).join("");

  if (window.lucide) lucide.createIcons();
}

function escapeQuotes(str) {
  return str.replace(/'/g, "\\'");
}

// ==========================================
// Live Autocomplete via Trie
// ==========================================

let searchDebounce = null;
async function onSearchInput(val) {
  const query = val.trim();
  const dropdown = document.getElementById("trie-autocomplete-box");
  if (!query) {
    dropdown.classList.add("hidden");
    return;
  }

  clearTimeout(searchDebounce);
  searchDebounce = setTimeout(async () => {
    try {
      const res = await fetch(`${API_BASE}/dsa/unit4/autocomplete?prefix=${encodeURIComponent(query)}`);
      const data = await res.json();
      if (data.matches && data.matches.length > 0) {
        dropdown.innerHTML = `
          <div class="text-[10px] text-slate-500 font-mono px-2 pb-1 border-b border-slate-800 flex justify-between">
            <span>TRIE PREFIX LOOKUP ($O(L)$)</span>
            <span>${data.steps} Steps</span>
          </div>
          ${data.matches.map(m => `
            <div onclick="selectTrieMatch('${escapeQuotes(m.term)}')" class="p-2 hover:bg-slate-800 rounded-lg cursor-pointer transition flex items-center justify-between text-xs">
              <span class="font-medium text-slate-200 capitalize">${m.term}</span>
              <span class="text-[10px] text-indigo-400 bg-indigo-500/10 px-1.5 py-0.5 rounded font-mono">Matched</span>
            </div>
          `).join("")}
        `;
        dropdown.classList.remove("hidden");
      } else {
        dropdown.innerHTML = `<div class="p-2 text-xs text-slate-500 text-center">No prefix match in Trie.</div>`;
        dropdown.classList.remove("hidden");
      }
    } catch (err) {
      console.error("trie autocomplete error:", err);
    }
  }, 200);
}

function selectTrieMatch(term) {
  document.getElementById("search-input").value = term;
  document.getElementById("trie-autocomplete-box").classList.add("hidden");
  // Filter books locally
  const filtered = currentBooks.filter(b => 
    b.title.toLowerCase().includes(term.toLowerCase()) || 
    b.author.toLowerCase().includes(term.toLowerCase())
  );
  renderBooksGrid(filtered);
}

// Close autocomplete when clicking outside
document.addEventListener("click", (e) => {
  const box = document.getElementById("trie-autocomplete-box");
  const input = document.getElementById("search-input");
  if (box && input && !box.contains(e.target) && !input.contains(e.target)) {
    box.classList.add("hidden");
  }
});

// ==========================================
// Sort Catalog
// ==========================================

async function applyCatalogSort() {
  const field = document.getElementById("sort-field").value;
  const algo = document.getElementById("sort-algo").value;

  try {
    const res = await fetch(`${API_BASE}/dsa/unit3/sort`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ field, algorithm: algo, ascending: true })
    });
    const data = await res.json();
    renderBooksGrid(data.sorted_books);

    // Show banner
    const banner = document.getElementById("sort-metrics-banner");
    const bannerText = document.getElementById("sort-metrics-text");
    bannerText.innerText = `Algorithm: ${data.algorithm} | Key: ${data.field} | Comparisons: ${data.comparisons} | Swaps/Shifts: ${data.swaps}`;
    banner.classList.remove("hidden");
    showToast(`Sorted via ${data.algorithm} in ${data.comparisons} comparisons`, "info");
  } catch (err) {
    showToast("Sorting error", "error");
  }
}

function closeSortBanner() {
  document.getElementById("sort-metrics-banner").classList.add("hidden");
}

// ==========================================
// Operational Buffers: Drop-box, VIP Deque, Priority Queue
// ==========================================

async function refreshActiveBuffers() {
  try {
    // 1. Drop-Box Circular Queue
    const cqRes = await fetch(`${API_BASE}/dsa/unit1/dropbox-state`);
    const cqData = await cqRes.json();
    renderDropboxSlots(cqData);

    // 2. VIP Deque
    const dqRes = await fetch(`${API_BASE}/dsa/unit1/vip-deque-state`);
    const dqData = await dqRes.json();
    renderVipDeque(dqData);

    // 3. Priority Queue
    const pqRes = await fetch(`${API_BASE}/dsa/unit1/priority-queue-state`);
    const pqData = await pqRes.json();
    renderPriorityQueue(pqData);
  } catch (e) {
    // silently catch offline polling
  }
}

function renderDropboxSlots(cq) {
  const container = document.getElementById("dropbox-slots");
  const status = document.getElementById("dropbox-status-text");
  status.innerText = `Front: ${cq.front} | Rear: ${cq.rear} | Count: ${cq.count}/${cq.capacity} ${cq.is_full ? '(BUFFER FULL)' : ''}`;

  container.innerHTML = cq.slots.map(s => {
    let classes = "cq-slot";
    if (s.value) classes += " slot-occupied";
    if (s.is_front) classes += " slot-front";
    if (s.is_rear) classes += " slot-rear";

    return `
      <div class="${classes}" title="${s.value ? JSON.stringify(s.value) : 'Empty Slot'}">
        <span class="text-[9px] text-slate-400">#${s.index}</span>
        <span class="font-bold text-[11px]">${s.value ? 'Book' : '-'}</span>
      </div>
    `;
  }).join("");
}

async function processDropboxItem() {
  try {
    const res = await fetch(`${API_BASE}/dsa/unit1/dropbox-process`, { method: "POST" });
    const data = await res.json();
    if (data.success) {
      showToast(`Processed item from drop-box: ${data.processed_item.title}`, "success");
      refreshActiveBuffers();
    } else {
      showToast(data.message, "warning");
    }
  } catch (e) {
    showToast("Error processing drop-box", "error");
  }
}

function renderVipDeque(dq) {
  const container = document.getElementById("vip-deque-list");
  if (!dq.items || dq.items.length === 0) {
    container.innerHTML = `<div class="text-slate-500 py-2">No pending VIP/Faculty requests.</div>`;
    return;
  }
  container.innerHTML = dq.items.map((item, idx) => `
    <div class="p-2.5 rounded-lg bg-slate-900 border border-slate-800 flex items-center justify-between">
      <div class="flex items-center space-x-2">
        <span class="text-[10px] font-mono px-1.5 py-0.5 rounded ${idx === 0 ? 'bg-emerald-500/20 text-emerald-300' : 'bg-slate-800 text-slate-400'}">
          ${idx === 0 ? 'FRONT' : `Pos #${idx+1}`}
        </span>
        <span class="font-medium text-slate-200">${item.name || item.student_id}</span>
      </div>
      <span class="text-[10px] text-slate-500 font-mono">Book #${item.book_id}</span>
    </div>
  `).join("");
}

function renderPriorityQueue(pq) {
  const container = document.getElementById("priority-queue-list");
  if (!pq.items || pq.items.length === 0) {
    container.innerHTML = `<div class="text-slate-500 py-2">No urgency reservations in queue.</div>`;
    return;
  }
  container.innerHTML = pq.items.map((item, idx) => `
    <div class="p-2.5 rounded-lg bg-slate-900 border border-slate-800 flex items-center justify-between">
      <div class="flex items-center space-x-2">
        <span class="text-[10px] font-mono px-1.5 py-0.5 rounded bg-purple-500/20 text-purple-300 font-bold">
          Priority ${item.priority}
        </span>
        <span class="font-medium text-slate-200">${item.data.name || item.data.student_id}</span>
      </div>
      <span class="text-[10px] text-slate-400 italic">${item.data.note || `Book #${item.data.book_id}`}</span>
    </div>
  `).join("");
}

// ==========================================
// Featured Carousel via CLL
// ==========================================

async function refreshFeaturedCarousel() {
  try {
    const res = await fetch(`${API_BASE}/dsa/unit2/cll-carousel`);
    const data = await res.json();
    const container = document.getElementById("featured-carousel-display");
    if (!data.chain || !data.chain.nodes) return;

    container.innerHTML = data.chain.nodes.map(n => `
      <div class="flex-shrink-0 w-48 p-3 rounded-xl border ${n.is_current ? 'border-indigo-500 bg-indigo-950/40' : 'border-slate-800 bg-slate-900/40'} transition-all">
        <span class="text-[9px] font-mono px-1.5 py-0.5 rounded bg-slate-800 text-slate-400">Node #${n.index}</span>
        <h5 class="text-xs font-bold text-slate-100 mt-1 truncate">${n.data.title}</h5>
        <p class="text-[10px] text-slate-400 truncate">${n.data.author}</p>
        <div class="mt-2 text-[9px] font-mono ${n.is_current ? 'text-indigo-400 font-bold' : 'text-slate-600'}">
          ${n.points_to_head ? 'Points -> HEAD (Loop)' : 'Points -> Next'}
        </div>
      </div>
    `).join("");
  } catch (e) {
    console.error(e);
  }
}

async function cycleFeaturedCarousel() {
  try {
    await fetch(`${API_BASE}/dsa/unit2/cll-carousel/cycle`, { method: "POST" });
    await refreshFeaturedCarousel();
  } catch (e) {
    console.error(e);
  }
}

// ==========================================
// Modals & Action Operations
// ==========================================

function openAddBookModal() {
  document.getElementById("modal-add-book").classList.remove("hidden");
}
function closeAddBookModal() {
  document.getElementById("modal-add-book").classList.add("hidden");
}

async function submitAddBook(e) {
  e.preventDefault();
  const title = document.getElementById("new-book-title").value.trim();
  const author = document.getElementById("new-book-author").value.trim();
  const isbn = document.getElementById("new-book-isbn").value.trim();
  const year = parseInt(document.getElementById("new-book-year").value);
  const category = document.getElementById("new-book-category").value;
  const copies = parseInt(document.getElementById("new-book-copies").value);

  try {
    const res = await fetch(`${API_BASE}/books`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ title, author, isbn, year, category, total_copies: copies })
    });
    const data = await res.json();
    closeAddBookModal();
    showToast(data.message, "success");
    await fetchBooks();
    await refreshVisualizerState();
  } catch (err) {
    showToast("Error adding book", "error");
  }
}

function openIssueModal(bookId, bookTitle) {
  selectedBookForIssue = bookId;
  document.getElementById("issue-modal-title").innerText = `Issue "${bookTitle}" (ID: ${bookId})`;
  document.getElementById("modal-issue-book").classList.remove("hidden");
}
function closeIssueModal() {
  document.getElementById("modal-issue-book").classList.add("hidden");
}

async function submitIssueBook() {
  if (!selectedBookForIssue) return;
  const studentId = document.getElementById("issue-student-select").value;
  const isVip = document.getElementById("issue-is-vip").checked;

  try {
    const res = await fetch(`${API_BASE}/books/issue`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ book_id: selectedBookForIssue, student_id: studentId, is_vip: isVip })
    });
    const data = await res.json();
    closeIssueModal();
    showToast(data.message, data.success ? "success" : "warning");
    await fetchBooks();
    await refreshActiveBuffers();
    await refreshVisualizerState();
  } catch (e) {
    showToast("Error issuing book", "error");
  }
}

async function promptReturnBook(bookId) {
  const days = prompt("Enter overdue days (0 if on time):", "0");
  if (days === null) return;
  const daysInt = parseInt(days) || 0;

  try {
    const res = await fetch(`${API_BASE}/books/return`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ book_id: bookId, student_id: "STU1001", overdue_days: daysInt })
    });
    const data = await res.json();
    showToast(data.message, "success");
    await fetchBooks();
    await refreshActiveBuffers();
    await refreshVisualizerState();
  } catch (e) {
    showToast("Error returning book", "error");
  }
}

async function triggerUndo() {
  try {
    const res = await fetch(`${API_BASE}/undo`, { method: "POST" });
    const data = await res.json();
    if (data.success) {
      showToast(data.message, "success");
      await fetchBooks();
      await refreshActiveBuffers();
      await refreshVisualizerState();
    } else {
      showToast(data.message, "warning");
    }
  } catch (e) {
    showToast("Error executing undo", "error");
  }
}

// ==========================================
// Fine Evaluator Modals
// ==========================================

function openFineCalculatorModal() {
  document.getElementById("modal-fine-eval").classList.remove("hidden");
}
function closeFineCalculatorModal() {
  document.getElementById("modal-fine-eval").classList.add("hidden");
}

async function computeModalFine() {
  const formula = document.getElementById("modal-formula-input").value;
  const days = document.getElementById("modal-formula-days").value;

  try {
    const res = await fetch(`${API_BASE}/dsa/unit1/evaluate-fine?formula=${encodeURIComponent(formula)}&days=${days}`, { method: "POST" });
    const data = await res.json();
    const box = document.getElementById("modal-fine-result");
    box.innerHTML = `
      <div><span class="text-slate-400">Postfix:</span> <span class="text-indigo-400">${data.postfix.join(" ")}</span></div>
      <div><span class="text-slate-400">Result:</span> <span class="text-emerald-400 font-bold">$${data.result}</span></div>
      <div class="text-[10px] text-slate-500 pt-1">Expression evaluated via Stack ADT Infix-to-Postfix</div>
    `;
    box.classList.remove("hidden");
  } catch (e) {
    showToast("Evaluation error in formula", "error");
  }
}

// ==========================================
// DSA Visualizer Inspector Handlers
// ==========================================

async function refreshVisualizerState() {
  if (currentDsaTab === "unit1") {
    await renderUnit1Visualizer();
  } else if (currentDsaTab === "unit2") {
    await renderUnit2Visualizer();
  } else if (currentDsaTab === "unit3") {
    await renderUnit3Visualizer();
  } else if (currentDsaTab === "unit4") {
    await renderUnit4Visualizer();
  } else if (currentDsaTab === "unit5") {
    await renderUnit5Visualizer();
  }
}

// UNIT 1: Stack & Expression Evaluation
async function renderUnit1Visualizer() {
  try {
    const res = await fetch(`${API_BASE}/dsa/unit1/stack-state`);
    const data = await res.json();
    const stack = data.undo_stack;

    document.getElementById("undo-stack-count").innerText = `${stack.size} Operations`;
    const diagram = document.getElementById("undo-stack-diagram");

    if (!stack.items || stack.items.length === 0) {
      diagram.innerHTML = `<div class="text-xs text-slate-500 text-center py-4">Stack is Empty (TOS = -1)</div>`;
    } else {
      diagram.innerHTML = stack.items.map((item, idx) => `
        <div class="p-2 rounded bg-indigo-950/60 border border-indigo-500/30 text-xs font-mono flex items-center justify-between">
          <span>[TOS-${idx}] ${item.action}: Book #${item.book_id}</span>
          <span class="text-[10px] text-indigo-400">${idx === 0 ? '<- TOP OF STACK' : ''}</span>
        </div>
      `).join("");
    }
  } catch (e) {
    console.error(e);
  }
}

async function runVisualizerEval() {
  const formula = document.getElementById("eval-formula-input").value;
  try {
    const res = await fetch(`${API_BASE}/dsa/unit1/evaluate-fine?formula=${encodeURIComponent(formula)}&days=5`, { method: "POST" });
    const data = await res.json();
    document.getElementById("eval-postfix").innerText = data.postfix.join(" ");
    document.getElementById("eval-final-res").innerText = `$${data.result}`;
  } catch (e) {
    showToast("Malformed Expression", "error");
  }
}

// UNIT 2: SLL & DLL Pointer Chains
async function renderUnit2Visualizer() {
  await refreshSllHistory();
  await refreshDllNavigator();
}

async function refreshSllHistory() {
  try {
    const res = await fetch(`${API_BASE}/dsa/unit2/sll-history`);
    const data = await res.json();
    const container = document.getElementById("sll-chain-container");

    if (!data.nodes || data.nodes.length === 0) {
      container.innerHTML = `<div class="text-xs text-slate-500">HEAD -> NULL (Empty Singly Linked List)</div>`;
      return;
    }

    let html = `<div class="text-xs font-mono font-bold text-indigo-400 mr-2">HEAD -></div>`;
    html += data.nodes.map(n => `
      <div class="dsa-node text-xs font-mono">
        <div class="text-[10px] text-slate-400">Node #${n.index}</div>
        <div class="font-bold text-white">${n.data.action}</div>
        <div class="text-[10px] text-indigo-300">Book #${n.data.book_id}</div>
      </div>
      ${n.has_next ? '<div class="dsa-arrow text-indigo-400">-></div>' : '<div class="dsa-arrow text-rose-400">-> NULL</div>'}
    `).join("");
    container.innerHTML = html;
  } catch (e) {
    console.error(e);
  }
}

async function refreshDllNavigator() {
  try {
    const res = await fetch(`${API_BASE}/dsa/unit2/dll-navigator`);
    const data = await res.json();
    const container = document.getElementById("dll-chain-container");

    if (!data.chain || !data.chain.nodes || data.chain.nodes.length === 0) {
      container.innerHTML = `<div class="text-xs text-slate-500">NULL <- HEAD <-> TAIL -> NULL</div>`;
      return;
    }

    let html = `<div class="text-xs font-mono text-slate-500 mr-2">NULL &lt;-&gt;</div>`;
    html += data.chain.nodes.map(n => `
      <div class="dsa-node ${n.is_current ? 'active-node' : ''} text-xs font-mono">
        <div class="text-[10px] text-slate-400">${n.is_current ? 'CURRENT' : `Node #${n.index}`}</div>
        <div class="font-bold text-white truncate max-w-[120px]">${n.data.title}</div>
      </div>
      ${n.has_next ? '<div class="dsa-arrow text-indigo-400">&lt;-&gt;</div>' : '<div class="dsa-arrow text-rose-400">&lt;-&gt; NULL</div>'}
    `).join("");
    container.innerHTML = html;
  } catch (e) {
    console.error(e);
  }
}

async function navigateDll(dir) {
  try {
    await fetch(`${API_BASE}/dsa/unit2/dll-navigator/step?direction=${dir}`, { method: "POST" });
    await refreshDllNavigator();
  } catch (e) {
    console.error(e);
  }
}

// UNIT 3: Hash Table & Search Benchmarks
async function renderUnit3Visualizer() {
  try {
    const res = await fetch(`${API_BASE}/dsa/unit3/hash-table-state`);
    const data = await res.json();

    document.getElementById("ht-metric-count").innerText = data.count;
    document.getElementById("ht-metric-load").innerText = data.load_factor;
    document.getElementById("ht-metric-occupied").innerText = `${data.occupied_buckets} / 101`;
    document.getElementById("ht-metric-maxchain").innerText = data.max_chain_length || 0;

    // Highlight active button
    if (data.strategy === "chaining") {
      document.getElementById("strat-chaining-btn").className = "px-2.5 py-1 text-xs rounded-md bg-indigo-600 text-white font-medium";
      document.getElementById("strat-probing-btn").className = "px-2.5 py-1 text-xs rounded-md text-slate-400 hover:text-white font-medium";
    } else {
      document.getElementById("strat-probing-btn").className = "px-2.5 py-1 text-xs rounded-md bg-indigo-600 text-white font-medium";
      document.getElementById("strat-chaining-btn").className = "px-2.5 py-1 text-xs rounded-md text-slate-400 hover:text-white font-medium";
    }

    // Render 101 cells
    const grid = document.getElementById("hash-table-buckets-grid");
    grid.innerHTML = data.buckets.map(b => {
      const hasData = (data.strategy === "chaining" && b.chain_length > 0) || (data.strategy === "probing" && b.status === "occupied");
      return `
        <div class="bucket-cell ${hasData ? 'has-data' : ''}" title="Bucket #${b.bucket} | Items: ${data.strategy === 'chaining' ? b.chain_length : (b.status || 'empty')}">
          <div class="font-bold text-slate-400">${b.bucket}</div>
          <div class="text-[9px] ${hasData ? 'text-indigo-400 font-bold' : 'text-slate-600'}">
            ${data.strategy === 'chaining' ? `${b.chain_length} items` : (b.status ? b.status[0].toUpperCase() : '-')}
          </div>
        </div>
      `;
    }).join("");

  } catch (e) {
    console.error(e);
  }
}

async function toggleHashStrategy(strat) {
  try {
    await fetch(`${API_BASE}/dsa/unit3/hash-table-strategy?strategy=${strat}`, { method: "POST" });
    showToast(`Switched collision resolution to ${strat.toUpperCase()}`, "info");
    await renderUnit3Visualizer();
  } catch (e) {
    showToast("Error switching hash table strategy", "error");
  }
}

async function runSearchBenchmark() {
  const targetId = document.getElementById("search-benchmark-id").value;
  try {
    const res = await fetch(`${API_BASE}/dsa/unit3/search-benchmark`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ query: targetId })
    });
    const data = await res.json();
    const container = document.getElementById("benchmark-results-grid");

    const algorithms = [
      { key: "sequential_search", label: "Sequential Search", color: "indigo" },
      { key: "binary_search_iterative", label: "Binary Search (Iterative)", color: "emerald" },
      { key: "binary_search_recursive", label: "Binary Search (Recursive)", color: "blue" },
      { key: "interpolation_search", label: "Interpolation Search", color: "purple" }
    ];

    container.innerHTML = algorithms.map(algo => {
      const result = data.results[algo.key];
      return `
        <div class="p-4 bg-slate-900/70 border border-slate-800 rounded-xl space-y-2">
          <div class="flex items-center justify-between">
            <span class="font-bold text-xs text-slate-200">${algo.label}</span>
            <span class="text-[10px] font-mono px-1.5 py-0.5 rounded bg-${algo.color}-500/20 text-${algo.color}-300">
              ${result.time_complexity}
            </span>
          </div>
          <div class="text-2xl font-black font-mono text-white">${result.steps} <span class="text-xs font-normal text-slate-400">Steps</span></div>
          <div class="text-[11px] text-slate-400">${result.found ? 'Found Target Key' : 'Target Not Found'}</div>
        </div>
      `;
    }).join("");

  } catch (e) {
    showToast("Benchmark execution error", "error");
  }
}

// UNIT 4: AVL Tree, Traversals, Heaps & B-Tree
let currentAvlTreeData = null;
async function renderUnit4Visualizer() {
  try {
    const res = await fetch(`${API_BASE}/dsa/unit4/avl-tree-state`);
    currentAvlTreeData = await res.json();

    document.getElementById("avl-rotation-badge").innerText = currentAvlTreeData.last_rotation || "Balanced";
    renderTreeCanvas(currentAvlTreeData.tree_json);
    showTraversal("inorder");

    // Heaps & BTree
    await refreshHeapsAndBtree();
  } catch (e) {
    console.error(e);
  }
}

function renderTreeCanvas(treeJson) {
  const container = document.getElementById("avl-tree-canvas-container");
  if (!treeJson) {
    container.innerHTML = `<div class="text-xs text-slate-500">AVL Tree is empty.</div>`;
    return;
  }

  // Generate recursive HTML tree
  function buildHtmlNode(node) {
    if (!node) return '';
    const hasChildren = node.children && node.children.length > 0;
    return `
      <div class="flex flex-col items-center">
        <div class="tree-node-circle" title="Key: ${node.name} | Balance Factor: ${node.balance} | Height: ${node.height}">
          <span class="text-[10px] text-slate-200 truncate max-w-[40px] px-1">${node.name.split(' ')[0]}</span>
        </div>
        <div class="text-[9px] text-indigo-400 font-mono">BF: ${node.balance}</div>
        ${hasChildren ? `
          <div class="w-px h-4 bg-slate-700"></div>
          <div class="flex items-start gap-4">
            ${node.children.map(c => buildHtmlNode(c)).join("")}
          </div>
        ` : ''}
      </div>
    `;
  }

  container.innerHTML = `<div class="flex justify-center p-4">${buildHtmlNode(treeJson)}</div>`;
}

function showTraversal(type) {
  if (!currentAvlTreeData || !currentAvlTreeData.traversals) return;
  const list = currentAvlTreeData.traversals[type] || [];
  const display = document.getElementById("traversal-display");

  // Update tabs
  ["inorder", "preorder", "postorder"].forEach(t => {
    const btn = document.getElementById(`trav-btn-${t}`);
    if (t === type) {
      btn.className = "px-2.5 py-0.5 rounded bg-indigo-600 text-white";
    } else {
      btn.className = "px-2.5 py-0.5 rounded text-slate-400 hover:text-white";
    }
  });

  display.innerText = list.map(item => `[${item.key} (BF:${item.balance})]`).join(" -> ");
}

async function refreshAvlTree() {
  await renderUnit4Visualizer();
  showToast("AVL Tree re-rendered", "info");
}

async function refreshHeapsAndBtree() {
  try {
    const heapRes = await fetch(`${API_BASE}/dsa/unit4/heaps-state`);
    const heapData = await heapRes.json();

    const minContainer = document.getElementById("min-heap-array");
    const minElems = heapData.min_heap_overdue.elements || [];
    minContainer.innerHTML = minElems.slice(0, 8).map((el, idx) => `
      <span class="px-2 py-1 rounded bg-emerald-950/60 border border-emerald-500/30 text-[11px] ${idx === 0 ? 'border-emerald-400 font-bold' : ''}">
        ${idx === 0 ? 'ROOT: ' : ''}${el.score}d (#${el.data.id})
      </span>
    `).join("");

    const maxContainer = document.getElementById("max-heap-array");
    const maxElems = heapData.max_heap_trending.elements || [];
    maxContainer.innerHTML = maxElems.slice(0, 8).map((el, idx) => `
      <span class="px-2 py-1 rounded bg-amber-950/60 border border-amber-500/30 text-[11px] ${idx === 0 ? 'border-amber-400 font-bold' : ''}">
        ${idx === 0 ? 'ROOT: ' : ''}${el.score} borrows (#${el.data.id})
      </span>
    `).join("");

    // B-Tree
    const btreeRes = await fetch(`${API_BASE}/dsa/unit4/btree-state`);
    const btreeData = await btreeRes.json();
    const btreeContainer = document.getElementById("btree-container");
    btreeContainer.innerHTML = `<pre class="text-[11px] text-indigo-300">${JSON.stringify(btreeData, null, 2)}</pre>`;
  } catch (e) {
    console.error(e);
  }
}

// UNIT 5: Graph Theory, Adj List/Matrix, BFS & DFS
async function renderUnit5Visualizer() {
  try {
    const res = await fetch(`${API_BASE}/dsa/unit5/graph-state`);
    const data = await res.json();

    // 1. Adjacency List
    const adjListContainer = document.getElementById("adj-list-container");
    adjListContainer.innerHTML = data.adjacency_list.map(entry => `
      <div class="border-b border-slate-800 pb-1">
        <span class="font-bold text-indigo-400">[${entry.node_id}] ${entry.label}:</span>
        <span class="text-slate-300 ml-1">
          ${entry.neighbors.length > 0 ? entry.neighbors.map(n => `${n.target_label} (${n.relation})`).join(", ") : 'No edges'}
        </span>
      </div>
    `).join("");

    // 2. Adjacency Matrix
    const adjMatrixContainer = document.getElementById("adj-matrix-container");
    const matrix = data.adjacency_matrix;
    let tableHtml = `<table class="w-full text-center border-collapse text-[10px]"><tr><th class="p-1"></th>`;
    matrix.labels.forEach(l => {
      tableHtml += `<th class="p-1 text-slate-400 font-bold">${l.substring(0, 4)}</th>`;
    });
    tableHtml += `</tr>`;

    matrix.matrix.forEach((row, rIdx) => {
      tableHtml += `<tr><td class="p-1 text-slate-400 font-bold text-left">${matrix.labels[rIdx].substring(0, 4)}</td>`;
      row.forEach(val => {
        tableHtml += `<td class="p-1 ${val > 0 ? 'text-indigo-400 font-bold bg-indigo-500/10' : 'text-slate-700'}">${val}</td>`;
      });
      tableHtml += `</tr>`;
    });
    tableHtml += `</table>`;
    adjMatrixContainer.innerHTML = tableHtml;

  } catch (e) {
    console.error(e);
  }
}

async function runBfsRecommendation() {
  const startId = document.getElementById("graph-start-node").value;
  try {
    const res = await fetch(`${API_BASE}/dsa/unit5/bfs-recommendations?start_id=${startId}`);
    const data = await res.json();
    const traceBox = document.getElementById("graph-trace-content");

    let html = `<div class="text-emerald-400 font-bold mb-1">BFS Traversal from ${data.start_label} (Max Depth = 2):</div>`;
    html += `<div class="mb-2">Recommended Books (Shortest Hop):</div><ul class="list-disc pl-4 space-y-1">`;
    data.recommendations.forEach(r => {
      html += `<li><strong>${r.label}</strong> (Hops: ${r.hops}) - Co-borrowed via "${r.recommended_via}"</li>`;
    });
    html += `</ul>`;
    html += `<div class="mt-2 text-[10px] text-slate-500">Traversed ${data.total_visited} nodes using custom Queue ADT.</div>`;

    traceBox.innerHTML = html;
  } catch (e) {
    showToast("BFS execution error", "error");
  }
}

async function runDfsExploration() {
  const startId = document.getElementById("graph-start-node").value;
  try {
    const res = await fetch(`${API_BASE}/dsa/unit5/dfs-exploration?start_id=${startId}`);
    const data = await res.json();
    const traceBox = document.getElementById("graph-trace-content");

    let html = `<div class="text-purple-400 font-bold mb-1">DFS Exploration from ${data.start_label}:</div>`;
    html += `<div class="mb-2">Discovery Order: <span class="text-slate-200">${data.exploration_order.join(" -> ")}</span></div>`;
    html += `<div class="text-[10px] text-slate-500">Explored ${data.total_explored} nodes via custom Stack ADT.</div>`;

    traceBox.innerHTML = html;
  } catch (e) {
    showToast("DFS execution error", "error");
  }
}
