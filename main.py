from fastapi import FastAPI,Request
from routers import collections,teams
###,teams,players
from database.database import engine, Base
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
from starlette.middleware.sessions import SessionMiddleware
from fastapi.templating import Jinja2Templates


# Initialize the FastAPI app
app = FastAPI()

app.add_middleware(SessionMiddleware, secret_key="supersecretkey")
templates = Jinja2Templates(directory="templates")

# Create database tables
Base.metadata.create_all(bind=engine)

# Include router
app.include_router(collections.router)
app.include_router(teams.router)
# app.include_router(players.router)


# Serve static files
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})
