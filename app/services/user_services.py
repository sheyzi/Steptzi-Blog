from typing import Optional

from app.repositories import UserRepository
from app.schemas.user_schemas import UserRead
from app.services import AuthServices
from app.schemas import UserCreate
from fastapi import BackgroundTasks, Depends, Request, status


class UserService:
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
        """
        :param skip: Number of users to skip
        :param limit: Maximum number of users to return
        :param search: Search string
        :return: List of users

        Get all users
        """
        return self.user_repositories.get_all(skip=skip, limit=limit, search=search)

    def get_user_by_id(self, user_id: int):
        """
        :param user_id: User ID
        :return: User

        Get user by ID
        """
        return self.user_repositories.get(user_id)

    def get_user_by_username(self, username: str):
        """
        :param username: Username
        :return: User

        Get user by username
        """
        return self.user_repositories.get_by_username(username)

    def update_user(
        self,
        user_id: int,
        user: UserCreate,
        request: Request,
        background_tasks: BackgroundTasks,
    ):
        """
        :param user_id: User ID
        :param user: User object
        :param request: Request object
        :param background_tasks: Background tasks object
        :return: User

        Update user
        """
        user_in_db = self.user_repositories.get(user_id)

        # Resend verification mail if email changed
        if user.email and user.email != user_in_db.email:
            print("Here")
            self.auth_service.send_verification_mail(
                request=request,
                email=user_in_db.email,
                background_tasks=background_tasks,
            )
            user_in_db.is_verified = False
            user_in_db.email = user.email

        if user.username:
            user_in_db.username = user.username

        return self.user_repositories.update(user_id, user_in_db)
