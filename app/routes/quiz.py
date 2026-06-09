import random
import string

from flask import Blueprint, request, jsonify, abort
from app.db.database import db
from app.models.session import QuizSession
from app.models.student import Student

quiz_bp = Blueprint("quiz", __name__, url_prefix="/quiz")

SUB_QUIZ_MAX_SCORES = {
    "1": 5,
    "2": 7,
    "3": 5,
    "4": 5,
    "5": 9,
    "6": 2,
    "7": 4,
    "8": 4,
    "9": 5,
    "10": 4
}


def gen_code(length: int = 6) -> str:
    return "".join(random.choices(string.digits, k=length))


# ─── POST /quiz/start ────────────────────────────────────────────
@quiz_bp.post("/start")
def start_quiz():
    data = request.get_json(force=True, silent=True) or {}
    quiz_type = data.get("quiz_type", "option1")
    if quiz_type not in ["option1", "option2"]:
        quiz_type = "option1"

    # Deactivate all previous sessions
    QuizSession.query.update({"is_active": False})
    db.session.commit()

    code = gen_code()
    while QuizSession.query.filter_by(code=code).first():
        code = gen_code()

    session = QuizSession(code=code, is_active=True, quiz_type=quiz_type)
    db.session.add(session)
    db.session.commit()

    return jsonify({"code": code, "session_id": session.id, "link": f"/quiz-page?code={code}", "quiz_type": quiz_type})


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
        return jsonify({"ok": True, "student_id": existing.id, "session_id": session.id, "quiz_type": session.quiz_type, "message": "Tái kết nối"})

    student = Student(name=name, score=0, session_id=session.id)
    db.session.add(student)
    db.session.commit()

    return jsonify({"ok": True, "student_id": student.id, "session_id": session.id, "quiz_type": session.quiz_type, "message": "Tham gia thành công"})


# ─── POST /quiz/submit ───────────────────────────────────────────
@quiz_bp.post("/submit")
def submit_quiz():
    data = request.get_json(force=True)
    student_id = data.get("student_id")

    student = Student.query.filter_by(id=student_id).first()
    if not student:
        abort(404, description="Không tìm thấy học viên")

    session = QuizSession.query.filter_by(id=student.session_id).first()
    if not session:
        abort(404, description="Không tìm thấy phòng thi")

    if session.quiz_type == "option2":
        sub_quiz_id = str(data.get("sub_quiz_id"))
        sub_score = data.get("sub_score", 0)

        # Check and initialize answer_order structure
        ao = student.answer_order
        if not isinstance(ao, dict):
            ao = {"scores": {}}
        if "scores" not in ao:
            ao["scores"] = {}

        ao["scores"][sub_quiz_id] = sub_score
        student.answer_order = ao
        student.score = sum(ao["scores"].values())
        db.session.commit()

        return jsonify({
            "done": True,
            "score": student.score,
            "total": sum(SUB_QUIZ_MAX_SCORES.values()),
            "sub_quiz_id": sub_quiz_id,
            "sub_score": sub_score,
            "completed": list(ao["scores"].keys())
        })
    else:
        answer_order = data.get("answer_order", [])
        score = 0
        for row in answer_order:
            r_idx = row.get("row_idx")
            img = row.get("image_id")
            left = row.get("left_id")
            right = row.get("right_id")
            note = row.get("note_id")
            reason = row.get("reason_id")

            step_num = r_idx + 1
            correct_img = step_num
            correct_left = step_num
            correct_right = 0 if step_num == 1 else step_num
            correct_note = step_num
            correct_reason = step_num

            if img == correct_img and left == correct_left and right == correct_right and note == correct_note and reason == correct_reason:
                score += 1

        student.answer_order = answer_order
        student.score = score
        db.session.commit()

        return jsonify({"done": True, "score": score, "total": 7})


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

    if session.quiz_type == "option2":
        total_steps = sum(SUB_QUIZ_MAX_SCORES.values())
    else:
        total_steps = 7

    def is_submitted(s):
        if session.quiz_type == "option2":
            return isinstance(s.answer_order, dict) and len(s.answer_order.get("scores", {})) > 0
        return s.answer_order is not None

    def get_progress_info(s):
        if session.quiz_type == "option2":
            if isinstance(s.answer_order, dict) and "scores" in s.answer_order:
                count = len(s.answer_order["scores"])
                return f"Đã làm {count}/10 bài"
            return "Chưa làm bài nào"
        return ""

    return jsonify({
        "code": code,
        "quiz_type": session.quiz_type,
        "total_steps": total_steps,
        "students": [
            {
                "id": s.id,
                "name": s.name,
                "score": s.score,
                "submitted": is_submitted(s),
                "progress_text": get_progress_info(s)
            }
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
    return jsonify({"active": True, "code": session.code, "quiz_type": session.quiz_type})


# ─── POST /quiz/reset ────────────────────────────────────────────
@quiz_bp.post("/reset")
def reset_student():
    data = request.get_json(force=True, silent=True) or {}
    student_id = data.get("student_id")
    if not student_id:
        abort(400, description="Thiếu student_id")

    student = Student.query.filter_by(id=student_id).first()
    if not student:
        abort(404, description="Không tìm thấy học viên")

    student.score = 0
    student.answer_order = None
    db.session.commit()

    return jsonify({"ok": True, "message": "Đã reset bài làm thành công"})
