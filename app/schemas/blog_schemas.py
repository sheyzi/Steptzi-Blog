from datetime import datetime
from pydantic import BaseModel
from typing import TYPE_CHECKING, List, Optional


class TagBase(BaseModel):
    """
    Base class for Tag model
    """

    title: str
    excerpt: Optional[str] = None
    description: Optional[str] = None
    cover_image: Optional[str] = None

    class Config:
        schema_extra = {
            "example": {
                "title": "programming",
                "excerpt": "This is programming excerpt",
                "description": "This is programming description",
                "cover_image": "https://www.example.com/programming.jpg",
            }
        }


class TagCreate(TagBase):
    """
    Model for creating a tag
    """

    pass


class TagUpdate(TagBase):
    """
    Model for updating a tag
    """

    title: Optional[str] = None
    excerpt: Optional[str] = None
    description: Optional[str] = None
    cover_image: Optional[str] = None


class TagRead(TagBase):
    """
    Model for reading a tag
    """

    id: int
    slug: str
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "id": 1,
                "title": "programming",
                "excerpt": "This is programming excerpt",
                "description": "This is programming description",
                "cover_image": "https://www.example.com/programming.jpg",
                "created_at": "2020-01-01T00:00:00",
                "updated_at": "2020-01-01T00:00:00",
            }
        }


class TagReadWithPosts(TagRead):
    """
    Model for reading a tag with posts
    """

    posts: List["PostRead"]

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "posts": [
                    {
                        "id": 1,
                        "title": "Post 1",
                        "slug": "post-1",
                        "excerpt": "This is the first post",
                        "content": "This is the first post",
                        "featured_image": "https://picsum.photos/id/1/200/300",
                        "is_published": True,
                        "is_featured": True,
                        "created_at": "2020-01-01T00:00:00",
                        "updated_at": "2020-01-01T00:00:00",
                    }
                ],
            }
        }


class PostBase(BaseModel):
    """
    Base class for Post model
    """

    title: str
    excerpt: Optional[str] = None
    content: Optional[str] = None
    featured_image: Optional[str] = None
    is_published: Optional[bool] = False
    is_featured: Optional[bool] = False

    class Config:
        schema_extra = {
            "example": {
                "title": "Post 1",
                "excerpt": "This is the first post",
                "content": "This is the first post",
                "featured_image": "https://picsum.photos/id/1/200/300",
                "is_published": True,
                "is_featured": True,
            }
        }


class PostCreate(PostBase):
    """
    Model for creating a post
    """

    tags: List[int]

    class Config:
        schema_extra = {
            "example": {
                "title": "Post 1",
                "excerpt": "This is the first post",
                "content": "This is the first post",
                "featured_image": "https://picsum.photos/id/1/200/300",
                "is_published": True,
                "is_featured": True,
                "tags": [1, 2],
            }
        }


class PostUpdate(PostBase):
    """
    Model for updating a post
    """

    title: Optional[str] = None
    excerpt: Optional[str] = None
    content: Optional[str] = None
    featured_image: Optional[str] = None
    is_published: Optional[bool] = None
    is_featured: Optional[bool] = None
    tags: Optional[List[int]] = None

    class Config:
        schema_extra = {
            "example": {
                "title": "Post 1",
                "excerpt": "This is the first post",
                "content": "This is the first post",
                "featured_image": "https://picsum.photos/id/1/200/300",
                "is_published": True,
                "is_featured": True,
                "tags": [1, 2],
            }
        }


class PostRead(PostBase):
    """
    Model for reading a post
    """

    id: int
    slug: str
    author: "UserRead"
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "id": 1,
                "title": "Post 1",
                "slug": "post-1",
                "excerpt": "This is the first post",
                "content": "This is the first post",
                "featured_image": "https://picsum.photos/id/1/200/300",
                "is_published": True,
                "is_featured": True,
                "author": {
                    "id": 1,
                    "username": "sheyzi",
                    "email": "gistkiosk@gmail.com",
                    "is_active": True,
                    "is_verified": True,
                    "is_admin": False,
                    "created_at": "2020-01-01T00:00:00",
                    "updated_at": "2020-01-01T00:00:00",
                },
                "created_at": "2020-01-01T00:00:00",
                "updated_at": "2020-01-01T00:00:00",
            }
        }


class PostReadWithTags(PostRead):
    """
    Model for reading a post with tags
    """

    tags: List["TagRead"]

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "id": 1,
                "title": "Post 1",
                "slug": "post-1",
                "excerpt": "This is the first post",
                "content": "This is the first post",
                "featured_image": "https://picsum.photos/id/1/200/300",
                "is_published": True,
                "is_featured": True,
                "author": {
                    "id": 1,
                    "username": "sheyzi",
                    "email": "gistkiosk@gmail.com",
                    "is_active": True,
                    "is_verified": True,
                    "is_admin": False,
                    "created_at": "2020-01-01T00:00:00",
                    "updated_at": "2020-01-01T00:00:00",
                },
                "tags": {
                    "id": 1,
                    "title": "programming",
                    "excerpt": "This is programming excerpt",
                    "description": "This is programming description",
                    "cover_image": "https://www.example.com/programming.jpg",
                    "created_at": "2020-01-01T00:00:00",
                    "updated_at": "2020-01-01T00:00:00",
                },
                "created_at": "2020-01-01T00:00:00",
                "updated_at": "2020-01-01T00:00:00",
            }
        }


from .user_schemas import UserRead

PostRead.update_forward_refs()
TagReadWithPosts.update_forward_refs()
PostReadWithTags.update_forward_refs()
