# Course Outcomes (CO) Implementation Document
## DSA-Powered Library Book Management System

This document outlines the **5 University Course Outcomes (COs)** implemented in this project, mapping each academic objective to the exact data structures, algorithms, code files, and user interface features.

---

### 📌 Summary of Implemented Course Outcomes

| Course Outcome | Academic Domain | Implemented Data Structure / Algorithm | Practical LMS Application | Source Files |
| :--- | :--- | :--- | :--- | :--- |
| **CO 1** | **Linear Data Structures** | Stack ADT, Circular Queue, Double-Ended Queue (Deque), Priority Queue, Infix-to-Postfix Evaluator | Action Undo System, Return Drop-Box Buffer, VIP/Faculty Priority Scheduling, Late-Fee Evaluator | `backend/dsa_engine/unit1_linear.py`<br>`index.html` (Lines 870–930) |
| **CO 2** | **Linked Lists & Basic Searching** | Singly Linked List, Doubly Linked List, Circular Linked List, Sequential Search, Binary Search (Iterative & Recursive) | Borrower Transaction Logs, Recently Viewed Books Navigator, Infinite Featured Books Carousel, Search Step Benchmarks | `backend/dsa_engine/unit2_linked_search.py`<br>`index.html` (Lines 770–840) |
| **CO 3** | **Hashing, Advanced Searching & Sorting** | Custom Hash Table ($h(k) = k \bmod 101$), Separate Chaining, Linear Probing, Interpolation Search, Merge/Quick/Insertion/Bubble/Selection Sort | $O(1)$ Book & Member Lookups, Collision Resolution Inspection, Dynamic Probe Indexing, Multi-Key Catalog Sorting | `backend/dsa_engine/unit3_hash_sort.py`<br>`index.html` (Lines 680–740, 940–990) |
| **CO 4** | **Hierarchical Structures & Heaps** | Binary Search Tree (BST), Self-Balancing AVL Tree (LL/RR/LR/RL Rotations), Trie (Prefix Tree), Min-Heap, Max-Heap, B-Tree ($t=3$) | Self-Balancing Catalog Indexing, $O(L)$ Autocomplete Search, $O(1)$ Earliest Due Dates (Min-Heap), $O(1)$ Trending Books (Max-Heap), Disk Block Index Simulation | `backend/dsa_engine/unit4_trees_heaps.py`<br>`index.html` (Lines 740–770) |
| **CO 5** | **Graph Theory & Recommendation Networks** | Graph ADT, Adjacency List, Adjacency Matrix, Breadth-First Search (BFS), Depth-First Search (DFS) | Library Recommendation Network, "Readers who borrowed X also borrowed Y" (BFS), Prerequisite Topic Chain Exploration (DFS) | `backend/dsa_engine/unit5_graphs.py`<br>`backend/main.py` (Lines 440–480) |

---

### Detailed Breakdown of Each Course Outcome

#### CO 1: Design and Implement Linear Data Structures
- **Stack ADT (`Stack`)**: Fixed and dynamic array implementation using `push`, `pop`, `peek`, and `is_empty`.
  - **Feature 1 (Audit Log & Undo System)**: Pushes each library transaction (`ISSUE`, `RETURN`, `ADD_BOOK`, `ENQUEUE`) onto a LIFO stack. Pressing "Undo" pops the latest action and restores the exact previous state.
  - **Feature 2 (Expression Evaluation)**: Converts infix late-fee arithmetic formulas (e.g., `days * rate + fee`) to postfix notation using an operator stack, then computes the fee.
- **Circular Queue (`CircularQueue`)**: Fixed-size circular buffer ($capacity = 6$) using front/rear pointers and modulo wrap-around `(rear + 1) % capacity`. Used for the **Return Drop-Box**, buffering returned books awaiting librarian check-in without memory reallocation.
- **Double-Ended Queue (`DoubleEndedQueue`)**: Front and rear pointer operations for **VIP & Faculty Scheduling**. VIPs and professors insert at the front of the queue; standard student requests append to the rear.
- **Priority Queue (`PriorityQueue`)**: Urgency-based reservation system. Books in high demand are queued by urgency score (e.g., thesis deadlines vs. general reading) rather than arrival time.

#### CO 2: Implement Linked Lists and Basic Searching Algorithms
- **Singly Linked List (`SinglyLinkedList`)**: Pointer-based node chain (`HEAD -> [Node] -> NULL`) maintaining each student's historical borrowing trail.
- **Doubly Linked List (`DoublyLinkedList`)**: Bidirectional node pointers (`NULL <- [Prev | Data | Next] -> NULL`) powering the **Recently Viewed Books Navigator** on the dashboard, allowing forward and backward browsing navigation in $O(1)$ time.
- **Circular Linked List (`CircularLinkedList`)**: Infinite cyclic node chain powering the **Featured Books Showcase Carousel**. Advancing past the last element loops back to the head in $O(1)$ time.
- **Sequential Search**: Linear scan over unindexed author notes and book descriptions.
- **Binary Search (Iterative & Recursive)**: Divide-and-conquer search on sorted ISBN/ID arrays, returning exact step counts to prove $O(\log N)$ performance.

#### CO 3: Apply Hashing, Advanced Searching, and Sorting Algorithms
- **Custom Hash Table (`HashTable`)**: Fixed-size bucket array ($size = 101$) implementing modular hashing $h(k) = k \bmod 101$.
  - **Collision Resolution 1 (Separate Chaining)**: Buckets maintain Singly Linked Lists of colliding records.
  - **Collision Resolution 2 (Open Addressing / Linear Probing)**: Probes sequentially $(h(k) + i) \bmod 101$ when collisions occur.
  - **Interactive Inspection**: Frontend exposes bucket indices, collision counts, and current load factor ($\lambda$).
- **Interpolation Search (`InterpolationSearch`)**: Dynamic probe positioning based on key value distribution:
  $$pos = low + \left\lfloor \frac{target - arr[low]}{arr[high] - arr[low]} \times (high - low) \right\rfloor$$
- **Multi-Algorithm Search Benchmark**: Live comparative benchmark running Sequential vs. Binary (Iterative) vs. Binary (Recursive) vs. Interpolation Search on the same query to compare step counts.
- **Sorting Engine**: Pure from-scratch implementations of:
  - **Merge Sort** ($O(N \log N)$ stable)
  - **Quick Sort** ($O(N \log N)$ average)
  - **Insertion Sort** ($O(N^2)$ efficient for small/nearly sorted data)
  - **Bubble Sort** & **Selection Sort** ($O(N^2)$ comparison-based)
  - Measures and displays comparisons, swaps, and execution duration.

#### CO 4: Construct and Traverse Hierarchical Data Structures
- **AVL Tree (`AVLTree`) & BST (`BinarySearchTree`)**: Master catalog ordered by book title.
  - Maintains balance factor $\in \{-1, 0, 1\}$.
  - Auto-balances via **LL (Left-Left)**, **RR (Right-Right)**, **LR (Left-Right)**, and **RL (Right-Left)** rotations upon insertion/deletion.
  - Implements **In-order** (sorted), **Pre-order**, and **Post-order** traversals.
- **Trie / Prefix Tree (`Trie`)**: Character-tree providing real-time $O(L)$ prefix search autocomplete as users type book titles, authors, or genres into the search bar.
- **Min-Heap & Max-Heap (`BinaryHeap`)**: Array-based complete binary trees:
  - **Min-Heap**: $O(1)$ root retrieval of **Earliest Due Dates / Overdue Books**.
  - **Max-Heap**: $O(1)$ root retrieval of **Trending / Most Borrowed Books**.
- **B-Tree (`BTree`, $t = 3$)**: Multi-key block indexing simulation demonstrating disk block storage organization for large catalog databases.

#### CO 5: Formulate and Solve Graph Theory Problems
- **Library Recommendation & Knowledge Graph (`Graph`)**:
  - Vertices: Books, student borrowers, and categories.
  - Edges: Co-borrowing relations, prerequisites, and category memberships.
  - Exposes both **Adjacency List** and **Adjacency Matrix** representations.
- **Breadth-First Search (BFS)**: Computes shortest-hop book recommendations ("Readers who borrowed book X also borrowed book Y") using a FIFO queue.
- **Depth-First Search (DFS)**: Deep prerequisite chain traversal and topic dependency exploration using a LIFO stack.

---

### 🧪 Automated Verification
All 5 Course Outcomes are verified via an automated test suite:
```bash
python test_system.py
```
Test results verify all 7 integration modules across linear, linked, hashing, tree, and graph structures:
```text
Ran 7 tests in 0.183s
OK
```
