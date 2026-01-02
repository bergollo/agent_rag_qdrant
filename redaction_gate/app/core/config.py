from pydantic import AnyHttpUrl
from pydantic_settings import BaseSettings
from pydantic import ConfigDict

import os
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    REDACTION_GATE_NAME: str = "MCP Redaction Gate"
    REDACTION_GATE_ENV: str = "production"
    REDACTION_GATE_HOST: str = "0.0.0.0"
    REDACTION_GATE_PORT: int = 8080

    REDACTION_GATE_TOKEN: str = "dev-token"
    REDACTION_POLICY_VERSION: str = "v0"

    REDACTION_DB_URL: str = "postgresql+asyncpg://redact:redact@redaction_db:5432/redaction"

    model_config = ConfigDict(
        env_file = ".env",
        env_file_encoding = "utf-8",
        extra="ignore",
    )

def get_settings() -> Settings:
    return Settings()