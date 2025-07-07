from fastapi import FastAPI
from app.routers import debug, auth, favorites, recipes, comments, users, verification
from app.core.database import Base, engine

import app.models  # Garante que todos os models sejam registrados

# Criação das tabelas
Base.metadata.create_all(bind=engine)
print("Tabelas criadas ou já existentes.")

# Inicialização da aplicação
app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "API funcionando!"}

# Registro das rotas
app.include_router(debug.router, prefix="/debug", tags=["Debug"])
app.include_router(auth.router, prefix="/auth", tags=["Auth"])
app.include_router(comments.router, prefix="/comments", tags=["Comments"])
app.include_router(favorites.router, prefix="/favorites", tags=["Favorites"])
app.include_router(recipes.router, prefix="/recipes", tags=["Recipes"])
app.include_router(users.router, prefix="/users", tags=["Users"])
app.include_router(verification.router, prefix="/verification", tags=["Verification"])