from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.resume import ResumeCreate, ResumeResponse
from app.services.resume_service import (
    create_resume,
    get_resume,
    get_resumes,
)


router = APIRouter(
    prefix="/api/resumes",
    tags=["Resumes"],
)


@router.post(
    "",
    response_model=ResumeResponse,
)
def create_resume_endpoint(
    resume_data: ResumeCreate,
    db: Session = Depends(get_db),
):
    return create_resume(db, resume_data)


@router.get(
    "",
    response_model=list[ResumeResponse],
)
def list_resumes(
    db: Session = Depends(get_db),
):
    return get_resumes(db)


@router.get(
    "/{resume_id}",
    response_model=ResumeResponse,
)
def get_resume_endpoint(
    resume_id: int,
    db: Session = Depends(get_db),
):
    resume = get_resume(db, resume_id)

    if not resume:
        raise HTTPException(
            status_code=404,
            detail="Resume not found",
        )

    return resume