import os
import shutil

from fastapi import APIRouter, UploadFile, File, Depends, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.database.models import Job, Candidate

from app.services.parser import ResumeParser
from app.services.extractor import ResumeExtractor
from app.services.matcher import SemanticMatcher
from app.services.ranking import CandidateRanking

router = APIRouter()

templates = Jinja2Templates(directory="app/templates")

UPLOAD_FOLDER = "uploads"


@router.get("/upload", response_class=HTMLResponse)
def upload_page(
    request: Request,
    db: Session = Depends(get_db)
):

    jobs = db.query(Job).all()

    return templates.TemplateResponse(
        request=request,
        name="upload.html",
        context={
            "jobs": jobs
        }
    )


@router.post("/resumes/upload")
def upload_resume(

    job_id: int = Form(...),

    files: list[UploadFile] = File(...),

    db: Session = Depends(get_db)

):

    os.makedirs(UPLOAD_FOLDER, exist_ok=True)

    job = db.query(Job).filter(Job.id == job_id).first()

    if not job:

        return RedirectResponse(
            url="/upload",
            status_code=303
        )

    required_skills = []

    if job.required_skills:

        required_skills = [

            skill.strip().lower()

            for skill in job.required_skills.split(",")

            if skill.strip()

        ]

    for file in files:

        filepath = os.path.join(

            UPLOAD_FOLDER,

            file.filename

        )

        with open(filepath, "wb") as buffer:

            shutil.copyfileobj(

                file.file,

                buffer

            )

        resume_text = ResumeParser.extract_text(filepath)

        candidate_name = ResumeExtractor.extract_name(resume_text)

        candidate_email = ResumeExtractor.extract_email(resume_text)

        candidate_phone = ResumeExtractor.extract_phone(resume_text)

        candidate_skills = ResumeExtractor.extract_skills(resume_text)

        missing_skills = []

        for skill in required_skills:

            if skill not in candidate_skills:

                missing_skills.append(skill)

        semantic_score = SemanticMatcher.similarity(

            job.job_description,

            resume_text

        )

        skill_score = CandidateRanking.calculate_score(

            required_skills,

            candidate_skills

        )

        final_score = round(

            (semantic_score * 0.70) +

            (skill_score * 0.30),

            2

        )

        existing_candidate = (

            db.query(Candidate)

            .filter(

                Candidate.job_id == job.id,

                Candidate.email == candidate_email

            )

            .first()

        )

        if existing_candidate:

            existing_candidate.name = candidate_name

            existing_candidate.phone = candidate_phone

            existing_candidate.skills = ", ".join(candidate_skills)

            existing_candidate.missing_skills = ", ".join(missing_skills)

            existing_candidate.score = int(final_score)

            existing_candidate.resume_file = file.filename

        else:

            candidate = Candidate(

                job_id=job.id,

                name=candidate_name,

                email=candidate_email,

                phone=candidate_phone,

                skills=", ".join(candidate_skills),

                missing_skills=", ".join(missing_skills),

                score=int(final_score),

                resume_file=file.filename

            )

            db.add(candidate)

    db.commit()

    return RedirectResponse(

        url="/ranking",

        status_code=303

    )