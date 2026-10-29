"""
Seed dataset containing 16+ classic CS textbooks, students, transactions, and graph relationships.
"""

INITIAL_BOOKS = [
    {
        "id": 101,
        "title": "Introduction to Algorithms",
        "author": "Thomas H. Cormen",
        "isbn": "978-0262033848",
        "year": 2009,
        "category": "Algorithms",
        "total_copies": 4,
        "available_copies": 2,
        "borrow_count": 48,
        "tags": ["dsa", "core", "algorithms", "cormen"]
    },
    {
        "id": 102,
        "title": "Clean Code: A Handbook of Agile Software Craftsmanship",
        "author": "Robert C. Martin",
        "isbn": "978-0132350884",
        "year": 2008,
        "category": "Software Engineering",
        "total_copies": 5,
        "available_copies": 3,
        "borrow_count": 62,
        "tags": ["craftsmanship", "clean-code", "refactoring"]
    },
    {
        "id": 103,
        "title": "Operating System Concepts",
        "author": "Abraham Silberschatz",
        "isbn": "978-1119800361",
        "year": 2018,
        "category": "Systems",
        "total_copies": 3,
        "available_copies": 1,
        "borrow_count": 35,
        "tags": ["os", "dinosaur", "concurrency", "memory"]
    },
    {
        "id": 104,
        "title": "Artificial Intelligence: A Modern Approach",
        "author": "Stuart Russell & Peter Norvig",
        "isbn": "978-0134610993",
        "year": 2020,
        "category": "AI & ML",
        "total_copies": 4,
        "available_copies": 2,
        "borrow_count": 55,
        "tags": ["ai", "agents", "machine-learning", "norvig"]
    },
    {
        "id": 105,
        "title": "Computer Networks",
        "author": "Andrew S. Tanenbaum",
        "isbn": "978-0132126953",
        "year": 2010,
        "category": "Networking",
        "total_copies": 3,
        "available_copies": 0,
        "borrow_count": 41,
        "tags": ["tcp-ip", "routing", "tanenbaum"]
    },
    {
        "id": 106,
        "title": "Design Patterns: Elements of Reusable Object-Oriented Software",
        "author": "Erich Gamma, Richard Helm, Ralph Johnson, John Vlissides",
        "isbn": "978-0201633610",
        "year": 1994,
        "category": "Software Engineering",
        "total_copies": 4,
        "available_copies": 2,
        "borrow_count": 39,
        "tags": ["gof", "oop", "architecture"]
    },
    {
        "id": 107,
        "title": "Structure and Interpretation of Computer Programs",
        "author": "Harold Abelson & Gerald Jay Sussman",
        "isbn": "978-0262510875",
        "year": 1996,
        "category": "Computer Science",
        "total_copies": 3,
        "available_copies": 3,
        "borrow_count": 27,
        "tags": ["sicp", "lisp", "lambda", "fundamentals"]
    },
    {
        "id": 108,
        "title": "Database System Concepts",
        "author": "Abraham Silberschatz, Henry F. Korth",
        "isbn": "978-0078022159",
        "year": 2019,
        "category": "Databases",
        "total_copies": 4,
        "available_copies": 2,
        "borrow_count": 32,
        "tags": ["dbms", "sql", "transactions", "b-trees"]
    },
    {
        "id": 109,
        "title": "Computer Systems: A Programmer's Perspective",
        "author": "Randal E. Bryant & David R. O'Hallaron",
        "isbn": "978-0134092669",
        "year": 2015,
        "category": "Systems",
        "total_copies": 5,
        "available_copies": 1,
        "borrow_count": 51,
        "tags": ["csapp", "assembly", "caching", "virtual-memory"]
    },
    {
        "id": 110,
        "title": "The Pragmatic Programmer",
        "author": "David Thomas & Andrew Hunt",
        "isbn": "978-0135957059",
        "year": 2019,
        "category": "Software Engineering",
        "total_copies": 4,
        "available_copies": 3,
        "borrow_count": 45,
        "tags": ["craftsmanship", "career", "pragmatic"]
    },
    {
        "id": 111,
        "title": "Designing Data-Intensive Applications",
        "author": "Martin Kleppmann",
        "isbn": "978-1449373320",
        "year": 2017,
        "category": "Distributed Systems",
        "total_copies": 6,
        "available_copies": 1,
        "borrow_count": 70,
        "tags": ["ddia", "distributed", "replication", "partitioning"]
    },
    {
        "id": 112,
        "title": "Compilers: Principles, Techniques, and Tools",
        "author": "Alfred V. Aho, Monica S. Lam, Ravi Sethi, Jeffrey D. Ullman",
        "isbn": "978-0321486813",
        "year": 2006,
        "category": "Compilers",
        "total_copies": 3,
        "available_copies": 2,
        "borrow_count": 22,
        "tags": ["dragon-book", "parsing", "ast", "lexing"]
    },
    {
        "id": 113,
        "title": "The Art of Computer Programming, Volume 1",
        "author": "Donald E. Knuth",
        "isbn": "978-0201896831",
        "year": 1997,
        "category": "Algorithms",
        "total_copies": 2,
        "available_copies": 1,
        "borrow_count": 18,
        "tags": ["knuth", "taocp", "math", "algorithms"]
    },
    {
        "id": 114,
        "title": "Deep Learning",
        "author": "Ian Goodfellow, Yoshua Bengio, Aaron Courville",
        "isbn": "978-0262035613",
        "year": 2016,
        "category": "AI & ML",
        "total_copies": 4,
        "available_copies": 3,
        "borrow_count": 42,
        "tags": ["deep-learning", "neural-networks", "goodfellow"]
    },
    {
        "id": 115,
        "title": "Modern Operating Systems",
        "author": "Andrew S. Tanenbaum & Herbert Bos",
        "isbn": "978-0133591620",
        "year": 2014,
        "category": "Systems",
        "total_copies": 3,
        "available_copies": 2,
        "borrow_count": 29,
        "tags": ["mos", "tanenbaum", "kernel", "linux"]
    },
    {
        "id": 116,
        "title": "Code Complete: A Practical Handbook of Software Construction",
        "author": "Steve McConnell",
        "isbn": "978-0735619678",
        "year": 2004,
        "category": "Software Engineering",
        "total_copies": 3,
        "available_copies": 2,
        "borrow_count": 31,
        "tags": ["code-complete", "construction", "debugging"]
    }
]

INITIAL_STUDENTS = [
    {"id": "STU1001", "name": "Alice Johnson", "role": "student", "department": "Computer Science"},
    {"id": "STU1002", "name": "Bob Smith", "role": "student", "department": "Data Science"},
    {"id": "STU1003", "name": "Carol Danvers", "role": "faculty", "department": "Computer Engineering"},
    {"id": "STU1004", "name": "David Miller", "role": "vip", "department": "Information Technology"},
    {"id": "STU1005", "name": "Elena Rostova", "role": "student", "department": "Computer Science"}
]

GRAPH_NODES = [
    {"id": "B101", "label": "Intro to Algorithms", "type": "book"},
    {"id": "B102", "label": "Clean Code", "type": "book"},
    {"id": "B103", "label": "Operating Systems", "type": "book"},
    {"id": "B104", "label": "Artificial Intelligence", "type": "book"},
    {"id": "B105", "label": "Computer Networks", "type": "book"},
    {"id": "B106", "label": "Design Patterns", "type": "book"},
    {"id": "B108", "label": "Database Systems", "type": "book"},
    {"id": "B109", "label": "Computer Systems (CSAPP)", "type": "book"},
    {"id": "B111", "label": "Designing Data-Intensive Apps", "type": "book"},
    {"id": "B114", "label": "Deep Learning", "type": "book"},
    {"id": "CAT_SYS", "label": "Systems & Networks", "type": "category"},
    {"id": "CAT_SWE", "label": "Software Engineering", "type": "category"},
    {"id": "CAT_AI", "label": "AI & Data", "type": "category"}
]

GRAPH_EDGES = [
    {"src": "B101", "dst": "B102", "relation": "co-borrowed", "weight": 4.5},
    {"src": "B101", "dst": "B104", "relation": "prerequisite", "weight": 5.0},
    {"src": "B102", "dst": "B106", "relation": "co-borrowed", "weight": 4.8},
    {"src": "B103", "dst": "B105", "relation": "co-borrowed", "weight": 4.2},
    {"src": "B103", "dst": "B109", "relation": "prerequisite", "weight": 5.0},
    {"src": "B108", "dst": "B111", "relation": "prerequisite", "weight": 4.9},
    {"src": "B109", "dst": "B105", "relation": "co-borrowed", "weight": 3.8},
    {"src": "B104", "dst": "B114", "relation": "prerequisite", "weight": 5.0},
    {"src": "B103", "dst": "CAT_SYS", "relation": "belongs_to", "weight": 2.0},
    {"src": "B105", "dst": "CAT_SYS", "relation": "belongs_to", "weight": 2.0},
    {"src": "B109", "dst": "CAT_SYS", "relation": "belongs_to", "weight": 2.0},
    {"src": "B102", "dst": "CAT_SWE", "relation": "belongs_to", "weight": 2.0},
    {"src": "B106", "dst": "CAT_SWE", "relation": "belongs_to", "weight": 2.0},
    {"src": "B104", "dst": "CAT_AI", "relation": "belongs_to", "weight": 2.0},
    {"src": "B114", "dst": "CAT_AI", "relation": "belongs_to", "weight": 2.0}
]

