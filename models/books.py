from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel
from .chapters import Chapter


class Book(BaseModel):
    id: int
    title: str
    imdb_id: Optional[str] = None
    description: Optional[str] = None
    finalPrice: Optional[float] = None
    prev_book_id: Optional[int] = None
    auther_id: Optional[int] = None
    status: Optional[int] = None
    published_date: Optional[datetime] = None
    chapters: List[Chapter] = []
