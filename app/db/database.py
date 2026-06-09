import os
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def init_db(app):
    """Attach SQLAlchemy to the Flask app and create tables."""
    db.init_app(app)
    with app.app_context():
        from app.models import user, student, session  # noqa: F401 – register models
        db.create_all()
        _seed_users()


def _seed_users():
    """Insert default users if the users table is empty."""
    from app.models.user import User
    try:
        if User.query.count() == 0:
            seed = [
                User(username="admin",   password="123", role="admin"),
                User(username="hv90122", password="123", role="teacher"),
                User(username="hv10921", password="123", role="teacher"),
            ]
            db.session.add_all(seed)
            db.session.commit()
            print("✅ Seeded 3 default users")
        else:
            print("ℹ️  Users already exist – skip seed")
    except Exception as e:
        db.session.rollback()
        print(f"⚠️  Seed warning: {e}")
