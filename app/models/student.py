from sqlalchemy import Column, Integer, String, ForeignKey, JSON
from app.db.database import Base


class Student(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    score = Column(Integer, default=0)
    answer_order = Column(JSON, nullable=True)   # list of step numbers student submitted
    session_id = Column(Integer, ForeignKey("quiz_sessions.id"), nullable=False)
