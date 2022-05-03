from typing import List
from fastapi import Depends, Query
from fastapi_utils.inferring_router import InferringRouter
from fastapi_utils.cbv import cbv

from app.services import BlogServices
from database.models.blog import TagCreate, TagUpdate, TagRead
from database.models.users import UserRead
from config.dependencies import get_active_user, get_admin_user


blog_router = InferringRouter()


@cbv(blog_router)
class BlogRouter:
    def __init__(self, blog_service: BlogServices = Depends(BlogServices)) -> None:
        self.blog_service = blog_service

    @blog_router.post("/tags", response_model=TagRead)
    def create(
        self, tag: TagCreate, admin_user: UserRead = Depends(get_admin_user)
    ) -> TagRead:
        """
        Create a new tag
        """
        return self.blog_service.create(tag)

    @blog_router.get("/tags", response_model=List[TagRead])
    def get_all(
        self, skip: int = 0, limit: int = Query(100, le=100), search: str = None
    ) -> List[TagRead]:
        """
        Get all tags
        """
        return self.blog_service.get_all(skip, limit, search)

    @blog_router.get("/tags/{slug}", response_model=TagRead)
    def get_by_slug(self, slug: str) -> TagRead:
        """
        Get a tag by slug
        """
        return self.blog_service.get_by_slug(slug)

    @blog_router.put("/tags/{slug}", response_model=TagRead)
    def update(
        self, tag: TagUpdate, slug: str, admin_user: UserRead = Depends(get_admin_user)
    ) -> TagRead:
        """
        Update a tag
        """
        return self.blog_service.update(tag, slug)

    @blog_router.delete("/tags/{slug}")
    def delete(self, slug: str, admin_user: UserRead = Depends(get_admin_user)):
        """
        Delete a tag
        """
        return self.blog_service.delete(slug)
