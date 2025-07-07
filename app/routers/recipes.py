# app/routers/recipes.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app import schemas, models, crud
from app.core.database import get_db
from app.core.auth import get_current_user
from app.models import User
from app.models import UserRole



router = APIRouter()

@router.get("/", response_model=List[schemas.RecipeOut])
def list_recipes(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return crud.get_recipes(db, skip=skip, limit=limit)

@router.post("/", response_model=schemas.RecipeOut)
def create_recipe(
    recipe_in: schemas.RecipeCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if current_user.role not in [UserRole.chef_verified, UserRole.admin]:
        raise HTTPException(status_code=403, detail="Apenas chefs verificados ou administradores podem criar receitas.")

    recipe = models.Recipe(
        title=recipe_in.title,
        ingredients=recipe_in.ingredients,
        preparation=recipe_in.preparation,
        preparation_time_minutes=recipe_in.preparation_time_minutes,
        author_id=current_user.id
    )

    db.add(recipe)
    db.commit()
    db.refresh(recipe)
    return recipe

@router.get("/{recipe_id}", response_model=schemas.RecipeOut)
def get_recipe(recipe_id: int, db: Session = Depends(get_db)):
    recipe = crud.get_recipe(db, recipe_id)
    if not recipe:
        raise HTTPException(status_code=404, detail="Receita não encontrada.")
    return recipe
