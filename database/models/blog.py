import random
from sqlalchemy import (
    Boolean,
    Column,
    String,
    Integer,
    DateTime,
    ForeignKey,
    Table,
    Text,
    event,
    func,
)
from sqlalchemy.orm import relationship
from slugify import slugify

from database.session import Base


def get_slug(title):
    return f"{slugify(title)}-{random.randint(100000, 999999)}"


TagPost = Table(
    "tag_post",
    Base.metadata,
    Column("tag_id", Integer, ForeignKey("tags.id"), primary_key=True),
    Column("post_id", Integer, ForeignKey("posts.id"), primary_key=True),
)


class Tag(Base):
    __tablename__ = "tags"
    id = Column(Integer, primary_key=True)
    title = Column(String(255), unique=True)
    slug = Column(String(255), unique=True, nullable=True)
    excerpt = Column(String(500), nullable=True, default=None)
    description = Column(Text, nullable=True, default=None)
    cover_image = Column(String(500), nullable=True, default=None)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    posts = relationship("Post", secondary=TagPost, back_populates="tags")

    @staticmethod
    def generate_slug(target, value, oldvalue, initiator):
        if value and (not target.slug):
            target.slug = get_slug(value)

    def __repr__(self):
        return f"<Tag(name='{self.title}')>"


class Post(Base):
    __tablename__ = "posts"
    id = Column(Integer, primary_key=True)
    title = Column(String(255))
    slug = Column(String(255), unique=True, nullable=True)
    excerpt = Column(String(500), nullable=True, default=None)
    content = Column(String(5000))
    featured_image = Column(String(500), nullable=True, default=None)
    is_featured = Column(Boolean, default=False)
    is_published = Column(Boolean, default=False)
    author_id = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    author = relationship("User", backref="posts")
    tags = relationship("Tag", secondary=TagPost, back_populates="posts")

    @staticmethod
    def generate_slug(target, value, oldvalue, initiator):
        if value and (not target.slug):
            target.slug = get_slug(value)

    def __repr__(self):
        return f"<Post(title='{self.title}')>"


event.listen(Tag.title, "set", Tag.generate_slug)
event.listen(Post.title, "set", Post.generate_slug)
