from typing import Optional
from fastapi import BackgroundTasks, Depends, HTTPException, Request, status

from app.repositories import UserRepository
from app.services import AuthServices
from database.models.users import UserCreate


class UserServices:
    def __init__(
        self,
        user_repositories: UserRepository = Depends(UserRepository),
        auth_servicve: AuthServices = Depends(AuthServices),
    ):
        self.user_repositories = user_repositories
        self.auth_service = auth_servicve

    def get_all_users(
        self,
        skip: Optional[int] = 0,
        limit: Optional[int] = 100,
        search: Optional[str] = None,
    ):
        return self.user_repositories.get_all(skip=skip, limit=limit, search=search)

    def get_user_by_id(self, user_id: int):
        return self.user_repositories.get(user_id)

    def get_user_by_username(self, username: str):
        return self.user_repositories.get_by_username(username)

    def update_user(
        self,
        user_id: int,
        user: UserCreate,
        request: Request,
        background_tasks: BackgroundTasks,
    ):

        user_in_db = self.user_repositories.get(user_id)

        # Resend verification mail if email changed
        if user.email and user.email != user_in_db.email:
            self.auth_service.send_verification_mail(
                request=request,
                email=user_in_db.email,
                background_tasks=background_tasks,
            )
            user_in_db.is_verified = False
            user_in_db.email = user.email

        return self.user_repositories.update(user_id, user_in_db)
