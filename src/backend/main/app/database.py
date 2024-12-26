from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from fastapi import Depends
from sqlalchemy.orm import Session
from dotenv import load_dotenv
import os

load_dotenv()

# Configuração do banco de dados (exemplo com PostgreSQL)
DATABASE_URL = os.getenv('DATABASE_URL')

# Criação do engine de conexão
engine = create_engine(DATABASE_URL)

# Criação da base para os modelos
Base = declarative_base()

# Criando a sessão
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Função para obter uma sessão de banco de dados
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
