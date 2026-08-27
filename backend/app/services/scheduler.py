from apscheduler.schedulers.asyncio import AsyncIOScheduler

from app.services.job_pipeline import run_job_pipeline


scheduler = AsyncIOScheduler(
    timezone="Asia/Kolkata"
)


def start_scheduler():

    scheduler.add_job(
        run_job_pipeline,
        trigger="cron",
        hour=8,
        minute=0,
        id="morning_job_pipeline",
        replace_existing=True,
        max_instances=1,
    )

    scheduler.add_job(
        run_job_pipeline,
        trigger="cron",
        hour=20,
        minute=0,
        id="evening_job_pipeline",
        replace_existing=True,
        max_instances=1,
    )

    scheduler.start()

    print(
        "JOB SCHEDULER STARTED"
    )

    print(
        "Morning: 08:00 IST"
    )

    print(
        "Evening: 20:00 IST"
    )