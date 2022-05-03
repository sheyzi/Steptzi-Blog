from fastapi import APIRouter

from .auth_router import auth_router
from .user_routers import user_router

router = APIRouter()

router.include_router(auth_router, prefix="/auth", tags=["Authentication"])
router.include_router(user_router, prefix="/users", tags=["Users"])
