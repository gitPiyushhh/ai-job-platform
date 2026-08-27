from datetime import datetime

from sqlalchemy.orm import Session

from app.models.application import Application
from app.models.job import Job


async def create_application_tasks(
    db: Session,
) -> dict:

    jobs = (
        db.query(Job)
        .filter(
            Job.status.in_(
                ["MATCHED", "REVIEW"]
            )
        )
        .all()
    )

    created = 0
    existing = 0

    for job in jobs:

        already_exists = (
            db.query(Application)
            .filter(Application.job_id == job.id)
            .first()
        )

        if already_exists:
            existing += 1
            continue

        application = Application(
            job_id=job.id,
            resume_type=job.best_resume,
            status="MANUAL_REQUIRED",
            application_url=job.job_url,
            application_method="MANUAL",
            notes=(
                "Application requires manual submission. "
                "Use the recommended resume and review the "
                "job before submitting."
            ),
        )

        db.add(application)

        job.status = "APPLICATION_READY"

        created += 1

    db.commit()

    return {
        "matched_jobs": len(jobs),
        "application_tasks_created": created,
        "already_existing": existing,
    }