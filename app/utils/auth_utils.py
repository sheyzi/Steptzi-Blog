from fastapi import Depends, HTTPException, status
from passlib.context import CryptContext
from jose import jwt, JWTError
from datetime import datetime, timedelta

from app.repositories import UserRepository, AuthRepository, auth_repository
from config.settings import settings
from database.models.users import User


class AuthUtils:
    def __init__(
        self,
        user_repository: UserRepository = Depends(UserRepository),
        auth_repository: AuthRepository = Depends(AuthRepository),
    ):
        self.pwd_context = CryptContext(
            schemes=["bcrypt"],
            deprecated="auto",
        )
        self.user_repository = user_repository
        self.auth_repository = auth_repository

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        return self.pwd_context.verify(plain_password, hashed_password)

    def get_password_hash(self, plain_password: str) -> str:
        return self.pwd_context.hash(plain_password)

    def get_access_token(self, user: User) -> str:
        payload = {
            "sub": str(user.id),
            "iat": datetime.utcnow(),
            "exp": datetime.utcnow()
            + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES),
            "scope": "access",
        }

        return jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

    def get_refresh_token(self, user: User) -> str:
        payload = {
            "sub": str(user.id),
            "iat": datetime.utcnow(),
            "exp": datetime.utcnow()
            + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS),
            "scope": "refresh",
        }

        return jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

    def verify_access_token(self, token: str) -> User:
        try:
            payload = jwt.decode(
                token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
            )
            if payload["scope"] != "access":
                raise JWTError()

            user_id = int(payload["sub"])
            user = self.user_repository.get_or_none(user_id)
            if user is None:
                raise JWTError()

            return user

        except JWTError as e:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Can't validate credentials",
            )

    def verify_refresh_token(self, token: str) -> User:
        try:
            if self.auth_repository.get_used_token(token) is not None:
                raise HTTPException(status_code=400, detail="Token already used")

            payload = jwt.decode(
                token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
            )
            if payload["scope"] != "refresh":
                raise JWTError()
            user_id = int(payload["sub"])
            user = self.user_repository.get_or_none(user_id)
            if user is None:
                raise JWTError()
            self.auth_repository.add_used_token(token)
            return user
        except JWTError as e:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Can't validate credentials",
            )

    def encode_verification_token(self, user_id) -> str:
        payload = {
            "sub": str(user_id),
            "iat": datetime.utcnow(),
            "exp": datetime.utcnow()
            + timedelta(days=settings.EMAIL_TOKEN_EXPIRE_MINUTES),
            "scope": "email_verification",
        }

        return jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

    def encode_reset_password_token(self, user_id) -> str:
        payload = {
            "sub": str(user_id),
            "iat": datetime.utcnow(),
            "exp": datetime.utcnow()
            + timedelta(days=settings.EMAIL_TOKEN_EXPIRE_MINUTES),
            "scope": "reset_password",
        }

        return jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

    def verify_email(self, token: str) -> User:
        try:
            if self.auth_repository.get_used_token(token) is not None:
                raise HTTPException(status_code=400, detail="Token already used")
            payload = jwt.decode(
                token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
            )
            if payload["scope"] != "email_verification":
                raise JWTError()
            user_id = int(payload["sub"])
            user = self.user_repository.get_or_none(user_id)
            if user is None:
                raise JWTError()
            self.auth_repository.add_used_token(token)
            return user
        except JWTError as e:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Can't validate credentials",
            )

    def verify_password_reset_token(self, token: str) -> User:
        try:
            if self.auth_repository.get_used_token(token) is not None:
                raise HTTPException(status_code=400, detail="Token already used")
            payload = jwt.decode(
                token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
            )
            if payload["scope"] != "reset_password":
                raise JWTError()
            user_id = int(payload["sub"])
            user = self.user_repository.get_or_none(user_id)
            if user is None:
                raise JWTError()
            self.auth_repository.add_used_token(token)
            return user
        except JWTError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Can't validate credentials",
            )
