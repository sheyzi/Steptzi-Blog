from typing import List, Optional

from fastapi import BackgroundTasks, Depends, HTTPException, Query, Request, status
from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter

from app.services import UserService
from config.dependencies import get_active_user, get_admin_user
from app.schemas import UserCreate, UserRead, UserUpdate

user_router = InferringRouter()


@cbv(user_router)
class UserRouter:
    def __init__(
        self,
        user_services: UserService = Depends(UserService),
        background_tasks: BackgroundTasks = BackgroundTasks,
        request: Request = Request,
    ) -> None:
        self.user_services = user_services
        self.background_tasks = background_tasks
        self.request = request

    @user_router.get("/me", response_model=UserRead)
    def get_current_user(
        self, request: Request, current_user: UserRead = Depends(get_active_user)
    ) -> UserRead:
        """
        Get current user
        """
        return current_user

    @user_router.get("/", response_model=List[UserRead])
    def get_all_users(
        self,
        limit: Optional[int] = Query(100, alias="limit", le=100),
        skip: Optional[int] = 0,
        search: Optional[str] = None,
    ):
        """
        Get all users
        """
        return self.user_services.get_all_users(limit=limit, skip=skip, search=search)

    @user_router.put("/{user_id}", response_model=UserRead)
    def update_user(
        self,
        user_id: int,
        user: UserUpdate,
        current_user: UserRead = Depends(get_active_user),
    ):
        """
        Update user
        """
        if user_id != current_user.id and not current_user.is_admin:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden"
            )

        return self.user_services.update_user(
            user_id, user, self.request, self.background_tasks
        )

    # @user_router.get("/{username}", response_model=UserRead)
    # def get_user_by_username(self, username: str):
    #     """
    #     Get user by username
    #     """
    #     return self.user_services.get_user_by_username(username)

    @user_router.get("/{user_id}", response_model=UserRead)
    def get_user(self, user_id: int, admin_user: UserRead = Depends(get_admin_user)):
        """
        Get user by id
        """
        return self.user_services.get_user_by_id(user_id)
