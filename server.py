"""
server.py - Python HTTP Server + REST API for LuminaLib
"""
import http.server
import socketserver
import json
import os
import sys
import webbrowser
import urllib.parse
from dsa_core import HashTable, Trie, DoublyLinkedList, Stack, Queue
import db

PORT = 3000
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_DIR = os.path.join(BASE_DIR, "static")

# Instantiate In-Memory Data Structures
book_ht = HashTable(capacity=17)
search_trie = Trie()
recently_viewed_dll = DoublyLinkedList()
undo_stack = Stack()
waitlist_queues = {} # ISBN -> Queue()
transaction_dll = DoublyLinkedList()

def sync_memory_from_db():
    """Initializes in-memory DSA nodes directly from the SQLite store."""
    conn = db.get_connection()
    cursor = conn.cursor()

    # Load Books
    cursor.execute("SELECT * FROM books")
    books = cursor.fetchall()
    for b in books:
        book_dict = dict(b)
        book_ht.insert(book_dict["isbn"], book_dict)
        search_trie.insert(book_dict["title"], book_dict)
        search_trie.insert(book_dict["author"], book_dict)
        waitlist_queues[book_dict["isbn"]] = Queue()

    # Load Waitlist Queues in chronological FIFO order
    cursor.execute("SELECT * FROM waitlists ORDER BY id ASC")
    for row in cursor.fetchall():
        isbn = row["isbn"]
        if isbn in waitlist_queues:
            waitlist_queues[isbn].enqueue({
                "member_id": row["member_id"],
                "created_at": row["created_at"]
            })

    # Load Transactions
    cursor.execute("SELECT * FROM transactions ORDER BY id ASC")
    for row in cursor.fetchall():
        transaction_dll.append(dict(row))

    conn.close()


class LuminaRequestHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=STATIC_DIR, **kwargs)

    def _send_json(self, status, payload):
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()
        self.wfile.write(json.dumps(payload).encode("utf-8"))

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path
        query = urllib.parse.parse_qs(parsed.query)

        if path == "/api/books":
            books = book_ht.get_all()
            self._send_json(200, {"success": True, "data": books})

        elif path == "/api/search":
            q = query.get("q", [""])[0]
            matches = search_trie.search_prefix(q)
            self._send_json(200, {"success": True, "data": matches})

        elif path == "/api/members":
            conn = db.get_connection()
            members = [dict(m) for m in conn.cursor().execute("SELECT * FROM members").fetchall()]
            conn.close()
            self._send_json(200, {"success": True, "data": members})

        elif path == "/api/waitlist":
            res = {}
            for isbn, q in waitlist_queues.items():
                if not q.is_empty():
                    res[isbn] = q.to_list()
            self._send_json(200, {"success": True, "data": res})

        elif path == "/api/history":
            self._send_json(200, {"success": True, "data": transaction_dll.to_list()})

        elif path == "/api/recently-viewed":
            self._send_json(200, {"success": True, "data": recently_viewed_dll.to_list()})

        elif path == "/api/dsa-state":
            # Live memory snapshot for DSA inspector
            self._send_json(200, {
                "success": True,
                "hash_table": book_ht.get_bucket_state(),
                "stack": undo_stack.to_list(),
                "waitlists": {isbn: q.to_list() for isbn, q in waitlist_queues.items() if not q.is_empty()},
                "metrics": {
                    "hash_size": book_ht.size,
                    "stack_depth": undo_stack.size(),
                    "total_waitlist": sum(q.size() for q in waitlist_queues.values())
                }
            })
        else:
            super().do_GET()

    def do_POST(self):
        content_length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(content_length)
        data = json.loads(body.decode("utf-8")) if body else {}

        if self.path == "/api/books":
            isbn = data.get("isbn")
            title = data.get("title")
            author = data.get("author")
            year = int(data.get("year", 2024))
            category = data.get("category", "General")
            copies = int(data.get("total_copies", 1))

            conn = db.get_connection()
            conn.cursor().execute("""
                INSERT INTO books (isbn, title, author, year, category, total_copies, available_copies)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (isbn, title, author, year, category, copies, copies))
            conn.commit()
            conn.close()

            new_book = {
                "isbn": isbn, "title": title, "author": author,
                "year": year, "category": category,
                "total_copies": copies, "available_copies": copies
            }
            book_ht.insert(isbn, new_book)
            search_trie.insert(title, new_book)
            search_trie.insert(author, new_book)
            waitlist_queues[isbn] = Queue()

            undo_stack.push({"action": "ADD_BOOK", "isbn": isbn, "description": f"Added '{title}'"})
            self._send_json(201, {"success": True, "data": new_book})

        elif self.path == "/api/checkout":
            isbn = data.get("isbn")
            member_id = data.get("member_id", "MEM101")
            book = book_ht.search(isbn)

            if not book:
                self._send_json(404, {"success": False, "message": "Book not found"})
                return

            if book["available_copies"] <= 0:
                # Add to FIFO Queue
                waitlist_queues[isbn].enqueue({"member_id": member_id, "created_at": "Just now"})
                conn = db.get_connection()
                conn.cursor().execute("INSERT INTO waitlists (isbn, member_id) VALUES (?, ?)", (isbn, member_id))
                conn.commit()
                conn.close()

                undo_stack.push({
                    "action": "WAITLIST_ENQUEUE",
                    "isbn": isbn,
                    "member_id": member_id,
                    "description": f"Enqueued {member_id} for '{book['title']}'"
                })
                self._send_json(200, {"success": True, "waitlisted": True, "message": "Enqueued in FIFO Waitlist"})
                return

            # Decrement inventory
            book["available_copies"] -= 1
            book_ht.insert(isbn, book)

            conn = db.get_connection()
            cursor = conn.cursor()
            cursor.execute("UPDATE books SET available_copies = available_copies - 1 WHERE isbn = ?", (isbn,))
            txn_id = f"TXN-{os.urandom(2).hex().upper()}"
            cursor.execute("""
                INSERT INTO transactions (txn_id, type, isbn, title, member_id)
                VALUES (?, 'ISSUE', ?, ?, ?)
            """, (txn_id, isbn, book["title"], member_id))
            conn.commit()
            conn.close()

            txn_record = {"txn_id": txn_id, "type": "ISSUE", "isbn": isbn, "title": book["title"], "member_id": member_id, "created_at": "Just now"}
            transaction_dll.append(txn_record)
            undo_stack.push({"action": "ISSUE", "isbn": isbn, "member_id": member_id, "description": f"Issued '{book['title']}' to {member_id}"})

            self._send_json(200, {"success": True, "waitlisted": False, "book": book})

        elif self.path == "/api/return":
            isbn = data.get("isbn")
            member_id = data.get("member_id", "MEM101")
            book = book_ht.search(isbn)

            if not book:
                self._send_json(404, {"success": False, "message": "Book not found"})
                return

            queue = waitlist_queues.get(isbn)
            conn = db.get_connection()
            cursor = conn.cursor()

            if queue and not queue.is_empty():
                # Automatic FIFO handover
                next_member = queue.dequeue()
                cursor.execute("DELETE FROM waitlists WHERE id = (SELECT id FROM waitlists WHERE isbn = ? ORDER BY id ASC LIMIT 1)", (isbn,))
                txn_id = f"TXN-{os.urandom(2).hex().upper()}"
                cursor.execute("""
                    INSERT INTO transactions (txn_id, type, isbn, title, member_id)
                    VALUES (?, 'AUTO_ALLOCATE', ?, ?, ?)
                """, (txn_id, isbn, book["title"], next_member["member_id"]))
                conn.commit()

                txn_record = {"txn_id": txn_id, "type": "AUTO_ALLOCATE", "isbn": isbn, "title": book["title"], "member_id": next_member["member_id"], "created_at": "Just now"}
                transaction_dll.append(txn_record)
                undo_stack.push({"action": "AUTO_ALLOCATE", "isbn": isbn, "to_member": next_member["member_id"], "description": f"Auto-allocated '{book['title']}' to {next_member['member_id']}"})
                conn.close()

                self._send_json(200, {"success": True, "auto_allocated": True, "to_member": next_member["member_id"]})
                return

            # Normal Return
            book["available_copies"] = min(book["total_copies"], book["available_copies"] + 1)
            book_ht.insert(isbn, book)

            cursor.execute("UPDATE books SET available_copies = available_copies + 1 WHERE isbn = ?", (isbn,))
            txn_id = f"TXN-{os.urandom(2).hex().upper()}"
            cursor.execute("""
                INSERT INTO transactions (txn_id, type, isbn, title, member_id)
                VALUES (?, 'RETURN', ?, ?, ?)
            """, (txn_id, isbn, book["title"], member_id))
            conn.commit()
            conn.close()

            txn_record = {"txn_id": txn_id, "type": "RETURN", "isbn": isbn, "title": book["title"], "member_id": member_id, "created_at": "Just now"}
            transaction_dll.append(txn_record)
            undo_stack.push({"action": "RETURN", "isbn": isbn, "member_id": member_id, "description": f"Returned '{book['title']}' from {member_id}"})

            self._send_json(200, {"success": True, "auto_allocated": False, "book": book})

        elif self.path == "/api/undo":
            if undo_stack.is_empty():
                self._send_json(400, {"success": False, "message": "Undo stack empty"})
                return

            last_action = undo_stack.pop()
            action_type = last_action["action"]
            isbn = last_action["isbn"]
            book = book_ht.search(isbn)

            conn = db.get_connection()
            cursor = conn.cursor()

            if action_type == "ISSUE":
                if book:
                    book["available_copies"] += 1
                    cursor.execute("UPDATE books SET available_copies = available_copies + 1 WHERE isbn = ?", (isbn,))
            elif action_type == "RETURN":
                if book:
                    book["available_copies"] = max(0, book["available_copies"] - 1)
                    cursor.execute("UPDATE books SET available_copies = available_copies - 1 WHERE isbn = ?", (isbn,))
            elif action_type == "WAITLIST_ENQUEUE":
                # Rebuild queue removing user
                mem = last_action["member_id"]
                cursor.execute("DELETE FROM waitlists WHERE id = (SELECT id FROM waitlists WHERE isbn = ? AND member_id = ? ORDER BY id DESC LIMIT 1)", (isbn, mem))
                new_q = Queue()
                for item in waitlist_queues[isbn].to_list():
                    if item["member_id"] != mem:
                        new_q.enqueue(item)
                waitlist_queues[isbn] = new_q

            conn.commit()
            conn.close()
            self._send_json(200, {"success": True, "undone": last_action})

        elif self.path == "/api/view-book":
            isbn = data.get("isbn")
            book = book_ht.search(isbn)
            if book:
                recently_viewed_dll.append(book)
                self._send_json(200, {"success": True, "data": recently_viewed_dll.to_list()})
            else:
                self._send_json(404, {"success": False, "message": "Book not found"})


def main():
    db.init_db()
    sync_memory_from_db()

    os.makedirs(STATIC_DIR, exist_ok=True)
    os.chdir(BASE_DIR)

    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.TCPServer(("", PORT), LuminaRequestHandler) as httpd:
        url = f"http://localhost:{PORT}/index.html"
        print("=" * 65)
        print("  LuminaLib — Fully Modular DSA Library Management System")
        print("=" * 65)
        print(f"  [+] Local Server:  {url}")
        print(f"  [+] Database:      {db.DB_FILE}")
        print(f"  [+] Active Status: Serving API & Static Assets")
        print("=" * 65)

        try:
            webbrowser.open(url)
        except Exception:
            pass

        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nShutting down LuminaLib server cleanly...")
            httpd.server_close()

if __name__ == "__main__":
    main()

