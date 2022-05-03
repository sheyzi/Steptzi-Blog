from fastapi import Depends, Security, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.utils.auth_utils import AuthUtils
from database.models.users import User

security = HTTPBearer()


def get_user(
    credentials: HTTPAuthorizationCredentials = Security(security),
    auth_utils: AuthUtils = Depends(AuthUtils),
):
    token = credentials.credentials

    user = auth_utils.verify_access_token(token)
    return user


def get_active_user(user: User = Depends(get_user)):
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User account is not active",
        )

    if not user.is_verified:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User email is not verified",
        )
    return user


def get_admin_user(user: User = Depends(get_active_user)):
    if not user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not an admin user",
        )
    return user
