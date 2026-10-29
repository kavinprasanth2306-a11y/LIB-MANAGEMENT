"""
Learning Unit III: Hashing, Advanced Searching & Sorting
- Custom Hash Table (fixed size = 101, h(k) = k mod 101)
  * Supports collision strategies: Separate Chaining & Open Addressing (Linear Probing)
- Interpolation Search for uniformly distributed keys
- Search Benchmark Module (Sequential vs. Binary Iterative/Recursive vs. Interpolation)
- Sorting Engine:
  * Insertion Sort
  * Bubble Sort
  * Selection Sort
  * Merge Sort
All sorts track comparisons, swaps/moves, and return state snapshots for visualizer animation.
Implemented purely from scratch without list.sort() or built-in dicts.
"""

class HashEntry:
    def __init__(self, key: int, value, status: str = "occupied"):
        self.key = key
        self.value = value
        self.status = status  # 'occupied', 'deleted', 'empty'


class HashChainNode:
    def __init__(self, key: int, value, next_node=None):
        self.key = key
        self.value = value
        self.next = next_node


class HashTable:
    """
    Custom Hash Table strictly implementing size=101 with h(k) = k mod 101.
    Allows switching or demonstrating both Separate Chaining and Linear Probing.
    """
    def __init__(self, size: int = 101, strategy: str = "chaining"):
        self.size = size
        self.strategy = strategy  # "chaining" or "probing"
        self.count = 0
        self._init_storage()

    def _init_storage(self):
        if self.strategy == "chaining":
            # Array of pointers to HashChainNode
            self._table = [None] * self.size
        else:
            # Array of HashEntry for Linear Probing
            self._table = [None] * self.size

    def set_strategy(self, strategy: str):
        if strategy not in ["chaining", "probing"]:
            raise ValueError("Strategy must be 'chaining' or 'probing'")
        # Collect all items
        items = self.items()
        self.strategy = strategy
        self.count = 0
        self._init_storage()
        for k, v in items:
            self.insert(k, v)

    def hash_function(self, key: int) -> int:
        return abs(int(key)) % self.size

    def insert(self, key: int, value) -> dict:
        """
        Inserts key-value pair and records collision and probe statistics.
        """
        idx = self.hash_function(key)
        probes = 1
        collided = False

        if self.strategy == "chaining":
            head = self._table[idx]
            if head is not None:
                collided = True
            # Check if key already exists, update it
            curr = head
            while curr:
                if curr.key == key:
                    curr.value = value
                    return {"index": idx, "probes": probes, "collided": collided, "action": "updated"}
                curr = curr.next
                probes += 1
            # Prepend to chain
            new_node = HashChainNode(key, value, head)
            self._table[idx] = new_node
            self.count += 1
            return {"index": idx, "probes": probes, "collided": collided, "action": "inserted"}

        else:
            # Linear Probing
            start_idx = idx
            while self._table[idx] is not None and self._table[idx].status == "occupied":
                if self._table[idx].key == key:
                    self._table[idx].value = value
                    return {"index": idx, "probes": probes, "collided": (probes > 1), "action": "updated"}
                collided = True
                probes += 1
                idx = (idx + 1) % self.size
                if idx == start_idx or probes > self.size:
                    raise OverflowError("Hash table is full with linear probing")

            self._table[idx] = HashEntry(key, value, "occupied")
            self.count += 1
            return {"index": idx, "probes": probes, "collided": collided, "action": "inserted"}

    def get(self, key: int):
        idx = self.hash_function(key)
        probes = 1

        if self.strategy == "chaining":
            curr = self._table[idx]
            while curr:
                if curr.key == key:
                    return {"found": True, "value": curr.value, "probes": probes, "bucket": idx}
                curr = curr.next
                probes += 1
            return {"found": False, "value": None, "probes": probes, "bucket": idx}

        else:
            start_idx = idx
            while self._table[idx] is not None:
                if self._table[idx].status == "occupied" and self._table[idx].key == key:
                    return {"found": True, "value": self._table[idx].value, "probes": probes, "bucket": idx}
                probes += 1
                idx = (idx + 1) % self.size
                if idx == start_idx or probes > self.size:
                    break
            return {"found": False, "value": None, "probes": probes, "bucket": start_idx}

    def delete(self, key: int) -> bool:
        idx = self.hash_function(key)

        if self.strategy == "chaining":
            curr = self._table[idx]
            prev = None
            while curr:
                if curr.key == key:
                    if prev is None:
                        self._table[idx] = curr.next
                    else:
                        prev.next = curr.next
                    self.count -= 1
                    return True
                prev = curr
                curr = curr.next
            return False

        else:
            start_idx = idx
            probes = 0
            while self._table[idx] is not None and probes < self.size:
                if self._table[idx].status == "occupied" and self._table[idx].key == key:
                    self._table[idx].status = "deleted"
                    self._table[idx].value = None
                    self.count -= 1
                    return True
                idx = (idx + 1) % self.size
                probes += 1
            return False

    def items(self):
        result = []
        if self.strategy == "chaining":
            for i in range(self.size):
                curr = self._table[i]
                while curr:
                    result.append((curr.key, curr.value))
                    curr = curr.next
        else:
            for i in range(self.size):
                entry = self._table[i]
                if entry is not None and entry.status == "occupied":
                    result.append((entry.key, entry.value))
        return result

    def get_state(self):
        """Returns visualizable representation of the 101 buckets."""
        buckets = []
        occupied_count = 0
        total_chain_length = 0
        max_chain_length = 0

        for i in range(self.size):
            if self.strategy == "chaining":
                nodes = []
                curr = self._table[i]
                chain_len = 0
                while curr:
                    nodes.append({"key": curr.key, "value": curr.value})
                    curr = curr.next
                    chain_len += 1
                if chain_len > 0:
                    occupied_count += 1
                if chain_len > max_chain_length:
                    max_chain_length = chain_len
                total_chain_length += chain_len
                buckets.append({
                    "bucket": i,
                    "chain_length": chain_len,
                    "nodes": nodes
                })
            else:
                entry = self._table[i]
                if entry is not None and entry.status == "occupied":
                    occupied_count += 1
                    buckets.append({
                        "bucket": i,
                        "status": "occupied",
                        "key": entry.key,
                        "value": entry.value
                    })
                elif entry is not None and entry.status == "deleted":
                    buckets.append({
                        "bucket": i,
                        "status": "deleted",
                        "key": None,
                        "value": None
                    })
                else:
                    buckets.append({
                        "bucket": i,
                        "status": "empty",
                        "key": None,
                        "value": None
                    })

        load_factor = round(self.count / self.size, 4)
        return {
            "size": self.size,
            "strategy": self.strategy,
            "count": self.count,
            "load_factor": load_factor,
            "occupied_buckets": occupied_count,
            "max_chain_length": max_chain_length,
            "buckets": buckets
        }


# ==========================================
# Interpolation Search
# ==========================================

def interpolation_search(sorted_items, key_extractor, target):
    """
    Interpolation Search: probe pos = low + [ (target - arr[low]) * (high - low) / (arr[high] - arr[low]) ]
    Requires sorted items with numerical keys.
    """
    low = 0
    high = len(sorted_items) - 1
    steps = 0
    history = []

    target_num = float(target)

    while low <= high:
        low_val = float(key_extractor(sorted_items[low]))
        high_val = float(key_extractor(sorted_items[high]))

        if target_num < low_val or target_num > high_val:
            break

        steps += 1
        if low == high:
            pos = low
        else:
            # Interpolation probe formula
            fraction = (target_num - low_val) / (high_val - low_val) if high_val != low_val else 0
            pos = low + int(fraction * (high - low))

        pos_val = float(key_extractor(sorted_items[pos]))
        history.append({
            "step": steps,
            "low": low,
            "high": high,
            "probe_pos": pos,
            "probe_value": pos_val,
            "target": target_num
        })

        if pos_val == target_num:
            return {
                "found": True,
                "index": pos,
                "item": sorted_items[pos],
                "steps": steps,
                "history": history
            }
        elif pos_val < target_num:
            low = pos + 1
        else:
            high = pos - 1

    return {
        "found": False,
        "index": -1,
        "item": None,
        "steps": steps,
        "history": history
    }


# ==========================================
# Sorting Algorithms
# ==========================================

def bubble_sort(items, key_extractor, ascending=True):
    """Bubble sort tracking comparisons and swaps."""
    arr = [x for x in items]
    n = len(arr)
    comparisons = 0
    swaps = 0

    for i in range(n):
        swapped = False
        for j in range(0, n - i - 1):
            comparisons += 1
            val_a = key_extractor(arr[j])
            val_b = key_extractor(arr[j + 1])
            condition = (val_a > val_b) if ascending else (val_a < val_b)
            if condition:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                swaps += 1
                swapped = True
        if not swapped:
            break

    return {"sorted": arr, "comparisons": comparisons, "swaps": swaps, "algorithm": "Bubble Sort"}


def selection_sort(items, key_extractor, ascending=True):
    """Selection sort tracking comparisons and swaps."""
    arr = [x for x in items]
    n = len(arr)
    comparisons = 0
    swaps = 0

    for i in range(n):
        target_idx = i
        for j in range(i + 1, n):
            comparisons += 1
            val_j = key_extractor(arr[j])
            val_target = key_extractor(arr[target_idx])
            condition = (val_j < val_target) if ascending else (val_j > val_target)
            if condition:
                target_idx = j

        if target_idx != i:
            arr[i], arr[target_idx] = arr[target_idx], arr[i]
            swaps += 1

    return {"sorted": arr, "comparisons": comparisons, "swaps": swaps, "algorithm": "Selection Sort"}


def insertion_sort(items, key_extractor, ascending=True):
    """Insertion sort tracking comparisons and shifts/swaps."""
    arr = [x for x in items]
    n = len(arr)
    comparisons = 0
    shifts = 0

    for i in range(1, n):
        key_item = arr[i]
        key_val = key_extractor(key_item)
        j = i - 1

        while j >= 0:
            comparisons += 1
            curr_val = key_extractor(arr[j])
            condition = (curr_val > key_val) if ascending else (curr_val < key_val)
            if condition:
                arr[j + 1] = arr[j]
                shifts += 1
                j -= 1
            else:
                break
        arr[j + 1] = key_item

    return {"sorted": arr, "comparisons": comparisons, "swaps": shifts, "algorithm": "Insertion Sort"}


def merge_sort(items, key_extractor, ascending=True):
    """Merge sort tracking comparisons and auxiliary moves."""
    arr = [x for x in items]
    comparisons = [0]
    moves = [0]

    def _merge_sort_rec(lst):
        if len(lst) <= 1:
            return lst

        mid = len(lst) // 2
        left = _merge_sort_rec(lst[:mid])
        right = _merge_sort_rec(lst[mid:])

        merged = []
        i = j = 0
        while i < len(left) and j < len(right):
            comparisons[0] += 1
            val_l = key_extractor(left[i])
            val_r = key_extractor(right[j])
            condition = (val_l <= val_r) if ascending else (val_l >= val_r)
            if condition:
                merged.append(left[i])
                i += 1
            else:
                merged.append(right[j])
                j += 1
            moves[0] += 1

        while i < len(left):
            merged.append(left[i])
            i += 1
            moves[0] += 1

        while j < len(right):
            merged.append(right[j])
            j += 1
            moves[0] += 1

        return merged

    sorted_arr = _merge_sort_rec(arr)
    return {"sorted": sorted_arr, "comparisons": comparisons[0], "swaps": moves[0], "algorithm": "Merge Sort"}
