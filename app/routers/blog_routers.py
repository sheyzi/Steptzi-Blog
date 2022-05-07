from typing import List

from fastapi import Depends, Query, HTTPException, status
from fastapi_utils.inferring_router import InferringRouter
from fastapi_utils.cbv import cbv
from app.schemas.blog_schemas import (
    CommentCreate,
    CommentRead,
    PostReadWithTags,
    PostUpdate,
)

from app.services import TagService
from app.services.blog_services import PostService, CommentService
from app.schemas import (
    PostCreate,
    PostRead,
    TagCreate,
    TagUpdate,
    TagRead,
    TagReadWithPosts,
)
from app.schemas import UserRead
from config.dependencies import get_active_user, get_admin_user


blog_router = InferringRouter()


@cbv(blog_router)
class TagRouter:
    def __init__(self, tag_service: TagService = Depends(TagService)) -> None:
        self.tag_service = tag_service

    @blog_router.post("/tags", response_model=TagRead)
    def create(
        self, tag: TagCreate, admin_user: UserRead = Depends(get_admin_user)
    ) -> TagRead:
        """
        Create a new tag
        """
        return self.tag_service.create(tag)

    @blog_router.get("/tags", response_model=List[TagRead])
    def get_all(
        self, skip: int = 0, limit: int = Query(100, le=100), search: str = None
    ) -> List[TagRead]:
        """
        Get all tags
        """
        return self.tag_service.get_all(skip, limit, search)

    @blog_router.get("/tags/{slug}", response_model=TagReadWithPosts)
    def get_by_slug(self, slug: str) -> TagRead:
        """
        Get a tag by slug
        """
        return self.tag_service.get_by_slug(slug)

    @blog_router.put("/tags/{slug}", response_model=TagRead)
    def update(
        self, tag: TagUpdate, slug: str, admin_user: UserRead = Depends(get_admin_user)
    ) -> TagRead:
        """
        Update a tag
        """
        return self.tag_service.update(tag, slug)

    @blog_router.delete("/tags/{slug}")
    def delete(self, slug: str, admin_user: UserRead = Depends(get_admin_user)):
        """
        Delete a tag
        """
        return self.tag_service.delete(slug)


@cbv(blog_router)
class PostRouter:
    def __init__(
        self,
        post_service: PostService = Depends(PostService),
        comment_service: CommentService = Depends(CommentService),
    ) -> None:
        self.post_service = post_service
        self.comment_service = comment_service

    @blog_router.post("/posts", response_model=PostRead)
    def create_posts(
        self, post: PostCreate, current_user: UserRead = Depends(get_active_user)
    ) -> PostRead:
        """
        Create a new post
        """
        return self.post_service.create(post, current_user.id)

    @blog_router.put("/posts/{slug}", response_model=PostRead)
    def update_posts(
        self,
        post: PostUpdate,
        slug: str,
        current_user: UserRead = Depends(get_active_user),
    ) -> PostRead:
        """
        Update a post
        """
        post_in_db = self.post_service.get_by_slug(slug)
        if current_user.id != post_in_db.author_id and not current_user.is_admin:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You can only update your own posts",
            )
        return self.post_service.update(post, slug)

    @blog_router.get("/posts", response_model=List[PostRead])
    def get_all_posts(
        self,
        skip: int = 0,
        limit: int = Query(100, le=100),
        search: str = None,
    ) -> List[PostRead]:
        """
        Get all posts
        """
        return self.post_service.get_all(skip, limit, search)

    @blog_router.get("/posts/featured", response_model=List[PostRead])
    def get_featured_posts(
        self,
        skip: int = 0,
        limit: int = Query(100, le=100),
    ) -> List[PostRead]:
        """
        Get all featured posts
        """
        return self.post_service.get_featured(skip, limit)

    @blog_router.get("/posts/{slug}", response_model=PostReadWithTags)
    def get_post_by_slug(self, slug: str) -> PostReadWithTags:
        """
        Get a post by slug
        """
        return self.post_service.get_by_slug(slug)

    @blog_router.delete("/posts/{slug}")
    def delete_post(
        self, slug: str, get_active_user: UserRead = Depends(get_active_user)
    ):
        """
        Delete a post
        """
        post_in_db = self.post_service.get_by_slug(slug)
        if get_active_user.id != post_in_db.author_id and not get_active_user.is_admin:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You can only delete your own posts",
            )
        return self.post_service.delete(slug)


@cbv(blog_router)
class CommentRouter:
    def __init__(
        self, comment_service: CommentService = Depends(CommentService)
    ) -> None:
        self.comment_service = comment_service

    @blog_router.post("/comments", response_model=CommentRead)
    def create_comments(
        self,
        comment: CommentCreate,
        current_user: UserRead = Depends(get_active_user),
    ) -> CommentRead:
        """
        Create a new comment
        """
        return self.comment_service.create(comment, current_user.id)

    @blog_router.get("/comments", response_model=List[CommentRead])
    def get_all_comments(
        self,
        skip: int = 0,
        limit: int = Query(100, le=100),
        search: str = None,
        admin_user: UserRead = Depends(get_admin_user),
    ) -> List[CommentRead]:
        """
        Get all comments
        """
        return self.comment_service.get_all(skip, limit, search)

    @blog_router.get("/comments/{id}", response_model=CommentRead)
    def get_comment_by_id(
        self, id: int, admin_user: UserRead = Depends(get_admin_user)
    ) -> CommentRead:
        """
        Get a comment by id
        """
        return self.comment_service.get(id)

    @blog_router.delete("/comments/{id}")
    def delete_comment(self, id: int, active_user: UserRead = Depends(get_active_user)):
        """
        Delete a comment
        """
        comment_in_db = self.comment_service.get(id)
        if active_user.id != comment_in_db.author_id and not active_user.is_admin:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You can only delete your own comments",
            )
        return self.comment_service.delete(id)
