from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.database.models import Candidate

router = APIRouter()

templates = Jinja2Templates(directory="app/templates")


@router.get("/ranking", response_class=HTMLResponse)
def ranking(request: Request, db: Session = Depends(get_db)):

    candidates = (
        db.query(Candidate)
        .order_by(Candidate.score.desc())
        .all()
    )

    return templates.TemplateResponse(
        request=request,
        name="ranking.html",
        context={
            "candidates": candidates
        }
    )


@router.get("/candidate/{candidate_id}", response_class=HTMLResponse)
def candidate_details(
    candidate_id: int,
    request: Request,
    db: Session = Depends(get_db)
):

    candidate = (
        db.query(Candidate)
        .filter(Candidate.id == candidate_id)
        .first()
    )

    return templates.TemplateResponse(
        request=request,
        name="candidate.html",
        context={
            "candidate": candidate
        }
    )