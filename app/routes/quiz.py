from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List
from app.db.database import get_db
from app.models.session import QuizSession
from app.models.student import Student
import random
import string

router = APIRouter()

# Correct order of steps (1-indexed image filenames)
CORRECT_ORDER = [1, 2, 3, 4, 5, 6, 7]


def gen_code(length: int = 6) -> str:
    return "".join(random.choices(string.digits, k=length))


# ─────────────────────────────────────────────
# POST /quiz/start  →  giảng viên tạo session
# ─────────────────────────────────────────────
@router.post("/start")
def start_quiz(db: Session = Depends(get_db)):
    # Deactivate all previous sessions to keep things clean (optional)
    db.query(QuizSession).update({"is_active": False})
    db.commit()

    code = gen_code()
    # Retry if collision
    while db.query(QuizSession).filter_by(code=code).first():
        code = gen_code()

    session = QuizSession(code=code, is_active=True)
    db.add(session)
    db.commit()
    db.refresh(session)

    return {"code": code, "session_id": session.id, "link": f"/quiz?code={code}"}


# ─────────────────────────────────────────────
# POST /quiz/join  →  học viên vào phòng
# ─────────────────────────────────────────────
class JoinReq(BaseModel):
    name: str
    code: str


@router.post("/join")
def join_quiz(data: JoinReq, db: Session = Depends(get_db)):
    session = db.query(QuizSession).filter_by(code=data.code, is_active=True).first()
    if not session:
        raise HTTPException(status_code=404, detail="Mã phòng không hợp lệ hoặc đã kết thúc")

    # Check duplicate name in same session
    existing = db.query(Student).filter_by(name=data.name, session_id=session.id).first()
    if existing:
        # Return existing student info so they can continue
        return {"ok": True, "student_id": existing.id, "session_id": session.id, "message": "Tái kết nối"}

    student = Student(name=data.name, score=0, session_id=session.id)
    db.add(student)
    db.commit()
    db.refresh(student)

    return {"ok": True, "student_id": student.id, "session_id": session.id, "message": "Tham gia thành công"}


# ─────────────────────────────────────────────
# POST /quiz/submit  →  học viên nộp bài
# ─────────────────────────────────────────────
class SubmitReq(BaseModel):
    student_id: int
    answer_order: List[int]   # e.g. [3,1,2,5,4,7,6]


@router.post("/submit")
def submit_quiz(data: SubmitReq, db: Session = Depends(get_db)):
    student = db.query(Student).filter_by(id=data.student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Không tìm thấy học viên")

    # Score: count positions that match correct order
    score = sum(
        1 for i, step in enumerate(data.answer_order)
        if i < len(CORRECT_ORDER) and step == CORRECT_ORDER[i]
    )
    total = len(CORRECT_ORDER)

    student.answer_order = data.answer_order
    student.score = score
    db.commit()

    return {
        "done": True,
        "score": score,
        "total": total,
        "correct_order": CORRECT_ORDER,
    }


# ─────────────────────────────────────────────
# GET /quiz/results  →  giảng viên xem kết quả
# ─────────────────────────────────────────────
@router.get("/results")
def get_results(code: str, db: Session = Depends(get_db)):
    session = db.query(QuizSession).filter_by(code=code).first()
    if not session:
        raise HTTPException(status_code=404, detail="Session không tồn tại")

    students = (
        db.query(Student)
        .filter_by(session_id=session.id)
        .order_by(Student.score.desc())
        .all()
    )

    return {
        "code": code,
        "total_steps": len(CORRECT_ORDER),
        "students": [
            {
                "id": s.id,
                "name": s.name,
                "score": s.score,
                "submitted": s.answer_order is not None,
            }
            for s in students
        ],
    }


# ─────────────────────────────────────────────
# GET /quiz/active  →  lấy session đang active
# ─────────────────────────────────────────────
@router.get("/active")
def get_active(db: Session = Depends(get_db)):
    session = db.query(QuizSession).filter_by(is_active=True).order_by(QuizSession.id.desc()).first()
    if not session:
        return {"active": False}
    return {"active": True, "code": session.code}
