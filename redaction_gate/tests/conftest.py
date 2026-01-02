import os
import sys
from pathlib import Path
import importlib

import pytest_asyncio

# Ensure the app package is importable when tests are executed from repo root.
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

# Use a local sqlite database for fast, isolated test runs.
TEST_DB_PATH = ROOT / "test_redaction_gate.temp.db"
os.environ["REDACTION_DB_URL"] = f"sqlite+aiosqlite:///{TEST_DB_PATH}"

import app.db as db  # noqa: E402
import app.models as models  # noqa: E402

# Ensure the database module picks up the test database URL even if it was
# imported earlier (e.g., during interactive debugging).
db = importlib.reload(db)
models = importlib.reload(models)


@pytest_asyncio.fixture(scope="session")
async def database_engine():
    assert str(db.engine.url).startswith("sqlite")
    if TEST_DB_PATH.exists():
        TEST_DB_PATH.unlink()
    async with db.engine.begin() as conn:
        await conn.run_sync(models.Base.metadata.create_all)
    yield db.engine
    await db.engine.dispose()
    if TEST_DB_PATH.exists():
        TEST_DB_PATH.unlink()


@pytest_asyncio.fixture
async def reset_tables(database_engine):
    async with database_engine.begin() as conn:
        await conn.run_sync(models.Base.metadata.drop_all)
        await conn.run_sync(models.Base.metadata.create_all)
    yield
