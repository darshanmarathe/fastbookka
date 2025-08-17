from datetime import datetime
from pydantic import BaseModel
from enum import Enum


class ContentType(str, Enum):
    Text = "Text"
    Markdown = "Markdown"
    HTML = "HTML"


class ChapterStatus(str, Enum):
    Draft = "Draft"
    Published = "Published"
    Archived = "Archived"


class Chapter(BaseModel):
    id: int
    book_id: int
    chapter_title: str
    content: str
    content_type: ContentType  # Only Text, Markdown, HTML allowed
    chapter_price: float
    publishDate: datetime
    status: ChapterStatus  # Only Draft, Published, Archived
