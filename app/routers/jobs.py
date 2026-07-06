from fastapi import APIRouter
from fastapi import Depends
from fastapi import Form
from fastapi import Request

from fastapi.responses import HTMLResponse
from fastapi.responses import RedirectResponse

from fastapi.templating import Jinja2Templates

from sqlalchemy.orm import Session

from app.database.database import get_db
from app.database.models import Job

router = APIRouter()

templates = Jinja2Templates(directory="app/templates")


@router.get("/jobs", response_class=HTMLResponse)
def jobs_page(
    request: Request,
    db: Session = Depends(get_db)
):

    jobs = db.query(Job).all()

    return templates.TemplateResponse(
        request=request,
        name="jobs.html",
        context={
            "jobs": jobs
        }
    )


@router.post("/jobs/create")
def create_job(

    job_title: str = Form(...),
    department: str = Form(...),
    location: str = Form(...),
    experience: str = Form(...),
    education: str = Form(...),
    required_skills: str = Form(...),
    preferred_skills: str = Form(""),
    job_description: str = Form(...),

    db: Session = Depends(get_db)

):

    job = Job(

        job_title=job_title,

        department=department,

        location=location,

        experience=experience,

        education=education,

        required_skills=required_skills,

        preferred_skills=preferred_skills,

        job_description=job_description

    )

    db.add(job)

    db.commit()

    return RedirectResponse(
        url="/jobs",
        status_code=303
    )