from fastapi import Depends, HTTPException, status
from fastapi_utils.inferring_router import InferringRouter
from fastapi_utils.cbv import cbv

from app.schemas import Token, Login
from app.services import AuthServices
from config.dependencies import get_active_user
from database.models.users import UserCreate, UserRead

auth_router = InferringRouter()


@cbv(auth_router)
class AuthView:
    def __init__(self, auth_services: AuthServices = Depends(AuthServices)):
        self.auth_services = auth_services

    @auth_router.post("/register", response_model=UserRead)
    def register(self, user_create: UserCreate) -> UserRead:
        return self.auth_services.register(user_create)

    @auth_router.post("/login", response_model=Token)
    def login(self, data: Login) -> Token:
        return self.auth_services.login(data.username, data.password)

    @auth_router.get("/refresh", response_model=Token)
    def refresh(self, token: str) -> Token:
        return self.auth_services.refresh_token(token)

    @auth_router.get("/me", response_model=UserRead)
    def me(self, user: UserRead = Depends(get_active_user)) -> UserRead:
        return user
