from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from models.books import Book


class Books_controller:

    def __init__(self):
        self.router = APIRouter(prefix="/books", tags=["books"])
        self.setup_routes()
        self.books: List[Book] = []

    def setup_routes(self):
        self.router.get("/books")(self.index)
        self.router.get("/books/{id}")(self.show)
        self.router.post("/books")(self.store)
        self.router.put("/books/{id}")(self.update)
        self.router.delete("/books/{id}")(self.destroy)

    def index(self) -> List[Book]:
        return self.books

    def show(self, id: int) -> Book:
        """
        Get a book by id
        """
        book = next((i for i in self.books if i.id == id), None)
        if not book:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")
        return book

    def store(self, book: Book) -> Book:
        new_book = Book(id=len(self.books) + 1, title=book.title)
        self.books.append(new_book)
        return new_book

    def update(self, id: int, book: Book) -> Book:
        _book = next((i for i in self.books if i.id == id), None)
        if not _book:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")

        for field, value in book.items():
            setattr(_book, field, value)
        
        return _book


    def destroy(self, id: int) -> Book:
        book = next((i for i in self.books if i.id == id), None)
        if not book:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")
        
        self.books.remove(book)
        return book
