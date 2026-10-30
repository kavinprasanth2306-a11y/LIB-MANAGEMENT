/**
 * app.js - LuminaLib Frontend DSA Application Logic & REST Client
 */

// Sorting Implementations in JavaScript for Client-Side Visualization
function mergeSort(arr, comparator) {
  if (arr.length <= 1) return arr;
  const mid = Math.floor(arr.length / 2);
  const left = mergeSort(arr.slice(0, mid), comparator);
  const right = mergeSort(arr.slice(mid), comparator);
  return merge(left, right, comparator);
}

function merge(left, right, comparator) {
  const result = [];
  let i = 0, j = 0;
  while (i < left.length && j < right.length) {
    if (comparator(left[i], right[j]) <= 0) result.push(left[i++]);
    else result.push(right[j++]);
  }
  return [...result, ...left.slice(i), ...right.slice(j)];
}

function quickSort(arr, comparator) {
  if (arr.length <= 1) return arr;
  const pivot = arr[arr.length - 1];
  const left = [], right = [];
  for (let i = 0; i < arr.length - 1; i++) {
    if (comparator(arr[i], pivot) <= 0) left.push(arr[i]);
    else right.push(arr[i]);
  }
  return [...quickSort(left, comparator), pivot, ...quickSort(right, comparator)];
}

// Global cached state
let allBooks = [];
let currentUser = null;

try {
  const saved = localStorage.getItem("lumina_user");
  if (saved) currentUser = JSON.parse(saved);
} catch (e) {
  currentUser = null;
}

// Toast System
function showToast(title, message, type = "info") {
  const container = document.getElementById("toast-center");
  const toast = document.createElement("div");
  const borders = {
    info: "border-indigo-400 bg-white/90 text-indigo-950",
    success: "border-emerald-400 bg-white/90 text-emerald-950",
    warning: "border-amber-400 bg-white/90 text-amber-950",
    error: "border-rose-400 bg-white/90 text-rose-950"
  };

  toast.className = `p-4 rounded-2xl glass-card border shadow-xl flex items-start space-x-3 transition-all duration-300 transform translate-y-2 pointer-events-auto ${borders[type] || borders.info}`;
  toast.innerHTML = `
    <div class="mt-0.5"><i data-lucide="${type === 'success' ? 'check-circle-2' : type === 'warning' ? 'alert-triangle' : 'info'}" class="w-4 h-4"></i></div>
    <div class="text-xs space-y-0.5">
      <div class="font-extrabold">${title}</div>
      <div class="text-slate-500 font-medium">${message}</div>
    </div>
  `;
  container.appendChild(toast);
  if (window.lucide) lucide.createIcons();

  setTimeout(() => {
    toast.classList.add("opacity-0", "translate-y-4");
    setTimeout(() => toast.remove(), 300);
  }, 3500);
}

// REST Client Fetchers
async function fetchBooks() {
  const res = await fetch("/api/books");
  const json = await res.json();
  allBooks = json.data;
  return allBooks;
}

async function fetchMembers() {
  const res = await fetch("/api/members");
  return (await res.json()).data;
}

// View Controller
const views = ['dashboard', 'catalog', 'desk', 'waitlist', 'history', 'visualizer', 'outcomes'];
function navigateTo(targetView) {
  views.forEach(v => {
    const el = document.getElementById(`view-${v}`);
    const navBtn = document.getElementById(`nav-${v}`);
    if (v === targetView) {
      el.classList.remove('hidden');
      navBtn.className = "w-full flex items-center space-x-3 px-3.5 py-2.5 rounded-xl text-sm font-semibold transition-all bg-indigo-50 text-indigo-600 border border-indigo-100 shadow-sm";
    } else {
      el.classList.add('hidden');
      navBtn.className = "w-full flex items-center space-x-3 px-3.5 py-2.5 rounded-xl text-sm font-medium transition-all text-slate-600 hover:text-slate-900 hover:bg-white/60";
    }
  });

  if (targetView === 'catalog') renderFullCatalog();
  if (targetView === 'desk') populateDeskDropdowns();
  if (targetView === 'waitlist') renderWaitlist();
  if (targetView === 'history') renderHistory();
  if (targetView === 'visualizer') renderVisualizer();
  if (window.lucide) lucide.createIcons();
}

// Catalog View
async function renderFullCatalog(customList = null) {
  const books = customList || await fetchBooks();
  const container = document.getElementById("full-catalog-grid");

  container.innerHTML = books.map(b => {
    const isAvail = b.available_copies > 0;
    return `
      <div class="glass-card glass-card-hover p-5 rounded-2xl flex flex-col justify-between space-y-4">
        <div>
          <div class="flex items-start justify-between gap-2">
            <span class="text-[10px] font-mono px-2 py-0.5 rounded-lg bg-slate-100 text-slate-600 border border-slate-200">
              ${b.isbn}
            </span>
            <span class="text-[10px] font-extrabold px-2 py-0.5 rounded-lg ${isAvail ? 'bg-emerald-50 text-emerald-700 border border-emerald-200' : 'bg-amber-50 text-amber-700 border border-amber-200'}">
              ${isAvail ? `${b.available_copies} Available` : 'Waitlist Active'}
            </span>
          </div>
          <h4 class="font-bold text-sm text-slate-900 mt-3 line-clamp-1">${b.title}</h4>
          <p class="text-xs text-slate-500">${b.author} • ${b.year}</p>
          <div class="mt-2 inline-block text-[11px] font-semibold text-indigo-600 bg-indigo-50 px-2 py-0.5 rounded-md">
            ${b.category}
          </div>
        </div>

        <div class="pt-3 border-t border-slate-200/60 flex items-center justify-between">
          <span class="text-xs text-slate-400 font-mono">Copies: ${b.available_copies}/${b.total_copies}</span>
          <button onclick="handleQuickCheckout('${b.isbn}')" class="px-3 py-1.5 rounded-xl text-xs font-bold transition ${isAvail ? 'bg-indigo-600 hover:bg-indigo-700 text-white shadow-sm' : 'bg-amber-500 hover:bg-amber-600 text-white'}">
            ${isAvail ? 'Issue' : 'Join Queue'}
          </button>
        </div>
      </div>
    `;
  }).join("");

  updateMetrics();
  if (window.lucide) lucide.createIcons();
}

function triggerCatalogSort() {
  const field = document.getElementById("catalog-sort-field").value;
  const algo = document.getElementById("catalog-sort-algo").value;

  const comparator = (a, b) => {
    if (field === 'year' || field === 'available_copies') return a[field] - b[field];
    return String(a[field]).localeCompare(String(b[field]));
  };

  const start = performance.now();
  const sorted = algo === 'merge' ? mergeSort([...allBooks], comparator) : quickSort([...allBooks], comparator);
  const duration = (performance.now() - start).toFixed(3);

  renderFullCatalog(sorted);
  const box = document.getElementById("sort-metrics-box");
  document.getElementById("sort-metrics-content").innerHTML = `Sorted ${sorted.length} records by <strong>${field}</strong> with <strong>${algo.toUpperCase()} Sort</strong> in <strong>${duration} ms</strong>.`;
  box.classList.remove("hidden");
  showToast("Sorted", `Execution completed in ${duration} ms`, "success");
}

// Autocomplete
async function handleSearchInput(val) {
  const dropdown = document.getElementById("trie-autocomplete-dropdown");
  if (!val.trim()) {
    dropdown.classList.add("hidden");
    return;
  }

  const res = await fetch(`/api/search?q=${encodeURIComponent(val)}`);
  const matches = (await res.json()).data;

  if (matches.length === 0) {
    dropdown.innerHTML = `<div class="p-3 text-xs text-slate-400 text-center font-medium">No results in Trie.</div>`;
    dropdown.classList.remove("hidden");
    return;
  }

  dropdown.innerHTML = `
    <div class="px-3 py-1 text-[10px] font-mono font-bold text-slate-400 border-b border-slate-100 flex justify-between items-center bg-slate-50 rounded-lg">
      <span>TRIE PREFIX LOOKUP</span>
      <span class="text-indigo-600">O(L)</span>
    </div>
    ${matches.map(m => `
      <div onclick="selectTrieResult('${m.isbn}')" class="p-2.5 hover:bg-indigo-50 rounded-xl cursor-pointer transition flex items-center justify-between text-xs">
        <div>
          <div class="font-bold text-slate-900">${m.title}</div>
          <div class="text-[11px] text-slate-500">${m.author} (${m.year})</div>
        </div>
        <span class="text-[10px] font-mono font-bold px-2 py-0.5 rounded ${m.available_copies > 0 ? 'bg-emerald-50 text-emerald-700' : 'bg-amber-50 text-amber-700'}">
          ${m.available_copies > 0 ? `${m.available_copies} In Stock` : 'Waitlist'}
        </span>
      </div>
    `).join("")}
  `;
  dropdown.classList.remove("hidden");
}

async function selectTrieResult(isbn) {
  const book = allBooks.find(b => b.isbn === isbn);
  if (!book) return;

  document.getElementById("trie-autocomplete-dropdown").classList.add("hidden");
  document.getElementById("global-search-input").value = book.title;

  await fetch("/api/view-book", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ isbn })
  });

  renderDllNavigator();
  navigateTo("catalog");
  renderFullCatalog([book]);
}

// DLL Navigator
async function renderDllNavigator() {
  const res = await fetch("/api/recently-viewed");
  const items = (await res.json()).data;
  const container = document.getElementById("dll-horizontal-chain");

  if (items.length === 0) {
    container.innerHTML = `<span class="text-xs text-slate-400">No recently viewed records.</span>`;
    return;
  }

  container.innerHTML = items.map((node, idx) => `
    <div class="flex items-center shrink-0">
      <div class="px-3 py-1.5 rounded-xl text-xs font-mono ${node.is_current ? 'bg-indigo-600 text-white font-bold ring-2 ring-indigo-400/50' : 'dsa-node-pill text-slate-700'}">
        <div class="text-[9px] uppercase tracking-wider">${node.is_current ? 'ACTIVE' : `NODE #${idx+1}`}</div>
        <div class="font-sans font-bold truncate max-w-[120px]">${node.data.title}</div>
      </div>
      ${idx < items.length - 1 ? `<div class="mx-2 text-indigo-400 font-bold">&harr;</div>` : ''}
    </div>
  `).join("");
}

// Issue & Return Desk
async function populateDeskDropdowns() {
  await fetchBooks();
  const members = await fetchMembers();

  const issueSelect = document.getElementById("desk-issue-book-select");
  const returnSelect = document.getElementById("desk-return-book-select");
  const memberSelect = document.getElementById("desk-issue-member-select");
  const returnMemberInput = document.getElementById("desk-return-member");

  if (issueSelect && returnSelect && memberSelect) {
    issueSelect.innerHTML = allBooks.map(b => `<option value="${b.isbn}">${b.title} (${b.available_copies} available)</option>`).join("");
    returnSelect.innerHTML = allBooks.map(b => `<option value="${b.isbn}">${b.title}</option>`).join("");
    memberSelect.innerHTML = members.map(m => `<option value="${m.member_id}">${m.member_id} - ${m.full_name} (${m.role})</option>`).join("");

    if (currentUser && currentUser.member_id) {
      memberSelect.value = currentUser.member_id;
      if (returnMemberInput) returnMemberInput.value = currentUser.member_id;
    }
  }
}

async function handleIssueSubmit() {
  const isbn = document.getElementById("desk-issue-book-select").value;
  const member_id = document.getElementById("desk-issue-member-select").value;
  handleQuickCheckout(isbn, member_id);
}

async function handleQuickCheckout(isbn, member_id = null) {
  if (!currentUser) {
    showToast("Sign In Required", "Please sign in to borrow or join the waitlist.", "warning");
    openAuthModal();
    return;
  }

  const targetMember = member_id || currentUser.member_id || "MEM101";

  const res = await fetch("/api/checkout", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ isbn, member_id: targetMember })
  });
  const data = await res.json();

  if (data.waitlisted) {
    showToast("Waitlist (FIFO)", `Out of stock. Added ${targetMember} to Queue.`, "warning");
  } else {
    showToast("Issued", `Book checked out to ${targetMember}.`, "success");
  }
  await fetchBooks();
  renderFullCatalog();
}

async function handleReturnSubmit() {
  const isbn = document.getElementById("desk-return-book-select").value;
  const member_id = document.getElementById("desk-return-member").value || (currentUser ? currentUser.member_id : "MEM101");

  const res = await fetch("/api/return", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ isbn, member_id })
  });
  const data = await res.json();

  if (data.auto_allocated) {
    showToast("FIFO Auto-Allocated", `Assigned to waitlisted user: ${data.to_member}`, "info");
  } else {
    showToast("Returned", `Added back to available copies.`, "success");
  }
  await fetchBooks();
  renderFullCatalog();
}

async function executeUndoAction() {
  if (currentUser && !currentUser.is_admin && currentUser.role.toLowerCase() !== "admin") {
    showToast("Admin Only", "Only the Librarian / Admin can undo global library actions.", "warning");
    return;
  }

  const res = await fetch("/api/undo", { method: "POST" });
  const data = await res.json();
  if (data.success) {
    showToast("Undone (Stack LIFO)", data.undone.description, "info");
    await fetchBooks();
    renderFullCatalog();
  } else {
    showToast("Stack Empty", "No actions to revert.", "warning");
  }
}

// Visualizer State Sync
async function renderVisualizer() {
  const res = await fetch("/api/dsa-state");
  const state = (await res.json());

  // 1. Hash Table Buckets
  const htContainer = document.getElementById("vis-hash-table-buckets");
  htContainer.innerHTML = state.hash_table.map(b => `
    <div class="p-3 rounded-xl bg-white/70 border ${b.count > 0 ? 'border-indigo-200 bg-indigo-50/20' : 'border-slate-200'} space-y-1.5 text-xs">
      <div class="flex items-center justify-between font-mono">
        <span class="font-bold text-slate-700">Bucket #${b.bucket_index}</span>
        <span class="text-[10px] px-1.5 py-0.2 rounded font-bold ${b.count > 1 ? 'bg-rose-100 text-rose-700' : b.count === 1 ? 'bg-indigo-100 text-indigo-700' : 'text-slate-400'}">
          ${b.count} ${b.count > 1 ? 'Collision!' : 'nodes'}
        </span>
      </div>
      <div class="space-y-1 font-mono text-[11px]">
        ${b.chain.length > 0 ? b.chain.map(node => `
          <div class="p-1.5 bg-white rounded-lg border border-slate-200 shadow-xs flex items-center justify-between">
            <span class="truncate max-w-[140px] font-sans font-medium text-slate-800">${node.title}</span>
            <span class="text-[9px] text-indigo-600 font-mono">${node.key.slice(-6)}</span>
          </div>
        `).join("") : '<div class="text-[11px] text-slate-400 italic">Empty bucket (null)</div>'}
      </div>
    </div>
  `).join("");

  document.getElementById("vis-ht-metrics").innerText = `Total: ${state.metrics.hash_size} | Capacity: 17 | Load: ${(state.metrics.hash_size / 17).toFixed(2)}`;

  // 2. Undo Stack LIFO
  const stackContainer = document.getElementById("vis-stack-container");
  document.getElementById("vis-stack-count").innerText = `${state.metrics.stack_depth} Snapshots`;
  stackContainer.innerHTML = state.stack.length > 0 ? state.stack.map((item, idx) => `
    <div class="p-2.5 rounded-xl bg-white border border-rose-200 shadow-sm text-xs font-mono flex items-center justify-between">
      <div>
        <span class="font-bold text-rose-600">[TOP - ${idx}]</span>
        <span class="text-slate-800 ml-1 font-sans">${item.description}</span>
      </div>
      <span class="text-[10px] text-slate-400">${item.action}</span>
    </div>
  `).join("") : `<div class="text-xs text-slate-400 text-center py-8">Undo stack empty.</div>`;

  // 3. FIFO Waitlists
  const queueContainer = document.getElementById("vis-queue-container");
  const qKeys = Object.keys(state.waitlists);
  queueContainer.innerHTML = qKeys.length > 0 ? qKeys.map(isbn => {
    const book = allBooks.find(b => b.isbn === isbn);
    return `
      <div class="p-3 bg-white rounded-xl border border-amber-200 space-y-2 text-xs">
        <div class="font-bold text-slate-900">${book ? book.title : isbn}</div>
        <div class="flex items-center space-x-1.5 overflow-x-auto font-mono text-[11px]">
          <span class="text-amber-600 font-bold">FRONT &rarr;</span>
          ${state.waitlists[isbn].map(it => `<span class="px-2 py-0.5 bg-amber-50 rounded border border-amber-200 text-amber-900">${it.member_id}</span>`).join("&rarr;")}
          <span class="text-slate-400">&rarr; REAR</span>
        </div>
      </div>
    `;
  }).join("") : `<div class="text-xs text-slate-400 text-center py-8">No active waitlist queues.</div>`;
}

async function renderWaitlist() {
  const res = await fetch("/api/waitlist");
  const waitlists = (await res.json()).data;
  const container = document.getElementById("waitlist-queues-container");
  const isbns = Object.keys(waitlists);

  if (isbns.length === 0) {
    container.innerHTML = `<div class="p-8 text-center text-xs text-slate-400">All books currently have zero active waitlists.</div>`;
    return;
  }

  container.innerHTML = isbns.map(isbn => {
    const book = allBooks.find(b => b.isbn === isbn);
    const items = waitlists[isbn];
    return `
      <div class="p-4 rounded-2xl bg-white/60 border border-slate-200 space-y-3">
        <div class="flex items-center justify-between">
          <h4 class="font-bold text-sm text-slate-900">${book ? book.title : isbn}</h4>
          <span class="text-xs font-mono font-bold px-2 py-0.5 rounded bg-amber-50 text-amber-700">${items.length} in queue</span>
        </div>
        <div class="flex items-center space-x-2 overflow-x-auto py-1">
          <span class="text-[10px] font-mono font-bold text-amber-600">HEAD &rarr;</span>
          ${items.map(it => `
            <div class="px-3 py-1.5 rounded-xl bg-white border border-amber-200 text-xs font-mono">
              <strong>${it.member_id}</strong>
            </div>
          `).join("&rarr;")}
          <span class="text-[10px] font-mono font-bold text-slate-400">&rarr; REAR</span>
        </div>
      </div>
    `;
  }).join("");
}

async function renderHistory() {
  const res = await fetch("/api/history");
  const list = (await res.json()).data;
  const container = document.getElementById("history-transactions-list");

  if (list.length === 0) {
    container.innerHTML = `<div class="p-6 text-center text-xs text-slate-400">No transactions recorded.</div>`;
    return;
  }

  container.innerHTML = list.reverse().map(item => `
    <div class="p-3.5 rounded-xl bg-white/70 border border-slate-200 flex items-center justify-between text-xs">
      <div class="flex items-center space-x-3">
        <span class="font-mono text-[10px] font-bold px-2 py-0.5 rounded-md ${item.data.type === 'ISSUE' ? 'bg-indigo-50 text-indigo-700' : 'bg-emerald-50 text-emerald-700'}">
          ${item.data.type}
        </span>
        <span class="font-bold text-slate-900">${item.data.title}</span>
      </div>
      <div class="text-slate-500 font-mono text-[11px]">
        Member: <strong class="text-slate-800">${item.data.member_id}</strong> • ${item.data.created_at}
      </div>
    </div>
  `).join("");
}

async function updateMetrics() {
  const res = await fetch("/api/dsa-state");
  const state = await res.json();
  const available = allBooks.reduce((sum, b) => sum + b.available_copies, 0);

  document.getElementById("metric-total-books").innerText = state.metrics.hash_size;
  document.getElementById("metric-available-books").innerText = available;
  document.getElementById("metric-waitlist-count").innerText = state.metrics.total_waitlist;
  document.getElementById("metric-stack-depth").innerText = state.metrics.stack_depth;

  document.getElementById("sidebar-stack-count").innerText = state.metrics.stack_depth;
  document.getElementById("sidebar-hash-count").innerText = state.metrics.hash_size;
}

// =========================================================
// AUTHENTICATION & ROLE-BASED ACCESS CONTROL (RBAC)
// =========================================================
function updateUserUi() {
  const widget = document.getElementById("user-profile-widget");
  const addBtn = document.getElementById("header-add-book-btn");

  if (!widget) return;

  if (currentUser) {
    const isAdm = currentUser.is_admin || (currentUser.role && currentUser.role.toLowerCase() === "admin");
    const initial = (currentUser.full_name || currentUser.username || "U").charAt(0).toUpperCase();

    widget.innerHTML = `
      <div class="flex items-center space-x-2.5 bg-white/80 border border-slate-200/80 rounded-2xl px-3 py-1.5 shadow-xs">
        <div class="w-7 h-7 rounded-xl bg-gradient-to-tr ${isAdm ? 'from-indigo-600 to-purple-600' : 'from-emerald-500 to-teal-500'} text-white flex items-center justify-center font-bold text-xs shadow-xs">
          ${initial}
        </div>
        <div class="text-left text-xs leading-tight">
          <div class="font-extrabold text-slate-900 truncate max-w-[110px]">${currentUser.full_name || currentUser.username}</div>
          <div class="text-[10px] font-mono ${isAdm ? 'text-indigo-600 font-bold' : 'text-slate-500'}">
            ${isAdm ? '👑 Librarian' : `${currentUser.role || 'Member'} (${currentUser.member_id || 'ID'})`}
          </div>
        </div>
        <button onclick="handleLogout()" title="Switch Account / Sign Out" class="p-1 text-slate-400 hover:text-rose-600 hover:bg-rose-50 rounded-lg transition ml-0.5">
          <i data-lucide="log-out" class="w-3.5 h-3.5"></i>
        </button>
      </div>
    `;

    // Librarian only can add books
    if (addBtn) {
      if (isAdm) addBtn.classList.remove("hidden");
      else addBtn.classList.add("hidden");
    }
  } else {
    widget.innerHTML = `
      <button onclick="openAuthModal()" class="flex items-center space-x-1.5 px-3.5 py-1.5 bg-indigo-600 hover:bg-indigo-700 text-white rounded-xl text-xs font-bold shadow-md shadow-indigo-600/20 transition">
        <i data-lucide="log-in" class="w-3.5 h-3.5"></i>
        <span>Sign In</span>
      </button>
    `;
    if (addBtn) addBtn.classList.add("hidden");
  }

  if (window.lucide) lucide.createIcons();
}

function openAuthModal() {
  const modal = document.getElementById("modal-auth");
  if (modal) modal.classList.remove("hidden");
  if (window.lucide) lucide.createIcons();
}

function closeAuthModal() {
  document.getElementById("modal-auth")?.classList.add("hidden");
}

function switchAuthTab(tab) {
  const signinForm = document.getElementById("form-auth-signin");
  const registerForm = document.getElementById("form-auth-register");
  const tabSignin = document.getElementById("auth-tab-signin");
  const tabRegister = document.getElementById("auth-tab-register");

  if (tab === "signin") {
    signinForm?.classList.remove("hidden");
    registerForm?.classList.add("hidden");
    if (tabSignin) tabSignin.className = "flex-1 py-1.5 rounded-lg bg-white text-indigo-600 shadow-xs transition";
    if (tabRegister) tabRegister.className = "flex-1 py-1.5 rounded-lg hover:text-slate-900 transition";
  } else {
    signinForm?.classList.add("hidden");
    registerForm?.classList.remove("hidden");
    if (tabRegister) tabRegister.className = "flex-1 py-1.5 rounded-lg bg-white text-emerald-600 shadow-xs transition";
    if (tabSignin) tabSignin.className = "flex-1 py-1.5 rounded-lg hover:text-slate-900 transition";
  }
}

async function quickLogin(username, password) {
  const uInput = document.getElementById("signin-username");
  const pInput = document.getElementById("signin-password");
  if (uInput) uInput.value = username;
  if (pInput) pInput.value = password;
  await performLogin(username, password);
}

async function handleSignInSubmit(e) {
  e.preventDefault();
  const username = document.getElementById("signin-username").value.trim();
  const password = document.getElementById("signin-password").value.trim();
  await performLogin(username, password);
}

async function performLogin(username, password) {
  const btn = document.getElementById("signin-submit-btn");
  if (btn) btn.disabled = true;

  try {
    const res = await fetch("/api/login", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ username, password })
    });
    const data = await res.json();

    if (res.ok && data.success) {
      currentUser = data.user;
      localStorage.setItem("lumina_user", JSON.stringify(currentUser));
      closeAuthModal();
      updateUserUi();
      populateDeskDropdowns();
      showToast("Signed In", `Logged in as ${currentUser.full_name} (${currentUser.role})`, "success");
    } else {
      showToast("Login Failed", data.message || "Invalid credentials", "error");
    }
  } catch (err) {
    showToast("Server Error", "Could not connect to authentication API.", "error");
  } finally {
    if (btn) btn.disabled = false;
  }
}

async function handleRegisterSubmit(e) {
  e.preventDefault();
  const full_name = document.getElementById("register-fullname").value.trim();
  const username = document.getElementById("register-username").value.trim();
  const role = document.getElementById("register-role").value;
  const password = document.getElementById("register-password").value.trim();
  const btn = document.getElementById("register-submit-btn");

  if (btn) btn.disabled = true;

  try {
    const res = await fetch("/api/register", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ full_name, username, role, password })
    });
    const data = await res.json();

    if (res.ok && data.success) {
      currentUser = data.user;
      localStorage.setItem("lumina_user", JSON.stringify(currentUser));
      closeAuthModal();
      updateUserUi();
      populateDeskDropdowns();
      showToast("Account Created", data.message || "Registered successfully!", "success");
    } else {
      showToast("Registration Failed", data.message || "Could not register account.", "error");
    }
  } catch (err) {
    showToast("Server Error", "Could not connect to authentication API.", "error");
  } finally {
    if (btn) btn.disabled = false;
  }
}

function handleLogout() {
  currentUser = null;
  localStorage.removeItem("lumina_user");
  updateUserUi();
  populateDeskDropdowns();
  showToast("Signed Out", "You have signed out. Sign in to borrow or manage books.", "info");
  openAuthModal();
}

// Modal Form
function openAddBookModal() {
  if (currentUser && !currentUser.is_admin && currentUser.role.toLowerCase() !== "admin") {
    showToast("Admin Privilege Required", "Only the Librarian / Admin can add books to the catalog.", "warning");
    return;
  }
  document.getElementById("modal-add-book").classList.remove("hidden");
}
function closeAddBookModal() { document.getElementById("modal-add-book").classList.add("hidden"); }

async function handleAddBookSubmit(e) {
  e.preventDefault();
  const payload = {
    title: document.getElementById("add-book-title").value.trim(),
    author: document.getElementById("add-book-author").value.trim(),
    isbn: document.getElementById("add-book-isbn").value.trim(),
    year: parseInt(document.getElementById("add-book-year").value),
    category: document.getElementById("add-book-category").value,
    total_copies: parseInt(document.getElementById("add-book-copies").value)
  };

  const res = await fetch("/api/books", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload)
  });

  if (res.ok) {
    closeAddBookModal();
    showToast("Book Saved", `Persisted to Database and In-Memory Hash Table.`, "success");
    await fetchBooks();
    renderFullCatalog();
  }
}

// Bootstrapping
window.addEventListener("DOMContentLoaded", async () => {
  await fetchBooks();
  renderFullCatalog();
  renderDllNavigator();
  updateMetrics();
  updateUserUi();
  if (window.lucide) lucide.createIcons();
});

