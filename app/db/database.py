import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.pool import NullPool
from app.config import DATABASE_URL

# Fix "postgres://" → "postgresql://"
_url = (DATABASE_URL or "sqlite:///./quiz.db").strip()
if _url.startswith("postgres://"):
    _url = _url.replace("postgres://", "postgresql://", 1)

_is_sqlite = _url.startswith("sqlite")

if _is_sqlite:
    engine = create_engine(_url, connect_args={"check_same_thread": False})
else:
    # Supabase / PostgreSQL
    # NullPool: mỗi request mở/đóng connection riêng — phù hợp Supabase pooler
    engine = create_engine(
        _url,
        poolclass=NullPool,
        connect_args={
            "sslmode": "require",
            "connect_timeout": 10,
            "keepalives": 1,
            "keepalives_idle": 30,
            "keepalives_interval": 10,
            "keepalives_count": 5,
        },
    )

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
