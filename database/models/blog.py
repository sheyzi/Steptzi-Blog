from datetime import datetime
from random import randint
from pydantic import root_validator
from sqlalchemy import Column, String
from sqlmodel import Relationship, SQLModel, Field
from typing import List, Optional
from slugify import slugify

from database.models.users import User


class TagBase(SQLModel):
    """
    Base class for Tag model
    """

    title: str
    excerpt: Optional[str] = Field(nullable=True, default=None)
    description: Optional[str] = Field(nullable=True, default=None)
    cover_image: Optional[str] = Field(nullable=True, default=None)


class TagCreate(TagBase):
    """
    Model for creating a tag
    """

    pass

    class Config:

        schema_extra = {
            "example": {
                "title": "Python",
                "excerpt": "Python is a programming language",
                "description": "Python is a programming language",
                "cover_image": "https://www.python.org/static/opengraph-icon-200x200.png",
            }
        }


class TagUpdate(TagBase):
    """
    Model for updating a tag
    """

    title: Optional[str] = None
    excerpt: Optional[str] = None
    description: Optional[str] = None
    cover_image: Optional[str] = None


class Tag(TagBase, table=True):
    """
    Database representation for a tag
    """

    __tablename__ = "tags"
    id: Optional[int] = Field(default=None, nullable=True, primary_key=True)
    slug: Optional[str] = Field(sa_column=Column(String, unique=True))
    created_at: datetime = Field(default=datetime.utcnow(), nullable=False)
    updated_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)

    @root_validator
    def create_slug(cls, values):
        title = values.get("title")
        slugify_title = f"{slugify(title)}-{randint(100000, 999999)}"
        values["slug"] = slugify_title
        return values

    class Config:
        validate_assignment = True


class TagRead(TagBase):
    """
    Model for reading a tag
    """

    id: int
    slug: str
    created_at: datetime
    updated_at: datetime


class PostBase(SQLModel):
    """
    Base class for Post model
    """

    title: str
    excerpt: Optional[str] = Field(nullable=True, default=None)
    content: str
    featured_image: Optional[str] = Field(nullable=True, default=None)
    is_featured: Optional[bool] = Field(nullable=False, default=None)
    is_published: Optional[bool] = Field(nullable=False, default=None)


class PostCreate(PostBase):
    """
    Model for creating a post
    """

    class Config:

        schema_extra = {
            "example": {
                "title": "Sample post",
                "excerpt": "Sample post excerpt",
                "content": "Sample post content",
                "featured_image": "https://www.python.org/static/opengraph-icon-200x200.png",
                "is_featured": False,
                "is_published": True,
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
    is_featured: Optional[bool] = None
    is_published: Optional[bool] = None


class Post(PostBase, table=True):
    """
    Database representation for a post
    """

    __tablename__ = "posts"
    id: Optional[int] = Field(default=None, nullable=True, primary_key=True)
    author_id: int = Field(nullable=False, foreign_key="users.id")
    slug: Optional[str] = Field(sa_column=Column(String, unique=True))
    created_at: datetime = Field(default=datetime.utcnow(), nullable=False)
    updated_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)

    @root_validator
    def create_slug(cls, values):
        title = values.get("title")
        slugify_title = f"{slugify(title)}-{randint(100000, 999999)}"
        values["slug"] = slugify_title
        return values

    class Config:
        validate_assignment = True


class PostRead(PostBase):
    """
    Model for reading a post
    """

    id: int
    author_id: int
    slug: str
    created_at: datetime
    updated_at: datetime
