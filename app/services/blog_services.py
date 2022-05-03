from fastapi import Depends
from typing import Optional, List

from app.repositories import BlogRepository
from database.models.blog import TagUpdate, TagCreate, TagRead, Tag


class BlogServices:
    def __init__(self, blog_repository: BlogRepository = Depends(BlogRepository)):
        self.blog_repository = blog_repository

    def get_all(
        self,
        skip: Optional[int] = 0,
        limit: Optional[int] = 100,
        search: Optional[str] = None,
    ) -> List[Tag]:
        query = self.blog_repository.get_all(skip, limit, search)
        return query

    def get(self, tag_id: int) -> Tag:
        tag = self.blog_repository.get(tag_id)
        return tag

    def get_by_slug(self, slug: str) -> Tag:
        tag = self.blog_repository.get_by_slug(slug)
        return tag

    def update(self, tag: TagUpdate, slug: str) -> Tag:
        tag_in_db = self.blog_repository.get_by_slug(slug)
        return self.blog_repository.update(tag, tag_in_db.id)

    def create(self, tag: TagCreate) -> Tag:
        return self.blog_repository.create(tag)

    def delete(self, slug: str):
        tag_in_db = self.blog_repository.get_by_slug(slug)
        return self.blog_repository.delete(tag_in_db.id)
