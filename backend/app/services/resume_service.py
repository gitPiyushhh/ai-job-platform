from sqlalchemy.orm import Session

from app.models.resume import Resume
from app.schemas.resume import ResumeCreate


def create_resume(
    db: Session,
    resume_data: ResumeCreate,
) -> Resume:
    resume = Resume(
        name=resume_data.name,
        resume_type=resume_data.resume_type,
        file_url=resume_data.file_url,
    )

    db.add(resume)
    db.commit()
    db.refresh(resume)

    return resume


def get_resumes(db: Session) -> list[Resume]:
    return (
        db.query(Resume)
        .order_by(Resume.created_at.desc())
        .all()
    )


def get_resume(
    db: Session,
    resume_id: int,
) -> Resume | None:
    return db.query(Resume).filter(
        Resume.id == resume_id
    ).first()