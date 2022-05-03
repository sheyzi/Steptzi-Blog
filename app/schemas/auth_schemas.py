from typing import Any, List, Dict
from pydantic import BaseModel, EmailStr


class Token(BaseModel):
    access_token: str
    refresh_token: str


class ResetPassword(BaseModel):
    password: str
    confirm_password: str


class Login(BaseModel):
    username: str
    password: str

    class Config:
        schema_extra = {
            "example": {
                "username": "username",
                "password": "password",
            }
        }


class EmailSchema(BaseModel):
    emails: List[EmailStr]
    body: Dict[str, Any]
