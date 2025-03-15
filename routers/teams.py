from fastapi import APIRouter, Depends, Form, Request
from sqlalchemy.orm import Session
from database.database import get_db
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from repository import teams as team_repository

router = APIRouter(tags=["teams"])
templates = Jinja2Templates(directory="templates")

@router.get("/teams/{collection_id}")
def list_teams(request: Request, collection_id: int, db: Session = Depends(get_db)):
    collection_teams = team_repository.get_teams_by_collection(db, collection_id)
    return templates.TemplateResponse("teams.html", {
        "request": request,
        "teams": collection_teams
    })

@router.post("/teams/add/{collection_id}")
def add_team(request: Request, collection_id: int, name: str = Form(...), role: str = Form(...), db: Session = Depends(get_db)):
    result = team_repository.add_team(db, collection_id, name, role)
    collection_teams = team_repository.get_teams_by_collection(db, collection_id)
    return templates.TemplateResponse("teams.html", {
        "request": request,
        "teams": collection_teams,
        "message": result["message"],
        "message_type": result["message_type"]
    })

@router.get("/teams/detail/{team_id}")
def team_detail(request: Request, team_id: int, db: Session = Depends(get_db)):
    team = team_repository.get_team_by_id(db, team_id)
    players = team_repository.get_team_players(db, team_id)
    return templates.TemplateResponse("team_detail.html", {
        "request": request,
        "team": team,
        "players": players
    })
