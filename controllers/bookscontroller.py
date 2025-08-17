from fastapi import APIRouter, HTTPException, status
from typing import List
from models.books import Book
from repositories.bookrepo import BookRepository
from repositories.chapterrepo import ChapterRepository
from utils.console import console


class BooksController:

    def __init__(self):
        self.router = APIRouter(prefix="/books", tags=["books"])
        self.setup_routes()
        self.booksRepo = BookRepository()
        self.chaptersRepo = ChapterRepository();
        self.console = console()

    def setup_routes(self):
        self.router.get("/")(self.index)  # Now resolves to /books/
        self.router.get("/{id}")(self.show)  # Now resolves to /books/{id}
        self.router.post("/")(self.store)  # Now resolves to /books/
        self.router.put("/{id}")(self.update)  # Now resolves to /books/{id}
        self.router.delete("/{id}")(self.destroy)  # Now resolves to /books/{id}

    def index(self) -> List[Book]:
        return self.booksRepo.get_all_books()

    def show(self, id: int) -> Book:
        book = self.booksRepo.get_book(id)
        if not book:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Book not found"
            )
        book.chapters = self.chaptersRepo.get_chapters_by_book_published(book.id)
        return book

    def store(self, book: Book) -> Book:
        self.console.dir(book.__dict__)
        new_book = self.booksRepo.add_book(book)
        return new_book

    def update(self, id: int, book: Book) -> Book:
        _book = self.booksRepo.get_book(id)
        if not _book:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Book not found"
            )

        # Update fields except 'id'
        for field in book.__dict__:
            if field != "id":
                setattr(_book, field, getattr(book, field))

        return _book

    def destroy(self, id: int) -> Book:
        book = self.booksRepo.get_book(id)
        if not book:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Book not found"
            )

        self.books.remove(book)
        return book
