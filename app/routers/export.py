from io import StringIO

import pandas as pd
from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session

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
            "Phone": "'" + (c.phone or ""),
            "Skills": c.skills,
            "Score": c.score,
            "Resume": c.resume_file
        })

    df = pd.DataFrame(data)

    csv_buffer = StringIO()
    df.to_csv(csv_buffer, index=False)
    csv_buffer.seek(0)

    return StreamingResponse(
        iter([csv_buffer.getvalue()]),
        media_type="text/csv",
        headers={
            "Content-Disposition": "attachment; filename=candidates.csv"
        }
    )