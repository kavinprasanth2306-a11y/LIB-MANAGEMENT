"""
Domain Entities and Pydantic Schemas for Library Book Management
"""

from typing import Optional, List
from pydantic import BaseModel, Field


class Book(BaseModel):
    id: int
    title: str
    author: str
    isbn: str
    year: int
    category: str
    total_copies: int = 3
    available_copies: int = 3
    borrow_count: int = 0
    tags: List[str] = []


class Student(BaseModel):
    id: str
    name: str
    role: str = "student"  # "student", "faculty", "vip"
    department: str = "Computer Science"
    active_borrows: List[int] = []


class BorrowRequest(BaseModel):
    book_id: int
    student_id: str
    is_vip: bool = False


class ReturnRequest(BaseModel):
    book_id: int
    student_id: str
    overdue_days: int = 0
    formula: Optional[str] = "days * 2"


class BookCreate(BaseModel):
    title: str
    author: str
    isbn: str
    year: int
    category: str
    total_copies: int = 3


class SearchQuery(BaseModel):
    query: str
    method: str = "sequential"  # "sequential", "binary_iterative", "binary_recursive", "interpolation"
    key_field: str = "id"       # "id", "isbn", "title"


class SortRequest(BaseModel):
    field: str = "title"        # "title", "year", "borrow_count", "available_copies"
    algorithm: str = "merge_sort" # "insertion_sort", "bubble_sort", "selection_sort", "merge_sort"
    ascending: bool = True

