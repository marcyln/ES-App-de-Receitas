from sqlalchemy.orm import Session
from app import models, schemas
from typing import List, Optional
from app.core.security import get_password_hash, verify_password

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def create_user(db: Session, user: schemas.UserCreate):
    hashed_pw = get_password_hash(user.password)
    db_user = models.User(
        full_name=user.full_name,
        email=user.email,
        hashed_password=hashed_pw,
        role=user.role
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def authenticate_user(db: Session, email: str, password: str):
    user = get_user_by_email(db, email)
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user

# Usuários

def get_user(db: Session, user_id: int) -> Optional[models.User]:
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_user_by_email(db: Session, email: str) -> Optional[models.User]:
    return db.query(models.User).filter(models.User.email == email).first()

def get_users(db: Session, skip: int = 0, limit: int = 100) -> List[models.User]:
    return db.query(models.User).offset(skip).limit(limit).all()

def create_user(db: Session, user_in: schemas.UserCreate, hashed_password: str) -> models.User:
    db_user = models.User(
        full_name=user_in.full_name,
        email=user_in.email,
        hashed_password=hashed_password,
        bio=user_in.bio or "",
        profile_image=user_in.profile_image,
        role=user_in.role
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def update_user(db: Session, user_id: int, user_in: schemas.UserUpdate) -> Optional[models.User]:
    user = get_user(db, user_id)
    if not user:
        return None

    if user_in.full_name is not None:
        user.full_name = user_in.full_name
    if user_in.email is not None:
        user.email = user_in.email
    if user_in.bio is not None:
        user.bio = user_in.bio
    if user_in.profile_image is not None:
        user.profile_image = user_in.profile_image
    if user_in.password is not None:
        user.hashed_password = get_password_hash(user_in.password)

    db.commit()
    db.refresh(user)
    return user

# Receitas

def get_recipe(db: Session, recipe_id: int) -> Optional[models.Recipe]:
    return db.query(models.Recipe).filter(models.Recipe.id == recipe_id).first()

def get_recipes(db: Session, skip: int = 0, limit: int = 100) -> List[models.Recipe]:
    return db.query(models.Recipe).offset(skip).limit(limit).all()

def create_recipe(db: Session, recipe_in: schemas.RecipeCreate, author_id: int) -> models.Recipe:
    db_recipe = models.Recipe(
        title=recipe_in.title,
        ingredients=recipe_in.ingredients,
        preparation=recipe_in.preparation,
        preparation_time_minutes=recipe_in.preparation_time_minutes,
        author_id=author_id,
    )
    db.add(db_recipe)
    db.commit()
    db.refresh(db_recipe)
    return db_recipe

# Autenticação (já deve ter, mas só pra referência)
def authenticate_user(db: Session, email: str, password: str) -> Optional[models.User]:
    user = get_user_by_email(db, email)
    if not user:
        return None
    from app.core.security import verify_password
    if not verify_password(password, user.hashed_password):
        return None
    return user

# Comentários

def get_comments_by_recipe(db: Session, recipe_id: int):
    return db.query(models.Comment).filter(models.Comment.recipe_id == recipe_id).all()

def create_comment(db: Session, comment_in: schemas.CommentCreate, user_id: int):
    db_comment = models.Comment(
        content=comment_in.content,
        recipe_id=comment_in.recipe_id,
        user_id=user_id,
    )
    db.add(db_comment)
    db.commit()
    db.refresh(db_comment)
    return db_comment

# Favoritos

def get_favorites_by_user(db: Session, user_id: int):
    return db.query(models.FavoriteRecipe).filter(models.FavoriteRecipe.user_id == user_id).all()

def create_favorite(db: Session, favorite_in: schemas.FavoriteRecipeCreate, user_id: int):
    # Checar se já existe para evitar duplicata (opcional)
    exists = db.query(models.FavoriteRecipe).filter(
        models.FavoriteRecipe.user_id == user_id,
        models.FavoriteRecipe.recipe_id == favorite_in.recipe_id
    ).first()
    if exists:
        return exists
    db_favorite = models.FavoriteRecipe(
        user_id=user_id,
        recipe_id=favorite_in.recipe_id,
    )
    db.add(db_favorite)
    db.commit()
    db.refresh(db_favorite)
    return db_favorite

def delete_favorite(db: Session, favorite_id: int, user_id: int) -> bool:
    fav = db.query(models.FavoriteRecipe).filter(
        models.FavoriteRecipe.id == favorite_id,
        models.FavoriteRecipe.user_id == user_id
    ).first()
    if not fav:
        return False
    db.delete(fav)
    db.commit()
    return True