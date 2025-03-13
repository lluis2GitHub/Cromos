from fastapi import FastAPI
from routers import collections,teams,players
from database.database import engine, Base
from fastapi.staticfiles import StaticFiles
from starlette.middleware.sessions import SessionMiddleware

# Initialize the FastAPI app
app = FastAPI()

app.add_middleware(SessionMiddleware, secret_key="supersecretkey")

# Create database tables
Base.metadata.create_all(bind=engine)

# Include router
app.include_router(collections.router)
app.include_router(teams.router)
app.include_router(players.router)

# Serve static files
app.mount("/static", StaticFiles(directory="static"), name="static")
