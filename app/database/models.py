from sqlalchemy import Column, Integer, String, Text

from app.database.database import Base


class Job(Base):

    __tablename__ = "jobs"

    id = Column(Integer, primary_key=True, index=True)

    job_title = Column(String(200), nullable=False)

    department = Column(String(100))

    location = Column(String(100))

    experience = Column(String(50))

    education = Column(String(100))

    required_skills = Column(Text)

    preferred_skills = Column(Text)

    job_description = Column(Text)

class Candidate(Base):

    __tablename__ = "candidates"

    id = Column(Integer, primary_key=True, index=True)

    job_id = Column(Integer)

    name = Column(String(200))

    email = Column(String(200))

    phone = Column(String(50))

    skills = Column(Text)

    missing_skills = Column(Text)   # ← Add this line

    score = Column(Integer)

    resume_file = Column(String(255))