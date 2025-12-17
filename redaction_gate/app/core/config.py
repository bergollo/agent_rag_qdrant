from pydantic import AnyHttpUrl
from pydantic_settings import BaseSettings
from pydantic import ConfigDict

import os
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    APP_NAME: str = "MCP Redaction Gate"
    ENV: str = "development"
    HOST: str = "0.0.0.0"
    PORT: int = 8002

    REDACTION_GATE_TOKEN: str = "dev-token"
    REDACTION_POLICY_VERSION: str = "v0"

    DATABASE_URL: str = "postgresql+asyncpg://redact:redact@redaction_db:5432/redaction"

    model_config = ConfigDict(
        env_file = ".env",
        env_file_encoding = "utf-8",
        extra="ignore",
    )

def get_settings() -> Settings:
    return Settings()