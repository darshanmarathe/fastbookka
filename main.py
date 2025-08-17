"""Entrypoint for the Application"""

from fastapi import FastAPI
from routes import create_routes
from utils.console import console


app = FastAPI(title="My fast API", description="this is a cool api")

create_routes(app)


@app.get("/")
def Index():
    return {"message": "Bookka API"}


console().clear()
print("Api is going to start")
