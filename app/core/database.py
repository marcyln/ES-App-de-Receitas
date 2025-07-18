# app/core/database.py
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base, Session
from app.core.config import settings

DATABASE_URL = os.getenv("DB_URL")

engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# ✅ Função que faltava
def get_db():
    db: Session = SessionLocal()
    try:
        yield db
    finally:
        db.close()
