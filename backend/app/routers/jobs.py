from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db

from app.models.job import Job
from app.models.application import Application

from app.services.job_service import discover_jobs
from app.services.job_matching_service import match_discovered_jobs
from app.services.application_service import create_application_tasks
from app.services.job_pipeline import run_job_pipeline


router = APIRouter(
    prefix="/api/jobs",
    tags=["Jobs"],
)


# ============================================================
# GET JOBS — Frontend
# ============================================================

@router.get("")
async def get_jobs(
    db: Session = Depends(get_db),
):
    jobs = (
        db.query(Job)
        .order_by(
            Job.match_score.desc().nullslast(),
            Job.created_at.desc(),
        )
        .all()
    )

    return [
        {
            "id": job.id,
            "external_id": job.external_id,
            "source": job.source,
            "title": job.title,
            "company": job.company,
            "location": job.location,
            "description": job.description,
            "job_url": job.job_url,
            "employment_type": job.employment_type,
            "salary": job.salary,
            "skills": job.skills,
            "match_score": job.match_score,
            "status": job.status,

            # AI matching
            "recommendation": getattr(
                job,
                "recommendation",
                None,
            ),
            "role_fit": getattr(
                job,
                "role_fit",
                None,
            ),
            "experience_fit": getattr(
                job,
                "experience_fit",
                None,
            ),
            "genai_fit": getattr(
                job,
                "genai_fit",
                None,
            ),
            "backend_fit": getattr(
                job,
                "backend_fit",
                None,
            ),
            "match_reason": getattr(
                job,
                "match_reason",
                None,
            ),
            "best_resume": getattr(
                job,
                "best_resume",
                None,
            ),
        }
        for job in jobs
    ]


# ============================================================
# GET APPLICATIONS — Frontend
# ============================================================

@router.get("/applications")
async def get_applications(
    db: Session = Depends(get_db),
):
    applications = (
        db.query(Application)
        .order_by(
            Application.created_at.desc()
        )
        .all()
    )

    results = []

    for application in applications:

        job = (
            db.query(Job)
            .filter(
                Job.id == application.job_id
            )
            .first()
        )

        results.append(
            {
                "id": application.id,
                "job_id": application.job_id,

                "status": application.status,
                "application_url": application.application_url,
                "application_method": getattr(
                    application,
                    "application_method",
                    None,
                ),
                "resume_type": getattr(
                    application,
                    "resume_type",
                    None,
                ),
                "notes": application.notes,
                "applied_at": application.applied_at,
                "created_at": application.created_at,

                "job": {
                    "title": job.title if job else None,
                    "company": job.company if job else None,
                    "location": job.location if job else None,
                    "match_score": job.match_score if job else None,
                    "match_reason": (
                        getattr(job, "match_reason", None)
                        if job
                        else None
                    ),
                    "best_resume": (
                        getattr(job, "best_resume", None)
                        if job
                        else None
                    ),
                },
            }
        )

    return results


# ============================================================
# DISCOVER
# ============================================================

@router.post("/discover")
async def discover_jobs_endpoint(
    db: Session = Depends(get_db),
):
    return await discover_jobs(db)


# ============================================================
# MATCH
# ============================================================

@router.post("/match")
async def match_jobs_endpoint(
    db: Session = Depends(get_db),
):
    return await match_discovered_jobs(db)


# ============================================================
# CREATE APPLICATION TASKS
# ============================================================

@router.post("/applications/create")
async def create_application_tasks_endpoint(
    db: Session = Depends(get_db),
):
    return await create_application_tasks(db)


# ============================================================
# COMPLETE PIPELINE
# ============================================================

@router.post("/pipeline/run")
async def run_pipeline_endpoint():
    return await run_job_pipeline()