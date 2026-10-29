"""
Learning Unit IV: Hierarchical Data Structures
- Binary Search Tree (BST) & AVL Tree
  * Supports insertion, deletion, rotations (LL, RR, LR, RL), balance factor calculation
  * In-order, Pre-order, Post-order Traversals
- Trie / Prefix Tree:
  * O(L) autocomplete for book titles and authors
- Min-Heap & Max-Heap (Array-based):
  * Min-Heap: Earliest Due Dates / Overdue Books at root (O(1) retrieval)
  * Max-Heap: Trending / Most Borrowed Books at root (O(1) retrieval)
- B-Tree:
  * Multi-key block indexing for persistent catalog storage simulation
Implemented strictly without built-in dicts or sorting functions.
"""

# ==========================================
# Binary Search Tree (BST)
# ==========================================

class BSTNode:
    def __init__(self, key: str, value=None):
        self.key = key
        self.value = value
        self.left = None
        self.right = None


class BinarySearchTree:
    def __init__(self):
        self.root = None

    def insert(self, key: str, value=None):
        self.root = self._insert_node(self.root, key, value)

    def _insert_node(self, node: BSTNode, key: str, value):
        if not node:
            return BSTNode(key, value)
        if key < node.key:
            node.left = self._insert_node(node.left, key, value)
        elif key > node.key:
            node.right = self._insert_node(node.right, key, value)
        else:
            node.value = value
        return node

    def search(self, key: str):
        curr = self.root
        steps = 0
        while curr:
            steps += 1
            if key == curr.key:
                return {"found": True, "node": curr, "steps": steps}
            elif key < curr.key:
                curr = curr.left
            else:
                curr = curr.right
        return {"found": False, "node": None, "steps": steps}

    def inorder(self):
        result = []
        def _inorder(node):
            if not node:
                return
            _inorder(node.left)
            result.append({"key": node.key, "value": node.value})
            _inorder(node.right)
        _inorder(self.root)
        return result

    def preorder(self):
        result = []
        def _preorder(node):
            if not node:
                return
            result.append({"key": node.key, "value": node.value})
            _preorder(node.left)
            _preorder(node.right)
        _preorder(self.root)
        return result

    def postorder(self):
        result = []
        def _postorder(node):
            if not node:
                return
            _postorder(node.left)
            _postorder(node.right)
            result.append({"key": node.key, "value": node.value})
        _postorder(self.root)
        return result


# ==========================================
# AVL Tree
# ==========================================

class AVLNode:
    def __init__(self, key: str, value=None):
        self.key = key
        self.value = value
        self.left = None
        self.right = None
        self.height = 1


class AVLTree:
    """
    Self-Balancing AVL Tree.
    Maintains Balance Factor in [-1, 0, 1] via LL, RR, LR, RL Rotations.
    Records rotation events and exposes full tree hierarchy for visualizer.
    """
    def __init__(self):
        self.root = None
        self.last_rotation = None

    def get_height(self, node: AVLNode) -> int:
        return node.height if node else 0

    def get_balance(self, node: AVLNode) -> int:
        return self.get_height(node.left) - self.get_height(node.right) if node else 0

    def _rotate_right(self, y: AVLNode) -> AVLNode:
        """Right Rotation (LL case)"""
        x = y.left
        T2 = x.right

        # Perform rotation
        x.right = y
        y.left = T2

        # Update heights
        y.height = 1 + max(self.get_height(y.left), self.get_height(y.right))
        x.height = 1 + max(self.get_height(x.left), self.get_height(x.right))
        self.last_rotation = f"Right Rotation (LL) on '{y.key}'"
        return x

    def _rotate_left(self, x: AVLNode) -> AVLNode:
        """Left Rotation (RR case)"""
        y = x.right
        T2 = y.left

        # Perform rotation
        y.left = x
        x.right = T2

        # Update heights
        x.height = 1 + max(self.get_height(x.left), self.get_height(x.right))
        y.height = 1 + max(self.get_height(y.left), self.get_height(y.right))
        self.last_rotation = f"Left Rotation (RR) on '{x.key}'"
        return y

    def insert(self, key: str, value=None):
        self.root = self._insert(self.root, key, value)

    def _insert(self, node: AVLNode, key: str, value) -> AVLNode:
        if not node:
            return AVLNode(key, value)

        if key < node.key:
            node.left = self._insert(node.left, key, value)
        elif key > node.key:
            node.right = self._insert(node.right, key, value)
        else:
            node.value = value
            return node

        # Update height of ancestor node
        node.height = 1 + max(self.get_height(node.left), self.get_height(node.right))

        # Check balance factor
        balance = self.get_balance(node)

        # Case 1: Left Left (LL)
        if balance > 1 and key < node.left.key:
            return self._rotate_right(node)

        # Case 2: Right Right (RR)
        if balance < -1 and key > node.right.key:
            return self._rotate_left(node)

        # Case 3: Left Right (LR)
        if balance > 1 and key > node.left.key:
            self.last_rotation = f"Left-Right Rotation (LR) on '{node.key}'"
            node.left = self._rotate_left(node.left)
            return self._rotate_right(node)

        # Case 4: Right Left (RL)
        if balance < -1 and key < node.right.key:
            self.last_rotation = f"Right-Left Rotation (RL) on '{node.key}'"
            node.right = self._rotate_right(node.right)
            return self._rotate_left(node)

        return node

    def delete(self, key: str):
        self.root = self._delete(self.root, key)

    def _min_value_node(self, node: AVLNode) -> AVLNode:
        curr = node
        while curr.left:
            curr = curr.left
        return curr

    def _delete(self, node: AVLNode, key: str) -> AVLNode:
        if not node:
            return node

        if key < node.key:
            node.left = self._delete(node.left, key)
        elif key > node.key:
            node.right = self._delete(node.right, key)
        else:
            if not node.left:
                temp = node.right
                node = None
                return temp
            elif not node.right:
                temp = node.left
                node = None
                return temp

            temp = self._min_value_node(node.right)
            node.key = temp.key
            node.value = temp.value
            node.right = self._delete(node.right, temp.key)

        if not node:
            return node

        node.height = 1 + max(self.get_height(node.left), self.get_height(node.right))
        balance = self.get_balance(node)

        # Left Left
        if balance > 1 and self.get_balance(node.left) >= 0:
            return self._rotate_right(node)

        # Left Right
        if balance > 1 and self.get_balance(node.left) < 0:
            node.left = self._rotate_left(node.left)
            return self._rotate_right(node)

        # Right Right
        if balance < -1 and self.get_balance(node.right) <= 0:
            return self._rotate_left(node)

        # Right Left
        if balance < -1 and self.get_balance(node.right) > 0:
            node.right = self._rotate_right(node.right)
            return self._rotate_left(node)

        return node

    def inorder(self):
        result = []
        def _inorder(node):
            if not node:
                return
            _inorder(node.left)
            result.append({"key": node.key, "balance": self.get_balance(node), "height": node.height, "value": node.value})
            _inorder(node.right)
        _inorder(self.root)
        return result

    def preorder(self):
        result = []
        def _preorder(node):
            if not node:
                return
            result.append({"key": node.key, "balance": self.get_balance(node), "height": node.height, "value": node.value})
            _preorder(node.left)
            _preorder(node.right)
        _preorder(self.root)
        return result

    def postorder(self):
        result = []
        def _postorder(node):
            if not node:
                return
            _postorder(node.left)
            _postorder(node.right)
            result.append({"key": node.key, "balance": self.get_balance(node), "height": node.height, "value": node.value})
        _postorder(self.root)
        return result

    def to_tree_json(self):
        """Hierarchical nested dictionary format for D3 / Canvas / CSS tree visualization."""
        def _convert(node):
            if not node:
                return None
            return {
                "name": node.key,
                "height": node.height,
                "balance": self.get_balance(node),
                "value": node.value,
                "children": [
                    child for child in [_convert(node.left), _convert(node.right)] if child is not None
                ]
            }
        return _convert(self.root)


# ==========================================
# Trie / Prefix Tree
# ==========================================

class TrieNode:
    def __init__(self, char: str = ""):
        self.char = char
        # Custom child map using list of tuples (char, node)
        self.children = []
        self.is_end_of_word = False
        self.metadata = []  # List of book metadata matching this exact word

    def get_child(self, char: str):
        for c, node in self.children:
            if c == char:
                return node
        return None

    def add_child(self, char: str):
        existing = self.get_child(char)
        if existing:
            return existing
        new_node = TrieNode(char)
        self.children.append((char, new_node))
        return new_node


class Trie:
    """
    Trie (Prefix Tree) for real-time $O(L)$ autocomplete for book titles and authors.
    """
    def __init__(self):
        self.root = TrieNode()
        self.total_words = 0

    def insert(self, word: str, data=None):
        if not word:
            return
        curr = self.root
        lower_word = word.lower()
        for char in lower_word:
            curr = curr.add_child(char)
        if not curr.is_end_of_word:
            self.total_words += 1
        curr.is_end_of_word = True
        if data is not None:
            curr.metadata.append(data)

    def search_prefix(self, prefix: str, max_results: int = 8):
        """
        Traverse down to prefix end, then collect all descendants.
        Returns matching words, associated metadata, and step count.
        """
        if not prefix:
            return {"prefix": prefix, "matches": [], "steps": 0}

        curr = self.root
        lower_prefix = prefix.lower()
        steps = 0

        for char in lower_prefix:
            steps += 1
            curr = curr.get_child(char)
            if not curr:
                return {"prefix": prefix, "matches": [], "steps": steps}

        # DFS from curr to collect matched terms
        results = []

        def _dfs(node, current_str):
            if len(results) >= max_results:
                return
            if node.is_end_of_word:
                results.append({
                    "term": current_str,
                    "metadata": node.metadata
                })
            for _, child in node.children:
                _dfs(child, current_str + child.char)

        _dfs(curr, lower_prefix)
        return {
            "prefix": prefix,
            "matches": results,
            "steps": steps,
            "count": len(results)
        }


# ==========================================
# Binary Heaps (Min-Heap & Max-Heap)
# ==========================================

class BinaryHeap:
    """
    Array-based Binary Heap base class.
    is_min = True for Min-Heap (Earliest due dates)
    is_min = False for Max-Heap (Trending / most borrowed)
    """
    def __init__(self, is_min: bool = True, capacity: int = 100):
        self.is_min = is_min
        self.capacity = capacity
        self._heap = [None] * capacity
        self.size = 0

    def _compare(self, a, b) -> bool:
        """Returns True if a should be placed above b."""
        if self.is_min:
            return a["score"] < b["score"]
        else:
            return a["score"] > b["score"]

    def _parent(self, i: int) -> int:
        return (i - 1) // 2

    def _left_child(self, i: int) -> int:
        return 2 * i + 1

    def _right_child(self, i: int) -> int:
        return 2 * i + 2

    def insert(self, score: float, data):
        if self.size >= self.capacity:
            # resize
            new_cap = self.capacity * 2
            new_heap = [None] * new_cap
            for i in range(self.size):
                new_heap[i] = self._heap[i]
            self._heap = new_heap
            self.capacity = new_cap

        entry = {"score": score, "data": data}
        self._heap[self.size] = entry
        self._sift_up(self.size)
        self.size += 1

    def _sift_up(self, i: int):
        while i > 0 and self._compare(self._heap[i], self._heap[self._parent(i)]):
            p = self._parent(i)
            self._heap[i], self._heap[p] = self._heap[p], self._heap[i]
            i = p

    def peek(self):
        if self.size == 0:
            return None
        return self._heap[0]

    def extract(self):
        if self.size == 0:
            raise IndexError("extract from empty heap")
        root = self._heap[0]
        self._heap[0] = self._heap[self.size - 1]
        self._heap[self.size - 1] = None
        self.size -= 1
        if self.size > 0:
            self._sift_down(0)
        return root

    def _sift_down(self, i: int):
        target = i
        left = self._left_child(i)
        right = self._right_child(i)

        if left < self.size and self._compare(self._heap[left], self._heap[target]):
            target = left
        if right < self.size and self._compare(self._heap[right], self._heap[target]):
            target = right

        if target != i:
            self._heap[i], self._heap[target] = self._heap[target], self._heap[i]
            self._sift_down(target)

    def to_list(self):
        result = []
        for i in range(self.size):
            result.append(self._heap[i])
        return result

    def get_state(self):
        return {
            "type": "MinHeap" if self.is_min else "MaxHeap",
            "size": self.size,
            "root": self.peek(),
            "elements": self.to_list()
        }


class MinHeap(BinaryHeap):
    def __init__(self, capacity: int = 100):
        super().__init__(is_min=True, capacity=capacity)


class MaxHeap(BinaryHeap):
    def __init__(self, capacity: int = 100):
        super().__init__(is_min=False, capacity=capacity)


# ==========================================
# B-Tree
# ==========================================

class BTreeNode:
    def __init__(self, is_leaf: bool = True):
        self.is_leaf = is_leaf
        self.keys = []      # list of keys
        self.values = []    # list of associated payloads
        self.children = []  # list of BTreeNode pointers


class BTree:
    """
    B-Tree of degree t (t >= 2).
    Each node has at most 2t - 1 keys and 2t children.
    Simulates multi-key block indexing for persistent catalog storage.
    """
    def __init__(self, t: int = 3):
        self.t = t  # Minimum degree
        self.root = BTreeNode(is_leaf=True)

    def search(self, key: int, node: BTreeNode = None):
        if node is None:
            node = self.root

        i = 0
        while i < len(node.keys) and key > node.keys[i]:
            i += 1

        if i < len(node.keys) and key == node.keys[i]:
            return {"found": True, "value": node.values[i], "node": node}

        if node.is_leaf:
            return {"found": False, "value": None, "node": None}

        return self.search(key, node.children[i])

    def insert(self, key: int, value=None):
        root = self.root
        if len(root.keys) == (2 * self.t - 1):
            s = BTreeNode(is_leaf=False)
            self.root = s
            s.children.append(root)
            self._split_child(s, 0)
            self._insert_non_full(s, key, value)
        else:
            self._insert_non_full(root, key, value)

    def _split_child(self, parent: BTreeNode, i: int):
        t = self.t
        y = parent.children[i]
        z = BTreeNode(is_leaf=y.is_leaf)

        # Median key to move up
        median_key = y.keys[t - 1]
        median_val = y.values[t - 1]

        # z gets right half of keys and values
        z.keys = y.keys[t:(2 * t - 1)]
        z.values = y.values[t:(2 * t - 1)]

        if not y.is_leaf:
            z.children = y.children[t:(2 * t)]
            y.children = y.children[0:t]

        y.keys = y.keys[0:(t - 1)]
        y.values = y.values[0:(t - 1)]

        # Insert z into parent children at i+1
        parent.children.insert(i + 1, z)
        parent.keys.insert(i, median_key)
        parent.values.insert(i, median_val)

    def _insert_non_full(self, node: BTreeNode, key: int, value):
        i = len(node.keys) - 1

        if node.is_leaf:
            # Insert in sorted order
            node.keys.append(None)
            node.values.append(None)
            while i >= 0 and key < node.keys[i]:
                node.keys[i + 1] = node.keys[i]
                node.values[i + 1] = node.values[i]
                i -= 1
            node.keys[i + 1] = key
            node.values[i + 1] = value
        else:
            while i >= 0 and key < node.keys[i]:
                i -= 1
            i += 1
            if len(node.children[i].keys) == (2 * self.t - 1):
                self._split_child(node, i)
                if key > node.keys[i]:
                    i += 1
            self._insert_non_full(node.children[i], key, value)

    def to_tree_json(self):
        """Serializes B-Tree into hierarchical JSON for visualization."""
        def _convert(node: BTreeNode):
            if not node:
                return None
            key_labels = [f"ID:{k}" for k in node.keys]
            return {
                "name": " | ".join(key_labels) if key_labels else "Empty",
                "keys": node.keys,
                "values": node.values,
                "is_leaf": node.is_leaf,
                "children": [_convert(c) for c in node.children]
            }
        return _convert(self.root)

