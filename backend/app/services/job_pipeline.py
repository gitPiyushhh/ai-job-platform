from sqlalchemy.orm import Session

from app.core.database import SessionLocal
from app.services.job_service import discover_jobs
from app.services.job_matching_service import match_discovered_jobs
from app.services.application_service import create_application_tasks


async def run_job_pipeline():
    print("====================================")
    print("STARTING AI JOB PIPELINE")
    print("====================================")

    db: Session = SessionLocal()

    try:
        # 1. Discover
        print("1. Discovering jobs...")

        discovery_result = await discover_jobs(db)

        print(
            f"Discovered: "
            f"{discovery_result.get('discovered', 0)}"
        )

        # 2. Match
        print("2. Matching jobs...")

        matching_result = await match_discovered_jobs(db)

        print(
            f"Analyzed: "
            f"{matching_result.get('analyzed', 0)}"
        )

        # 3. Create application tasks
        print("3. Creating application tasks...")

        application_result = (
            await create_application_tasks(db)
        )

        print(
            f"Application tasks: "
            f"{application_result.get('application_tasks_created', 0)}"
        )

        print("====================================")
        print("JOB PIPELINE FINISHED")
        print("====================================")

        return {
            "discovery": discovery_result,
            "matching": matching_result,
            "applications": application_result,
        }

    except Exception as exc:

        print(
            f"JOB PIPELINE FAILED: {exc}"
        )

        raise

    finally:
        db.close()