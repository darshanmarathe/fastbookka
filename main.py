"""Entrypoint for the Application"""

from fastapi import FastAPI
from models.user import User
from utils.console import console

app = FastAPI(title="My fast API", description="this is a cool api")

from controllers.books_controller import Books_controller

Books_controller()
console().clear()
print("Api is going to start")
