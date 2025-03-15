from sqlalchemy.orm import Session
from models.teams import Team
from models.collection import Collection
from models.player import Player
from fastapi import HTTPException

def get_teams_by_collection(db: Session, collection_id: int):
    """Retorna tots els equips associats a una col·lecció."""
    return db.query(Team).filter(Team.collection_id == collection_id).all()

def get_team_by_id(db: Session, team_id: int):
    """Retorna un equip per ID."""
    team = db.query(Team).filter(Team.id == team_id).first()
    if not team:
        raise HTTPException(status_code=404, detail="Equip no trobat")
    return team

def add_team(db: Session, collection_id: int, name: str, role: str):
    """Afegeix un nou equip a una col·lecció si no està duplicat."""
    existing_team = db.query(Team).filter(Team.collection_id == collection_id, Team.name == name).first()
    
    if existing_team:
        return {"message": f"L'equip '{name}' ja existeix en aquesta col·lecció.", "message_type": "danger"}

    new_team = Team(name=name, role=role, collection_id=collection_id)
    db.add(new_team)
    db.commit()
    return {"message": f"L'equip '{name}' s'ha afegit correctament!", "message_type": "success"}

def edit_team(db: Session, team_id: int, name: str, role: str):
    """Edita la informació d'un equip existent."""
    team = db.query(Team).filter(Team.id == team_id).first()
    if not team:
        raise HTTPException(status_code=404, detail="Equip no trobat")

    team.name = name
    team.role = role
    db.commit()
    return team

def delete_team(db: Session, team_id: int):
    """Elimina un equip."""
    team = db.query(Team).filter(Team.id == team_id).first()
    if not team:
        raise HTTPException(status_code=404, detail="Equip no trobat")

    collection_id = team.collection_id
    db.delete(team)
    db.commit()
    return collection_id

def get_team_players(db: Session, team_id: int):
    """Retorna tots els jugadors d'un equip."""
    return db.query(Player).filter(Player.team_id == team_id).all()
