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
    "5": 2,
    "6": 4,
    "7": 4,
    "8": 5,
    "9": 10
}


def gen_code(length: int = 6) -> str:
    return "".join(random.choices(string.digits, k=length))


# ─── POST /quiz/start ────────────────────────────────────────────
@quiz_bp.post("/start")
def start_quiz():
    data = request.get_json(force=True, silent=True) or {}
    quiz_type = data.get("quiz_type", "option1")

    from app.models.quiz_option import QuizOption
    # Allow option2 (hardcoded) or any custom/seeded option registered in the DB
    if quiz_type != "option2" and not QuizOption.query.filter_by(code=quiz_type).first():
        quiz_type = "option1"

    # Fetch user based on username passed from frontend
    username = data.get("username")
    from app.models.user import User
    user = None
    if username:
        user = User.query.filter_by(username=username).first()

    # Deactivate only this user's previous sessions
    if user:
        QuizSession.query.filter_by(user_id=user.id).update({"is_active": False})
    else:
        QuizSession.query.filter_by(user_id=None).update({"is_active": False})
    db.session.commit()

    code = gen_code()
    while QuizSession.query.filter_by(code=code).first():
        code = gen_code()

    session = QuizSession(code=code, is_active=True, quiz_type=quiz_type, user_id=user.id if user else None)
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
        import copy
        ao = copy.deepcopy(student.answer_order)
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
        from app.models.quiz_option import QuizOption
        from app.models.quiz_step import QuizStep

        # Fetch option
        option = QuizOption.query.filter_by(code=session.quiz_type).first()
        if not option:
            abort(404, description="Không tìm thấy cấu hình đề thi")

        steps = QuizStep.query.filter_by(option_id=option.id).order_by(QuizStep.step_num).all()
        steps_dict = {s.step_num: s for s in steps}
        total_steps = len(steps)

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
            if step_num not in steps_dict:
                continue

            correct_step = steps_dict[step_num]

            # Dynamic text comparison logic (avoids hardcoding equivalence groups)
            img_ok = False
            if img and img in steps_dict:
                img_ok = (steps_dict[img].image_url == correct_step.image_url)

            left_ok = False
            if left and left in steps_dict:
                left_ok = (steps_dict[left].left_text == correct_step.left_text)

            right_ok = False
            if right and right in steps_dict:
                right_ok = (steps_dict[right].right_text == correct_step.right_text)

            note_ok = False
            if note and note in steps_dict:
                note_ok = (steps_dict[note].note_text == correct_step.note_text)

            reason_ok = False
            if reason and reason in steps_dict:
                reason_ok = (steps_dict[reason].reason_text == correct_step.reason_text)

            if img_ok and left_ok and right_ok and note_ok and reason_ok:
                score += 1

        student.answer_order = answer_order
        student.score = score
        db.session.commit()

        return jsonify({"done": True, "score": score, "total": total_steps})


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
        from app.models.quiz_option import QuizOption
        from app.models.quiz_step import QuizStep
        option = QuizOption.query.filter_by(code=session.quiz_type).first()
        if option:
            total_steps = QuizStep.query.filter_by(option_id=option.id).count()
        else:
            total_steps = 23

    def is_submitted(s):
        if session.quiz_type == "option2":
            return isinstance(s.answer_order, dict) and len(s.answer_order.get("scores", {})) > 0
        return s.answer_order is not None

    def get_progress_info(s):
        if session.quiz_type == "option2":
            if isinstance(s.answer_order, dict) and "scores" in s.answer_order:
                count = len(s.answer_order["scores"])
                return f"Đã làm {count}/9 bài"
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
                "progress_text": get_progress_info(s),
                "answer_order": s.answer_order
            }
            for s in students
        ],
    })


# ─── GET /quiz/active ────────────────────────────────────────────
@quiz_bp.get("/active")
def get_active():
    username = request.args.get("username", "").strip()
    
    session = None
    if username:
        from app.models.user import User
        user = User.query.filter_by(username=username).first()
        if user:
            session = (
                QuizSession.query
                .filter_by(is_active=True, user_id=user.id)
                .order_by(QuizSession.id.desc())
                .first()
            )
    
    # Fallback to general active session if no username provided or not found
    if not session:
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


# ─── QUIZ DEFINTION & CRUD ROUTES ────────────────────────────────
@quiz_bp.get("/definition/<string:quiz_type>")
def get_definition(quiz_type):
    from app.models.quiz_option import QuizOption
    from app.models.quiz_step import QuizStep

    option = QuizOption.query.filter_by(code=quiz_type).first()
    if not option:
        abort(404, description="Đề thi không tồn tại hoặc chưa được định nghĩa")

    steps = QuizStep.query.filter_by(option_id=option.id).order_by(QuizStep.step_num).all()
    
    return jsonify({
        "title": option.title,
        "code": option.code,
        "is_custom": option.is_custom,
        "steps": [
            {
                "id": s.id,
                "step_num": s.step_num,
                "image_url": s.image_url,
                "left_text": s.left_text or "",
                "right_text": s.right_text or "",
                "note_text": s.note_text or "",
                "reason_text": s.reason_text or ""
            }
            for s in steps
        ]
    })


@quiz_bp.get("/options")
def get_options():
    from app.models.quiz_option import QuizOption
    options = QuizOption.query.all()
    # Add Option 2 dynamically so it appears in list but is read-only
    result = [
        {
            "id": opt.id,
            "title": opt.title,
            "code": opt.code,
            "is_custom": opt.is_custom
        } for opt in options
    ]
    # Check if option2 is in the database, otherwise list it as system read-only
    if not any(x["code"] == "option2" for x in result):
        result.append({
            "id": 9999,
            "title": "Kiểm tra TIE",
            "code": "option2",
            "is_custom": False
        })
    return jsonify(result)


@quiz_bp.post("/options")
def create_option():
    from app.models.quiz_option import QuizOption
    data = request.get_json(force=True)
    title = (data.get("title") or "").strip()
    code = (data.get("code") or "").strip().lower()

    if not title or not code:
        return jsonify({"ok": False, "message": "Tiêu đề và mã đề thi không được để trống"}), 400

    if code == "option2":
        return jsonify({"ok": False, "message": "Không thể dùng mã 'option2' vì đây là mã bảo lưu hệ thống"}), 400

    existing = QuizOption.query.filter_by(code=code).first()
    if existing:
        return jsonify({"ok": False, "message": f"Mã đề thi '{code}' đã tồn tại"}), 400

    option = QuizOption(title=title, code=code, is_custom=True)
    db.session.add(option)
    db.session.commit()
    return jsonify({"ok": True, "message": "Tạo đề thi mới thành công", "option_id": option.id})


@quiz_bp.put("/options/<int:option_id>")
def update_option(option_id):
    from app.models.quiz_option import QuizOption
    option = QuizOption.query.get(option_id)
    if not option:
        return jsonify({"ok": False, "message": "Đề thi không tồn tại"}), 404

    if not option.is_custom and option.code == "option1":
        # Allow editing Title for Option 1, but keep code unchanged
        data = request.get_json(force=True)
        title = (data.get("title") or "").strip()
        if title:
            option.title = title
            db.session.commit()
            return jsonify({"ok": True, "message": "Cập nhật tiêu đề đề thi thành công"})
        return jsonify({"ok": False, "message": "Tiêu đề không được trống"}), 400

    if not option.is_custom:
        return jsonify({"ok": False, "message": "Không thể sửa đổi cấu hình hệ thống mặc định"}), 400

    data = request.get_json(force=True)
    title = (data.get("title") or "").strip()
    code = (data.get("code") or "").strip().lower()

    if not title or not code:
        return jsonify({"ok": False, "message": "Tiêu đề và mã không được để trống"}), 400

    if code != option.code:
        existing = QuizOption.query.filter_by(code=code).first()
        if existing:
            return jsonify({"ok": False, "message": f"Mã đề thi '{code}' đã tồn tại"}), 400
        option.code = code

    option.title = title
    db.session.commit()
    return jsonify({"ok": True, "message": "Cập nhật đề thi thành công"})


@quiz_bp.delete("/options/<int:option_id>")
def delete_option(option_id):
    from app.models.quiz_option import QuizOption
    option = QuizOption.query.get(option_id)
    if not option:
        return jsonify({"ok": False, "message": "Đề thi không tồn tại"}), 404

    if not option.is_custom:
        return jsonify({"ok": False, "message": "Không thể xóa đề thi hệ thống"}), 400

    db.session.delete(option)
    db.session.commit()
    return jsonify({"ok": True, "message": "Xóa đề thi thành công"})


@quiz_bp.get("/options/<int:option_id>/steps")
def get_option_steps(option_id):
    from app.models.quiz_step import QuizStep
    steps = QuizStep.query.filter_by(option_id=option_id).order_by(QuizStep.step_num).all()
    return jsonify([
        {
            "id": s.id,
            "step_num": s.step_num,
            "image_url": s.image_url or "",
            "left_text": s.left_text or "",
            "right_text": s.right_text or "",
            "note_text": s.note_text or "",
            "reason_text": s.reason_text or ""
        }
        for s in steps
    ])


@quiz_bp.post("/options/<int:option_id>/steps")
def add_option_step(option_id):
    from app.models.quiz_option import QuizOption
    from app.models.quiz_step import QuizStep

    option = QuizOption.query.get(option_id)
    if not option:
        return jsonify({"ok": False, "message": "Đề thi không tồn tại"}), 404

    data = request.get_json(force=True)
    
    # Calculate next step_num
    max_step = db.session.query(db.func.max(QuizStep.step_num)).filter_by(option_id=option_id).scalar() or 0
    next_step_num = max_step + 1

    step = QuizStep(
        option_id=option_id,
        step_num=next_step_num,
        image_url=data.get("image_url") or "",
        left_text=data.get("left_text") or "",
        right_text=data.get("right_text") or "",
        note_text=data.get("note_text") or "",
        reason_text=data.get("reason_text") or ""
    )
    db.session.add(step)
    db.session.commit()
    return jsonify({"ok": True, "message": "Thêm bước mới thành công", "step_id": step.id})


@quiz_bp.put("/steps/<int:step_id>")
def update_step(step_id):
    from app.models.quiz_step import QuizStep
    step = QuizStep.query.get(step_id)
    if not step:
        return jsonify({"ok": False, "message": "Bước không tồn tại"}), 404

    data = request.get_json(force=True)
    step.image_url = data.get("image_url") or ""
    step.left_text = data.get("left_text") or ""
    step.right_text = data.get("right_text") or ""
    step.note_text = data.get("note_text") or ""
    step.reason_text = data.get("reason_text") or ""

    db.session.commit()
    return jsonify({"ok": True, "message": "Cập nhật bước thành công"})


@quiz_bp.delete("/steps/<int:step_id>")
def delete_step(step_id):
    from app.models.quiz_step import QuizStep
    step = QuizStep.query.get(step_id)
    if not step:
        return jsonify({"ok": False, "message": "Bước không tồn tại"}), 404

    option_id = step.option_id
    deleted_num = step.step_num

    db.session.delete(step)
    db.session.commit()

    # Reorder steps
    remaining_steps = QuizStep.query.filter_by(option_id=option_id).order_by(QuizStep.step_num).all()
    for idx, s in enumerate(remaining_steps):
        s.step_num = idx + 1
    db.session.commit()

    return jsonify({"ok": True, "message": "Xóa bước thành công"})


@quiz_bp.post("/upload-image")
def upload_image():
    import os
    from werkzeug.utils import secure_filename
    from flask import current_app

    if 'file' not in request.files:
        return jsonify({"ok": False, "message": "Không tìm thấy file tải lên"}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({"ok": False, "message": "Chưa chọn file"}), 400

    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}
    def allowed_file(filename):
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        # Ensure unique name
        uploads_dir = os.path.join(current_app.root_path, "static", "uploads")
        os.makedirs(uploads_dir, exist_ok=True)
        
        base, ext = os.path.splitext(filename)
        counter = 1
        while os.path.exists(os.path.join(uploads_dir, filename)):
            filename = f"{base}_{counter}{ext}"
            counter += 1

        file.save(os.path.join(uploads_dir, filename))
        return jsonify({"ok": True, "image_url": f"/static/uploads/{filename}"})

    return jsonify({"ok": False, "message": "Định dạng file không được hỗ trợ (chỉ chấp nhận png, jpg, jpeg, gif, webp)"}), 400

