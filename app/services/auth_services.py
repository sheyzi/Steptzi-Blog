from fastapi import BackgroundTasks, HTTPException, status, Depends, Request

from app.schemas import Token, ResetPassword
from app.utils.auth_utils import AuthUtils
from app.repositories import UserRepository, user_repository
from config.mail import send_email, EmailSchema
from config.settings import settings
from database.models import User
from app.schemas import UserCreate


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

    def generate_verification_link(self, request: Request, user_id: int):
        email_token = self.auth_utils.encode_verification_token(user_id=user_id)
        base_url = request.base_url
        frontend_url = settings.FRONTEND_URL
        verification_link = (
            f"{frontend_url or base_url}auth/email-verify/confirm?token={email_token}"
        )
        return verification_link

    def generate_reset_password_link(self, request: Request, user_id: int):
        reset_password_token = self.auth_utils.encode_reset_password_token(
            user_id=user_id
        )
        base_url = request.base_url
        frontend_url = settings.FRONTEND_URL
        reset_password_link = f"{frontend_url or base_url}auth/reset-password/confirm?token={reset_password_token}"
        return reset_password_link

    def send_verification_mail(
        self, background_tasks: BackgroundTasks, email: str, request: Request
    ):
        user = self.user_repository.get_by_email(email)
        verification_link = self.generate_verification_link(request, user.id)
        email = EmailSchema(
            emails=[user.email],
            body={"verification_link": verification_link},
        )
        send_email(
            background_tasks,
            subject=f"{settings.PROJECT_TITLE} email verification",
            email=email,
            template_name="email_verification.html",
        )

    def send_reset_password_mail(
        self, background_tasks: BackgroundTasks, email: str, request: Request
    ):
        user = self.user_repository.get_by_email(email)
        reset_password_link = self.generate_reset_password_link(request, user.id)
        email = EmailSchema(
            emails=[user.email],
            body={"reset_password_link": reset_password_link},
        )
        send_email(
            background_tasks,
            subject=f"{settings.PROJECT_TITLE} password reset",
            email=email,
            template_name="reset_password.html",
        )

    def verify_email(self, token: str) -> User:
        user = self.auth_utils.verify_email(token)
        if user.is_verified:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="This user is already verified",
            )

        user.is_verified = True
        user = self.user_repository.update(user.id, user)
        return user

    def reset_password(self, token: str, reset_password: ResetPassword):
        if reset_password.password != reset_password.confirm_password:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="The passwords do not match",
            )
        user = self.auth_utils.verify_password_reset_token(token)
        user.password = self.auth_utils.get_password_hash(reset_password.password)
        user = self.user_repository.update(user.id, user)
        return user
