import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    # Fix "postgres://" → "postgresql://" for SQLAlchemy 1.4+
    _raw_url = os.getenv("DATABASE_URL", "sqlite:///quiz.db").strip()
    if _raw_url.startswith("postgres://"):
        _raw_url = _raw_url.replace("postgres://", "postgresql://", 1)

    SQLALCHEMY_DATABASE_URI = _raw_url
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    SECRET_KEY = os.getenv("SECRET_KEY", "fallback-secret-key")

    # Extra connect args for PostgreSQL (Supabase / pooler)
    _is_pg = not _raw_url.startswith("sqlite")
    if _is_pg:
        SQLALCHEMY_ENGINE_OPTIONS = {
            "pool_pre_ping": True,
            "connect_args": {
                "sslmode": "require",
                "connect_timeout": 10,
            },
        }
