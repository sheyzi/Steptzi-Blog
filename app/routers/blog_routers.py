from typing import List
from fastapi import Depends, Query
from fastapi_utils.inferring_router import InferringRouter
from fastapi_utils.cbv import cbv

from app.services import TagServices
from database.models.blog import TagCreate, TagUpdate, TagRead
from database.models.users import UserRead
from config.dependencies import get_active_user, get_admin_user


blog_router = InferringRouter()


@cbv(blog_router)
class BlogRouter:
    def __init__(self, tag_service: TagServices = Depends(TagServices)) -> None:
        self.tag_service = tag_service

    @blog_router.post("/tags", response_model=TagRead)
    def create_tag(
        self, tag: TagCreate, admin_user: UserRead = Depends(get_admin_user)
    ) -> TagRead:
        """
        Create a new tag
        """
        return self.tag_service.create(tag)

    @blog_router.get("/tags", response_model=List[TagRead])
    def get_all_tags(
        self, skip: int = 0, limit: int = Query(100, le=100), search: str = None
    ) -> List[TagRead]:
        """
        Get all tags
        """
        return self.tag_service.get_all(skip, limit, search)

    @blog_router.get("/tags/{slug}", response_model=TagRead)
    def get_tag_by_slug(self, slug: str) -> TagRead:
        """
        Get a tag by slug
        """
        return self.tag_service.get_by_slug(slug)

    @blog_router.put("/tags/{slug}", response_model=TagRead)
    def update_tag(
        self, tag: TagUpdate, slug: str, admin_user: UserRead = Depends(get_admin_user)
    ) -> TagRead:
        """
        Update a tag
        """
        return self.tag_service.update(tag, slug)

    @blog_router.delete("/tags/{slug}")
    def delete_tag(self, slug: str, admin_user: UserRead = Depends(get_admin_user)):
        """
        Delete a tag
        """
        return self.tag_service.delete(slug)
