from fastapi import APIRouter, Depends, Request, Form
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from database import SessionLocal,get_db
from models.collection import Collection
from fastapi import HTTPException
from fastapi.responses import RedirectResponse,HTMLResponse
from starlette.status import HTTP_303_SEE_OTHER


router = APIRouter(tags=["Colleccio"])
templates = Jinja2Templates(directory="templates")

# Dependency to get the database session

    
@router.get("/collections/{collection_id}")
def get_collection_details(request: Request,collection_id: int, db: Session = Depends(get_db)):
    collection = db.query(Collection).filter(Collection.id == collection_id).first()

    if not collection:
        return RedirectResponse(url="/", status_code=HTTP_303_SEE_OTHER)

    return templates.TemplateResponse("collection_detail.html", {"request": request, "collection": collection})


@router.post("/collections/add")
def add_collection(request: Request, name: str = Form(...), description: str = Form(...), db: Session = Depends(get_db)):
    new_collection = Collection(name=name, description=description)
    db.add(new_collection)
    db.commit()
    
    request.session["message"] = "La col·lecció s'ha afegit correctament!"
    request.session["message_type"] = "success"  # Verd
    
    return RedirectResponse(url="/", status_code=HTTP_303_SEE_OTHER)

@router.get("/")
def read_collections(request: Request, db: Session = Depends(get_db)):
    collections = db.query(Collection).all()
    message = request.session.pop("message", None)
    message_type = request.session.pop("message_type", None)

    return templates.TemplateResponse(
        "index.html", 
        {"request": request, "collections": collections, "message": message, "message_type": message_type}
    )


@router.post("/collections/delete/{collection_id}")
def delete_collection(collection_id: int, db: Session = Depends(get_db)):
    collection = db.query(Collection).filter(Collection.id == collection_id).first()
    if collection:
        db.delete(collection)
        db.commit()
    return RedirectResponse(url="/", status_code=HTTP_303_SEE_OTHER)


@router.get("/collections/edit/{collection_id}", response_class=HTMLResponse)
async def edit_collection(request: Request, collection_id: int, db: Session = Depends(get_db)):
    collection = db.query(Collection).filter(Collection.id == collection_id).first()
    if collection is None:
        raise HTTPException(status_code=404, detail="Collection not found")
    
    return templates.TemplateResponse("edit_collection.html", {"request": request, "collection": collection})

@router.post("/collections/edit/{collection_id}")
def update_collection(
    request: Request,
    collection_id: int, 
    name: str = Form(...), 
    description: str = Form(...), 
    db: Session = Depends(get_db)
):
    collection = db.query(Collection).filter(Collection.id == collection_id).first()
    if collection is None:
        raise HTTPException(status_code=404, detail="Collection not found")
    
    if collection is None:
        message = "Error: La col·lecció no s'ha trobat."
        message_type = "danger"  # ALERT (vermell)
        return templates.TemplateResponse("edit_collection.html", {"request": request,"collection":collection,  "message": message, "message_type": message_type})

    if not name or not description:
        message = "Atenció: El nom i la descripció no poden estar buits."
        message_type = "warning"  # INFO (groc)
        return templates.TemplateResponse("edit_collection.html", {"request": request, "collection": collection, "message": message, "message_type": message_type})

    
    
    collection.name = name
    collection.description = description
    db.commit()

    message = "La col·lecció s'ha actualitzat correctament!"
    message_type = "success"  # SUCCESS (verd)
    
    return templates.TemplateResponse("edit_collection.html", {"request": request, "collection": collection, "message": message, "message_type": message_type})

