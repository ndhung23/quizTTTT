import os
from flask import Flask, send_from_directory, send_file, jsonify

from app.config import Config
from app.db.database import init_db
from app.routes.auth import auth_bp
from app.routes.quiz import quiz_bp

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEMPLATES_DIR = os.path.join(os.path.dirname(__file__), "templates")


def create_app() -> Flask:
    app = Flask(__name__, template_folder="templates")
    app.config.from_object(Config)

    # Init DB + seed
    init_db(app)

    # Blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(quiz_bp)

    # ── Serve step images (1.png – 7.png) from project root ──────
    @app.route("/images/<path:filename>")
    def serve_image(filename):
        return send_from_directory(ROOT_DIR, filename)

    # ── Page routes ──────────────────────────────────────────────
    @app.route("/")
    def login_page():
        return send_file(os.path.join(TEMPLATES_DIR, "login.html"))

    @app.route("/dashboard")
    def dashboard_page():
        return send_file(os.path.join(TEMPLATES_DIR, "dashboard.html"))

    @app.route("/quiz-page")
    def quiz_student_page():
        return send_file(os.path.join(TEMPLATES_DIR, "quiz.html"))

    # ── JSON error handlers ──────────────────────────────────────
    @app.errorhandler(404)
    def not_found(e):
        return jsonify({"detail": str(e)}), 404

    @app.errorhandler(400)
    def bad_request(e):
        return jsonify({"detail": str(e)}), 400

    return app


app = create_app()
