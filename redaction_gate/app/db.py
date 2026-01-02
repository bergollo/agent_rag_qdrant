import os
from collections.abc import AsyncIterator

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.core.deps import get_settings_dep

# Prefer an explicit DATABASE_URL environment override (useful for tests) and
# fall back to the configured settings value for normal operation.
settings = get_settings_dep()
database_url = settings.REDACTION_DB_URL

engine = create_async_engine(database_url, pool_pre_ping=True)
SessionLocal = async_sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)


async def get_session() -> AsyncIterator[AsyncSession]:
    """Yield a database session for FastAPI dependencies."""
    async with SessionLocal() as session:
        yield session
