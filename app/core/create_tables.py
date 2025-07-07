# create_tables.py

from app.core.database import Base, engine
# 👇 Importa os models explicitamente para garantir que eles sejam registrados
from app import models

print("Criando todas as tabelas no banco de dados...")
Base.metadata.create_all(bind=engine)
print("✅ Tabelas criadas com sucesso.")
