from typing import List

from decouple import config
from pydantic import BaseModel


class Settings(BaseModel):
    # Project settings
    PROJECT_TITLE: str = "Steptzi"
    PROJECT_DESCRIPTION: str = (
        "Steptzi is a blogging platform for the programming community."
    )
    PROJECT_VERSION: str = "0.0.1"

    # Database settings
    DB_HOST: str = config("DB_HOST", default="localhost")
    DB_PORT: int = config("DB_PORT", default=5432, cast=int)
    DB_USER: str = config("DB_USER")
    DB_PASSWORD: str = config("DB_PASSWORD")
    DB_NAME: str = config("DB_NAME")
    DB_URI: str = (
        f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    )

    # Security settings
    SECRET_KEY: str = config("SECRET_KEY")
    ALGORITHM: str = config("ALGORITHM", default="HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = config(
        "ACCESS_TOKEN_EXPIRE_MINUTES", default=30, cast=int
    )
    REFRESH_TOKEN_EXPIRE_DAYS: int = config(
        "REFRESH_TOKEN_EXPIRE_DAYS", default=30, cast=int
    )
    EMAIL_TOKEN_EXPIRE_MINUTES: int = config(
        "EMAIL_TOKEN_EXPIRE_MINUTES", default=30, cast=int
    )

    # CORS settings
    CORS_ORIGINS: List[str] = [
        "http://localhost:3000",
        "localhost:3000",
        "steptzi.com.ng" "https://steptzi.com.ng",
        "https://www.steptzi.com.ng",
    ]
    CORS_METHODS: List[str] = ["GET", "POST", "PUT", "DELETE", "OPTIONS"]
    CORS_HEADERS: List[str] = ["Content-Type", "Authorization"]
    CORS_ALLOW_CREDENTIALS: bool = True

    # Email settings
    EMAIL_USERNAME: str = config("EMAIL_USERNAME")
    EMAIL_PASSWORD: str = config("EMAIL_PASSWORD")
    EMAIL_FROM: str = config("EMAIL_FROM")
    EMAIL_PORT: str = config("EMAIL_PORT")
    EMAIL_SERVER: str = config("EMAIL_SERVER")

    FRONTEND_URL: str = config("FRONTEND_URL", default=None)


settings = Settings()
