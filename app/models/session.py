from app.db.database import db


class QuizSession(db.Model):
    __tablename__ = "quiz_sessions"

    id        = db.Column(db.Integer, primary_key=True)
    code      = db.Column(db.String(10), unique=True, nullable=False)
    is_active = db.Column(db.Boolean, default=True)
    quiz_type = db.Column(db.String(50), default="option1", nullable=False)
    user_id   = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=True)

