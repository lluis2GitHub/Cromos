from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session

# Ruta per a la base de dades SQLite
DATABASE_URL = "sqlite:///./collections.db"  # Pots canviar el nom del fitxer segons les teves necessitats

# Crear l'engine de la base de dades
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

# Crear la sessió
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base de les classes del model
Base = declarative_base()

# Funció per obtenir la sessió de la base de dades
def get_db() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
