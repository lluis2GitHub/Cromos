from database.core import engine, Base, SessionLocal

# Crear les taules a la base de dades (si no existeixen)
Base.metadata.create_all(bind=engine)

# Funció per obtenir una sessió de la base de dades
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
