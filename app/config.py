import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./quiz.db")
SECRET_KEY = os.getenv("SECRET_KEY", "fallback-secret-key")

# ── Multi-user support ─────────────────────────────────────────
# Format trong .env:  USERS=hv90122:123,hv10921:123
def _load_users() -> dict:
    raw = os.getenv("USERS", "")
    users = {}
    for entry in raw.split(","):
        entry = entry.strip()
        if ":" in entry:
            u, p = entry.split(":", 1)
            users[u.strip()] = p.strip()
    # fallback default admin
    if not users:
        users["admin"] = "123456"
    return users

USERS: dict = _load_users()
