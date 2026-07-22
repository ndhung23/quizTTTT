import random
import string
import os

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
    if quiz_type:
        import unicodedata
        quiz_type = unicodedata.normalize('NFC', str(quiz_type))

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
        return jsonify({
            "ok": True,
            "student_id": existing.id,
            "session_id": session.id,
            "quiz_type": session.quiz_type,
            "message": "Tái kết nối",
            "tab_switch_count": existing.tab_switch_count or 0
        })

    student = Student(name=name, score=0, session_id=session.id)
    db.session.add(student)
    db.session.commit()

    return jsonify({"ok": True, "student_id": student.id, "session_id": session.id, "quiz_type": session.quiz_type, "message": "Tham gia thành công"})


# ─── POST /quiz/submit ───────────────────────────────────────────
@quiz_bp.post("/submit")
def submit_quiz():
    import os
    data = request.get_json(force=True)
    student_id = data.get("student_id")

    student = Student.query.filter_by(id=student_id).first()
    if not student:
        abort(404, description="Không tìm thấy học viên")

    session = QuizSession.query.filter_by(id=student.session_id).first()
    if not session:
        abort(404, description="Không tìm thấy phòng thi")

    from app.models.quiz_option import QuizOption
    from app.models.quiz_step import QuizStep

    import unicodedata
    q_type_norm = unicodedata.normalize('NFC', session.quiz_type) if session.quiz_type else ""
    option = QuizOption.query.filter_by(code=q_type_norm).first()

    def safe_int(val):
        try:
            return int(float(str(val).strip()))
        except Exception:
            return 0

    def safe_float(val, default=1.0):
        try:
            return float(str(val).strip())
        except Exception:
            return default

    if option and option.quiz_format == "option5":
        answers = data.get("matching_answers", {})
        steps = QuizStep.query.filter_by(option_id=option.id).order_by(QuizStep.step_num).all()
        valid_ids = {str(step.id): step for step in steps}
        score = 0
        for step in steps:
            selected_id = str(answers.get(str(step.id), ""))
            selected = valid_ids.get(selected_id)
            if selected and selected.id == step.id:
                score += 1

        student.score = score
        student.answer_order = {"matching_answers": answers}
        db.session.commit()
        return jsonify({"done": True, "score": score, "total": len(steps)})

    if option and option.quiz_format == "option3":
        device_answers = data.get("device_answers", [])
        quality_answers = data.get("quality_answers", [])

        steps = QuizStep.query.filter_by(option_id=option.id).order_by(QuizStep.step_num).all()
        device_steps = [s for s in steps if s.step_num <= 16]
        quality_steps = [s for s in steps if s.step_num > 16]

        device_score = 0
        for i in range(16):
            if i < 2:
                device_score += 1
            else:
                user_text = str(device_answers[i]).strip().lower() if i < len(device_answers) and device_answers[i] else ""
                correct_text = device_steps[i].left_text.strip().lower() if i < len(device_steps) and device_steps[i].left_text else ""
                if user_text == correct_text and correct_text:
                    device_score += 1

        quality_score = 0
        for j in range(20):
            if j < 2:
                quality_score += 1
            else:
                user_text = str(quality_answers[j]).strip().lower() if j < len(quality_answers) and quality_answers[j] else ""
                correct_text = quality_steps[j].left_text.strip().lower() if j < len(quality_steps) and quality_steps[j].left_text else ""
                if user_text == correct_text and correct_text:
                    quality_score += 1

        total_score = device_score + quality_score
        student.score = total_score
        student.answer_order = {
            "device_answers": device_answers,
            "quality_answers": quality_answers,
            "device_score": device_score,
            "quality_score": quality_score
        }
        db.session.commit()
        return jsonify({
            "done": True,
            "score": total_score,
            "total": 36,
            "device_score": device_score,
            "quality_score": quality_score
        })

    elif option and option.quiz_format == "option4":
        odd_answers = data.get("odd_answers", {})
        even_answers = data.get("even_answers", {})

        steps = QuizStep.query.filter_by(option_id=option.id).order_by(QuizStep.step_num).all()
        # Ensure we have at least 26 steps seeded
        if len(steps) < 26:
            abort(500, description="Dữ liệu đáp án chưa hoàn thiện (cần 26 bước)")

        # ─── ODD TEST SCORING (Topics 1, 3, 5, 7) ───
        odd_score = 0
        odd_max = 0

        # Topic 1: steps 1..4 (steps[0..3]) - Quantity x weight (with custom penalties)
        t1_ans = odd_answers.get("t1", [])
        for i in range(4):
            correct_q = safe_int(steps[i].left_text)
            weight = safe_int(steps[i].reason_text) if steps[i].reason_text else 2
            entered_q = safe_int(t1_ans[i]) if i < len(t1_ans) else 0
            pen_def = safe_float(steps[i].right_text, 1.0)
            pen_exc = safe_float(steps[i].note_text, 1.0)
            if entered_q < correct_q:
                row_score = max(0.0, float(correct_q) - float(correct_q - entered_q) * pen_def)
            elif entered_q > correct_q:
                row_score = max(0.0, float(correct_q) - float(entered_q - correct_q) * pen_exc)
            else:
                row_score = float(correct_q)
            odd_score += row_score * weight
            odd_max += correct_q * weight

        # Topic 3: steps 9..12 (steps[8..11]) - Loc, Stat, Quant x weight
        t3_ans = odd_answers.get("t3", [])
        for i in range(4):
            step = steps[8 + i]
            correct_loc = step.left_text.strip().lower() if step.left_text else ""
            correct_stat = step.right_text.strip().lower() if step.right_text else ""
            correct_q = safe_int(step.note_text)
            weight = safe_int(step.reason_text) if step.reason_text else 1

            user_ans = t3_ans[i] if i < len(t3_ans) else {}
            user_loc = str(user_ans.get("loc", "")).strip().lower()
            user_stat = str(user_ans.get("stat", "")).strip().lower()
            user_q = safe_int(user_ans.get("quant", 0))

            if user_loc == correct_loc and user_stat == correct_stat:
                if user_q <= correct_q:
                    row_score = user_q
                else:
                    row_score = max(0, 2 * correct_q - user_q)
            else:
                row_score = 0
            odd_score += row_score * weight
            odd_max += correct_q * weight

        # Topic 5: steps 17..20 (steps[16..19]) - Loc, Stat x weight
        t5_ans = odd_answers.get("t5", [])
        for i in range(4):
            step = steps[16 + i]
            correct_loc = step.left_text.strip().lower() if step.left_text else ""
            correct_stat = step.right_text.strip().lower() if step.right_text else ""
            weight = safe_int(step.reason_text) if step.reason_text else 1

            user_ans = t5_ans[i] if i < len(t5_ans) else {}
            user_loc = str(user_ans.get("loc", "")).strip().lower()
            user_stat = str(user_ans.get("stat", "")).strip().lower()

            if user_loc == correct_loc and user_stat == correct_stat:
                odd_score += weight
            odd_max += weight

        # Topic 7: step 25 (steps[24]) - Image, Quant x weight
        t7_ans = odd_answers.get("t7", {})
        step = steps[24]
        correct_img = os.path.basename(step.image_url.strip().replace("\\", "/")) if step.image_url else ""
        correct_q = safe_int(step.left_text)
        weight = safe_int(step.reason_text) if step.reason_text else 1

        user_img = os.path.basename(str(t7_ans.get("image_url", "")).strip().replace("\\", "/"))
        user_q = safe_int(t7_ans.get("quant", 0))

        t7_score = 0
        if user_img == correct_img and correct_img:
            if user_q <= correct_q:
                t7_score = user_q
            else:
                t7_score = max(0, 2 * correct_q - user_q)
            odd_score += t7_score * weight
        odd_max += correct_q * weight

        # ─── EVEN TEST SCORING (Topics 2, 4, 6, 8) ───
        even_score = 0
        even_max = 0

        # Topic 2: steps 5..8 (steps[4..7]) - Quantity x weight (with custom penalties)
        t2_ans = even_answers.get("t2", [])
        for i in range(4):
            correct_q = safe_int(steps[4 + i].left_text)
            weight = safe_int(steps[4 + i].reason_text) if steps[4 + i].reason_text else 2
            entered_q = safe_int(t2_ans[i]) if i < len(t2_ans) else 0
            pen_def = safe_float(steps[4 + i].right_text, 1.0)
            pen_exc = safe_float(steps[4 + i].note_text, 1.0)
            if entered_q < correct_q:
                row_score = max(0.0, float(correct_q) - float(correct_q - entered_q) * pen_def)
            elif entered_q > correct_q:
                row_score = max(0.0, float(correct_q) - float(entered_q - correct_q) * pen_exc)
            else:
                row_score = float(correct_q)
            even_score += row_score * weight
            even_max += correct_q * weight

        # Topic 4: steps 13..16 (steps[12..15]) - Loc, Stat, Quant x weight
        t4_ans = even_answers.get("t4", [])
        for i in range(4):
            step = steps[12 + i]
            correct_loc = step.left_text.strip().lower() if step.left_text else ""
            correct_stat = step.right_text.strip().lower() if step.right_text else ""
            correct_q = safe_int(step.note_text)
            weight = safe_int(step.reason_text) if step.reason_text else 1

            user_ans = t4_ans[i] if i < len(t4_ans) else {}
            user_loc = str(user_ans.get("loc", "")).strip().lower()
            user_stat = str(user_ans.get("stat", "")).strip().lower()
            user_q = safe_int(user_ans.get("quant", 0))

            if user_loc == correct_loc and user_stat == correct_stat:
                if user_q <= correct_q:
                    row_score = user_q
                else:
                    row_score = max(0, 2 * correct_q - user_q)
            else:
                row_score = 0
            even_score += row_score * weight
            even_max += correct_q * weight

        # Topic 6: steps 21..24 (steps[20..23]) - Loc, Stat x weight
        t6_ans = even_answers.get("t6", [])
        for i in range(4):
            step = steps[20 + i]
            correct_loc = step.left_text.strip().lower() if step.left_text else ""
            correct_stat = step.right_text.strip().lower() if step.right_text else ""
            weight = safe_int(step.reason_text) if step.reason_text else 1

            user_ans = t6_ans[i] if i < len(t6_ans) else {}
            user_loc = str(user_ans.get("loc", "")).strip().lower()
            user_stat = str(user_ans.get("stat", "")).strip().lower()

            if user_loc == correct_loc and user_stat == correct_stat:
                even_score += weight
            even_max += weight

        # Topic 8: step 26 (steps[25]) - Image, Quant x weight
        t8_ans = even_answers.get("t8", {})
        step = steps[25]
        correct_img = os.path.basename(step.image_url.strip().replace("\\", "/")) if step.image_url else ""
        correct_q = safe_int(step.left_text)
        weight = safe_int(step.reason_text) if step.reason_text else 1

        user_img = os.path.basename(str(t8_ans.get("image_url", "")).strip().replace("\\", "/"))
        user_q = safe_int(t8_ans.get("quant", 0))

        t8_score = 0
        if user_img == correct_img and correct_img:
            if user_q <= correct_q:
                t8_score = user_q
            else:
                t8_score = max(0, 2 * correct_q - user_q)
            even_score += t8_score * weight
        even_max += correct_q * weight

        total_score = odd_score + even_score
        total_max = odd_max + even_max
        student.score = int(round(total_score))
        student.answer_order = {
            "odd_answers": odd_answers,
            "even_answers": even_answers,
            "odd_score": odd_score,
            "even_score": even_score,
            "odd_max": odd_max,
            "even_max": even_max
        }
        db.session.commit()
        return jsonify({
            "done": True,
            "score": total_score,
            "total": total_max,
            "odd_score": odd_score,
            "even_score": even_score,
            "odd_max": odd_max,
            "even_max": even_max
        })

    elif session.quiz_type == "option2":
        sub_quiz_id = str(data.get("sub_quiz_id"))
        sub_score = data.get("sub_score", 0)
        answers = data.get("answers", {})

        # Check and initialize answer_order structure
        import copy
        ao = copy.deepcopy(student.answer_order)
        if not isinstance(ao, dict):
            ao = {"scores": {}, "answers": {}}
        if "scores" not in ao:
            ao["scores"] = {}
        if "answers" not in ao:
            ao["answers"] = {}

        ao["scores"][sub_quiz_id] = sub_score
        ao["answers"][sub_quiz_id] = answers
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
        # Fetch option
        import unicodedata
        q_type_norm = unicodedata.normalize('NFC', session.quiz_type) if session.quiz_type else ""
        option = QuizOption.query.filter_by(code=q_type_norm).first()
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
                placed_img_url = steps_dict[img].image_url or ""
                correct_img_url = correct_step.image_url or ""
                if not correct_img_url.strip():
                    img_ok = not placed_img_url.strip()
                else:
                    img_ok = (placed_img_url == correct_img_url)

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

    from app.models.quiz_option import QuizOption
    from app.models.quiz_step import QuizStep
    import unicodedata
    q_type_norm = unicodedata.normalize('NFC', session.quiz_type) if session.quiz_type else ""
    option = QuizOption.query.filter_by(code=q_type_norm).first()

    def safe_int(val):
        try:
            return int(float(str(val).strip()))
        except Exception:
            return 0

    def fmt_score(val):
        try:
            val_f = float(val)
            if val_f.is_integer():
                return str(int(val_f))
            return f"{val_f:.2f}".rstrip('0').rstrip('.')
        except Exception:
            return str(val)

    if option:
        if option.quiz_format == "option5":
            total_steps = QuizStep.query.filter_by(option_id=option.id).count()
        elif option.quiz_format == "option3":
            total_steps = 36
        elif option.quiz_format == "option4":
            steps = QuizStep.query.filter_by(option_id=option.id).order_by(QuizStep.step_num).all()
            if len(steps) >= 26:
                odd_max = 0
                even_max = 0
                for i in range(4):
                    odd_max += safe_int(steps[i].left_text) * (safe_int(steps[i].reason_text) if steps[i].reason_text else 2)
                    even_max += safe_int(steps[4 + i].left_text) * (safe_int(steps[4 + i].reason_text) if steps[4 + i].reason_text else 2)
                    odd_max += safe_int(steps[8 + i].note_text) * (safe_int(steps[8 + i].reason_text) if steps[8 + i].reason_text else 1)
                    even_max += safe_int(steps[12 + i].note_text) * (safe_int(steps[12 + i].reason_text) if steps[12 + i].reason_text else 1)
                    odd_max += safe_int(steps[16 + i].reason_text) if steps[16 + i].reason_text else 1
                    even_max += safe_int(steps[20 + i].reason_text) if steps[20 + i].reason_text else 1
                odd_max += safe_int(steps[24].left_text) * (safe_int(steps[24].reason_text) if steps[24].reason_text else 1)
                even_max += safe_int(steps[25].left_text) * (safe_int(steps[25].reason_text) if steps[25].reason_text else 1)
                total_steps = odd_max + even_max
            else:
                total_steps = 84
        else:
            total_steps = QuizStep.query.filter_by(option_id=option.id).count()
    elif session.quiz_type == "option2":
        total_steps = sum(SUB_QUIZ_MAX_SCORES.values())
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
        if option and option.quiz_format == "option3":
            if isinstance(s.answer_order, dict) and "device_score" in s.answer_order:
                ds = s.answer_order["device_score"]
                qs = s.answer_order["quality_score"]
                return f"Trang 1: {ds}/16đ, Trang 2: {qs}/20đ"
            return "Chưa nộp"
        if option and option.quiz_format == "option4":
            if isinstance(s.answer_order, dict) and "odd_score" in s.answer_order:
                os_ = s.answer_order["odd_score"]
                es_ = s.answer_order["even_score"]
                o_max = s.answer_order.get("odd_max", 42)
                e_max = s.answer_order.get("even_max", 42)
                return f"Đề lẻ: {fmt_score(os_)}/{fmt_score(o_max)}đ, Đề chẵn: {fmt_score(es_)}/{fmt_score(e_max)}đ"
            return "Chưa nộp"
        return ""

    return jsonify({
        "code": code,
        "quiz_type": session.quiz_type,
        "quiz_format": option.quiz_format if option else "option1",
        "total_steps": total_steps,
        "students": [
            {
                "id": s.id,
                "name": s.name,
                "score": s.score,
                "submitted": is_submitted(s),
                "progress_text": get_progress_info(s),
                "answer_order": s.answer_order,
                "tab_switch_count": s.tab_switch_count or 0
            }
            for s in students
        ],
    })


# ─── GET /quiz/student-detail/<int:student_id> ─────────────────────
@quiz_bp.get("/student-detail/<int:student_id>")
def get_student_detail(student_id):
    student = Student.query.filter_by(id=student_id).first()
    if not student:
        abort(404, description="Không tìm thấy học viên")
    
    session = QuizSession.query.filter_by(id=student.session_id).first()
    if not session:
        abort(404, description="Không tìm thấy phòng thi")

    import unicodedata
    q_type_norm = unicodedata.normalize('NFC', session.quiz_type) if session.quiz_type else ""

    if q_type_norm == "option2":
        scores = student.answer_order.get("scores", {}) if isinstance(student.answer_order, dict) else {}
        sub_quiz_max = {
            "1": 5, "2": 7, "3": 5, "4": 5, "5": 2, "6": 4, "7": 4, "8": 5, "9": 10
        }
        report = []
        for k in sorted(sub_quiz_max.keys(), key=int):
            earned = scores.get(k, 0)
            max_val = sub_quiz_max[k]
            report.append({
                "sub_quiz": f"Bài {k}",
                "earned": earned,
                "max": max_val,
                "is_dat": earned > 0 and earned == max_val
            })
        answers = student.answer_order.get("answers", {}) if isinstance(student.answer_order, dict) else {}
        return jsonify({
            "quiz_format": "option2",
            "quiz_title": "Kiểm tra TIE",
            "student_name": student.name,
            "score": student.score,
            "report": report,
            "student_answers": answers
        })

    from app.models.quiz_option import QuizOption
    from app.models.quiz_step import QuizStep
    option = QuizOption.query.filter_by(code=q_type_norm).first()
    if not option:
        abort(404, description="Không tìm thấy cấu hình đề thi")

    steps = QuizStep.query.filter_by(option_id=option.id).order_by(QuizStep.step_num).all()
    steps_dict = {s.step_num: s for s in steps}

    def safe_int(val):
        try:
            return int(float(str(val).strip()))
        except Exception:
            return 0

    def safe_float(val, default=1.0):
        try:
            return float(str(val).strip())
        except Exception:
            return default

    # Prepare detail report
    if option.quiz_format == "option5":
        answers = student.answer_order.get("matching_answers", {}) if isinstance(student.answer_order, dict) else {}
        by_id = {str(s.id): s for s in steps}
        report = []
        for step in steps:
            selected = by_id.get(str(answers.get(str(step.id), "")))
            report.append({
                "step_num": step.step_num,
                "category": step.left_text or "",
                "correct_role": step.right_text or "",
                "student_role": selected.right_text if selected else "",
                "is_correct": bool(selected and selected.id == step.id)
            })
        return jsonify({
            "quiz_format": "option5",
            "quiz_title": option.title,
            "student_name": student.name,
            "score": student.score,
            "report": report
        })

    if option.quiz_format == "option3":
        device_answers = student.answer_order.get("device_answers", []) if isinstance(student.answer_order, dict) else []
        quality_answers = student.answer_order.get("quality_answers", []) if isinstance(student.answer_order, dict) else []
        
        device_steps = [s for s in steps if s.step_num <= 16]
        quality_steps = [s for s in steps if s.step_num > 16]
        
        device_report = []
        for i in range(16):
            correct_text = device_steps[i].left_text if i < len(device_steps) and device_steps[i].left_text else ""
            note_text = device_steps[i].note_text if i < len(device_steps) and device_steps[i].note_text else f"Bước {i+1}"
            user_text = device_answers[i] if i < len(device_answers) else ""
            
            if i < 2:
                is_correct = True
            else:
                is_correct = (str(user_text).strip().lower() == correct_text.strip().lower() and bool(correct_text))
                
            device_report.append({
                "step_num": i + 1,
                "note_text": note_text,
                "correct_val": correct_text,
                "student_val": user_text,
                "is_correct": is_correct
            })
            
        quality_report = []
        for j in range(20):
            correct_text = quality_steps[j].left_text if j < len(quality_steps) and quality_steps[j].left_text else ""
            note_text = quality_steps[j].note_text if j < len(quality_steps) and quality_steps[j].note_text else f"Bước {j+1}"
            user_text = quality_answers[j] if j < len(quality_answers) else ""
            
            if j < 2:
                is_correct = True
            else:
                is_correct = (str(user_text).strip().lower() == correct_text.strip().lower() and bool(correct_text))
                
            quality_report.append({
                "step_num": j + 17,
                "note_text": note_text,
                "correct_val": correct_text,
                "student_val": user_text,
                "is_correct": is_correct
            })
            
        return jsonify({
            "quiz_format": "option3",
            "quiz_title": option.title,
            "student_name": student.name,
            "score": student.score,
            "device_report": device_report,
            "quality_report": quality_report
        })
        
    elif option.quiz_format == "option4":
        odd_answers = student.answer_order.get("odd_answers", {}) if isinstance(student.answer_order, dict) else {}
        even_answers = student.answer_order.get("even_answers", {}) if isinstance(student.answer_order, dict) else {}
        
        if len(steps) < 26:
            return jsonify({"error": "Dữ liệu cấu hình đề thi chưa đủ 26 bước"}), 500
            
        odd_report = []
        even_report = []
        import os
        
        # Topic 1: steps 1..4 (steps[0..3])
        t1_ans = odd_answers.get("t1", [])
        for i in range(4):
            correct_q = safe_int(steps[i].left_text)
            weight = safe_int(steps[i].reason_text) if steps[i].reason_text else 2
            entered_q = safe_int(t1_ans[i]) if i < len(t1_ans) else 0
            pen_def = safe_float(steps[i].right_text, 1.0)
            pen_exc = safe_float(steps[i].note_text, 1.0)
            if entered_q < correct_q:
                row_score = max(0.0, float(correct_q) - float(correct_q - entered_q) * pen_def)
            elif entered_q > correct_q:
                row_score = max(0.0, float(correct_q) - float(entered_q - correct_q) * pen_exc)
            else:
                row_score = float(correct_q)
            earned = row_score * weight
            max_score = correct_q * weight
            odd_report.append({
                "topic": "Đề tài 1",
                "step_num": i + 1,
                "correct_val": f"Số lượng: {correct_q}",
                "student_val": f"Số lượng: {entered_q}",
                "is_correct": entered_q == correct_q,
                "earned": earned,
                "max_score": max_score
            })
            
        # Topic 3: steps 9..12 (steps[8..11])
        t3_ans = odd_answers.get("t3", [])
        for i in range(4):
            step = steps[8 + i]
            correct_loc = step.left_text.strip().lower() if step.left_text else ""
            correct_stat = step.right_text.strip().lower() if step.right_text else ""
            correct_q = safe_int(step.note_text)
            weight = safe_int(step.reason_text) if step.reason_text else 1
            
            user_ans = t3_ans[i] if i < len(t3_ans) else {}
            user_loc = str(user_ans.get("loc", "")).strip().lower()
            user_stat = str(user_ans.get("stat", "")).strip().lower()
            user_q = safe_int(user_ans.get("quant", 0))
            
            loc_stat_ok = (user_loc == correct_loc and user_stat == correct_stat)
            if loc_stat_ok:
                if user_q <= correct_q:
                    row_score = user_q
                else:
                    row_score = max(0, 2 * correct_q - user_q)
            else:
                row_score = 0
            
            earned = row_score * weight
            max_score = correct_q * weight
            odd_report.append({
                "topic": "Đề tài 3",
                "step_num": i + 9,
                "correct_val": f"Vị trí: {step.left_text or ''}, Trạng thái: {step.right_text or ''}, SL: {correct_q}",
                "student_val": f"Vị trí: {user_ans.get('loc', '')}, Trạng thái: {user_ans.get('stat', '')}, SL: {user_q}",
                "is_correct": loc_stat_ok and user_q == correct_q,
                "earned": earned,
                "max_score": max_score
            })
            
        # Topic 5: steps 17..20 (steps[16..19])
        t5_ans = odd_answers.get("t5", [])
        for i in range(4):
            step = steps[16 + i]
            correct_loc = step.left_text.strip().lower() if step.left_text else ""
            correct_stat = step.right_text.strip().lower() if step.right_text else ""
            weight = safe_int(step.reason_text) if step.reason_text else 1
            
            user_ans = t5_ans[i] if i < len(t5_ans) else {}
            user_loc = str(user_ans.get("loc", "")).strip().lower()
            user_stat = str(user_ans.get("stat", "")).strip().lower()
            
            is_correct = (user_loc == correct_loc and user_stat == correct_stat)
            earned = weight if is_correct else 0
            
            odd_report.append({
                "topic": "Đề tài 5",
                "step_num": i + 17,
                "correct_val": f"Vị trí: {step.left_text or ''}, Trạng thái: {step.right_text or ''}",
                "student_val": f"Vị trí: {user_ans.get('loc', '')}, Trạng thái: {user_ans.get('stat', '')}",
                "is_correct": is_correct,
                "earned": earned,
                "max_score": weight
            })
            
        # Topic 7: step 25 (steps[24])
        t7_ans = odd_answers.get("t7", {})
        step = steps[24]
        correct_img = os.path.basename(step.image_url.strip().replace("\\", "/")) if step.image_url else ""
        correct_q = safe_int(step.left_text)
        weight = safe_int(step.reason_text) if step.reason_text else 1
        
        user_img = os.path.basename(str(t7_ans.get("image_url", "")).strip().replace("\\", "/"))
        user_q = safe_int(t7_ans.get("quant", 0))
        
        img_ok = (user_img == correct_img and bool(correct_img))
        if img_ok:
            if user_q <= correct_q:
                row_score = user_q
            else:
                row_score = max(0, 2 * correct_q - user_q)
        else:
            row_score = 0
            
        earned = row_score * weight
        max_score = correct_q * weight
        odd_report.append({
            "topic": "Đề tài 7",
            "step_num": 25,
            "correct_val": f"Hình ảnh: {correct_img}, SL: {correct_q}",
            "student_val": f"Hình ảnh: {user_img}, SL: {user_q}",
            "is_correct": img_ok and user_q == correct_q,
            "earned": earned,
            "max_score": max_score
        })
        
        # Topic 2: steps 5..8 (steps[4..7])
        t2_ans = even_answers.get("t2", [])
        for i in range(4):
            correct_q = safe_int(steps[4 + i].left_text)
            weight = safe_int(steps[4 + i].reason_text) if steps[4 + i].reason_text else 2
            entered_q = safe_int(t2_ans[i]) if i < len(t2_ans) else 0
            pen_def = safe_float(steps[4 + i].right_text, 1.0)
            pen_exc = safe_float(steps[4 + i].note_text, 1.0)
            if entered_q < correct_q:
                row_score = max(0.0, float(correct_q) - float(correct_q - entered_q) * pen_def)
            elif entered_q > correct_q:
                row_score = max(0.0, float(correct_q) - float(entered_q - correct_q) * pen_exc)
            else:
                row_score = float(correct_q)
            earned = row_score * weight
            max_score = correct_q * weight
            even_report.append({
                "topic": "Đề tài 2",
                "step_num": i + 5,
                "correct_val": f"Số lượng: {correct_q}",
                "student_val": f"Số lượng: {entered_q}",
                "is_correct": entered_q == correct_q,
                "earned": earned,
                "max_score": max_score
            })
            
        # Topic 4: steps 13..16 (steps[12..15])
        t4_ans = even_answers.get("t4", [])
        for i in range(4):
            step = steps[12 + i]
            correct_loc = step.left_text.strip().lower() if step.left_text else ""
            correct_stat = step.right_text.strip().lower() if step.right_text else ""
            correct_q = safe_int(step.note_text)
            weight = safe_int(step.reason_text) if step.reason_text else 1
            
            user_ans = t4_ans[i] if i < len(t4_ans) else {}
            user_loc = str(user_ans.get("loc", "")).strip().lower()
            user_stat = str(user_ans.get("stat", "")).strip().lower()
            user_q = safe_int(user_ans.get("quant", 0))
            
            loc_stat_ok = (user_loc == correct_loc and user_stat == correct_stat)
            if loc_stat_ok:
                if user_q <= correct_q:
                    row_score = user_q
                else:
                    row_score = max(0, 2 * correct_q - user_q)
            else:
                row_score = 0
            
            earned = row_score * weight
            max_score = correct_q * weight
            even_report.append({
                "topic": "Đề tài 4",
                "step_num": i + 13,
                "correct_val": f"Vị trí: {step.left_text or ''}, Trạng thái: {step.right_text or ''}, SL: {correct_q}",
                "student_val": f"Vị trí: {user_ans.get('loc', '')}, Trạng thái: {user_ans.get('stat', '')}, SL: {user_q}",
                "is_correct": loc_stat_ok and user_q == correct_q,
                "earned": earned,
                "max_score": max_score
            })
            
        # Topic 6: steps 21..24 (steps[20..23])
        t6_ans = even_answers.get("t6", [])
        for i in range(4):
            step = steps[20 + i]
            correct_loc = step.left_text.strip().lower() if step.left_text else ""
            correct_stat = step.right_text.strip().lower() if step.right_text else ""
            weight = safe_int(step.reason_text) if step.reason_text else 1
            
            user_ans = t6_ans[i] if i < len(t6_ans) else {}
            user_loc = str(user_ans.get("loc", "")).strip().lower()
            user_stat = str(user_ans.get("stat", "")).strip().lower()
            
            is_correct = (user_loc == correct_loc and user_stat == correct_stat)
            earned = weight if is_correct else 0
            
            even_report.append({
                "topic": "Đề tài 6",
                "step_num": i + 21,
                "correct_val": f"Vị trí: {step.left_text or ''}, Trạng thái: {step.right_text or ''}",
                "student_val": f"Vị trí: {user_ans.get('loc', '')}, Trạng thái: {user_ans.get('stat', '')}",
                "is_correct": is_correct,
                "earned": earned,
                "max_score": weight
            })
            
        # Topic 8: step 26 (steps[25])
        t8_ans = even_answers.get("t8", {})
        step = steps[25]
        correct_img = os.path.basename(step.image_url.strip().replace("\\", "/")) if step.image_url else ""
        correct_q = safe_int(step.left_text)
        weight = safe_int(step.reason_text) if step.reason_text else 1
        
        user_img = os.path.basename(str(t8_ans.get("image_url", "")).strip().replace("\\", "/"))
        user_q = safe_int(t8_ans.get("quant", 0))
        
        img_ok = (user_img == correct_img and bool(correct_img))
        if img_ok:
            if user_q <= correct_q:
                row_score = user_q
            else:
                row_score = max(0, 2 * correct_q - user_q)
        else:
            row_score = 0
            
        earned = row_score * weight
        max_score = correct_q * weight
        even_report.append({
            "topic": "Đề tài 8",
            "step_num": 26,
            "correct_val": f"Hình ảnh: {correct_img}, SL: {correct_q}",
            "student_val": f"Hình ảnh: {user_img}, SL: {user_q}",
            "is_correct": img_ok and user_q == correct_q,
            "earned": earned,
            "max_score": max_score
        })
        
        return jsonify({
            "quiz_format": "option4",
            "quiz_title": option.title,
            "student_name": student.name,
            "score": student.score,
            "odd_report": odd_report,
            "even_report": even_report
        })
    else: # option1 or custom format
        answer_order = student.answer_order if isinstance(student.answer_order, list) else []
        report = []
        for s in steps:
            step_num = s.step_num
            user_row = None
            for row in answer_order:
                if row.get("row_idx") == step_num - 1:
                    user_row = row
                    break
            
            correct_img_url = s.image_url or ""
            correct_left = s.left_text or ""
            correct_right = s.right_text or ""
            correct_note = s.note_text or ""
            correct_reason = s.reason_text or ""
            
            if user_row:
                img_id = user_row.get("image_id")
                left_id = user_row.get("left_id")
                right_id = user_row.get("right_id")
                note_id = user_row.get("note_id")
                reason_id = user_row.get("reason_id")
                
                img_ok = False
                placed_img_url = ""
                if img_id and img_id in steps_dict:
                    placed_img_url = steps_dict[img_id].image_url or ""
                    if not correct_img_url.strip():
                        img_ok = not placed_img_url.strip()
                    else:
                        img_ok = (placed_img_url == correct_img_url)
                        
                left_ok = False
                placed_left = ""
                if left_id and left_id in steps_dict:
                    placed_left = steps_dict[left_id].left_text or ""
                    left_ok = (placed_left == correct_left)
                    
                right_ok = False
                placed_right = ""
                if right_id and right_id in steps_dict:
                    placed_right = steps_dict[right_id].right_text or ""
                    right_ok = (placed_right == correct_right)
                    
                note_ok = False
                placed_note = ""
                if note_id and note_id in steps_dict:
                    placed_note = steps_dict[note_id].note_text or ""
                    note_ok = (placed_note == correct_note)
                    
                reason_ok = False
                placed_reason = ""
                if reason_id and reason_id in steps_dict:
                    placed_reason = steps_dict[reason_id].reason_text or ""
                    reason_ok = (placed_reason == correct_reason)
            else:
                img_ok = left_ok = right_ok = note_ok = reason_ok = False
                placed_img_url = placed_left = placed_right = placed_note = placed_reason = ""
                
            report.append({
                "step_num": step_num,
                "correct": {
                    "image_url": correct_img_url,
                    "left": correct_left,
                    "right": correct_right,
                    "note": correct_note,
                    "reason": correct_reason
                },
                "student": {
                    "image_url": placed_img_url,
                    "left": placed_left,
                    "right": placed_right,
                    "note": placed_note,
                    "reason": placed_reason
                },
                "status": {
                    "image": img_ok,
                    "left": left_ok,
                    "right": right_ok,
                    "note": note_ok,
                    "reason": reason_ok,
                    "row_ok": img_ok and left_ok and right_ok and note_ok and reason_ok
                }
            })
            
        return jsonify({
            "quiz_format": option.quiz_format or "option1",
            "quiz_title": option.title,
            "student_name": student.name,
            "score": student.score,
            "report": report
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
    import urllib.parse

    # Unquote url encoded characters (like %20 for spaces)
    quiz_type_unquoted = urllib.parse.unquote(quiz_type)

    # Recover UTF-8 if decoded as latin-1 by WSGI wrapper (Vercel serverless)
    try:
        quiz_type_decoded = quiz_type_unquoted.encode('latin-1').decode('utf-8')
    except Exception:
        quiz_type_decoded = quiz_type_unquoted

    import unicodedata
    q_type_norm = unicodedata.normalize('NFC', quiz_type_decoded).strip() if quiz_type_decoded else ""
    option = QuizOption.query.filter_by(code=q_type_norm).first()
    if not option:
        abort(404, description="Đề thi không tồn tại hoặc chưa được định nghĩa")

    steps = QuizStep.query.filter_by(option_id=option.id).order_by(QuizStep.step_num).all()
    
    return jsonify({
        "title": option.title,
        "code": option.code,
        "is_custom": option.is_custom,
        "quiz_format": option.quiz_format,
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
    result = [
        {
            "id": opt.id,
            "title": opt.title,
            "code": opt.code,
            "is_custom": opt.is_custom,
            "quiz_format": opt.quiz_format
        } for opt in options
    ]
    # Check if option2 is in the database, otherwise list it as system read-only
    if not any(x["code"] == "option2" for x in result):
        result.append({
            "id": 9999,
            "title": "Kiểm tra TIE",
            "code": "option2",
            "is_custom": False,
            "quiz_format": "option2"
        })
    return jsonify(result)


@quiz_bp.post("/options")
def create_option():
    from app.models.quiz_option import QuizOption
    from app.models.quiz_step import QuizStep
    data = request.get_json(force=True)
    title = (data.get("title") or "").strip()
    code = (data.get("code") or "").strip().lower()
    if code:
        import unicodedata
        code = unicodedata.normalize('NFC', code)
    quiz_format = (data.get("quiz_format") or "option1").strip()

    if not title or not code:
        return jsonify({"ok": False, "message": "Tiêu đề và mã đề thi không được để trống"}), 400

    if code in ["option2", "option3", "option4", "option5"]:
        return jsonify({"ok": False, "message": f"Không thể dùng mã '{code}' vì đây là mã bảo lưu hệ thống"}), 400

    existing = QuizOption.query.filter_by(code=code).first()
    if existing:
        return jsonify({"ok": False, "message": f"Mã đề thi '{code}' đã tồn tại"}), 400

    option = QuizOption(title=title, code=code, is_custom=True, quiz_format=quiz_format)
    db.session.add(option)
    db.session.commit()

    # Pre-seed 26 steps if format is option4
    if quiz_format == "option4":
        for i in range(26):
            step = QuizStep(
                option_id=option.id,
                step_num=i + 1,
                image_url="/static/imgoptions4/hinh1.png" if i == 24 else ("/static/imgoptions4/hinh2.png" if i == 25 else ""),
                left_text="2" if i < 4 else ("3" if i < 8 else ""),
                right_text="",
                note_text="",
                reason_text=""
            )
            db.session.add(step)
        db.session.commit()

    # Start new basic-category quizzes with the same eight editable pairs.
    if quiz_format == "option5":
        matching_rows = [
            ("Biểu đồ quản lý công số", "Quản lý hiện trạng sản xuất đạt được hằng ngày."),
            ("Tiến độ sản xuất", "Xác nhận rõ sự tiến triển và chậm trễ của sản xuất"),
            ("Quản lý lượng tồn kho", "Phát hiện dị thường theo sự tăng giảm của lượng tồn kho"),
            ("Bản thao tác tiêu chuẩn", "Xác minh rõ về qui định thao tác"),
            ("Hiệu suất hoạt động", "Thông báo bất thường từ số sản lượng của mỗi giờ"),
            ("Bản quản lý sản lượng", "Cấu thành dây chuyền sản xuất\nCân bằng thời gian yêu cầu ở mỗi dây chuyền"),
            ("Bản kế hoạch cải tiến", "Đối sách về các vấn đề đã phát sinh trong thực tế"),
            ("Andon", "Thông báo chỉ thị thao tác, hiện trạng hoạt động của dây chuyền"),
        ]
        for idx, (category, role) in enumerate(matching_rows, start=1):
            db.session.add(QuizStep(option_id=option.id, step_num=idx, image_url="", left_text=category, right_text=role, note_text="", reason_text=""))
        db.session.commit()

    return jsonify({"ok": True, "message": "Tạo đề thi mới thành công", "option_id": option.id})


@quiz_bp.put("/options/<int:option_id>")
def update_option(option_id):
    from app.models.quiz_option import QuizOption
    option = QuizOption.query.get(option_id)
    if not option:
        return jsonify({"ok": False, "message": "Đề thi không tồn tại"}), 404

    if not option.is_custom and option.code in ["option1", "option3", "option4", "option5"]:
        # Allow editing Title, but keep code and format unchanged
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
    if code:
        import unicodedata
        code = unicodedata.normalize('NFC', code)
    quiz_format = (data.get("quiz_format") or option.quiz_format).strip()

    if not title or not code:
        return jsonify({"ok": False, "message": "Tiêu đề và mã không được để trống"}), 400

    if code != option.code:
        existing = QuizOption.query.filter_by(code=code).first()
        if existing:
            return jsonify({"ok": False, "message": f"Mã đề thi '{code}' đã tồn tại"}), 400
        option.code = code

    option.title = title
    option.quiz_format = quiz_format
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


# ─── GET /quiz/imgoptions4 ──────────────────────────────────────
@quiz_bp.get("/imgoptions4")
def list_imgoptions4():
    from flask import current_app
    img_dir = os.path.join(current_app.root_path, "static", "imgoptions4")
    if not os.path.exists(img_dir):
        return jsonify([])
    files = [f for f in os.listdir(img_dir) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.webp'))]
    return jsonify([f"/static/imgoptions4/{f}" for f in files])


# ─── PUT /quiz/options/<int:option_id>/steps-batch ─────────────
@quiz_bp.put("/options/<int:option_id>/steps-batch")
def update_steps_batch(option_id):
    from app.models.quiz_option import QuizOption
    from app.models.quiz_step import QuizStep

    option = QuizOption.query.get(option_id)
    if not option:
        return jsonify({"ok": False, "message": "Đề thi không tồn tại"}), 404

    data = request.get_json(force=True)
    steps_data = data.get("steps", [])

    for s_data in steps_data:
        step_id = s_data.get("id")
        if step_id:
            step = QuizStep.query.filter_by(id=step_id, option_id=option_id).first()
            if step:
                step.image_url = s_data.get("image_url") or ""
                step.left_text = s_data.get("left_text") or ""
                step.right_text = s_data.get("right_text") or ""
                step.note_text = s_data.get("note_text") or ""
                step.reason_text = s_data.get("reason_text") or ""

    db.session.commit()
    return jsonify({"ok": True, "message": "Cập nhật các cấu hình thành công"})


# ─── POST /quiz/tab-switch ─────────────────────────────────────────
@quiz_bp.post("/tab-switch")
def post_tab_switch():
    data = request.get_json(force=True) or {}
    student_id = data.get("student_id")
    count = data.get("count", 0)

    student = Student.query.filter_by(id=student_id).first()
    if not student:
        abort(404, description="Không tìm thấy học viên")

    student.tab_switch_count = count
    db.session.commit()
    return jsonify({"ok": True, "tab_switch_count": student.tab_switch_count})


# ─── GET /quiz/student-status/<int:student_id> ─────────────────────
@quiz_bp.get("/student-status/<int:student_id>")
def get_student_status(student_id):
    student = Student.query.filter_by(id=student_id).first()
    if not student:
        return jsonify({"ok": False, "error": "Không tìm thấy học viên"})
    return jsonify({
        "ok": True,
        "tab_switch_count": student.tab_switch_count or 0
    })

