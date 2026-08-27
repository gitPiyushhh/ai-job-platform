import re

import httpx
from sqlalchemy.orm import Session

from app.integrations.jsearch import JSearchClient
from app.models.job import Job


TARGET_SEARCHES = [
    "Generative AI Engineer",
    "GenAI Engineer",
    "LLM Engineer",
    "AI Engineer",
    "Backend AI Engineer",
]


SKILL_KEYWORDS = [
    "Python",
    "FastAPI",
    "Django",
    "Flask",
    "REST APIs",
    "PostgreSQL",
    "SQL",
    "Redis",
    "Docker",
    "AWS",
    "Azure",
    "GCP",
    "React",
    "Next.js",
    "JavaScript",
    "TypeScript",
    "LLM",
    "LLMs",
    "Generative AI",
    "GenAI",
    "RAG",
    "LangChain",
    "LangGraph",
    "LlamaIndex",
    "Prompt Engineering",
    "Vector Database",
    "Pinecone",
    "Weaviate",
    "Qdrant",
    "FAISS",
    "pgvector",
    "OpenAI",
    "Claude",
    "Gemini",
    "MCP",
    "Agentic AI",
    "Machine Learning",
    "Deep Learning",
    "PyTorch",
    "TensorFlow",
    "Kubernetes",
    "CI/CD",
]


def extract_skills(description: str | None) -> str | None:
    """
    Extract known technical skills from the job description.

    Stored as a comma-separated string because the Job model
    currently uses Text for the skills column.
    """

    if not description:
        return None

    text = description.lower()

    found = []

    for skill in SKILL_KEYWORDS:

        if skill.lower() in text:
            found.append(skill)

    if not found:
        return None

    return ", ".join(found)


def extract_experience(
    description: str | None,
) -> tuple[int | None, int | None]:

    if not description:
        return None, None

    text = description.lower()

    patterns = [
        r"(\d+)\s*[-–]\s*(\d+)\s*(?:years?|yrs?)",
        r"(\d+)\s*to\s*(\d+)\s*(?:years?|yrs?)",
        r"(\d+)\+?\s*(?:years?|yrs?)\s*(?:of\s+)?experience",
    ]

    for pattern in patterns:

        match = re.search(pattern, text)

        if not match:
            continue

        groups = match.groups()

        if len(groups) == 2:
            return int(groups[0]), int(groups[1])

        minimum = int(groups[0])
        return minimum, None

    return None, None


async def discover_jobs(db: Session) -> dict:

    client = JSearchClient()

    discovered = 0
    new_jobs = 0
    duplicates = 0

    for query in TARGET_SEARCHES:

        try:

            jobs = await client.search_jobs(
                query=query,
                country="in",
                num_pages=1,
                date_posted="3days",
            )

        except httpx.TimeoutException:

            print(
                f"JSearch timeout for query: {query}"
            )
            continue

        except httpx.HTTPError as exc:

            print(
                f"JSearch error for query "
                f"'{query}': {exc}"
            )
            continue

        discovered += len(jobs)

        for job_data in jobs:

            external_id = job_data.get("job_id")

            if not external_id:
                continue

            existing_job = (
                db.query(Job)
                .filter(
                    Job.external_id == external_id
                )
                .first()
            )

            if existing_job:

                duplicates += 1
                continue

            title = job_data.get(
                "job_title",
                "",
            )

            company = job_data.get(
                "employer_name",
                "",
            )

            description = job_data.get(
                "job_description"
            )

            experience_min, experience_max = (
                extract_experience(description)
            )

            skills = extract_skills(
                description
            )

            job = Job(
                external_id=external_id,

                source="JSEARCH",

                title=title,

                company=company,

                location=job_data.get(
                    "job_location"
                ),

                description=description,

                job_url=job_data.get(
                    "job_apply_link"
                ),

                employment_type=job_data.get(
                    "job_employment_type"
                ),

                experience_min=experience_min,

                experience_max=experience_max,

                salary=(
                    str(job_data.get("job_min_salary"))
                    if job_data.get("job_min_salary")
                    is not None
                    else None
                ),

                skills=skills,

                status="DISCOVERED",
            )

            db.add(job)

            new_jobs += 1

    db.commit()

    return {
        "discovered": discovered,
        "new_jobs": new_jobs,
        "duplicates": duplicates,
    }