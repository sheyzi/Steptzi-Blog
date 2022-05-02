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
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
        )
    return user
