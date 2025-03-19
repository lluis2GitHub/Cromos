from sqlalchemy.orm import Session
from models.collection import Collection,Team

def get_collection(db: Session, collection_id: int):
    return db.query(Collection).filter(Collection.id == collection_id).first()

def get_all_collections(db: Session):
    return db.query(Collection).all()

def create_collection(db: Session, name: str, description: str):
    new_collection = Collection(name=name, description=description)
    db.add(new_collection)
    db.commit()
    db.refresh(new_collection)
    return new_collection

def update_collection(db: Session, collection_id: int, name: str, description: str):
    collection = get_collection(db, collection_id)
    if collection:
        collection.name = name
        collection.description = description
        db.commit()
        db.refresh(collection)
    return collection

def delete_collection(db: Session, collection_id: int):
    collection = get_collection(db, collection_id)
    if collection:
        db.delete(collection)
        db.commit()
    return collection

def create_team(db: Session, name: str, role: str):
    # Comprovem si l'equip ja existeix en la base de dades per nom (o qualsevol altra propietat única)
    existing_team = db.query(Team).filter(Team.name == name).first()
    
    if existing_team:
        raise ValueError(f"L'equip amb nom {name} ja existeix")

    # Si no existeix, creem el nou equip
    new_team = Team(name=name, role=role)
    
    # Afegim l'equip a la base de dades
    db.add(new_team)
    db.commit()
    db.refresh(new_team)  # Per assegurar-nos que el nou equip té l'ID genera
    
def add_team_to_collection(db: Session, team_id: int, collection_id: int):
    team = db.query(Team).filter(Team.id == team_id).first()
    if not team:
        raise ValueError(f"Equip amb ID {team_id} no trobat")

    collection = db.query(Collection).filter(Collection.id == collection_id).first()
    if not collection:
        raise ValueError(f"Col·lecció amb ID {collection_id} no trobada")

    # Establir la relació afegint l'equip a la col·lecció
    collection.teams.append(team)

    db.commit()  # Guardem els canvis
    db.refresh(collection)  # Opcional, per obtenir la col·lecció actualitzada

    return collection

def create_team_and_add_to_collection(db: Session, name: str, role: str, collection_id: int):
    # Primer, intentem crear l'equip
    try:
        new_team = create_team(db, name, role)
    except ValueError as e:
        # Si l'equip ja existeix, es pot retornar un missatge d'error
        raise HTTPException(status_code=400, detail=str(e))
    
    # Després, afegir l'equip a la col·lecció
    collection = add_team_to_collection(db, new_team.id, collection_id)
    
    return new_team, collection