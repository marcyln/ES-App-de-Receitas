# app/routers/comments.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app import schemas, models, crud
from app.core.database import get_db
from app.core.auth import get_current_user

router = APIRouter()

@router.get("/recipe/{recipe_id}", response_model=List[schemas.CommentOut])
def get_comments_for_recipe(recipe_id: int, db: Session = Depends(get_db)):
    return crud.get_comments_by_recipe(db, recipe_id)

@router.post("/", response_model=schemas.CommentOut)
def create_comment(comment_in: schemas.CommentCreate, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    return crud.create_comment(db, comment_in, current_user.id)
