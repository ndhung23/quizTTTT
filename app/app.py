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
    from app.db.database import Base, engine
    try:
        Base.metadata.create_all(bind=engine)
        print("✅ Database tables ready")
    except Exception as e:
        print(f"⚠️  DB init warning: {e}")


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
