from fastapi import APIRouter, Request, Depends, Form, HTTPException
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from database import get_db
from repository.collections import get_collection, get_all_collections, create_collection, update_collection, delete_collection
from fastapi.templating import Jinja2Templates

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/")
def read_collections(request: Request, db: Session = Depends(get_db)):
    collections = get_all_collections(db)
    message = request.session.pop("message", None)
    message_type = request.session.pop("message_type", None)

    return templates.TemplateResponse(
        "index.html", 
        {"request": request, "collections": collections, "message": message, "message_type": message_type}
    )

@router.get("/collections/{collection_id}")
def get_collection_details(request: Request, collection_id: int, db: Session = Depends(get_db)):
    collection = get_collection(db, collection_id)
    if not collection:
        return RedirectResponse(url="/", status_code=303)

    return templates.TemplateResponse("collection_detail.html", {"request": request, "collection": collection})

@router.post("/collections/add")
def add_collection(request: Request, name: str = Form(...), description: str = Form(...), db: Session = Depends(get_db)):
    create_collection(db, name, description)
    
    request.session["message"] = "La col·lecció s'ha afegit correctament!"
    request.session["message_type"] = "success"
    
    return RedirectResponse(url="/", status_code=303)

@router.get("/collections/edit/{collection_id}")
def edit_collection(request: Request, collection_id: int, db: Session = Depends(get_db)):
    collection = get_collection(db, collection_id)
    if not collection:
        raise HTTPException(status_code=404, detail="Collection not found")

    return templates.TemplateResponse("edit_collection.html", {"request": request, "collection": collection})

@router.post("/collections/edit/{collection_id}")
def edit_collection_post(request: Request, collection_id: int, name: str = Form(...), description: str = Form(...), db: Session = Depends(get_db)):
    collection = update_collection(db, collection_id, name, description)
    if not collection:
        raise HTTPException(status_code=404, detail="Collection not found")

    request.session["message"] = "La col·lecció s'ha actualitzat correctament!"
    request.session["message_type"] = "success"

    return RedirectResponse(url="/", status_code=303)

@router.post("/collections/delete/{collection_id}")
def delete_collection_route(collection_id: int, db: Session = Depends(get_db)):
    collection = delete_collection(db, collection_id)
    if not collection:
        raise HTTPException(status_code=404, detail="Collection not found")

    return RedirectResponse(url="/", status_code=303)
