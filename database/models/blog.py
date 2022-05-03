from datetime import datetime
from random import randint
from pydantic import root_validator
from sqlalchemy import Column, String
from sqlmodel import SQLModel, Field
from typing import List, Optional
from slugify import slugify


class TagBase(SQLModel):
    title: str
    excerpt: Optional[str] = Field(nullable=True, default=None)
    description: Optional[str] = Field(nullable=True, default=None)
    cover_image: Optional[str] = Field(nullable=True, default=None)


class TagCreate(TagBase):
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
    title: Optional[str] = None
    excerpt: Optional[str] = None
    description: Optional[str] = None
    cover_image: Optional[str] = None


class Tag(TagBase, table=True):
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
    id: int
    slug: str
    created_at: datetime
    updated_at: datetime
