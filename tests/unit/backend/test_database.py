from backend.database.engine import get_async_db_url


def test_get_async_db_url_postgres() -> None:
    url = "postgresql://user:pass@host:5432/db"
    assert get_async_db_url(url) == "postgresql+asyncpg://user:pass@host:5432/db"


def test_get_async_db_url_sqlite() -> None:
    url = "sqlite:///local.db"
    assert get_async_db_url(url) == "sqlite+aiosqlite:///local.db"


def test_get_async_db_url_already_async() -> None:
    url = "postgresql+asyncpg://user:pass@host:5432/db"
    assert get_async_db_url(url) == url
