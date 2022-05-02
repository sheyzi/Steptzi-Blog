from pydantic import BaseModel


class Token(BaseModel):
    access_token: str
    refresh_token: str


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
