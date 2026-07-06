import os
import logging
logging.basicConfig(
    filename="logs/app.log",
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s"
)
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.database.database import Base, engine
from app.database import models

from app.routers.login import router as login_router
from app.routers.dashboard import router as dashboard_router
from app.routers.jobs import router as jobs_router
from app.routers.resumes import router as resume_router
from app.routers.ranking import router as ranking_router
from app.routers.export import router as export_router

# Create database tables
Base.metadata.create_all(bind=engine)

# Create FastAPI app
app = FastAPI(
    title="HireSense AI",
    version="1.0.0"
)

# Mount static files
app.mount(
    "/static",
    StaticFiles(directory="app/static"),
    name="static"
)

# Register routers
app.include_router(login_router)
app.include_router(dashboard_router)
app.include_router(jobs_router)
app.include_router(resume_router)
app.include_router(ranking_router)
app.include_router(export_router)