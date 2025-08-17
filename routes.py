from controllers.bookscontroller import BooksController
from controllers.chapterscontroller import ChaptersController


def create_routes(app):
    books_controller = BooksController()
    chapters_controller = ChaptersController()
    app.include_router(books_controller.router)
    app.include_router(chapters_controller.router)
