from fastapi import APIRouter

from .auth_router import auth_router

router = APIRouter()

router.include_router(auth_router, prefix="/auth", tags=["Authentication"])
