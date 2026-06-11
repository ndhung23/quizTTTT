import os
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def init_db(app):
    """Attach SQLAlchemy to the Flask app and create tables."""
    db.init_app(app)
    with app.app_context():
        from app.models import user, student, session  # noqa: F401 – register models
        db.create_all()
        try:
            db.session.execute(db.text("ALTER TABLE quiz_sessions ADD COLUMN quiz_type VARCHAR(20) DEFAULT 'option1'"))
            db.session.commit()
            print("Successfully added quiz_type column to quiz_sessions")
        except Exception:
            db.session.rollback()
        try:
            db.session.execute(db.text("ALTER TABLE quiz_sessions ADD COLUMN user_id INTEGER"))
            db.session.commit()
            print("Successfully added user_id column to quiz_sessions")
        except Exception:
            db.session.rollback()
        _seed_users()


def _seed_users():
    """Insert default users or update passwords."""
    from app.models.user import User
    try:
        users_to_check = [
            {"username": "admin", "password": "hvdn@dens0", "role": "admin"},
            {"username": "hv90122", "password": "hvdn@dens0", "role": "teacher"},
            {"username": "hv10921", "password": "hvdn@dens0", "role": "teacher"},
        ]
        for u_data in users_to_check:
            user = User.query.filter_by(username=u_data["username"]).first()
            if not user:
                user = User(username=u_data["username"], password=u_data["password"], role=u_data["role"])
                db.session.add(user)
            else:
                user.password = u_data["password"]
                user.role = u_data["role"]
        db.session.commit()
        print("Synchronized default users and updated passwords to 'hvdn@dens0'")
    except Exception as e:
        db.session.rollback()
        print(f"Seed/update warning: {e}")

