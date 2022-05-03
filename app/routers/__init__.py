from fastapi import APIRouter

from .auth_router import auth_router
from .user_routers import user_router
from .blog_routers import blog_router

router = APIRouter()

router.include_router(auth_router, prefix="/auth", tags=["Authentication"])
router.include_router(user_router, prefix="/users", tags=["Users"])
router.include_router(blog_router, prefix="/blogs", tags=["Blogs"])
