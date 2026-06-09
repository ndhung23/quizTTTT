import random
import string

from flask import Blueprint, request, jsonify, abort
from app.db.database import db
from app.models.session import QuizSession
from app.models.student import Student

quiz_bp = Blueprint("quiz", __name__, url_prefix="/quiz")

CORRECT_ORDER = [1, 2, 3, 4, 5, 6, 7]


def gen_code(length: int = 6) -> str:
    return "".join(random.choices(string.digits, k=length))


# ─── POST /quiz/start ────────────────────────────────────────────
@quiz_bp.post("/start")
def start_quiz():
    # Deactivate all previous sessions
    QuizSession.query.update({"is_active": False})
    db.session.commit()

    code = gen_code()
    while QuizSession.query.filter_by(code=code).first():
        code = gen_code()

    session = QuizSession(code=code, is_active=True)
    db.session.add(session)
    db.session.commit()

    return jsonify({"code": code, "session_id": session.id, "link": f"/quiz?code={code}"})


# ─── POST /quiz/join ─────────────────────────────────────────────
@quiz_bp.post("/join")
def join_quiz():
    data = request.get_json(force=True)
    name = (data.get("name") or "").strip()
    code = (data.get("code") or "").strip()

    session = QuizSession.query.filter_by(code=code, is_active=True).first()
    if not session:
        abort(404, description="Mã phòng không hợp lệ hoặc đã kết thúc")

    existing = Student.query.filter_by(name=name, session_id=session.id).first()
    if existing:
        return jsonify({"ok": True, "student_id": existing.id, "session_id": session.id, "message": "Tái kết nối"})

    student = Student(name=name, score=0, session_id=session.id)
    db.session.add(student)
    db.session.commit()

    return jsonify({"ok": True, "student_id": student.id, "session_id": session.id, "message": "Tham gia thành công"})


# ─── POST /quiz/submit ───────────────────────────────────────────
@quiz_bp.post("/submit")
def submit_quiz():
    data = request.get_json(force=True)
    student_id   = data.get("student_id")
    answer_order = data.get("answer_order", [])

    student = Student.query.filter_by(id=student_id).first()
    if not student:
        abort(404, description="Không tìm thấy học viên")

    score = sum(
        1 for i, step in enumerate(answer_order)
        if i < len(CORRECT_ORDER) and step == CORRECT_ORDER[i]
    )
    student.answer_order = answer_order
    student.score = score
    db.session.commit()

    return jsonify({"done": True, "score": score, "total": len(CORRECT_ORDER), "correct_order": CORRECT_ORDER})


# ─── GET /quiz/results ───────────────────────────────────────────
@quiz_bp.get("/results")
def get_results():
    code = request.args.get("code", "")
    session = QuizSession.query.filter_by(code=code).first()
    if not session:
        abort(404, description="Session không tồn tại")

    students = (
        Student.query
        .filter_by(session_id=session.id)
        .order_by(Student.score.desc())
        .all()
    )

    return jsonify({
        "code": code,
        "total_steps": len(CORRECT_ORDER),
        "students": [
            {"id": s.id, "name": s.name, "score": s.score, "submitted": s.answer_order is not None}
            for s in students
        ],
    })


# ─── GET /quiz/active ────────────────────────────────────────────
@quiz_bp.get("/active")
def get_active():
    session = (
        QuizSession.query
        .filter_by(is_active=True)
        .order_by(QuizSession.id.desc())
        .first()
    )
    if not session:
        return jsonify({"active": False})
    return jsonify({"active": True, "code": session.code})
