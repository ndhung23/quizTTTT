from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from app.routes import auth, quiz
from app.db.database import Base, engine
import os

# Auto-create all tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="DENSO Quiz System")

# CORS - allows frontend fetch to work
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files (images 1-7.png are at root, serve from there)
# Images are in the project root - we expose them under /static
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
app.mount("/images", StaticFiles(directory=ROOT_DIR), name="images")

templates = Jinja2Templates(directory="app/templates")

# Include routers
app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(quiz.router, prefix="/quiz", tags=["quiz"])


# ── Page routes ──────────────────────────────
@app.get("/")
def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


@app.get("/dashboard")
def dashboard_page(request: Request):
    return templates.TemplateResponse("dashboard.html", {"request": request})


@app.get("/quiz-page")
def quiz_student_page(request: Request):
    return templates.TemplateResponse("quiz.html", {"request": request})
