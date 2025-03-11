from fastapi import APIRouter, Depends, Form, Request
from sqlalchemy.orm import Session
from models.teams import Team
from models.collection import Collection
from models.player import Player
from database import get_db
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi import HTTPException

router = APIRouter(tags=["teams"])
templates = Jinja2Templates(directory="templates")

# Afegir un equip - Formulari
@router.get("/teams/add/{collection_id}")
def add_team_form(request: Request, collection_id: int, db: Session = Depends(get_db)):
    collection = db.query(Collection).filter(Collection.id == collection_id).first()
    if not collection:
        raise HTTPException(status_code=404, detail="Col·lecció no trobada")
    
    return templates.TemplateResponse("add_team.html", {
        "request": request,
        "collection": collection
    })

# Afegir un equip - Mètode POST
@router.post("/teams/add/{collection_id}")
def add_team(request: Request, collection_id: int, name: str = Form(...), role: str = Form(...), db: Session = Depends(get_db)):
    existing_team = db.query(Team).filter(Team.collection_id == collection_id, Team.name == name).first()
    
    if existing_team:
        message = f"L'equip '{name}' ja existeix en aquesta col·lecció."
        message_type = "danger"  # ALERTA (vermell)
    else:
        # Afegir el nou equip si no és duplicat
        new_team = Team(name=name, role=role, collection_id=collection_id)
        db.add(new_team)
        db.commit()
        
        message = f"L'equip '{name}' s'ha afegit correctament!"
        message_type = "success"  # ÈXIT (verd)

    # Retornar a la pàgina de detall de la col·lecció amb el missatge
    collection = db.query(Collection).filter(Collection.id == collection_id).first()
    teams = db.query(Team).filter(Team.collection_id == collection_id).all()

    return templates.TemplateResponse("collection_detail.html", {
        "request": request,
        "collection": collection,
        "teams": teams,
        "message": message,
        "message_type": message_type
    })

# Editar un equip - Formulari
@router.get("/teams/edit/{team_id}")
def edit_team_form(request: Request, team_id: int, db: Session = Depends(get_db)):
    team = db.query(Team).filter(Team.id == team_id).first()
    if not team:
        raise HTTPException(status_code=404, detail="Equip no trobat")
    
    return templates.TemplateResponse("edit_team.html", {
        "request": request,
        "team": team
    })

# Editar un equip - Mètode POST
@router.post("/teams/edit/{team_id}")
def edit_team(request: Request, team_id: int, name: str = Form(...), role: str = Form(...), db: Session = Depends(get_db)):
    team = db.query(Team).filter(Team.id == team_id).first()
    if not team:
        raise HTTPException(status_code=404, detail="Equip no trobat")

    team.name = name
    team.role = role
    db.commit()

    return RedirectResponse(url=f"/collections/{team.collection_id}", status_code=303)

# Eliminar un equip
@router.post("/teams/delete/{team_id}")
def delete_team(request: Request, team_id: int, db: Session = Depends(get_db)):
    team = db.query(Team).filter(Team.id == team_id).first()
    if not team:
        raise HTTPException(status_code=404, detail="Equip no trobat")

    collection_id = team.collection_id
    db.delete(team)
    db.commit()

    return RedirectResponse(url=f"/collections/{collection_id}", status_code=303)


@router.get("/teams/detail/{team_id}")
def team_detail(request: Request, team_id: int, db: Session = Depends(get_db)):
    team = db.query(Team).filter(Team.id == team_id).first()
    
    if not team:
        raise HTTPException(status_code=404, detail="Equip no trobat")

    players = db.query(Player).filter(Player.team_id == team_id).all()

    return templates.TemplateResponse("team_detail.html", {
        "request": request,
        "team": team,
        "players": players
    })
    

@router.get("/teams/{collection_id}")
def list_teams(request: Request, collection_id: int, db: Session = Depends(get_db)):
    # Obtenim la col·lecció
    collection = db.query(Collection).filter(Collection.id == collection_id).first()
    if not collection:
        raise HTTPException(status_code=404, detail="Col·lecció no trobada")

    # Obtenim tots els equips associats a la col·lecció
    teams = db.query(Team).filter(Team.collection_id == collection_id).all()

    # Retornem la plantilla amb la informació
    return templates.TemplateResponse("teams.html", {
        "request": request,
        "collection": collection,
        "teams": teams
    })