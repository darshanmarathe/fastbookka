from fastapi import APIRouter, HTTPException, status
from typing import List
from models.chapters import Chapter
from repositories.chapterrepo import ChapterRepository


class ChaptersController:
    def __init__(self):
        self.router = APIRouter(prefix="/books/{book_id}/chapters", tags=["chapters"])
        self.setup_routes()
        self.chaptersRepo = ChapterRepository()

    def setup_routes(self):
        self.router.get("/")(self.index)
        self.router.get("/{id}")(self.show)
        self.router.post("/")(self.store)
        self.router.put("/{id}")(self.update)
        self.router.delete("/{id}")(self.destroy)

    def index(self, book_id: int) -> List[Chapter]:
        chapters = self.chaptersRepo.get_chapters_by_book(book_id)
        return chapters

    def show(self, book_id: int, id: int) -> Chapter:
        chapter = self.chaptersRepo.get_chapter(id)
        if not chapter or chapter.book_id != book_id:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Chapter not found"
            )
        return chapter

    def store(self, book_id: int, chapter: Chapter) -> Chapter:
        chapter.book_id = book_id
        new_chapter = self.chaptersRepo.add_chapter(chapter)
        return new_chapter

    def update(self, book_id: int, id: int, chapter: Chapter) -> Chapter:
        existing = self.chaptersRepo.get_chapter(id)
        if not existing or existing.book_id != book_id:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Chapter not found"
            )
        chapter.book_id = book_id
        updated = self.chaptersRepo.update_chapter(id, chapter)
        if not updated:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Update failed"
            )
        return self.chaptersRepo.get_chapter(id)

    def destroy(self, book_id: int, id: int) -> Chapter:
        chapter = self.chaptersRepo.get_chapter(id)
        if not chapter or chapter.book_id != book_id:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Chapter not found"
            )
        self.chaptersRepo.delete_chapter(id)
        return chapter
