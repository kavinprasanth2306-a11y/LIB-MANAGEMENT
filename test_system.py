import unittest
from fastapi.testclient import TestClient
import backend.main as m

class TestDsaLibrarySystem(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.client = TestClient(m.app)

    def test_books_catalog(self):
        res = self.client.get('/api/books')
        self.assertEqual(res.status_code, 200)
        books = res.json()['books']
        self.assertGreaterEqual(len(books), 16)

    def test_unit1_linear(self):
        # Fine expression evaluator
        res = self.client.post('/api/dsa/unit1/evaluate-fine?formula=days*2+fee&days=5')
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertEqual(data['result'], 20.0)

        # Drop-box circular queue
        res = self.client.get('/api/dsa/unit1/dropbox-state')
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.json()['capacity'], 6)

        # VIP Deque
        res = self.client.get('/api/dsa/unit1/vip-deque-state')
        self.assertEqual(res.status_code, 200)

    def test_unit2_linked_search(self):
        # SLL History
        res = self.client.get('/api/dsa/unit2/sll-history')
        self.assertEqual(res.status_code, 200)
        self.assertIn('nodes', res.json())

        # DLL Navigator
        res = self.client.get('/api/dsa/unit2/dll-navigator')
        self.assertEqual(res.status_code, 200)

        # CLL Carousel
        res = self.client.get('/api/dsa/unit2/cll-carousel')
        self.assertEqual(res.status_code, 200)

    def test_unit3_hash_sort(self):
        # Hash table state
        res = self.client.get('/api/dsa/unit3/hash-table-state')
        self.assertEqual(res.status_code, 200)
        ht = res.json()
        self.assertEqual(ht['size'], 101)

        # Toggle strategy to probing
        res = self.client.post('/api/dsa/unit3/hash-table-strategy?strategy=probing')
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.json()['state']['strategy'], 'probing')

        # Restore strategy to chaining
        res = self.client.post('/api/dsa/unit3/hash-table-strategy?strategy=chaining')
        self.assertEqual(res.status_code, 200)

        # Benchmark
        res = self.client.post('/api/dsa/unit3/search-benchmark', json={'query': '109'})
        self.assertEqual(res.status_code, 200)
        bench = res.json()['results']
        self.assertTrue(bench['sequential_search']['found'])
        self.assertTrue(bench['binary_search_iterative']['found'])
        self.assertTrue(bench['binary_search_recursive']['found'])
        self.assertTrue(bench['interpolation_search']['found'])

    def test_unit4_trees_heaps(self):
        # AVL Tree
        res = self.client.get('/api/dsa/unit4/avl-tree-state')
        self.assertEqual(res.status_code, 200)
        self.assertIn('inorder', res.json()['traversals'])

        # Autocomplete Trie
        res = self.client.get('/api/dsa/unit4/autocomplete?prefix=algo')
        self.assertEqual(res.status_code, 200)
        self.assertGreaterEqual(res.json()['count'], 1)

        # Heaps
        res = self.client.get('/api/dsa/unit4/heaps-state')
        self.assertEqual(res.status_code, 200)

        # B-Tree
        res = self.client.get('/api/dsa/unit4/btree-state')
        self.assertEqual(res.status_code, 200)

    def test_unit5_graphs(self):
        # Graph State
        res = self.client.get('/api/dsa/unit5/graph-state')
        self.assertEqual(res.status_code, 200)
        self.assertIn('adjacency_list', res.json())
        self.assertIn('adjacency_matrix', res.json())

        # BFS Recommendations
        res = self.client.get('/api/dsa/unit5/bfs-recommendations?start_id=B101')
        self.assertEqual(res.status_code, 200)
        self.assertIn('recommendations', res.json())

        # DFS Exploration
        res = self.client.get('/api/dsa/unit5/dfs-exploration?start_id=B101')
        self.assertEqual(res.status_code, 200)
        self.assertIn('exploration_order', res.json())

    def test_undo_stack(self):
        # Issue book
        res = self.client.post('/api/books/issue', json={'book_id': 101, 'student_id': 'STU1001'})
        self.assertEqual(res.status_code, 200)

        # Undo
        res = self.client.post('/api/undo')
        self.assertEqual(res.status_code, 200)
        self.assertTrue(res.json()['success'])

if __name__ == '__main__':
    unittest.main()
