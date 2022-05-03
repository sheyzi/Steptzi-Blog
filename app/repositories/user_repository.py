from typing import List, Optional
from fastapi import HTTPException, status, Depends
from sqlmodel import Session

from database.models.users import User, UserCreate
from database.session import get_db


class UserRepository:
    def __init__(self, db: Session = Depends(get_db)):
        self.db = db

    def create(self, user: UserCreate) -> User:
        user.email = user.email.lower()
        user.username = user.username.lower()
        db_user = User(**user.dict())
        self.db.add(db_user)
        self.db.commit()
        self.db.refresh(db_user)
        return db_user

    def get(self, user_id: int) -> User:
        db_user = self.db.query(User).filter(User.id == user_id).first()
        if db_user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
            )
        return db_user

    def get_or_none(self, user_id: int) -> User:
        db_user = self.db.query(User).get(user_id)
        return db_user

    def get_by_username(self, username: str) -> User:
        db_user = self.db.query(User).filter(User.username == username).first()
        if db_user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
            )
        return db_user

    def get_by_username_or_none(self, username: str) -> User:
        db_user = self.db.query(User).filter(User.username == username).first()
        return db_user

    def get_by_email(self, email: str) -> User:
        db_user = self.db.query(User).filter(User.email == email).first()
        if db_user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
            )
        return db_user

    def get_by_email_or_none(self, email: str) -> User:
        db_user = self.db.query(User).filter(User.email == email).first()
        return db_user

    def get_all(
        self,
        skip: Optional[int] = 0,
        limit: Optional[int] = 100,
        search: Optional[str] = None,
    ) -> List[User]:
        query = self.db.query(User)
        if search:
            query = query.filter(User.username.contains(search))
        query = query.limit(limit).offset(skip)

        return query.all()

    def update(self, user_id: int, user: UserCreate) -> User:

        db_user = self.get(user_id)
        for key, value in user.dict(exclude_unset=True).items():
            setattr(db_user, key, value)
        self.db.commit()
        self.db.refresh(db_user)
        return db_user

    def delete(self, user_id: int) -> None:
        db_user = self.get(user_id)
        self.db.delete(db_user)
        self.db.commit()
