"""
DSA Engine Package
Implements University Curriculum Units 1-5 strictly from scratch without built-in dicts, deques, or list.sort().
"""

from .unit1_linear import (
    Stack,
    Queue,
    CircularQueue,
    DoubleEndedQueue,
    PriorityQueue,
    evaluate_infix_expression
)
from .unit2_linked_search import (
    SinglyLinkedList,
    DoublyLinkedList,
    CircularLinkedList,
    LinkedStack,
    LinkedQueue,
    sequential_search,
    binary_search_iterative,
    binary_search_recursive
)
from .unit3_hash_sort import (
    HashTable,
    interpolation_search,
    bubble_sort,
    selection_sort,
    insertion_sort,
    merge_sort
)
from .unit4_trees_heaps import (
    BinarySearchTree,
    AVLTree,
    Trie,
    MinHeap,
    MaxHeap,
    BTree
)
from .unit5_graphs import (
    Graph
)

__all__ = [
    "Stack",
    "Queue",
    "CircularQueue",
    "DoubleEndedQueue",
    "PriorityQueue",
    "evaluate_infix_expression",
    "SinglyLinkedList",
    "DoublyLinkedList",
    "CircularLinkedList",
    "LinkedStack",
    "LinkedQueue",
    "sequential_search",
    "binary_search_iterative",
    "binary_search_recursive",
    "HashTable",
    "interpolation_search",
    "bubble_sort",
    "selection_sort",
    "insertion_sort",
    "merge_sort",
    "BinarySearchTree",
    "AVLTree",
    "Trie",
    "MinHeap",
    "MaxHeap",
    "BTree",
    "Graph"
]

