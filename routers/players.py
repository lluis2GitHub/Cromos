from fastapi import APIRouter, Depends, Form, Request, HTTPException
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from database.database import get_db


from repository.players import (
    get_team, get_players_by_team, get_player, create_player, update_player, delete_player
)

router = APIRouter(tags=["players"])
templates = Jinja2Templates(directory="templates")

# 🔍 Llistar jugadors d'un equip
@router.get("/players/{team_id}")
def list_players(request: Request, team_id: int, collection_id: int = None, db: Session = Depends(get_db)):
    team = get_team(db, team_id)
    if not team:
        raise HTTPException(status_code=404, detail="Equip no trobat")

    players = get_players_by_team(db, team_id,collection_id)
    return templates.TemplateResponse("players.html", {
        "request": request,
        "team": team,
        "players": players,
  })

# ➕ Afegir un jugador
@router.post("/players/add/{team_id}")
def add_player(request: Request, team_id: int, name: str = Form(...), position: str = Form(...), db: Session = Depends(get_db)):
    new_player = create_player(db, team_id, name, position)
    
    if new_player:
        message = f"Jugador '{name}' afegit correctament!"
        message_type = "success"
    else:
        message = f"El jugador '{name}' ja existeix en aquest equip."
        message_type = "danger"

    return RedirectResponse(url=f"/players/{team_id}?message={message}&message_type={message_type}", status_code=303)

# 📝 Formulari per editar jugador
@router.get("/players/edit/{player_id}")
def edit_player_form(request: Request, player_id: int, db: Session = Depends(get_db)):
    player = get_player(db, player_id)
    if not player:
        raise HTTPException(status_code=404, detail="Jugador no trobat")

    return templates.TemplateResponse("edit_player.html", {
        "request": request,
        "player": player
    })

# ✅ Editar un jugador
@router.post("/players/edit/{player_id}")
def edit_player(player_id: int, name: str = Form(...), position: str = Form(...), db: Session = Depends(get_db)):
    player = update_player(db, player_id, name, position)
    if not player:
        raise HTTPException(status_code=404, detail="Jugador no trobat")

    return RedirectResponse(url=f"/players/{player.team_id}", status_code=303)

# ❌ Eliminar jugador
@router.post("/players/delete/{player_id}")
def delete_player_route(player_id: int, db: Session = Depends(get_db)):
    team_id = delete_player(db, player_id)
    if team_id is None:
        raise HTTPException(status_code=404, detail="Jugador no trobat")

    return RedirectResponse(url=f"/players/{team_id}", status_code=303)
