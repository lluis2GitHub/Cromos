from sqlalchemy.orm import Session
from models.collection import Collection

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
