from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlmodel import SQLModel

# URL do banco de dados SQLite
DATABASE_URL = "sqlite:///./main.db"

# Criação do engine
engine = create_engine(DATABASE_URL, echo=True, connect_args={"check_same_thread": False})

# Sessão do banco de dados
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base para os modelos
Base = declarative_base()
def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()