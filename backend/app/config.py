from typing import List

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # API Keys
    GEMINI_API_KEY: str
    GOOGLE_CLOUD_PROJECT_ID: str
    GOOGLE_APPLICATION_CREDENTIALS: str

    # Application
    APP_NAME: str = "NotebookLM Video Generator"
    DEBUG: bool = True

    # CORS
    CORS_ORIGINS: List[str] = ["http://localhost:5173", "http://localhost:3000"]

    # File Storage
    UPLOAD_DIR: str = "data/sources"
    GENERATED_DIR: str = "data/generated"
    MAX_UPLOAD_SIZE: int = 100 * 1024 * 1024  # 100MB

    # Video Generation
    DEFAULT_DURATION: int = 300  # 5 minutes
    DEFAULT_STYLE: str = "classic"
    MAX_SLIDES: int = 50

    # Database
    DATABASE_URL: str = "sqlite:///./data/app.db"

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
