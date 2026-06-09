from flask import Blueprint, request, jsonify
from app.db.database import db
from app.models.user import User

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")


@auth_bp.post("/login")
def login():
    data = request.get_json(force=True)
    username = (data.get("username") or "").strip()
    password = data.get("password") or ""

    user = User.query.filter_by(username=username).first()
    if user and user.password == password:
        return jsonify({
            "ok": True,
            "username": user.username,
            "role": user.role,
            "message": "Đăng nhập thành công",
        })
    return jsonify({"ok": False, "message": "Tên đăng nhập hoặc mật khẩu không đúng"}), 401
