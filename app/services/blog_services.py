from typing import Optional, List

from fastapi import Depends

from app.repositories import TagRepository, PostRepository
from app.schemas import TagUpdate, TagCreate, PostCreate, PostUpdate
from database.models import Tag, Post


class TagService:
    def __init__(self, tag_repository: TagRepository = Depends(TagRepository)):
        self.tag_repository = tag_repository

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
        query = self.tag_repository.get_all(skip, limit, search)
        return query

    def get(self, tag_id: int) -> Tag:
        """
        :param tag_id: ID of tag to return
        :return: Tag object

        Returns a tag by ID.
        """
        tag = self.tag_repository.get(tag_id)
        return tag

    def get_by_slug(self, slug: str) -> Tag:
        """
        :param slug: Slug of tag to return
        :return: Tag object

        Returns a tag by slug.
        """
        tag = self.tag_repository.get_by_slug(slug)
        return tag

    def update(self, tag: TagUpdate, slug: str) -> Tag:
        """
        :param tag: Tag object
        :param slug: Slug of tag to update
        :return: Tag object

        Updates a tag.
        """
        tag_in_db = self.tag_repository.get_by_slug(slug)
        return self.tag_repository.update(tag, tag_in_db.id)

    def create(self, tag: TagCreate) -> Tag:
        """
        :param tag: Tag object
        :return: Tag object

        Creates a tag.
        """
        return self.tag_repository.create(tag)

    def delete(self, slug: str):
        """
        :param slug: Slug of tag to delete
        :return: Tag object

        Deletes a tag.
        """
        tag_in_db = self.tag_repository.get_by_slug(slug)
        return self.tag_repository.delete(tag_in_db.id)


class PostService:
    def __init__(self, post_repository: PostRepository = Depends(PostRepository)):
        self.post_repository = post_repository

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
        query = self.post_repository.get_all(skip, limit, search)
        return query

    def get_by_slug(self, slug: str) -> Post:
        """
        :param slug: Slug of post to return
        :return: Post object

        Returns a post by slug.
        """
        post = self.post_repository.get_by_slug(slug)
        return post

    def create(self, post: PostCreate, author_id: int) -> Post:
        """
        :param post: Post object
        :param author_id: ID of author
        :return: Post object

        Creates a post.
        """
        return self.post_repository.create(post, author_id)

    def update(self, post: PostUpdate, slug: str) -> Post:
        """
        :param post: Post object
        :param slug: Slug of post to update
        :return: Post object

        Updates a post.
        """
        post_in_db = self.post_repository.get_by_slug(slug)
        return self.post_repository.update(post, post_in_db.id)

    def delete(self, slug: str):
        """
        :param slug: Slug of post to delete
        :return: Post object

        Deletes a post.
        """
        post_in_db = self.post_repository.get_by_slug(slug)
        return self.post_repository.delete(post_in_db.id)
