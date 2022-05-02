from fastapi import HTTPException, status, Depends

from app.schemas import Token
from app.utils.auth_utils import AuthUtils
from app.repositories import UserRepository
from database.models.users import User, UserCreate


class AuthServices:
    def __init__(
        self,
        user_repository: UserRepository = Depends(UserRepository),
        auth_utils: AuthUtils = Depends(AuthUtils),
    ):
        self.user_repository = user_repository
        self.auth_utils = auth_utils

    def login(self, username: str, password: str) -> Token:
        user = self.user_repository.get_by_username_or_none(username)
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
            )
        if not self.auth_utils.verify_password(password, user.password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
            )

        access_token = self.auth_utils.get_access_token(user)
        refresh_token = self.auth_utils.get_refresh_token(user)
        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
        }

    def register(self, user_create: UserCreate) -> User:
        user = self.user_repository.get_by_username_or_none(user_create.username)
        if user is not None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="The username is already taken",
            )
        if user_create.password != user_create.confirm_password:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="The passwords do not match",
            )
        user = self.user_repository.get_by_email_or_none(user_create.email)
        if user is not None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="The email is already taken",
            )

        user_create.password = self.auth_utils.get_password_hash(user_create.password)
        user = self.user_repository.create(user_create)
        return user

    def refresh_token(self, token: str) -> Token:
        user = self.auth_utils.verify_refresh_token(token)
        access_token = self.auth_utils.get_access_token(user)
        refresh_token = self.auth_utils.get_refresh_token(user)
        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
        }
