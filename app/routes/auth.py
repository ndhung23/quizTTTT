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


@auth_bp.get("/users")
def get_users():
    users = User.query.all()
    return jsonify([
        {
            "id": u.id,
            "username": u.username,
            "password": u.password,  # return password so it's simple to show/edit
            "role": u.role
        } for u in users
    ])


@auth_bp.post("/users")
def create_user():
    data = request.get_json(force=True)
    username = (data.get("username") or "").strip()
    password = data.get("password") or ""
    role = data.get("role") or "teacher"

    if not username or not password:
        return jsonify({"ok": False, "message": "Thiếu thông tin đăng nhập"}), 400

    existing = User.query.filter_by(username=username).first()
    if existing:
        return jsonify({"ok": False, "message": "Tên đăng nhập đã tồn tại"}), 400

    user = User(username=username, password=password, role=role)
    db.session.add(user)
    db.session.commit()
    return jsonify({"ok": True, "message": "Tạo tài khoản thành công"})


@auth_bp.put("/users/<int:user_id>")
def update_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({"ok": False, "message": "Không tìm thấy người dùng"}), 404

    data = request.get_json(force=True)
    username = (data.get("username") or "").strip()
    password = data.get("password") or ""
    role = data.get("role") or "teacher"

    if not username:
        return jsonify({"ok": False, "message": "Tên đăng nhập không được trống"}), 400

    # If username changed, check if it's taken
    if username != user.username:
        existing = User.query.filter_by(username=username).first()
        if existing:
            return jsonify({"ok": False, "message": "Tên đăng nhập đã tồn tại"}), 400
        user.username = username

    if password:
        user.password = password
    user.role = role
    db.session.commit()
    return jsonify({"ok": True, "message": "Cập nhật tài khoản thành công"})


@auth_bp.delete("/users/<int:user_id>")
def delete_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({"ok": False, "message": "Không tìm thấy người dùng"}), 404

    if user.username == "admin":
        return jsonify({"ok": False, "message": "Không được phép xóa tài khoản admin mặc định"}), 400

    from app.models.session import QuizSession
    QuizSession.query.filter_by(user_id=user_id).update({"user_id": None})
    
    db.session.delete(user)
    db.session.commit()
    return jsonify({"ok": True, "message": "Xóa tài khoản thành công"})

