"""FastAPI dependency helpers."""

from app.core.config import get_settings
from app.services.open_ai import OpenAIClient


def get_settings_dep():
    """Thin wrapper to keep dependency injection explicit for tests."""
    return get_settings()


def get_openai_client() -> OpenAIClient:
    """Instantiate an OpenAIClient bound to configured OpenAI + Qdrant credentials."""
    settings = get_settings_dep()
    return OpenAIClient(
        openai_api_key=settings.OPENAI_API_KEY,
        qdrant_url=settings.QDRANT_URL,
    )
