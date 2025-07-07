from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app import crud, schemas, models
from app.core.database import get_db
from app.core.security import create_access_token, get_password_hash
from app.core.auth import get_current_user, get_current_admin_user
from app.models import User

router = APIRouter()

@router.get("/admin-only")
async def admin_area(current_admin: User = Depends(get_current_admin_user)):
    return {"msg": f"Bem-vindo, administrador {current_admin.full_name}!"}

@router.post("/signup", response_model=schemas.UserOut, status_code=status.HTTP_201_CREATED)
async def signup(user_in: schemas.UserCreate, db: Session = Depends(get_db)):
    if crud.get_user_by_email(db, user_in.email):
        raise HTTPException(status_code=400, detail="Email já cadastrado.")
    hashed_password = get_password_hash(user_in.password)
    user = crud.create_user(db, user_in, hashed_password)
    return user

@router.post("/login", response_model=schemas.Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = crud.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Credenciais inválidas")
    access_token = create_access_token(data={"sub": str(user.id)})
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/me", response_model=schemas.UserOut)
async def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user
