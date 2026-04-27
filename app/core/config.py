import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "Calc"
    VERSION: str = "1.0.0"
    GRPC_HOST: str = os.getenv("GRPC_HOST", "calc-grpc:50051")
    
    # DB settings for demonstration
    DB_HOST: str | None = os.getenv("DB_HOST")
    DB_PORT: str | None = os.getenv("DB_PORT")
    DB_NAME: str | None = os.getenv("DB_NAME")
    DB_PASSWORD: str | None = os.getenv("DB_PASSWORD")

    class Config:
        case_sensitive = True

settings = Settings()
