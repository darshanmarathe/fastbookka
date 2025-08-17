# generate books repository with for sqlite database
# use the model defined in models/books.py

import sqlite3
from typing import List, Optional
from models.books import Book
from utils.env import ENV


class BookRepository:
    def __init__(self, db_path: str = ENV.db_url()):
        self.conn = sqlite3.connect(db_path, check_same_thread=False)
        self.create_table()

    def create_table(self):
        cursor = self.conn.cursor()
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS books (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                imdb_id TEXT,
                description TEXT,
                finalPrice REAL,
                prev_book_id INTEGER,
                auther_id INTEGER,
                status INTEGER,
                published_date TEXT
            )
            """
        )
        self.conn.commit()

    def add_book(self, book: Book) -> Book:
        cursor = self.conn.cursor()
        cursor.execute(
            """
            INSERT INTO books (title, imdb_id, description, finalPrice, prev_book_id, auther_id, status, published_date)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """,
            (
                book.title,
                book.imdb_id,
                book.description,
                book.finalPrice,
                book.prev_book_id,
                book.auther_id,
                book.status,
                book.published_date.isoformat() if book.published_date else None,
            ),
        )
        self.conn.commit()
        book.id = cursor.lastrowid
        return book

    def get_book(self, book_id: int) -> Optional[Book]:
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM books WHERE id = ?", (book_id,))
        row = cursor.fetchone()
        if row:
            return Book(
                id=row[0],
                title=row[1],
                imdb_id=row[2],
                description=row[3],
                finalPrice=row[4],
                prev_book_id=row[5],
                auther_id=row[6],
                status=row[7],
                published_date=row[8],
            )
        return None

    def get_all_books(self) -> List[Book]:
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM books")
        rows = cursor.fetchall()
        return [
            Book(
                id=row[0],
                title=row[1],
                imdb_id=row[2],
                description=row[3],
                finalPrice=row[4],
                prev_book_id=row[5],
                auther_id=row[6],
                status=row[7],
                published_date=row[8],
            )
            for row in rows
        ]

    def update_book(self, book_id: int, book: Book) -> bool:
        cursor = self.conn.cursor()
        cursor.execute(
            """
            UPDATE books SET
                title = ?,
                imdb_id = ?,
                description = ?,
                finalPrice = ?,
                prev_book_id = ?,
                auther_id = ?,
                status = ?,
                published_date = ?
            WHERE id = ?
        """,
            (
                book.title,
                book.imdb_id,
                book.description,
                book.finalPrice,
                book.prev_book_id,
                book.auther_id,
                book.status,
                book.published_date.isoformat() if book.published_date else None,
                book_id,
            ),
        )
        self.conn.commit()
        return cursor.rowcount > 0

    def delete_book(self, book_id: int) -> bool:
        cursor = self.conn.cursor()
        cursor.execute("DELETE FROM books WHERE id = ?", (book_id,))
        self.conn.commit()
        return cursor.rowcount > 0
