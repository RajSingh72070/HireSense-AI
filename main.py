import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s"
)
print("STEP 1")
from fastapi import FastAPI
print("STEP 2")
from fastapi.staticfiles import StaticFiles
print("STEP 3")
from app.database.database import Base, engine
print("STEP 4")
from app.database import models
print("STEP 5")
from app.routers.login import router as login_router
print("STEP 6")
from app.routers.dashboard import router as dashboard_router
print("STEP 7")
from app.routers.jobs import router as jobs_router
print("STEP 8")
from app.routers.resumes import router as resume_router
print("STEP 9")
from app.routers.ranking import router as ranking_router
print("STEP 10")
from app.routers.export import router as export_router

# Create database tables
Base.metadata.create_all(bind=engine)
print("STEP 11")
# Create FastAPI app
print("STEP 12")
app = FastAPI(
    title="HireSense AI",
    version="1.0.0"
)

@app.get("/")
def root():
    return {
        "message": "HireSense AI API is running successfully 🚀"
    }

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