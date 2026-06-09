from fastapi import APIRouter
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from app.config import ADMIN_EMAIL, ADMIN_PASSWORD

router = APIRouter()


class LoginReq(BaseModel):
    email: str
    password: str


@router.post("/login")
def login(data: LoginReq):
    if data.email == ADMIN_EMAIL and data.password == ADMIN_PASSWORD:
        return JSONResponse({"ok": True, "message": "Đăng nhập thành công"})
    return JSONResponse(
        status_code=401,
        content={"ok": False, "message": "Email hoặc mật khẩu không đúng"},
    )
