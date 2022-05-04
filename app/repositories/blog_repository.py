from datetime import datetime
from typing import List, Optional, Union
from fastapi import Depends, HTTPException, status
from app.schemas.blog_schemas import CommentCreate

from database.models import Tag, Post, Comment
from database.session import Session, get_db
from app.schemas import TagCreate, TagUpdate, PostCreate, PostUpdate


class TagRepository:
    def __init__(self, db: Session = Depends(get_db)):
        self.db = db

    def get_all(
        self,
        skip: Optional[int] = 0,
        limit: Optional[int] = 100,
        search: Optional[str] = None,
    ) -> List[Tag]:
        """
        :param skip: Number of items to skip
        :param limit: Max number of items to return
        :param search: Search term
        :return: List of tags

        Returns all tags.
        """
        query = self.db.query(Tag)
        if search:
            query = query.filter(Tag.title.contains(search))
        query = query.offset(skip).limit(limit)
        return query.all()

    def get(self, tag_id: int) -> Tag:
        """
        :param tag_id: ID of tag to return
        :return: Tag object

        Returns a tag by ID.
        """
        tag = self.db.query(Tag).get(tag_id)
        if tag is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Tag not found"
            )
        return tag

    def get_or_none(self, tag_id: int) -> Union[Tag, None]:
        """
        :param tag_id: ID of tag to return
        :return: Tag object or None

        Returns a tag by ID.
        """
        tag = self.db.query(Tag).get(tag_id)
        return tag

    def get_by_slug(self, slug: str) -> Tag:
        """
        :param slug: Slug of tag to return
        :return: Tag object

        Returns a tag by slug.
        """
        tag = self.db.query(Tag).filter(Tag.slug == slug).first()
        if tag is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Tag not found"
            )
        return tag

    def get_by_slug_or_none(self, slug: str) -> Union[Tag, None]:
        """
        :param slug: Slug of tag to return
        :return: Tag object or None

        Returns a tag by slug.
        """
        tag = self.db.query(Tag).filter(Tag.slug == slug).first()
        return tag

    def create(self, tag: TagCreate) -> Tag:
        """
        :param tag: Tag object to create
        :return: Tag object

        Creates a new tag.
        """
        tag = Tag(**tag.dict())
        self.db.add(tag)
        self.db.commit()
        self.db.refresh(tag)
        return tag

    def update(self, tag: TagUpdate, tag_id: int) -> Tag:
        """
        :param tag: Tag object to update
        :param tag_id: ID of tag to update

        Updates a tag.
        """
        tag_in_db: Tag = self.get(tag_id)
        for key, value in tag.dict(exclude_unset=True).items():
            setattr(tag_in_db, key, value)

        tag_in_db.updated_at = datetime.utcnow()
        self.db.commit()
        self.db.refresh(tag_in_db)
        return tag_in_db

    def delete(self, tag_id: int):
        """
        :param tag_id: ID of tag to delete

        Deletes a tag.
        """
        tag = self.get(tag_id)
        self.db.delete(tag)
        self.db.commit()
        return {"message": "Tag deleted"}


class PostRepository:
    def __init__(
        self,
        db: Session = Depends(get_db),
        tag_repository: TagRepository = Depends(TagRepository),
    ):
        self.db = db
        self.tag_repository = tag_repository

    def get_all(
        self,
        skip: Optional[int] = 0,
        limit: Optional[int] = 100,
        search: Optional[str] = None,
    ) -> List[Post]:
        """
        :param skip: Number of items to skip
        :param limit: Max number of items to return
        :param search: Search term
        :return: List of posts

        Returns all posts.
        """
        query = self.db.query(Post)
        if search:
            query = query.filter(Post.title.contains(search))
        query = query.offset(skip).limit(limit)
        return query.all()

    def get(self, post_id: int) -> Post:
        """
        :param post_id: ID of post to return
        :return: Post object

        Returns a post by ID.
        """
        post = self.db.query(Post).get(post_id)
        if post is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Post not found"
            )
        return post

    def get_or_none(self, post_id: int) -> Union[Post, None]:
        """
        :param post_id: ID of post to return
        :return: Post object or None

        Returns a post by ID.
        """
        post = self.db.query(Post).get(post_id)
        return post

    def get_by_slug(self, slug: str) -> Post:
        """
        :param slug: Slug of post to return
        :return: Post object

        Returns a post by slug.
        """
        post = self.db.query(Post).filter(Post.slug == slug).first()
        if post is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Post not found"
            )
        return post

    def get_by_slug_or_none(self, slug: str) -> Union[Post, None]:
        """
        :param slug: Slug of post to return
        :return: Post object or None

        Returns a post by slug.
        """
        post = self.db.query(Post).filter(Post.slug == slug).first()
        return post

    def create(self, post: PostCreate, author_id: int) -> Post:
        """
        :param post: Post object to create
        :param author_id: ID of author to associate with post
        :return: Post object

        Creates a new post.
        """
        post_in_db = Post(**post.dict(exclude={"tags"}))
        post_in_db.author_id = author_id
        for tag_id in post.tags:
            tag = self.tag_repository.get_or_none(tag_id)
            if tag is None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Tag with id {tag_id} was not found",
                )
            post_in_db.tags.append(tag)

        self.db.add(post_in_db)
        self.db.commit()
        self.db.refresh(post_in_db)
        return post_in_db

    def update(self, post: PostUpdate, post_id: int) -> Post:
        """
        :param post: Post object to update
        :param post_id: ID of post to update

        Updates a post.
        """
        post_in_db: Post = self.get(post_id)
        for key, value in post.dict(exclude_unset=True, exclude={"tags"}).items():
            setattr(post_in_db, key, value)

        if post.tags:
            post_in_db.tags = []
            for tag_id in post.tags:
                tag = self.tag_repository.get_or_none(tag_id)
                if tag is None:
                    raise HTTPException(
                        status_code=status.HTTP_404_NOT_FOUND,
                        detail=f"Tag with id {tag_id} was not found",
                    )
                post_in_db.tags.append(tag)

        post_in_db.updated_at = datetime.utcnow()
        self.db.commit()
        self.db.refresh(post_in_db)
        return post_in_db

    def delete(self, post_id: int):
        """
        :param post_id: ID of post to delete

        Deletes a post.
        """
        post = self.get(post_id)
        self.db.delete(post)
        self.db.commit()
        return {"message": "Post deleted"}


class CommentRepository:
    def __init__(
        self,
        db: Session = Depends(get_db),
        post_repository: PostRepository = Depends(PostRepository),
    ) -> None:
        self.db = db
        self.post_repository = post_repository

    def get_all(
        self,
        skip: Optional[int] = 0,
        limit: Optional[int] = 100,
        search: Optional[str] = None,
    ) -> List[Comment]:
        """
        :param skip: Number of items to skip
        :param limit: Max number of items to return
        :param search: Search term
        :return: List of comments

        Returns all comments.
        """
        query = self.db.query(Comment).filter(Comment.parent_id == None)
        if search:
            query = query.filter(Comment.body.contains(search))
        query = query.offset(skip).limit(limit)
        return query.all()

    def get(self, comment_id: int) -> Comment:
        """
        :param comment_id: ID of comment to return
        :return: Comment object

        Returns a comment by ID.
        """
        comment = self.db.query(Comment).get(comment_id)
        if comment is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Comment not found"
            )
        return comment

    def get_or_none(self, comment_id: int) -> Union[Comment, None]:
        """
        :param comment_id: ID of comment to return
        :return: Comment object or None

        Returns a comment by ID.
        """
        comment = self.db.query(Comment).get(comment_id)
        return comment

    def get_by_post_id(self, post_id: int) -> List[Comment]:
        """
        :param post_id: ID of post to return
        :return: List of Comment objects

        Returns all comments for a post.
        """
        post = self.post_repository.get(post_id)
        comments = self.db.query(Comment).filter(Comment.post_id == post_id)
        return comments.all()

    def create(self, comment: CommentCreate, author_id: int) -> Comment:
        """
        :param comment: Comment object to create
        :param author_id: ID of author to associate with comment
        :return: Comment object

        Creates a new comment.
        """
        if comment.parent_id:
            parent = self.get_or_none(comment.parent_id)
            if parent is None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Parent comment not found",
                )
        post = self.post_repository.get(comment.post_id)
        comment_in_db = Comment(**comment.dict())
        comment_in_db.author_id = author_id
        self.db.add(comment_in_db)
        self.db.commit()
        self.db.refresh(comment_in_db)
        return comment_in_db

    def delete(self, comment_id: int):
        """
        :param comment_id: ID of comment to delete

        Deletes a comment.
        """
        comment = self.get(comment_id)
        self.db.delete(comment)
        self.db.commit()
        return {"message": "Comment deleted"}
