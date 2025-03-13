from fastapi import APIRouter, Depends, Form, Request
from sqlalchemy.orm import Session
from models.player import Player
from models.teams import Team
from cromos.database.database import get_db
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi import HTTPException

router = APIRouter(tags=["players"])
templates = Jinja2Templates(directory="templates")

# 🔍 Llistar jugadors d'un equip
@router.get("/players/{team_id}")
def list_players(request: Request, team_id: int, db: Session = Depends(get_db)):
    print (team_id)
    team = db.query(Team).filter(Team.id == team_id).first()
    print (team)
    print (team_id)
    if not team:
        raise HTTPException(status_code=404, detail="Equip no trobat")

    players = db.query(Player).filter(Player.team_id == team_id).all()
    return templates.TemplateResponse("players.html", {
        "request": request,
        "team": team,
        "players": players
    })

# ➕ Afegir un jugador
@router.post("/players/add/{team_id}")
def add_player(
    request: Request, 
    team_id: int, 
    name: str = Form(...), 
    position: str = Form(...), 
    db: Session = Depends(get_db)
):
    existing_player = db.query(Player).filter(Player.team_id == team_id, Player.name == name).first()
    if existing_player:
        message = f"El jugador '{name}' ja existeix en aquest equip."
        message_type = "danger"
    else:
        new_player = Player(name=name, position=position, team_id=team_id)
        db.add(new_player)
        db.commit()
        message = f"Jugador '{name}' afegit correctament!"
        message_type = "success"

    return RedirectResponse(url=f"/players/{team_id}?message={message}&message_type={message_type}", status_code=303)

# 📝 Formulari per editar jugador
@router.get("/players/edit/{player_id}")
def edit_player_form(request: Request, player_id: int, db: Session = Depends(get_db)):
    player = db.query(Player).filter(Player.id == player_id).first()
    if not player:
        raise HTTPException(status_code=404, detail="Jugador no trobat")

    return templates.TemplateResponse("edit_player.html", {
        "request": request,
        "player": player
    })

# ✅ Editar un jugador
@router.post("/players/edit/{player_id}")
def edit_player(
    player_id: int, 
    name: str = Form(...), 
    position: str = Form(...), 
    db: Session = Depends(get_db)
):
    player = db.query(Player).filter(Player.id == player_id).first()
    if player:
        player.name = name
        player.position = position
        db.commit()
    
    return RedirectResponse(url=f"/players/{player.team_id}", status_code=303)

# ❌ Eliminar jugador
@router.post("/players/delete/{player_id}")
def delete_player(player_id: int, db: Session = Depends(get_db)):
    player = db.query(Player).filter(Player.id == player_id).first()
    if player:
        team_id = player.team_id
        db.delete(player)
        db.commit()
        return RedirectResponse(url=f"/players/{team_id}", status_code=303)
    
    raise HTTPException(status_code=404, detail="Jugador no trobat")
