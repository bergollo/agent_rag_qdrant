from pydantic import AnyHttpUrl
from pydantic_settings import BaseSettings
from pydantic import ConfigDict

class Settings(BaseSettings):
    APP_NAME: str = "MCP Backend"
    ENV: str = "development"
    HOST: str = "0.0.0.0"
    PORT: int = 8000

    AI_SERVICE_URL: AnyHttpUrl = "http://ai_service:8001" # ai_service | localhost
    QDRANT_URL: AnyHttpUrl = "http://qdrant:6333"

    model_config = ConfigDict(
        env_file = ".env",
        env_file_encoding = "utf-8",
        extra="ignore",
    )

def get_settings() -> Settings:
    return Settings()