from sqlmodel import SQLModel, Field
from typing import List, Optional
from sqlalchemy import Column, String
from pydantic import EmailStr


class UserBase(SQLModel):
    """
    The base class for user models.
    """

    username: str = Field(sa_column=Column(String, unique=True))
    email: EmailStr = Field(sa_column=Column(String, unique=True))


class UserCreate(UserBase):
    """
    The input class for user models.
    """

    password: str
    confirm_password: str

    class Config:
        schema_extra = {
            "example": {
                "username": "username",
                "email": "me@steptzi.com.ng",
                "password": "password",
                "confirm_password": "password",
            }
        }


class User(UserBase, table=True):
    """
    The user model.
    """

    __tablename__ = "users"
    id: Optional[int] = Field(default=None, nullable=True, primary_key=True)
    password: str
    is_active: Optional[bool] = Field(default=True)
    is_verified: Optional[bool] = Field(default=False)
    is_admin: Optional[bool] = Field(default=False)


class UserRead(UserBase):
    """
    The output class for user models.
    """

    is_active: bool
    is_verified: bool
    is_admin: bool

    class Config:
        schema_extra = {
            "example": {
                "username": "username",
                "email": "me@steptzi.com.ng",
                "is_active": True,
                "is_verified": False,
                "is_admin": False,
            }
        }
