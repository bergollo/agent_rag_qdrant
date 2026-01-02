from pydantic import AnyHttpUrl
from pydantic_settings import BaseSettings
from pydantic import ConfigDict

import os
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    AI_SERVICE_NAME: str = "AI Service Stub"
    AI_SERVICE_ENV: str = "development"
    AI_SERVICE_HOST: str = "0.0.0.0"
    AI_SERVICE_PORT: int = 8080
    AI_SERVICE_DOMAIN: str = "ai_service"

    # Get the OpenAI API key from the environment
    OPENAI_API_KEY: str | None = None
    QDRANT_URL: str = "http://qdrant:6333"

    REDACTION_GATE_URL: str = "http://redaction_gate:8080/mcp/mcp"
    REDACTION_GATE_TOKEN: str = "dev-token"
    MCP_TIMEOUT_S:float = 5.0

    model_config = ConfigDict(
        env_file = ".env",
        env_file_encoding = "utf-8",
        extra="ignore",
    )

def get_settings() -> Settings:
    return Settings()