"""Entrypoint for the Application"""

from fastapi import FastAPI

app = FastAPI(title="My fast API", description="this is a cool api")


@app.get("/hello")
def hello():
    """
    returns hello
    :return:
    """
    return "hello"


print("Api is going to start")
