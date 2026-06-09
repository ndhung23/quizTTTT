import os
from fastapi import FastAPI
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from app.routes import auth, quiz

app = FastAPI(title="DENSO Quiz System")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve step images (1.png – 7.png) from project root under /images/
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
app.mount("/images", StaticFiles(directory=ROOT_DIR), name="images")

# API routers
app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(quiz.router, prefix="/quiz", tags=["quiz"])

TEMPLATES = os.path.join(os.path.dirname(__file__), "templates")


@app.on_event("startup")
def startup():
    """Create DB tables on startup — runs AFTER engine is created."""
    from app.db.database import Base, engine, SessionLocal
    from app.models.user import User
    try:
        Base.metadata.create_all(bind=engine)
        print("✅ Database tables ready")
    except Exception as e:
        print(f"⚠️  DB init warning: {e}")
        return

    # Seed tài khoản mặc định nếu bảng users chưa có dữ liệu
    db = SessionLocal()
    try:
        if db.query(User).count() == 0:
            seed_users = [
                User(username="admin",   password="123", role="admin"),
                User(username="hv90122", password="123", role="teacher"),
                User(username="hv10921", password="123", role="teacher"),
            ]
            db.add_all(seed_users)
            db.commit()
            print("✅ Seeded 3 default users (admin, hv90122, hv10921)")
        else:
            print("ℹ️  Users table already has data — skip seed")
    except Exception as e:
        db.rollback()
        print(f"⚠️  Seed warning: {e}")
    finally:
        db.close()


# ── Page routes ──────────────────────────────────────────────────
@app.get("/")
def login_page():
    return FileResponse(os.path.join(TEMPLATES, "login.html"))

@app.get("/dashboard")
def dashboard_page():
    return FileResponse(os.path.join(TEMPLATES, "dashboard.html"))

@app.get("/quiz-page")
def quiz_student_page():
    return FileResponse(os.path.join(TEMPLATES, "quiz.html"))
