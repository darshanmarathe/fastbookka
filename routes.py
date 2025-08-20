from controllers.bookscontroller import BooksController
from controllers.chapterscontroller import ChaptersController
from controllers.usercontroller import UserController


def create_routes(app):
    books_controller = BooksController()
    chapters_controller = ChaptersController()
    users_controller = UserController()
    app.include_router(books_controller.router)
    app.include_router(chapters_controller.router)
    app.include_router(users_controller.router)
