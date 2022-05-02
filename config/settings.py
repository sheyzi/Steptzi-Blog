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
    ACCESS_TOKEN_EXPIRE_MINUTES: int = config(
        "ACCESS_TOKEN_EXPIRE_MINUTES", default=30, cast=int
    )
    REFRESH_TOKEN_EXPIRE_DAYS: int = config(
        "REFRESH_TOKEN_EXPIRE_DAYS", default=30, cast=int
    )
    ALGORITHM: str = config("ALGORITHM", default="HS256")

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
    # EMAIL_HOST: str = config("EMAIL_HOST")
    # EMAIL_PORT: int = config("EMAIL_PORT", default=587, cast=int)
    # EMAIL_HOST_USER: str = config("EMAIL_HOST_USER")
    # EMAIL_HOST_PASSWORD: str = config("EMAIL_HOST_PASSWORD")
    # EMAIL_USE_TLS: bool = config("EMAIL_USE_TLS", default=True, cast=bool)
    # EMAIL_USE_SSL: bool = config("EMAIL_USE_SSL", default=False, cast=bool)
    # EMAIL_SENDER: str = config("EMAIL_SENDER")


settings = Settings()
