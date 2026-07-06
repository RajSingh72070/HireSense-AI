from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.database.database import get_db
from app.database.models import Job, Candidate

router = APIRouter()

templates = Jinja2Templates(directory="app/templates")


@router.get("/dashboard", response_class=HTMLResponse)
async def dashboard(
    request: Request,
    db: Session = Depends(get_db)
):

    jobs_count = db.query(Job).count()

    resumes_count = db.query(Candidate).count()

    shortlisted = db.query(Candidate).filter(Candidate.score >= 50).count()

    average_score = db.query(func.avg(Candidate.score)).scalar()

    if average_score is None:
        average_score = 0

    return templates.TemplateResponse(
        request=request,
        name="dashboard.html",
        context={
            "jobs_count": jobs_count,
            "resumes_count": resumes_count,
            "shortlisted": shortlisted,
            "average_score": round(average_score, 2)
        }
    )