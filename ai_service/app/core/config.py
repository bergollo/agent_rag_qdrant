from pydantic import AnyHttpUrl
from pydantic_settings import BaseSettings
from pydantic import ConfigDict

import os
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    APP_NAME: str = "AI Service Stub"
    ENV: str = "development"
    HOST: str = "0.0.0.0"
    PORT: int = 8001

    # Get the OpenAI API key from the environment
    OPENAI_API_KEY: str | None = None
    QDRANT_URL: str = "http://qdrant:6333"

    model_config = ConfigDict(
        env_file = ".env",
        env_file_encoding = "utf-8",
        extra="ignore",
    )

def get_settings() -> Settings:
    return Settings()