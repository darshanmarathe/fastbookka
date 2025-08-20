import sqlite3
from typing import List, Optional
from models.user import User
from utils.env import ENV


class UserRepository:
    def __init__(self, db_path: str = ENV.db_url()):
        self.conn = sqlite3.connect(db_path, check_same_thread=False)
        self.conn.set_trace_callback(print)  # This will print all SQL queries
        self.create_table()

    def create_table(self):
        cursor = self.conn.cursor()
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL,
                email TEXT,
                dob TEXT,
                password TEXT NOT NULL,
                createdAt TEXT NOT NULL,
                lastLoggedin TEXT NULL
            )
        """
        )
        self.conn.commit()

    def add_user(self, user: User) -> User:
        cursor = self.conn.cursor()
        cursor.execute(
            """
            INSERT INTO users (
                username, email, dob, password, createdAt, lastLoggedin
            ) VALUES (?, ?, ?, ?, ?, ?)
        """,
            (
                user.username,
                user.email,
                user.dob.isoformat() if user.dob else None,
                user.password,
                user.createdAt.isoformat() if user.createdAt else None,
                user.lastLoggedin.isoformat() if user.lastLoggedin else None,
            ),
        )
        self.conn.commit()
        user.id = cursor.lastrowid
        return user

    def get_user(self, user_id: int) -> Optional[User]:
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
        row = cursor.fetchone()
        if row:
            return User(
                id=row[0],
                username=row[1],
                email=row[2],
                dob=row[3],
                password=row[4],
                createdAt=row[5],
                lastLoggedin=row[6],
            )
        return None

    def get_user_by_username(self, username: str) -> Optional[User]:
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
        row = cursor.fetchone()
        if row:
            return User(
                id=row[0],
                username=row[1],
                email=row[2],
                dob=row[3],
                password=row[4],
                createdAt=row[5],
                lastLoggedin=row[6],
            )
        return None

    def check_user_exists(self, username: str) -> bool:
        cursor = self.conn.cursor()
        cursor.execute("SELECT 1 FROM users WHERE username = ?", (username,))
        return cursor.fetchone() is not None

    def check_user_or_email_exists(self, name: str, email: str) -> bool:
        cursor = self.conn.cursor()
        cursor.execute(
            "SELECT 1 FROM users WHERE username = ? OR email = ?", (name, email)
        )
        return cursor.fetchone() is not None

    def get_all_users(self) -> List[User]:
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM users")
        rows = cursor.fetchall()
        return [
            User(
                id=row[0],
                username=row[1],
                email=row[2],
                dob=row[3],
                password=row[4],
                createdAt=row[5],
                lastLoggedin=row[6],
            )
            for row in rows
        ]

    def update_user(self, user_id: int, user: User) -> bool:
        cursor = self.conn.cursor()
        cursor.execute(
            """
            UPDATE users SET
                username = ?,
                email = ?,
                dob = ?,
                password = ?,
                createdAt = ?,
                lastLoggedin = ?
            WHERE id = ?
        """,
            (
                user.username,
                user.email,
                user.dob.isoformat() if user.dob else None,
                user.password,
                user.createdAt.isoformat(),
                user.lastLoggedin.isoformat(),
                user_id,
            ),
        )
        self.conn.commit()
        return cursor.rowcount > 0

    def delete_user(self, user_id: int) -> bool:
        cursor = self.conn.cursor()
        cursor.execute("DELETE FROM users WHERE id = ?", (user_id,))
        self.conn.commit()
        return cursor.rowcount > 0
