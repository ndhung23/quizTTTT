from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.models.user import User

router = APIRouter()


class LoginReq(BaseModel):
    username: str
    password: str


@router.post("/login")
def login(data: LoginReq, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == data.username.strip()).first()
    if user and user.password == data.password:
        return JSONResponse({
            "ok": True,
            "username": user.username,
            "role": user.role,
            "message": "Đăng nhập thành công",
        })
    return JSONResponse(
        status_code=401,
        content={"ok": False, "message": "Tên đăng nhập hoặc mật khẩu không đúng"},
    )
