from sqlalchemy.orm import Session
from models.player import Player
from models.teams import Team

def get_collection_id_by_team_id(db: Session, team_id: int):
    team = db.query(Team).filter(Team.id == team_id).first()  # Obtenir l'equip per ID
    if team:
        return team.collection_id  # Retorna el collection_id associat
    return None  # Si no troba l'equip, retorna None

def get_players_by_team(db: Session, team_id: int, collection_id: int):
    query = db.query(Player).filter(Player.team_id == team_id)

    if collection_id:
        query = query.filter(Player.collection_id == collection_id)  # Filtrar per collection_id si es passa

    return query.all()


def get_team(db: Session, team_id: int):
    return db.query(Team).filter(Team.id == team_id).first()

def get_players_by_team(db: Session, team_id: int, collection_id: int):
    return db.query(Player).filter(Player.team_id == team_id).all()

def get_player(db: Session, player_id: int):
    return db.query(Player).filter(Player.id == player_id).first()

def create_player(db: Session, team_id: int, name: str, position: str):
    # 🔍 Recupera l'equip per obtenir el collection_id
    team = db.query(Team).filter(Team.id == team_id).first()
    if not team:
        raise ValueError("Equip no trobat")

    # 🔄 Comprova si el jugador ja existeix en aquest equip
    existing_player = db.query(Player).filter(
        Player.team_id == team_id,
        Player.name == name
    ).first()

    if existing_player:
        return {"error": f"El jugador '{name}' ja està registrat en aquest equip."}

    # ✅ Assignem el collection_id correctament
    new_player = Player(
        name=name,
        position=position,
        team_id=team_id,
        collection_id=team.collection_id  # 🔥 Això evita el problema de `None`
    )

    db.add(new_player)
    db.commit()
    db.refresh(new_player)

    return new_player

def create_player_old(db: Session, name: str, position: str, team_id: int):
    collection_id = get_collection_id_by_team_id(db, team_id)

    existing_player = db.query(Player).filter(Player.team_id == team_id, Player.name == name).first()
    if existing_player:
        return None  # Indica que ja existeix un jugador amb aquest nom en l'equip
    
    new_player = Player(name=name, position=position, team_id=team_id, collection_id=collection_id)
    db.add(new_player)
    db.commit()
    db.refresh(new_player)
    return new_player

def update_player(db: Session, player_id: int, name: str, position: str):
    player = get_player(db, player_id)
    if player:
        player.name = name
        player.position = position
        db.commit()
        db.refresh(player)
    return player

def delete_player(db: Session, player_id: int):
    player = get_player(db, player_id)
    if player:
        team_id = player.team_id
        db.delete(player)
        db.commit()
        return team_id  # Retorna l'ID de l'equip per redirigir correctament
    return None
