from fastapi import APIRouter, Depends, Form, Request
from sqlalchemy.orm import Session
from models.collection import Collection,Team,Player
from database.database import get_db
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi import HTTPException

router = APIRouter(tags=["Teams"],prefix="/teams")
templates = Jinja2Templates(directory="templates")

# Recuperar tots els equips per ordre alfabètic
@router.get("/", name="list_teams")
def list_teams(request: Request, db: Session = Depends(get_db)):
    # Obtenim tots els equips ordenats per nom en ordre alfabètic
    teams = db.query(Team).order_by(Team.name).all()
    # Retornem la plantilla amb la informació dels equips
 ##   return templates.TemplateResponse("teams_detail.html", {
    message = request.session.pop("message", None)
    message_type = request.session.pop("message_type", None)


    return templates.TemplateResponse(
        "teams.html",        
        {"request": request,
        "teams": teams, 
        "message": message, "message_type": message_type}
    )

    
# Afegir un equip - Formulari
#@router.get("/add/{collection_id}")
#def add_team_form(request: Request, collection_id: int, db: Session = Depends(get_db)):
#    collection = db.query(Collection).filter(Collection.id == collection_id).first()
#    if not collection:
#        raise HTTPException(status_code=404, detail="Col·lecció no trobada")
#    
#    return templates.TemplateResponse("add_team.html", {
#        "request": request,
#        "collection": collection
#    })


# Afegir un equip - Mètode POST
@router.post("/add")
def add_team(request: Request, name: str = Form(...), role: str = Form(...), db: Session = Depends(get_db)):
###    existing_team = db.query(Team).filter(Team.collection_id == collection_id, Team.name == name).first()
    existing_team = db.query(Team).filter(Team.name == name).first()

    if existing_team:
        message = f"L'equip '{name}' ja existeix en aquesta col·lecció."
        message_type = "danger"  # ALERTA (vermell)
    else:
       # Si no existeix, creem el nou equip
        new_team = Team(name=name, role=role)
        db.add(new_team)
        db.commit()
        db.refresh(new_team)  # Per assegurar-nos que el nou equip té l'ID generat
       
        message = f"L'equip '{name}' s'ha afegit correctament!"
        message_type = "success"  # ÈXIT (verd)

    return RedirectResponse(url="/teams", status_code=303)


# Editar un equip - Formulari
@router.get("/edit/{team_id}")
def edit_team_form(request: Request, team_id: int, db: Session = Depends(get_db)):
    team = db.query(Team).filter(Team.id == team_id).first()
    if not team:
        raise HTTPException(status_code=404, detail="Equip no trobat")
    
    return templates.TemplateResponse("team_edit.html", {
        "request": request,
        "team": team
    })

# Editar un equip - Mètode POST
@router.post("/edit/{team_id}")
def edit_team(request: Request, team_id: int, name: str = Form(...), 
              role: str = Form(...), db: Session = Depends(get_db)):
    team = db.query(Team).filter(Team.id == team_id).first()
    if not team:
        raise HTTPException(status_code=404, detail="Equip no trobat")

    team.name = name
    team.role = role
    db.commit()

    return templates.TemplateResponse("team_edit.html", {
        "request": request,
        "team": team
    })

# Eliminar un equip
@router.post("/delete/{team_id}")
def delete_team(request: Request, team_id: int, db: Session = Depends(get_db)):
    team = db.query(Team).filter(Team.id == team_id).first()
    if not team:
        request.session["message"] = "La col·lecció s'ha esborrat correctament!"
        request.session["message_type"] = "success"
        ##raise HTTPException(status_code=404, detail="Equip no trobat")
        return RedirectResponse(url="/", status_code=404)
    team_id = team.id
    db.delete(team)
    db.commit()

    request.session["message"] = "La col·lecció s'ha afegit correctament!"
    request.session["message_type"] = "success"
    
    return RedirectResponse(url="/teams", status_code=303)

@router.get("/detail/{team_id}")
def team_detail(request: Request, team_id: int, db: Session = Depends(get_db)):
    team = db.query(Team).filter(Team.id == team_id).first()
    
    if not team:
        raise HTTPException(status_code=404, detail="Equip no trobat")

    return templates.TemplateResponse("team_detail.html", {
        "request": request,
        "team": team,
    })
    
