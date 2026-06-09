from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.database import SessionLocal
from app.models.deck import Deck

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/")
def create_deck(title: str, db: Session = Depends(get_db)):
    new_deck = Deck(title=title)
    db.add(new_deck)
    db.commit()
    db.refresh(new_deck)
    return new_deck

@router.get("/")
def get_decks(db: Session = Depends(get_db)):
    return db.query(Deck).all()
