from datetime import datetime
from pydantic import BaseModel


class Book(BaseModel):
    id: int
    title: str
    imdb_id: str
    description: str
    finalPrice: float
    prev_book_id: int
    auther_id: int
    status: int
    published_date: datetime
