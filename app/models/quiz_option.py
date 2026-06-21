from app.db.database import db

class QuizOption(db.Model):
    __tablename__ = "quiz_options"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    code = db.Column(db.String(50), unique=True, nullable=False)
    is_custom = db.Column(db.Boolean, default=True, nullable=False)
    quiz_format = db.Column(db.String(20), default='option1', nullable=False)

    steps = db.relationship("QuizStep", backref="quiz_option", cascade="all, delete-orphan", order_by="QuizStep.step_num")

