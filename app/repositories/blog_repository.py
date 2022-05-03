from datetime import datetime
from typing import List, Optional, Union
from fastapi import Depends, HTTPException, status

from database.models import Tag
from database.session import Session, get_db
from database.models.blog import TagCreate, TagUpdate


class BlogRepository:
    def __init__(self, db: Session = Depends(get_db)):
        self.db = db

    def get_all(
        self,
        skip: Optional[int] = 0,
        limit: Optional[int] = 100,
        search: Optional[str] = None,
    ) -> List[Tag]:
        query = self.db.query(Tag)
        if search:
            query = query.filter(Tag.title.contains(search))
        query = query.offset(skip).limit(limit)
        return query.all()

    def get(self, tag_id: int) -> Tag:
        tag = self.db.query(Tag).get(tag_id)
        if tag is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Tag not found"
            )
        return tag

    def get_or_none(self, tag_id: int) -> Union[Tag, None]:
        tag = self.db.query(Tag).get(tag_id)
        return tag

    def get_by_slug(self, slug: str) -> Tag:
        tag = self.db.query(Tag).filter(Tag.slug == slug).first()
        if tag is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Tag not found"
            )
        return tag

    def get_by_slug_or_none(self, slug: str) -> Union[Tag, None]:
        tag = self.db.query(Tag).filter(Tag.slug == slug).first()
        return tag

    def create(self, tag: TagCreate) -> Tag:
        tag = Tag(**tag.dict())
        self.db.add(tag)
        self.db.commit()
        self.db.refresh(tag)
        return tag

    def update(self, tag: TagUpdate, tag_id: int) -> Tag:
        tag_in_db: Tag = self.get(tag_id)
        for key, value in tag.dict(exclude_unset=True).items():
            setattr(tag_in_db, key, value)

        tag_in_db.updated_at = datetime.utcnow()
        self.db.commit()
        self.db.refresh(tag_in_db)
        return tag_in_db

    def delete(self, tag_id: int):
        tag = self.get(tag_id)
        self.db.delete(tag)
        self.db.commit()
        return {"message": "Tag deleted"}
