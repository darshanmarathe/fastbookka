import sqlite3
from typing import List, Optional
from models.chapters import Chapter, ContentType, ChapterStatus
from utils.env import ENV


class ChapterRepository:
    def __init__(self, db_path: str = ENV.db_url()):
        self.conn = sqlite3.connect(db_path, check_same_thread=False)
        self.create_table()

    def create_table(self):
        cursor = self.conn.cursor()
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS chapters (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                book_id INTEGER NOT NULL,
                chapter_title TEXT NOT NULL,
                content TEXT,
                content_type TEXT,
                chapter_price REAL,
                publishDate TEXT,
                status TEXT,
                FOREIGN KEY(book_id) REFERENCES books(id)
            )
        """
        )
        self.conn.commit()

    def add_chapter(self, chapter: Chapter) -> Chapter:
        cursor = self.conn.cursor()
        cursor.execute(
            """
            INSERT INTO chapters (
                book_id, chapter_title, content, content_type, chapter_price, publishDate, status
            ) VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
            (
                chapter.book_id,
                chapter.chapter_title,
                chapter.content,
                chapter.content_type.value,
                chapter.chapter_price,
                chapter.publishDate.isoformat() if chapter.publishDate else None,
                chapter.status.value,
            ),
        )
        self.conn.commit()
        chapter.id = cursor.lastrowid
        return chapter

    def get_chapter(self, chapter_id: int) -> Optional[Chapter]:
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM chapters WHERE id = ?", (chapter_id,))
        row = cursor.fetchone()
        if row:
            return Chapter(
                id=row[0],
                book_id=row[1],
                chapter_title=row[2],
                content=row[3],
                content_type=ContentType(row[4]),
                chapter_price=row[5],
                publishDate=row[6],
                status=ChapterStatus(row[7]),
            )
        return None

    def get_chapters_by_book(self, book_id: int) -> List[Chapter]:
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM chapters WHERE book_id = ?", (book_id,))
        rows = cursor.fetchall()
        return [
            Chapter(
                id=row[0],
                book_id=row[1],
                chapter_title=row[2],
                content=row[3],
                content_type=ContentType(row[4]),
                chapter_price=row[5],
                publishDate=row[6],
                status=ChapterStatus(row[7]),
            )
            for row in rows
        ]

    def update_chapter(self, chapter_id: int, chapter: Chapter) -> bool:
        cursor = self.conn.cursor()
        cursor.execute(
            """
            UPDATE chapters SET
                book_id = ?,
                chapter_title = ?,
                content = ?,
                content_type = ?,
                chapter_price = ?,
                publishDate = ?,
                status = ?
            WHERE id = ?
        """,
            (
                chapter.book_id,
                chapter.chapter_title,
                chapter.content,
                chapter.content_type.value,
                chapter.chapter_price,
                chapter.publishDate.isoformat() if chapter.publishDate else None,
                chapter.status.value,
                chapter_id,
            ),
        )
        self.conn.commit()
        return cursor.rowcount > 0

    def delete_chapter(self, chapter_id: int) -> bool:
        cursor = self.conn.cursor()
        cursor.execute("DELETE FROM chapters WHERE id = ?", (chapter_id,))
        self.conn.commit()
        return cursor.rowcount > 0
