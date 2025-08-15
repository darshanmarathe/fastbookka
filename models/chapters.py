from pydantic import BaseModel


class Chapter(BaseModel):
    id: int
    book_id: int
    chapter_title: str
    content: str
    content_type: str
    chapter_price: float
    publishDate: datetime
    status: str
