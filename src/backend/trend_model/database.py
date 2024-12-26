from sqlalchemy import create_engine, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

# Carregar variáveis de ambiente
load_dotenv()

# Acessar as variáveis do banco de dados
DATABASE_URL = os.getenv("DATABASE_URL")

# Criar engine de conexão
engine = create_engine(DATABASE_URL)

# Base para modelos SQLAlchemy
Base = declarative_base()

# Criar sessões para o banco de dados
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Função para obter uma sessão de banco de dados
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
