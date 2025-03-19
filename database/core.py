# core.py (o database/core.py)
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "sqlite:///./collectionsV2.db"  # Canvia el nom si cal

# Crear motor de base de dades
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

# Crear Base per als models
Base = declarative_base()

# Crear sessió per a la base de dades
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
