# Course Outcomes (CO) & Data Structures Implementation

---

## **CO 1: Linear Data Structures**
* **Concepts:** Stacks, Queues, Deques, Circular Buffers & Priority Queues
* **Data Structures / ADTs:**
  * Stack ADT (`Stack`)
  * Circular Queue (`CircularQueue`)
  * Deque (`DoubleEndedQueue`)
  * Priority Queue (`PriorityQueue`)
* **Real-World Applications:**
  * **Action Audit Log & Undo System:** Stack ADT for reversing loans, additions, and returns.
  * **Late-Fee Formula Evaluator:** Infix-to-Postfix conversion and stack evaluation.
  * **Return Drop-Box Buffering:** Fixed circular buffer with modulo wrap-around.
  * **VIP / Faculty Scheduling:** Deque enabling front-insertion for VIPs/faculty and rear-insertion for students.
  * **Waitlist Queue:** FIFO & Urgency-based reservation handling.

---

## **CO 2: Linked Lists & Basic Searching**
* **Concepts:** Singly, Doubly, Circular Linked Lists, Sequential & Binary Search
* **Data Structures / ADTs:**
  * Singly Linked List (`SinglyLinkedList`)
  * Doubly Linked List (`DoublyLinkedList`)
  * Circular Linked List (`CircularLinkedList`)
  * Sequential & Binary Search (Iterative & Recursive)
* **Real-World Applications:**
  * **Student Borrower Transaction History:** Singly linked list (`HEAD -> [Node] -> NULL`).
  * **Recently Viewed Books Navigator:** Doubly linked list (`NULL <- [Prev | Data | Next] -> NULL`).
  * **Featured Books Showcase Carousel:** Infinitely cycling circular linked list.
  * **Search Benchmark:** Step comparison of sequential scan vs. $O(\log N)$ divide-and-conquer binary search.

---

## **CO 3: Hashing, Advanced Searching & Sorting**
* **Concepts:** Hash Tables, Collision Resolution, Interpolation Search, Comparison Sorts
* **Data Structures / ADTs:**
  * Custom Hash Table (`HashTable`, $h(k) = k \bmod 101$)
  * Collision Strategies: Separate Chaining & Open Addressing (Linear Probing)
  * Interpolation Search
  * Sorting Suite: Merge, Quick, Insertion, Bubble, Selection Sort
* **Real-World Applications:**
  * **Fast Lookups:** $O(1)$ Book & Member Lookups with live bucket collision inspection.
  * **Dynamic Probe Calculation:** Interpolation search on uniformly distributed ISBN IDs.
  * **Multi-Algorithm Search Benchmark:** Real-time comparison of step counts across searching strategies.
  * **Catalog Sorting:** Multi-attribute sorting by Title, Year, Borrows, or Availability with comparison & swap metrics.

---

## **CO 4: Hierarchical Structures & Heaps**
* **Concepts:** BST, Balanced AVL Trees, Rotations, Tries, Binary Heaps & B-Trees
* **Data Structures / ADTs:**
  * AVL Tree (`AVLTree`) & Binary Search Tree (`BST`)
  * Balance Factor & Rotations (LL, RR, LR, RL)
  * Trie / Prefix Tree (`Trie`)
  * Min-Heap & Max-Heap (`BinaryHeap`)
  * B-Tree (`BTree`, $t = 3$)
* **Real-World Applications:**
  * **Self-Balancing Catalog:** Title-indexed AVL tree with In-order, Pre-order, and Post-order traversals.
  * **Autocomplete Search:** $O(L)$ real-time prefix search for titles & authors.
  * **Min-Heap Overdue Management:** $O(1)$ lookup for earliest overdue returns.
  * **Max-Heap Popularity Tracking:** $O(1)$ lookup for trending / most borrowed books.
  * **Secondary Storage Indexing:** Multi-key block indexing simulation.

