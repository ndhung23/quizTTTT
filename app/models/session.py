from sqlalchemy import Column, Integer, String, Boolean
from app.db.database import Base


class QuizSession(Base):
    __tablename__ = "quiz_sessions"

    id = Column(Integer, primary_key=True, index=True)
    code = Column(String(10), unique=True, nullable=False)
    is_active = Column(Boolean, default=True)
