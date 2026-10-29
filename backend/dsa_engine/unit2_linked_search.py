"""
Learning Unit II: Linked Lists & Basic Searching
- Singly Linked List (SLL): Borrower Transaction History
- Doubly Linked List (DLL): Bidirectional Book Reader / History Navigator (Next/Prev)
- Circular Linked List (CLL): Featured Books Carousel on dashboard (infinitely cyclic)
- Linked Stack & Linked Queue: Pointer-based nodes for Waitlist and Undo Stack
- Basic Searching:
  * Sequential Search (Unindexed author/notes search)
  * Binary Search (Iterative & Recursive) on sorted Book ID / ISBN arrays
Returns operation steps, pointer transitions, and comparison counts for frontend visualization.
"""

class SNode:
    """Singly Linked List Node"""
    def __init__(self, data, next_node=None):
        self.data = data
        self.next = next_node


class SinglyLinkedList:
    """
    Singly Linked List for Student Borrower History.
    Maintains Head and Count, supports append, prepend, traversal, search, and deletion.
    """
    def __init__(self):
        self.head = None
        self.count = 0

    def append(self, data):
        new_node = SNode(data)
        if not self.head:
            self.head = new_node
        else:
            curr = self.head
            while curr.next:
                curr = curr.next
            curr.next = new_node
        self.count += 1

    def prepend(self, data):
        new_node = SNode(data, self.head)
        self.head = new_node
        self.count += 1

    def delete(self, match_fn) -> bool:
        """Deletes first element where match_fn(data) is True."""
        if not self.head:
            return False
        if match_fn(self.head.data):
            self.head = self.head.next
            self.count -= 1
            return True
        curr = self.head
        while curr.next:
            if match_fn(curr.next.data):
                curr.next = curr.next.next
                self.count -= 1
                return True
            curr = curr.next
        return False

    def to_list(self):
        items = []
        curr = self.head
        while curr:
            items.append(curr.data)
            curr = curr.next
        return items

    def get_pointer_chain(self):
        """Returns structured node-pointer representation for SVG/HTML rendering."""
        nodes = []
        curr = self.head
        idx = 0
        while curr:
            nodes.append({
                "index": idx,
                "data": curr.data,
                "has_next": (curr.next is not None)
            })
            curr = curr.next
            idx += 1
        return {
            "type": "SinglyLinkedList",
            "length": self.count,
            "nodes": nodes
        }


class DNode:
    """Doubly Linked List Node"""
    def __init__(self, data, prev_node=None, next_node=None):
        self.data = data
        self.prev = prev_node
        self.next = next_node


class DoublyLinkedList:
    """
    Doubly Linked List for Bidirectional Book Reader / History Navigator.
    Allows moving backward and forward through recently viewed books.
    """
    def __init__(self):
        self.head = None
        self.tail = None
        self.current = None
        self.count = 0

    def append(self, data):
        new_node = DNode(data)
        if not self.head:
            self.head = new_node
            self.tail = new_node
            self.current = new_node
        else:
            self.tail.next = new_node
            new_node.prev = self.tail
            self.tail = new_node
            self.current = new_node
        self.count += 1

    def move_next(self):
        if self.current and self.current.next:
            self.current = self.current.next
            return self.current.data
        return self.current.data if self.current else None

    def move_prev(self):
        if self.current and self.current.prev:
            self.current = self.current.prev
            return self.current.data
        return self.current.data if self.current else None

    def get_current(self):
        return self.current.data if self.current else None

    def get_pointer_chain(self):
        nodes = []
        curr = self.head
        idx = 0
        while curr:
            nodes.append({
                "index": idx,
                "data": curr.data,
                "is_current": (curr == self.current),
                "has_prev": (curr.prev is not None),
                "has_next": (curr.next is not None)
            })
            curr = curr.next
            idx += 1
        return {
            "type": "DoublyLinkedList",
            "length": self.count,
            "nodes": nodes
        }

    def to_list(self):
        items = []
        curr = self.head
        while curr:
            items.append(curr.data)
            curr = curr.next
        return items


class CNode:
    """Circular Linked List Node"""
    def __init__(self, data, next_node=None):
        self.data = data
        self.next = next_node


class CircularLinkedList:
    """
    Circular Linked List for Featured Books Carousel.
    Cycles infinitely in $O(1)$ step time.
    """
    def __init__(self):
        self.head = None
        self.current = None
        self.count = 0

    def append(self, data):
        new_node = CNode(data)
        if not self.head:
            self.head = new_node
            new_node.next = self.head
            self.current = self.head
        else:
            # find last node
            curr = self.head
            while curr.next != self.head:
                curr = curr.next
            curr.next = new_node
            new_node.next = self.head
        self.count += 1

    def cycle_next(self):
        if not self.current:
            return None
        self.current = self.current.next
        return self.current.data

    def get_current(self):
        return self.current.data if self.current else None

    def to_list(self):
        if not self.head:
            return []
        res = []
        curr = self.head
        while True:
            res.append(curr.data)
            curr = curr.next
            if curr == self.head:
                break
        return res

    def get_pointer_chain(self, max_display: int = 10):
        if not self.head:
            return {"type": "CircularLinkedList", "length": 0, "nodes": []}
        nodes = []
        curr = self.head
        idx = 0
        while True:
            nodes.append({
                "index": idx,
                "data": curr.data,
                "is_current": (curr == self.current),
                "points_to_head": (curr.next == self.head)
            })
            curr = curr.next
            idx += 1
            if curr == self.head or idx >= max_display:
                break
        return {
            "type": "CircularLinkedList",
            "length": self.count,
            "nodes": nodes,
            "is_circular": True
        }


class LinkedStack:
    """Stack implemented purely via pointer-based Singly Linked Nodes."""
    def __init__(self):
        self.top = None
        self.count = 0

    def push(self, data):
        new_node = SNode(data, self.top)
        self.top = new_node
        self.count += 1

    def pop(self):
        if self.is_empty():
            raise IndexError("pop from empty LinkedStack")
        val = self.top.data
        self.top = self.top.next
        self.count -= 1
        return val

    def peek(self):
        return self.top.data if self.top else None

    def is_empty(self) -> bool:
        return self.top is None

    def to_list(self):
        res = []
        curr = self.top
        while curr:
            res.append(curr.data)
            curr = curr.next
        return res


class LinkedQueue:
    """Queue implemented purely via pointer-based Singly Linked Nodes with Head & Tail."""
    def __init__(self):
        self.front = None
        self.rear = None
        self.count = 0

    def enqueue(self, data):
        new_node = SNode(data)
        if not self.rear:
            self.front = new_node
            self.rear = new_node
        else:
            self.rear.next = new_node
            self.rear = new_node
        self.count += 1

    def dequeue(self):
        if self.is_empty():
            raise IndexError("dequeue from empty LinkedQueue")
        val = self.front.data
        self.front = self.front.next
        if not self.front:
            self.rear = None
        self.count -= 1
        return val

    def peek(self):
        return self.front.data if self.front else None

    def is_empty(self) -> bool:
        return self.front is None

    def to_list(self):
        res = []
        curr = self.front
        while curr:
            res.append(curr.data)
            curr = curr.next
        return res


# ==========================================
# Unit 2: Basic Searching Algorithms
# ==========================================

def sequential_search(items, key_extractor, target):
    """
    Linear / Sequential search over unindexed data.
    Returns: { "found": bool, "index": int, "item": Any, "steps": int, "history": list }
    """
    steps = 0
    history = []
    n = len(items)
    for i in range(n):
        steps += 1
        val = key_extractor(items[i])
        history.append({"step": steps, "index": i, "value": val, "matched": (val == target)})
        if val == target:
            return {
                "found": True,
                "index": i,
                "item": items[i],
                "steps": steps,
                "history": history
            }
    return {
        "found": False,
        "index": -1,
        "item": None,
        "steps": steps,
        "history": history
    }


def binary_search_iterative(sorted_items, key_extractor, target):
    """
    Iterative Binary Search on a sorted list.
    Returns: { "found": bool, "index": int, "steps": int, "history": list }
    """
    low = 0
    high = len(sorted_items) - 1
    steps = 0
    history = []

    while low <= high:
        steps += 1
        mid = (low + high) // 2
        mid_val = key_extractor(sorted_items[mid])
        history.append({
            "step": steps,
            "low": low,
            "mid": mid,
            "high": high,
            "mid_value": mid_val,
            "target": target
        })
        if mid_val == target:
            return {
                "found": True,
                "index": mid,
                "item": sorted_items[mid],
                "steps": steps,
                "history": history
            }
        elif mid_val < target:
            low = mid + 1
        else:
            high = mid - 1

    return {
        "found": False,
        "index": -1,
        "item": None,
        "steps": steps,
        "history": history
    }


def binary_search_recursive(sorted_items, key_extractor, target, low=0, high=None, history=None):
    """
    Recursive Binary Search with recursion call tracking.
    """
    if history is None:
        history = []
    if high is None:
        high = len(sorted_items) - 1

    if low > high:
        return {
            "found": False,
            "index": -1,
            "item": None,
            "steps": len(history),
            "history": history
        }

    mid = (low + high) // 2
    mid_val = key_extractor(sorted_items[mid])
    history.append({
        "step": len(history) + 1,
        "low": low,
        "mid": mid,
        "high": high,
        "mid_value": mid_val,
        "target": target
    })

    if mid_val == target:
        return {
            "found": True,
            "index": mid,
            "item": sorted_items[mid],
            "steps": len(history),
            "history": history
        }
    elif mid_val < target:
        return binary_search_recursive(sorted_items, key_extractor, target, mid + 1, high, history)
    else:
        return binary_search_recursive(sorted_items, key_extractor, target, low, mid - 1, history)
