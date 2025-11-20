"""FastAPI dependency helpers for the backend service."""

from app.core.config import get_settings
from app.services.ai_client import AIClient


def get_settings_dep():
    """Expose settings via DI so tests can override easily."""
    return get_settings()


def get_ai_client() -> AIClient:
    """Instantiate the async AI client bound to the configured ai_service URL."""
    settings = get_settings_dep()
    return AIClient(base_url=str(settings.AI_SERVICE_URL))
