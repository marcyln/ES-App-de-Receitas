
from app.core.database import Base, engine
from app import models  # Importa os models para registrá-los com o Base

def reset_database():
    print("🔁 Removendo todas as tabelas...")
    Base.metadata.drop_all(bind=engine)

    print("✅ Recriando todas as tabelas...")
    Base.metadata.create_all(bind=engine)

    print("✅ Banco de dados resetado com sucesso.")

if __name__ == "__main__":
    reset_database()