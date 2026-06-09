import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./quiz.db")
SECRET_KEY = os.getenv("SECRET_KEY", "fallback-secret-key-change-in-prod")
ADMIN_EMAIL = os.getenv("ADMIN_EMAIL", "admin@test.com")
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "123456")
