from fastapi import APIRouter
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from app.config import USERS

router = APIRouter()


class LoginReq(BaseModel):
    username: str
    password: str


@router.post("/login")
def login(data: LoginReq):
    expected = USERS.get(data.username.strip())
    if expected and expected == data.password:
        return JSONResponse({"ok": True, "username": data.username, "message": "Đăng nhập thành công"})
    return JSONResponse(
        status_code=401,
        content={"ok": False, "message": "Tên đăng nhập hoặc mật khẩu không đúng"},
    )
