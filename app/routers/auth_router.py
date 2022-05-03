from fastapi import BackgroundTasks, Depends, HTTPException, Request, status
from fastapi_utils.inferring_router import InferringRouter
from fastapi_utils.cbv import cbv

from app.schemas import Token, Login
from app.schemas.auth_schemas import ResetPassword
from app.services import AuthServices
from config.dependencies import get_active_user
from database.models.users import UserCreate, UserRead

auth_router = InferringRouter()


@cbv(auth_router)
class AuthView:
    def __init__(
        self,
        background_tasks: BackgroundTasks,
        request: Request,
        auth_services: AuthServices = Depends(AuthServices),
    ):
        self.auth_services = auth_services
        self.request = request
        self.background_tasks = background_tasks

    @auth_router.post("/register", response_model=UserRead)
    def register(self, user_create: UserCreate) -> UserRead:
        """
        Register a new user
        """
        user = self.auth_services.register(user_create)
        self.auth_services.send_verification_mail(
            self.background_tasks, user.email, self.request
        )
        return user

    @auth_router.post("/login", response_model=Token)
    def login(self, data: Login) -> Token:
        """
        Get access and refresh tokens
        """
        return self.auth_services.login(data.username, data.password)

    @auth_router.get("/refresh", response_model=Token)
    def refresh(self, token: str) -> Token:
        """
        Get new pairs of access and refresh tokens
        """
        return self.auth_services.refresh_token(token)

    @auth_router.get("/email-verify")
    def email_verify(self, email: str):
        """
        Send verification email
        """
        user = self.auth_services.user_repository.get_by_email(email)
        if user.is_verified:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="This user is already verified",
            )
        self.auth_services.send_verification_mail(
            self.background_tasks, email, self.request
        )
        return {"message": "Verification email sent"}

    @auth_router.get("/email-verify/confirm")
    def verify_email(self, token: str):
        """
        Verify email address
        """
        user = self.auth_services.verify_email(token)
        return {"message": "Email verified"}

    @auth_router.get("/reset-password")
    def reset_password(self, email: str):
        """
        Send reset password email
        """
        self.auth_services.send_reset_password_mail(
            self.background_tasks, email, self.request
        )
        return {"message": "Reset password email sent"}

    @auth_router.post("/reset-password/confirm")
    def confirm_reset_password(self, token: str, data: ResetPassword):
        """
        Confirm reset password
        """
        user = self.auth_services.reset_password(token, data)
        return {"message": "Password reset"}
