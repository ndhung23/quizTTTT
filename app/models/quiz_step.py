from app.db.database import db

class QuizStep(db.Model):
    __tablename__ = "quiz_steps"

    id = db.Column(db.Integer, primary_key=True)
    option_id = db.Column(db.Integer, db.ForeignKey("quiz_options.id"), nullable=False)
    step_num = db.Column(db.Integer, nullable=False)
    image_url = db.Column(db.String(255), nullable=True)
    left_text = db.Column(db.Text, nullable=True)
    right_text = db.Column(db.Text, nullable=True)
    note_text = db.Column(db.Text, nullable=True)
    reason_text = db.Column(db.Text, nullable=True)
