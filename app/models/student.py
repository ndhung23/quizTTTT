from app.db.database import db


class Student(db.Model):
    __tablename__ = "students"

    id           = db.Column(db.Integer, primary_key=True)
    name         = db.Column(db.String(100), nullable=False)
    score        = db.Column(db.Integer, default=0)
    answer_order = db.Column(db.JSON, nullable=True)
    session_id   = db.Column(db.Integer, db.ForeignKey("quiz_sessions.id"), nullable=False)
