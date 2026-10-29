"""
dsa_core.py - Core Data Structures implemented from scratch
Includes: HashTable (Separate Chaining), Trie (Prefix Tree),
DoublyLinkedList, Stack (LIFO), and Queue (FIFO).
"""

# -------------------------------------------------------------
# 1. HASH TABLE WITH SEPARATE CHAINING (O(1) Avg Lookup)
# -------------------------------------------------------------
class HashNode:
    def __init__(self, key, value, next_node=None):
        self.key = str(key)
        self.value = value
        self.next = next_node

class HashTable:
    def __init__(self, capacity=17):
        self.capacity = capacity
        self.buckets = [None] * capacity
        self.size = 0

    def _hash(self, key):
        hash_val = 0
        for char in str(key):
            hash_val = (hash_val * 31 + ord(char)) % self.capacity
        return hash_val

    def insert(self, key, value):
        idx = self._hash(key)
        curr = self.buckets[idx]
        while curr:
            if curr.key == key:
                curr.value = value
                return
            curr = curr.next
        self.buckets[idx] = HashNode(key, value, self.buckets[idx])
        self.size += 1

    def search(self, key):
        idx = self._hash(key)
        curr = self.buckets[idx]
        while curr:
            if curr.key == key:
                return curr.value
            curr = curr.next
        return None

    def delete(self, key):
        idx = self._hash(key)
        curr = self.buckets[idx]
        prev = None
        while curr:
            if curr.key == key:
                if prev is None:
                    self.buckets[idx] = curr.next
                else:
                    prev.next = curr.next
                self.size -= 1
                return curr.value
            prev = curr
            curr = curr.next
        return None

    def get_all(self):
        items = []
        for bucket in self.buckets:
            curr = bucket
            while curr:
                items.append(curr.value)
                curr = curr.next
        return items

    def get_bucket_state(self):
        state = []
        for i, bucket in enumerate(self.buckets):
            chain = []
            curr = bucket
            while curr:
                chain.append({"key": curr.key, "title": curr.value.get("title", "Unknown")})
                curr = curr.next
            state.append({"bucket_index": i, "count": len(chain), "chain": chain})
        return state


# -------------------------------------------------------------
# 2. TRIE (PREFIX TREE) FOR AUTOCOMPLETE SEARCH (O(L))
# -------------------------------------------------------------
class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end_of_word = False
        self.records = []

class Trie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word, record):
        if not word:
            return
        curr = self.root
        for char in word.lower().strip():
            if char not in curr.children:
                curr.children[char] = TrieNode()
            curr = curr.children[char]
        curr.is_end_of_word = True
        curr.records.append(record)

    def search_prefix(self, prefix, limit=6):
        if not prefix:
            return []
        curr = self.root
        for char in prefix.lower().strip():
            if char not in curr.children:
                return []
            curr = curr.children[char]

        results = []
        def _dfs(node):
            if len(results) >= limit:
                return
            if node.is_end_of_word:
                for rec in node.records:
                    if rec not in results:
                        results.append(rec)
            for child in node.children.values():
                _dfs(child)

        _dfs(curr)
        return results[:limit]


# -------------------------------------------------------------
# 3. DOUBLY LINKED LIST (FOR RECENTLY VIEWED & TRANSACTION LOGS)
# -------------------------------------------------------------
class DLLNode:
    def __init__(self, data, prev=None, next_node=None):
        self.data = data
        self.prev = prev
        self.next = next_node

class DoublyLinkedList:
    def __init__(self):
        self.head = None
        self.tail = None
        self.current = None
        self.size = 0

    def append(self, data):
        new_node = DLLNode(data)
        if not self.head:
            self.head = new_node
            self.tail = new_node
            self.current = new_node
        else:
            self.tail.next = new_node
            new_node.prev = self.tail
            self.tail = new_node
            self.current = new_node
        self.size += 1

    def move_prev(self):
        if self.current and self.current.prev:
            self.current = self.current.prev
            return self.current.data
        return self.current.data if self.current else None

    def move_next(self):
        if self.current and self.current.next:
            self.current = self.current.next
            return self.current.data
        return self.current.data if self.current else None

    def to_list(self):
        res = []
        curr = self.head
        while curr:
            res.append({
                "data": curr.data,
                "is_current": (curr == self.current)
            })
            curr = curr.next
        return res


# -------------------------------------------------------------
# 4. STACK (LIFO) FOR UNDO TRANSACTION ROOF
# -------------------------------------------------------------
class StackNode:
    def __init__(self, data, next_node=None):
        self.data = data
        self.next = next_node

class Stack:
    def __init__(self):
        self.top = None
        self._count = 0

    def push(self, data):
        self.top = StackNode(data, self.top)
        self._count += 1

    def pop(self):
        if self.is_empty():
            return None
        popped = self.top.data
        self.top = self.top.next
        self._count -= 1
        return popped

    def peek(self):
        return self.top.data if self.top else None

    def is_empty(self):
        return self.top is None

    def size(self):
        return self._count

    def to_list(self):
        items = []
        curr = self.top
        while curr:
            items.append(curr.data)
            curr = curr.next
        return items


# -------------------------------------------------------------
# 5. QUEUE (FIFO) FOR OUT-OF-STOCK WAITLISTS
# -------------------------------------------------------------
class QNode:
    def __init__(self, data, next_node=None):
        self.data = data
        self.next = next_node

class Queue:
    def __init__(self):
        self.front = None
        self.rear = None
        self._count = 0

    def enqueue(self, data):
        node = QNode(data)
        if not self.rear:
            self.front = node
            self.rear = node
        else:
            self.rear.next = node
            self.rear = node
        self._count += 1

    def dequeue(self):
        if self.is_empty():
            return None
        removed = self.front.data
        self.front = self.front.next
        if not self.front:
            self.rear = None
        self._count -= 1
        return removed

    def is_empty(self):
        return self._count == 0

    def size(self):
        return self._count

    def to_list(self):
        items = []
        curr = self.front
        while curr:
            items.append(curr.data)
            curr = curr.next
        return items

