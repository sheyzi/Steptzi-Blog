from datetime import datetime
from pydantic import BaseModel
from typing import List, Optional, TYPE_CHECKING


class UserBase(BaseModel):
    """
    Base class for User model
    """

    username: str
    email: str

    class Config:
        schema_extra = {"example": {"username": "sheyzi", "email": "email"}}


class UserCreate(UserBase):
    """
    Model for creating a user
    """

    password: str
    confirm_password: str

    class Config:
        schema_extra = {
            "example": {
                "username": "sheyzi",
                "email": "gistkiosk@gmail.com",
                "password": "password",
                "confirm_password": "password",
            }
        }


class UserUpdate(UserBase):
    """
    Model for updating a user
    """

    username: Optional[str] = None
    email: Optional[str] = None


class UserRead(UserBase):
    """
    Model for reading a user
    """

    id: int
    is_active: bool
    is_verified: bool
    is_admin: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "id": 1,
                "username": "sheyzi",
                "email": "gistkiosk@gmail.com",
                "is_active": True,
                "is_verified": True,
                "is_admin": False,
                "created_at": "2020-01-01T00:00:00",
                "updated_at": "2020-01-01T00:00:00",
            }
        }


class UserReadWithPosts(UserRead):
    """
    Model for reading a user with posts
    """

    posts: List["PostRead"]

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "id": 1,
                "username": "sheyzi",
                "email": "gistkiosk@gmail.com",
                "is_active": True,
                "is_verified": True,
                "is_admin": False,
                "created_at": "2020-01-01T00:00:00",
                "updated_at": "2020-01-01T00:00:00",
                "posts": [
                    {
                        "id": 1,
                        "title": "Post 1",
                        "slug": "post-1",
                        "excerpt": "This is the first post",
                        "content": "This is the first post",
                        "feature_image": "https://picsum.photos/id/1/200/300",
                        "is_published": True,
                        "is_featured": True,
                        "created_at": "2020-01-01T00:00:00",
                        "updated_at": "2020-01-01T00:00:00",
                    }
                ],
            }
        }


from .blog_schemas import PostRead

UserReadWithPosts.update_forward_refs()
