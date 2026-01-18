import os

from sqlalchemy import create_engine
from sqlalchemy.engine import URL
from sqlalchemy.orm import Session, sessionmaker

_engine = None
_SessionLocal = None


def get_db_url() -> str:
    try:
        port = int(os.getenv("DB_PORT", "3306"))
    except ValueError as exc:
        raise ValueError(f"Invalid DB_PORT: {port!r}") from exc
    return URL.create(
        "mysql+pymysql",
        username=os.getenv("DB_USER", "jabba"),
        password=os.getenv("DB_PASSWORD", "hutt"),
        host=os.getenv("DB_HOST", "127.0.0.1"),
        port=port,
        database=os.getenv("DB_NAME", "accounts"),
    )


def get_engine():
    global _engine
    if _engine is None:
        _engine = create_engine(get_db_url(), echo=False)
    return _engine


def get_session() -> Session:
    global _SessionLocal
    if _SessionLocal is None:
        _SessionLocal = sessionmaker(bind=get_engine(), autoflush=False, autocommit=False)
    return _SessionLocal()
