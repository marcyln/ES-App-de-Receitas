# app/routers/favorites.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app import schemas, models, crud
from app.core.database import get_db
from app.core.auth import get_current_user

router = APIRouter()

@router.get("/", response_model=List[schemas.FavoriteRecipeOut])
def get_user_favorites(db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    return crud.get_favorites_by_user(db, current_user.id)

@router.post("/", response_model=schemas.FavoriteRecipeOut)
def add_favorite(favorite_in: schemas.FavoriteRecipeCreate, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    # opcional: checar se já existe para evitar duplicata
    return crud.create_favorite(db, favorite_in, current_user.id)

@router.delete("/{favorite_id}")
def remove_favorite(favorite_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    success = crud.delete_favorite(db, favorite_id, current_user.id)
    if not success:
        raise HTTPException(status_code=404, detail="Favorito não encontrado ou você não tem permissão para deletar.")
    return {"detail": "Favorito removido com sucesso"}
