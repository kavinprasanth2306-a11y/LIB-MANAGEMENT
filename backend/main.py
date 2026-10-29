"""
FastAPI Server for DSA-Powered Library Book Management System
Exposes REST endpoints for:
- Book Management (CRUD, Issue, Return, Undo)
- Learning Unit I: Stack (Undo, Late Fee Evaluation), Circular Queue (Drop-box), Deque (VIP/Faculty), Priority Queue
- Learning Unit II: Singly Linked List (Borrower History), Doubly Linked List (Reader Nav), Circular Linked List (Carousel), Search
- Learning Unit III: Hash Table (Chaining vs Open Addressing), Interpolation Search, Benchmark, Sorting Algorithms
- Learning Unit IV: BST, AVL Tree (Hierarchy, Rotations, Traversals), Trie Autocomplete, Heaps (Min/Max), B-Tree
- Learning Unit V: Graph (Adjacency List/Matrix, BFS, DFS)
"""

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional

from .models import Book, Student, BorrowRequest, ReturnRequest, BookCreate, SearchQuery, SortRequest
from .seed_data import INITIAL_BOOKS, INITIAL_STUDENTS, GRAPH_NODES, GRAPH_EDGES

from .dsa_engine.unit1_linear import (
    Stack,
    Queue,
    CircularQueue,
    DoubleEndedQueue,
    PriorityQueue,
    evaluate_infix_expression
)
from .dsa_engine.unit2_linked_search import (
    SinglyLinkedList,
    DoublyLinkedList,
    CircularLinkedList,
    sequential_search,
    binary_search_iterative,
    binary_search_recursive
)
from .dsa_engine.unit3_hash_sort import (
    HashTable,
    interpolation_search,
    bubble_sort,
    selection_sort,
    insertion_sort,
    merge_sort
)
from .dsa_engine.unit4_trees_heaps import (
    BinarySearchTree,
    AVLTree,
    Trie,
    MinHeap,
    MaxHeap,
    BTree
)
from .dsa_engine.unit5_graphs import Graph

app = FastAPI(
    title="DSA-Powered Library Management System",
    description="Full-Stack System strictly powered by custom Data Structures & Algorithms from Scratch.",
    version="2.0.0"
)

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ==========================================
# In-Memory State powered strictly by DSA
# ==========================================

# 1. Master Hash Table for Books: h(k) = k mod 101
book_hash_table = HashTable(size=101, strategy="chaining")

# 2. Master AVL Tree and BST for catalog ordered by Title
avl_tree = AVLTree()
bst_tree = BinarySearchTree()

# 3. Trie for Autocomplete
search_trie = Trie()

# 4. Heaps
overdue_min_heap = MinHeap(capacity=100)
trending_max_heap = MaxHeap(capacity=100)

# 5. B-Tree for storage block indexing simulation
catalog_btree = BTree(t=3)

# 6. Action Undo Stack (Unit 1)
undo_action_stack = Stack(capacity=100)

# 7. Circular Queue for Return Drop-Box (Capacity 6)
return_dropbox = CircularQueue(capacity=6)

# 8. Deque for VIP & Faculty Scheduling
vip_faculty_deque = DoubleEndedQueue(capacity=30)

# 9. Priority Queue for Urgency-based reservations
urgency_reservation_pq = PriorityQueue(capacity=50)

# 10. Singly Linked List: Student Transaction Log
transaction_history_sll = SinglyLinkedList()

# 11. Doubly Linked List: Recently Viewed Books Navigator
reader_navigator_dll = DoublyLinkedList()

# 12. Circular Linked List: Featured Books Carousel
featured_carousel_cll = CircularLinkedList()

# 13. Graph: Co-borrowed recommendations & topic hierarchy
library_graph = Graph(directed=False)

# Raw list for array-based searching/benchmarking algorithms
books_raw_array = []
students_list = []


def seed_system():
    global books_raw_array, students_list
    books_raw_array = []
    students_list = [Student(**s) for s in INITIAL_STUDENTS]

    # Seed Books into Data Structures
    for b_data in INITIAL_BOOKS:
        book = Book(**b_data)
        books_raw_array.append(book)

        # Hash Table
        book_hash_table.insert(book.id, book.dict())

        # AVL Tree & BST
        avl_tree.insert(book.title, book.dict())
        bst_tree.insert(book.title, book.dict())

        # Trie: Index title and author
        search_trie.insert(book.title, {"id": book.id, "title": book.title, "type": "title"})
        search_trie.insert(book.author, {"id": book.id, "title": book.title, "author": book.author, "type": "author"})
        for tag in book.tags:
            search_trie.insert(tag, {"id": book.id, "title": book.title, "tag": tag, "type": "tag"})

        # Heaps
        trending_max_heap.insert(float(book.borrow_count), {"id": book.id, "title": book.title, "borrows": book.borrow_count})
        # Simulate due date: overdue score based on (borrow_count % 15) days overdue
        overdue_score = float((book.id * 7) % 20)
        overdue_min_heap.insert(overdue_score, {"id": book.id, "title": book.title, "days_due": overdue_score})

        # B-Tree
        catalog_btree.insert(book.id, {"title": book.title, "year": book.year})

        # Circular Linked List Carousel (take first 6 books)
        if len(featured_carousel_cll.to_list()) < 6:
            featured_carousel_cll.append(book.dict())

        # Doubly Linked List Navigator (first 4 books)
        if len(reader_navigator_dll.to_list()) < 4:
            reader_navigator_dll.append(book.dict())

    # Seed Graph
    for node in GRAPH_NODES:
        library_graph.add_node(node["id"], node["label"], node["type"])
    for edge in GRAPH_EDGES:
        library_graph.add_edge(edge["src"], edge["dst"], edge["relation"], edge["weight"])

    # Seed initial transactions in SLL
    transaction_history_sll.append({"id": "TXN101", "student_id": "STU1001", "book_id": 101, "action": "BORROW", "timestamp": "2026-10-25 10:30"})
    transaction_history_sll.append({"id": "TXN102", "student_id": "STU1002", "book_id": 103, "action": "BORROW", "timestamp": "2026-10-26 14:15"})
    transaction_history_sll.append({"id": "TXN103", "student_id": "STU1003", "book_id": 105, "action": "BORROW", "timestamp": "2026-10-27 09:00"})

    # Seed VIP Deque
    vip_faculty_deque.insert_front({"request_id": "VIP-99", "student_id": "STU1003", "name": "Carol Danvers (Faculty)", "book_id": 105})
    vip_faculty_deque.insert_rear({"request_id": "STU-01", "student_id": "STU1001", "name": "Alice Johnson", "book_id": 102})

    # Seed Priority Queue
    urgency_reservation_pq.enqueue({"student_id": "STU1001", "name": "Alice Johnson", "book_id": 105, "note": "Thesis Deadline"}, priority=9)
    urgency_reservation_pq.enqueue({"student_id": "STU1002", "name": "Bob Smith", "book_id": 105, "note": "Class Assignment"}, priority=5)

    # Seed Return Drop-box Circular Queue
    return_dropbox.enqueue({"book_id": 104, "title": "AI: A Modern Approach", "student_id": "STU1002", "drop_time": "17:15"})
    return_dropbox.enqueue({"book_id": 109, "title": "Computer Systems", "student_id": "STU1005", "drop_time": "17:45"})


# Run initialization
seed_system()


# ==========================================
# REST Endpoints: Book Management & Operations
# ==========================================

@app.get("/api/books")
def get_all_books():
    """Retrieve all books from master custom hash table."""
    items = book_hash_table.items()
    books = [item[1] for item in items]
    # Simple sort by ID for frontend display
    return {"count": len(books), "books": sorted(books, key=lambda x: x["id"])}


@app.post("/api/books")
def create_book(book_in: BookCreate):
    """Add a new book into all hierarchical & linear data structures."""
    # Find next available ID
    existing_items = book_hash_table.items()
    max_id = 100
    for k, _ in existing_items:
        if k > max_id:
            max_id = k
    new_id = max_id + 1

    book_dict = {
        "id": new_id,
        "title": book_in.title,
        "author": book_in.author,
        "isbn": book_in.isbn,
        "year": book_in.year,
        "category": book_in.category,
        "total_copies": book_in.total_copies,
        "available_copies": book_in.total_copies,
        "borrow_count": 0,
        "tags": [book_in.category.lower()]
    }

    # Insert into Hash Table
    book_hash_table.insert(new_id, book_dict)

    # Insert into AVL Tree & BST
    avl_tree.insert(book_in.title, book_dict)
    bst_tree.insert(book_in.title, book_dict)

    # Insert into Trie
    search_trie.insert(book_in.title, {"id": new_id, "title": book_in.title, "type": "title"})
    search_trie.insert(book_in.author, {"id": new_id, "title": book_in.title, "author": book_in.author, "type": "author"})

    # Insert into B-Tree
    catalog_btree.insert(new_id, {"title": book_in.title, "year": book_in.year})

    # Record undo action in Stack (Unit 1)
    undo_action_stack.push({
        "action": "ADD_BOOK",
        "book_id": new_id,
        "payload": book_dict
    })

    return {"message": f"Book '{book_in.title}' added successfully with ID {new_id}", "book": book_dict}


@app.post("/api/books/issue")
def issue_book(req: BorrowRequest):
    """
    Issue a book. If unavailable, place into VIP Deque or Priority Queue.
    Pushes state to Undo Stack.
    """
    res = book_hash_table.get(req.book_id)
    if not res["found"]:
        raise HTTPException(status_code=404, detail="Book not found in Hash Table")

    book = res["value"]
    if book["available_copies"] <= 0:
        # Book is fully loaned out! Enqueue waitlist
        if req.is_vip:
            vip_faculty_deque.insert_front({
                "request_id": f"WAIT-{req.book_id}",
                "student_id": req.student_id,
                "name": f"VIP-{req.student_id}",
                "book_id": req.book_id
            })
            return {"success": False, "queued": True, "type": "VIP Deque (Front)", "message": "Book unavailable; enqueued at FRONT of VIP Deque."}
        else:
            urgency_reservation_pq.enqueue({
                "student_id": req.student_id,
                "book_id": req.book_id,
                "note": "Standard Reservation"
            }, priority=3)
            return {"success": False, "queued": True, "type": "Priority Queue", "message": "Book unavailable; enqueued in Priority Waitlist."}

    # Decrement available copies & increment borrow count
    book["available_copies"] -= 1
    book["borrow_count"] += 1
    book_hash_table.insert(book["id"], book)

    # Add to SLL transaction history
    txn = {
        "id": f"TXN{transaction_history_sll.count + 101}",
        "student_id": req.student_id,
        "book_id": req.book_id,
        "book_title": book["title"],
        "action": "BORROW",
        "timestamp": "Just now"
    }
    transaction_history_sll.prepend(txn)

    # Add to DLL reader navigator
    reader_navigator_dll.append(book)

    # Update Max-Heap (Trending)
    trending_max_heap.insert(float(book["borrow_count"]), {"id": book["id"], "title": book["title"], "borrows": book["borrow_count"]})

    # Push to Undo Stack
    undo_action_stack.push({
        "action": "BORROW",
        "book_id": req.book_id,
        "student_id": req.student_id,
        "txn": txn
    })

    return {"success": True, "message": f"Successfully issued '{book['title']}' to {req.student_id}", "book": book}


@app.post("/api/books/return")
def return_book(req: ReturnRequest):
    """
    Return a book. Evaluates fine formula using Stack ADT expression evaluator.
    Pushes book to Circular Queue Return Drop-box.
    """
    res = book_hash_table.get(req.book_id)
    if not res["found"]:
        raise HTTPException(status_code=404, detail="Book not found in Hash Table")

    book = res["value"]

    # Calculate fine using Expression Evaluator (Unit 1 Stack ADT)
    formula = req.formula if req.formula else "days * 2"
    variables = {"days": req.overdue_days, "rate": 2.5, "fee": 5.0}
    fine_calc = evaluate_infix_expression(formula, variables)

    # Put into Return Drop-Box Circular Queue
    dropbox_success = return_dropbox.enqueue({
        "book_id": req.book_id,
        "title": book["title"],
        "student_id": req.student_id,
        "fine": fine_calc["result"],
        "drop_time": "Now"
    })

    # Return book to stock
    book["available_copies"] = min(book["total_copies"], book["available_copies"] + 1)
    book_hash_table.insert(book["id"], book)

    # Add to transaction history
    txn = {
        "id": f"TXN{transaction_history_sll.count + 101}",
        "student_id": req.student_id,
        "book_id": req.book_id,
        "book_title": book["title"],
        "action": "RETURN",
        "timestamp": "Just now",
        "fine": fine_calc["result"]
    }
    transaction_history_sll.prepend(txn)

    # Push to Undo Stack
    undo_action_stack.push({
        "action": "RETURN",
        "book_id": req.book_id,
        "student_id": req.student_id,
        "txn": txn
    })

    return {
        "success": True,
        "message": f"Book '{book['title']}' returned. Drop-box status: {'Enqueued' if dropbox_success else 'Buffer Full'}",
        "fine_details": fine_calc,
        "dropbox_enqueued": dropbox_success,
        "book": book
    }


@app.post("/api/undo")
def undo_last_action():
    """Undo the most recent library operation using Stack ADT."""
    if undo_action_stack.is_empty():
        return {"success": False, "message": "Nothing to undo. Undo Stack is empty."}

    action_entry = undo_action_stack.pop()
    action = action_entry["action"]

    if action == "ADD_BOOK":
        b_id = action_entry["book_id"]
        book_hash_table.delete(b_id)
        return {"success": True, "action": action, "message": f"Undid Add Book #{b_id}. Removed from catalog."}

    elif action == "BORROW":
        b_id = action_entry["book_id"]
        res = book_hash_table.get(b_id)
        if res["found"]:
            book = res["value"]
            book["available_copies"] += 1
            book["borrow_count"] = max(0, book["borrow_count"] - 1)
            book_hash_table.insert(b_id, book)
        return {"success": True, "action": action, "message": f"Undid Borrow for Book #{b_id}. Restored copy to library."}

    elif action == "RETURN":
        b_id = action_entry["book_id"]
        res = book_hash_table.get(b_id)
        if res["found"]:
            book = res["value"]
            book["available_copies"] = max(0, book["available_copies"] - 1)
            book_hash_table.insert(b_id, book)
        return {"success": True, "action": action, "message": f"Undid Return for Book #{b_id}. Reverted copy count."}

    return {"success": False, "message": f"Unknown action: {action}"}


# ==========================================
# Learning Unit I: Linear Data Structures Endpoints
# ==========================================

@app.get("/api/dsa/unit1/stack-state")
def get_stack_state():
    """Retrieve internal states of Undo Stack & Expression Evaluator."""
    return {
        "undo_stack": {
            "size": undo_action_stack.size(),
            "items": undo_action_stack.to_list()
        }
    }


@app.post("/api/dsa/unit1/evaluate-fine")
def evaluate_fine(formula: str = Query("days * 2"), days: int = Query(5)):
    """Evaluate custom infix late-fee formula using Stack ADT."""
    vars_dict = {"days": days, "rate": 2.5, "fee": 10.0}
    return evaluate_infix_expression(formula, vars_dict)


@app.get("/api/dsa/unit1/dropbox-state")
def get_dropbox_state():
    """Retrieve Circular Queue buffer slots and wrap-around pointers."""
    return return_dropbox.get_state()


@app.post("/api/dsa/unit1/dropbox-process")
def process_dropbox_item():
    """Dequeue an item from the drop-box buffer (Librarian check-in)."""
    if return_dropbox.is_empty():
        return {"success": False, "message": "Return Drop-Box is empty"}
    item = return_dropbox.dequeue()
    return {"success": True, "processed_item": item, "current_state": return_dropbox.get_state()}


@app.get("/api/dsa/unit1/vip-deque-state")
def get_vip_deque_state():
    """Retrieve VIP & Faculty Deque internal state."""
    return vip_faculty_deque.get_state()


@app.get("/api/dsa/unit1/priority-queue-state")
def get_priority_queue_state():
    """Retrieve Reservation Priority Queue state."""
    return {
        "size": urgency_reservation_pq.size(),
        "items": urgency_reservation_pq.to_list()
    }


# ==========================================
# Learning Unit II: Linked Lists & Basic Searching Endpoints
# ==========================================

@app.get("/api/dsa/unit2/sll-history")
def get_sll_history():
    """Return Singly Linked List pointer chain of borrower transactions."""
    return transaction_history_sll.get_pointer_chain()


@app.get("/api/dsa/unit2/dll-navigator")
def get_dll_navigator():
    """Return Doubly Linked List reader navigator pointer chain."""
    return {
        "chain": reader_navigator_dll.get_pointer_chain(),
        "current": reader_navigator_dll.get_current()
    }


@app.post("/api/dsa/unit2/dll-navigator/step")
def step_dll_navigator(direction: str = Query("next")):
    """Navigate backward or forward in recently viewed books DLL."""
    if direction == "next":
        curr = reader_navigator_dll.move_next()
    else:
        curr = reader_navigator_dll.move_prev()
    return {
        "direction": direction,
        "current": curr,
        "chain": reader_navigator_dll.get_pointer_chain()
    }


@app.get("/api/dsa/unit2/cll-carousel")
def get_cll_carousel():
    """Return Circular Linked List carousel state."""
    return {
        "chain": featured_carousel_cll.get_pointer_chain(),
        "current": featured_carousel_cll.get_current()
    }


@app.post("/api/dsa/unit2/cll-carousel/cycle")
def cycle_cll_carousel():
    """Advance the infinite circular linked list carousel."""
    next_item = featured_carousel_cll.cycle_next()
    return {
        "current": next_item,
        "chain": featured_carousel_cll.get_pointer_chain()
    }


# ==========================================
# Learning Unit III: Hashing, Searching & Sorting Benchmarks
# ==========================================

@app.get("/api/dsa/unit3/hash-table-state")
def get_hash_table_state():
    """Return full state of custom Hash Table (101 buckets) with current collision strategy."""
    return book_hash_table.get_state()


@app.post("/api/dsa/unit3/hash-table-strategy")
def set_hash_table_strategy(strategy: str = Query("chaining")):
    """Switch Hash Table collision resolution strategy between Chaining and Linear Probing."""
    if strategy not in ["chaining", "probing"]:
        raise HTTPException(status_code=400, detail="Invalid strategy. Use 'chaining' or 'probing'.")
    book_hash_table.set_strategy(strategy)
    return {
        "message": f"Strategy switched to {strategy}",
        "state": book_hash_table.get_state()
    }


@app.post("/api/dsa/unit3/search-benchmark")
def run_search_benchmark(query: SearchQuery):
    """
    Search Benchmark Module:
    Compares execution step counts of:
    1. Sequential Search
    2. Binary Search (Iterative)
    3. Binary Search (Recursive)
    4. Interpolation Search
    """
    # Fetch sorted array by ID
    all_books = [item[1] for item in book_hash_table.items()]
    # Sort strictly using our custom merge_sort
    sorted_res = merge_sort(all_books, lambda b: b["id"], ascending=True)
    sorted_books = sorted_res["sorted"]

    target_id = int(query.query) if query.query.isdigit() else 101

    # 1. Sequential Search
    seq_res = sequential_search(sorted_books, lambda b: b["id"], target_id)

    # 2. Binary Search Iterative
    bin_iter_res = binary_search_iterative(sorted_books, lambda b: b["id"], target_id)

    # 3. Binary Search Recursive
    bin_rec_res = binary_search_recursive(sorted_books, lambda b: b["id"], target_id)

    # 4. Interpolation Search
    interp_res = interpolation_search(sorted_books, lambda b: b["id"], target_id)

    return {
        "target_id": target_id,
        "catalog_size": len(sorted_books),
        "results": {
            "sequential_search": {
                "steps": seq_res["steps"],
                "found": seq_res["found"],
                "time_complexity": "O(N)",
                "history": seq_res["history"]
            },
            "binary_search_iterative": {
                "steps": bin_iter_res["steps"],
                "found": bin_iter_res["found"],
                "time_complexity": "O(log N)",
                "history": bin_iter_res["history"]
            },
            "binary_search_recursive": {
                "steps": bin_rec_res["steps"],
                "found": bin_rec_res["found"],
                "time_complexity": "O(log N)",
                "history": bin_rec_res["history"]
            },
            "interpolation_search": {
                "steps": interp_res["steps"],
                "found": interp_res["found"],
                "time_complexity": "O(log log N) avg / O(N) worst",
                "history": interp_res["history"]
            }
        }
    }


@app.post("/api/dsa/unit3/sort")
def run_sort(req: SortRequest):
    """
    Sorting Engine:
    Execute custom Insertion, Bubble, Selection, or Merge Sort on current catalog.
    Returns sorted books, comparisons, and swap/shift counts.
    """
    all_books = [item[1] for item in book_hash_table.items()]

    def extractor(b):
        if req.field == "year":
            return b["year"]
        elif req.field == "borrow_count":
            return b["borrow_count"]
        elif req.field == "available_copies":
            return b["available_copies"]
        else:
            return b["title"].lower()

    if req.algorithm == "bubble_sort":
        res = bubble_sort(all_books, extractor, req.ascending)
    elif req.algorithm == "selection_sort":
        res = selection_sort(all_books, extractor, req.ascending)
    elif req.algorithm == "insertion_sort":
        res = insertion_sort(all_books, extractor, req.ascending)
    else:
        res = merge_sort(all_books, extractor, req.ascending)

    return {
        "algorithm": res["algorithm"],
        "field": req.field,
        "ascending": req.ascending,
        "comparisons": res["comparisons"],
        "swaps": res["swaps"],
        "sorted_books": res["sorted"]
    }


# ==========================================
# Learning Unit IV: Hierarchical Structures Endpoints
# ==========================================

@app.get("/api/dsa/unit4/avl-tree-state")
def get_avl_tree_state():
    """Return AVL Tree hierarchical JSON, traversals, and balance factors."""
    return {
        "tree_json": avl_tree.to_tree_json(),
        "last_rotation": avl_tree.last_rotation,
        "traversals": {
            "inorder": avl_tree.inorder(),
            "preorder": avl_tree.preorder(),
            "postorder": avl_tree.postorder()
        }
    }


@app.get("/api/dsa/unit4/bst-state")
def get_bst_state():
    """Return BST Traversals."""
    return {
        "traversals": {
            "inorder": bst_tree.inorder(),
            "preorder": bst_tree.preorder(),
            "postorder": bst_tree.postorder()
        }
    }


@app.get("/api/dsa/unit4/autocomplete")
def trie_autocomplete(prefix: str = Query("", min_length=1)):
    """Prefix Tree real-time search autocomplete for titles & authors."""
    return search_trie.search_prefix(prefix)


@app.get("/api/dsa/unit4/heaps-state")
def get_heaps_state():
    """Return Min-Heap (Overdue) & Max-Heap (Trending) array states."""
    return {
        "min_heap_overdue": overdue_min_heap.get_state(),
        "max_heap_trending": trending_max_heap.get_state()
    }


@app.get("/api/dsa/unit4/btree-state")
def get_btree_state():
    """Return B-Tree block indexing hierarchy."""
    return catalog_btree.to_tree_json()


# ==========================================
# Learning Unit V: Graph Theory Endpoints
# ==========================================

@app.get("/api/dsa/unit5/graph-state")
def get_graph_state():
    """Return graph nodes, edges, adjacency list, and adjacency matrix."""
    return {
        "graph": library_graph.get_graph_state(),
        "adjacency_list": library_graph.get_adjacency_list_repr(),
        "adjacency_matrix": library_graph.get_adjacency_matrix_repr()
    }


@app.get("/api/dsa/unit5/bfs-recommendations")
def get_bfs_recommendations(start_id: str = Query("B101")):
    """Run BFS for shortest-hop book recommendations."""
    return library_graph.bfs_recommendations(start_id, max_depth=2)


@app.get("/api/dsa/unit5/dfs-exploration")
def get_dfs_exploration(start_id: str = Query("B101")):
    """Run DFS for deep prerequisite/topic chain exploration."""
    return library_graph.dfs_exploration(start_id)


# Simple root endpoint
@app.get("/")
def root():
    return {
        "system": "DSA-Powered Library Book Management System",
        "curriculum_units": [
            "Unit I: Linear Data Structures (Stack, Queue, CircularQueue, Deque, PriorityQueue)",
            "Unit II: Linked Lists (SLL, DLL, CLL) & Searching (Sequential, Binary)",
            "Unit III: Hashing (101 Buckets, Chaining/Probing), Interpolation & Sorting",
            "Unit IV: Trees & Heaps (BST, AVL Rotations, Trie Autocomplete, Heaps, B-Tree)",
            "Unit V: Graph Theory (Adj List/Matrix, BFS, DFS Recommendations)"
        ],
        "status": "Online",
        "docs": "/docs"
    }
