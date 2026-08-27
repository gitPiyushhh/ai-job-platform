from sqlalchemy.orm import Session

from app.integrations.gemini import GeminiClient
from app.models.job import Job


BATCH_SIZE = 20


def is_obviously_irrelevant(job: Job) -> bool:
    text = f"{job.title} {job.description or ''}".lower()

    senior_keywords = [
        "director",
        "vp ",
        "vice president",
        "chief",
        "principal",
        "head of",
        "architect",
    ]

    return any(
        keyword in text
        for keyword in senior_keywords
    )


async def match_discovered_jobs(
    db: Session,
) -> dict:

    gemini = GeminiClient()

    jobs = (
        db.query(Job)
        .filter(Job.status == "DISCOVERED")
        .all()
    )

    candidates = []
    pre_skipped = 0

    for job in jobs:

        if is_obviously_irrelevant(job):

            job.status = "REJECTED"
            job.match_score = 0
            job.recommendation = "SKIP"

            job.match_reason = (
                "Filtered before AI analysis because "
                "the role appears significantly above "
                "the target experience level."
            )

            pre_skipped += 1

        else:
            candidates.append(job)

    analyzed = 0
    apply_candidates = 0
    review_candidates = 0
    ai_skipped = 0
    failed = 0

    for i in range(
        0,
        len(candidates),
        BATCH_SIZE,
    ):

        batch = candidates[
            i:i + BATCH_SIZE
        ]

        payload = []

        for job in batch:

            payload.append(
                {
                    "job_id": job.id,
                    "title": job.title,
                    "company": job.company,
                    "location": job.location,
                    "description": job.description,
                }
            )

        print(
            f"Sending {len(batch)} jobs to Gemini..."
        )

        try:

            results = await gemini.analyze_jobs(
                payload
            )

        except Exception as exc:
            print(
                f"Gemini batch failed: {exc}"
            )

            # Gemini unavailable (quota/API/etc.)
            # Keep these jobs for manual review instead
            # of losing them from the pipeline.

            for job in batch:
                job.status = "REVIEW"
                job.recommendation = "REVIEW"
                job.match_reason = (
                    "AI matching unavailable. "
                    "Review this job manually."
                )

                job.match_score = None

            db.commit()

            failed += len(batch)
            review_candidates += len(batch)

            continue

        results_by_id = {
            result.get("job_id"): result
            for result in results
        }

        for job in batch:

            result = results_by_id.get(
                job.id
            )

            if not result:

                print(
                    f"No Gemini result for "
                    f"job {job.id}"
                )

                failed += 1
                continue

            job.match_score = result.get(
                "match_score"
            )

            job.recommendation = result.get(
                "recommendation"
            )

            job.role_fit = result.get(
                "role_fit"
            )

            job.experience_fit = result.get(
                "experience_fit"
            )

            job.genai_fit = result.get(
                "genai_fit"
            )

            job.backend_fit = result.get(
                "backend_fit"
            )

            job.match_reason = result.get(
                "reason"
            )

            job.best_resume = result.get(
                "best_resume"
            )

            recommendation = (
                result.get("recommendation")
            )

            if recommendation == "APPLY":

                job.status = "MATCHED"
                apply_candidates += 1

            elif recommendation == "REVIEW":

                job.status = "REVIEW"
                review_candidates += 1

            else:

                job.status = "REJECTED"
                ai_skipped += 1

            analyzed += 1

        db.commit()

    return {
        "total_jobs": len(jobs),
        "ai_candidates": len(candidates),
        "pre_filtered": pre_skipped,
        "analyzed": analyzed,
        "apply_candidates": apply_candidates,
        "review_candidates": review_candidates,
        "skipped": (
            pre_skipped +
            ai_skipped
        ),
        "failed": failed,
    }