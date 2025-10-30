from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    MONGO_USER_NAME: str
    MONGO_USER_PASSWORD: str
    MONGO_CLUSTER: str
    MONGO_APP_NAME: str
    MONGO_DATABASE: str

    # CORS settings
    CORS_ORIGINS: str = "*"
    CORS_CREDENTIALS: bool = True
    CORS_METHODS: str = "*"
    CORS_HEADERS: str = "*"

    # JWT settings
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7

    # Cloudinary settings
    CLOUDINARY_CLOUD_NAME: str
    CLOUDINARY_API_KEY: str
    CLOUDINARY_API_SECRET: str

    class Config:
        env_file = ".env"


settings = Settings()
