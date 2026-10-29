"""
db.py - SQLite Database Schema & Persistence
"""
import sqlite3
import os

DB_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "library.db")

def get_connection():
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    # Books Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS books (
        isbn TEXT PRIMARY KEY,
        title TEXT NOT NULL,
        author TEXT NOT NULL,
        year INTEGER NOT NULL,
        category TEXT NOT NULL,
        total_copies INTEGER NOT NULL,
        available_copies INTEGER NOT NULL
    )
    """)

    # Members Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS members (
        member_id TEXT PRIMARY KEY,
        full_name TEXT NOT NULL,
        role TEXT NOT NULL
    )
    """)

    # Active Waitlists (FIFO persistence)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS waitlists (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        isbn TEXT NOT NULL,
        member_id TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (isbn) REFERENCES books(isbn),
        FOREIGN KEY (member_id) REFERENCES members(member_id)
    )
    """)

    # Transaction History Log
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS transactions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        txn_id TEXT NOT NULL,
        type TEXT NOT NULL,
        isbn TEXT NOT NULL,
        title TEXT NOT NULL,
        member_id TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    conn.commit()

    # Seed Books if empty
    cursor.execute("SELECT COUNT(*) as cnt FROM books")
    if cursor.fetchone()["cnt"] == 0:
        seed_books = [
            ("978-0262033848", "Introduction to Algorithms", "Thomas H. Cormen", 2009, "Algorithms", 4, 2),
            ("978-0132350884", "Clean Code", "Robert C. Martin", 2008, "Software Architecture", 5, 4),
            ("978-0201633610", "Design Patterns (GoF)", "Erich Gamma et al.", 1994, "Software Architecture", 3, 1),
            ("978-1119800361", "Operating System Concepts", "Abraham Silberschatz", 2018, "Computer Science", 3, 0),
            ("978-0134610993", "Artificial Intelligence: A Modern Approach", "Stuart Russell, Peter Norvig", 2020, "Artificial Intelligence", 4, 3),
            ("978-0262510875", "Structure and Interpretation of Computer Programs", "Harold Abelson", 1996, "Computer Science", 3, 2),
            ("978-1449373320", "Designing Data-Intensive Applications", "Martin Kleppmann", 2017, "Computer Science", 5, 1),
            ("978-0134092669", "Computer Systems: A Programmer's Perspective", "Randal Bryant", 2015, "Computer Science", 3, 0),
            ("978-0135957059", "The Pragmatic Programmer", "David Thomas", 2019, "Software Architecture", 4, 4),
            ("978-0201896831", "The Art of Computer Programming", "Donald E. Knuth", 1997, "Algorithms", 2, 1),
            ("978-0321486813", "Compilers: Principles, Techniques, Tools", "Alfred Aho et al.", 2006, "Computer Science", 3, 2),
            ("978-0262035613", "Deep Learning", "Ian Goodfellow et al.", 2016, "Artificial Intelligence", 3, 2),
            ("978-0078022159", "Database System Concepts", "Abraham Silberschatz", 2019, "Computer Science", 3, 1),
            ("978-0735619678", "Code Complete", "Steve McConnell", 2004, "Software Architecture", 4, 3)
        ]
        cursor.executemany("""
            INSERT INTO books (isbn, title, author, year, category, total_copies, available_copies)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, seed_books)

        # Seed Members
        seed_members = [
            ("MEM101", "Alan Turing", "Researcher"),
            ("MEM102", "Ada Lovelace", "Fellow"),
            ("MEM103", "Grace Hopper", "Faculty"),
            ("MEM104", "Linus Torvalds", "Student"),
            ("MEM105", "Barbara Liskov", "Professor")
        ]
        cursor.executemany("INSERT INTO members (member_id, full_name, role) VALUES (?, ?, ?)", seed_members)

        # Seed initial queue for out of stock
        cursor.execute("INSERT INTO waitlists (isbn, member_id) VALUES ('978-1119800361', 'MEM102')")
        cursor.execute("INSERT INTO waitlists (isbn, member_id) VALUES ('978-1119800361', 'MEM103')")
        cursor.execute("INSERT INTO waitlists (isbn, member_id) VALUES ('978-0134092669', 'MEM104')")

        conn.commit()
    conn.close()

