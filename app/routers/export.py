from fastapi import APIRouter, Depends
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
import pandas as pd

from app.database.database import get_db
from app.database.models import Candidate

router = APIRouter()


@router.get("/export")
def export_csv(db: Session = Depends(get_db)):

    candidates = db.query(Candidate).all()

    data = []

    for c in candidates:

        data.append({

            "Name": c.name,
            "Email": c.email,
            "Phone": "'" + c.phone,
            "Skills": c.skills,
            "Score": c.score,
            "Resume": c.resume_file

        })

    df = pd.DataFrame(data)

    output = "outputs/candidates.csv"

    df.to_csv(output, index=False)

    return FileResponse(
        output,
        filename="candidates.csv"
    )