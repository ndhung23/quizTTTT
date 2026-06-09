from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.db.database import Base

class Deck(Base):
    __tablename__ = "decks"

    id = Column(Integer, primary_key=True)
    title = Column(String)

    user_id = Column(Integer, ForeignKey("users.id"))
