from pydantic import AnyHttpUrl
from pydantic_settings import BaseSettings
from pydantic import ConfigDict

class Settings(BaseSettings):
    BACKEND_APP_NAME: str = "MCP Backend"
    BACKEND_ENV: str = "development"
    BACKEND_HOST: str = "0.0.0.0"
    BACKEND_PORT: int = 8000

    AI_SERVICE_URL: AnyHttpUrl = "http://ai_service:8001" # ai_service | localhost

    model_config = ConfigDict(
        env_file = ".env",
        env_file_encoding = "utf-8",
        extra="ignore",
    )

def get_settings() -> Settings:
    return Settings()