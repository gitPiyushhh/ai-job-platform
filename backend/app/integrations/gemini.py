import asyncio
import json

from google import genai

from app.core.config import settings


class GeminiClient:

    def __init__(self):
        self.client = genai.Client(
            api_key=settings.GEMINI_API_KEY
        )

    async def analyze_jobs(
        self,
        jobs: list[dict],
    ) -> list[dict]:

        jobs_text = json.dumps(
            jobs,
            ensure_ascii=False,
        )

        prompt = f"""
You are an expert technical recruiter.

Evaluate these jobs for a software engineer with approximately
3 years of experience targeting Backend + Generative AI roles.

TARGET ROLES:
- Generative AI Engineer
- GenAI Engineer
- AI Engineer
- LLM Engineer
- Applied AI Engineer
- Backend AI Engineer
- Python Backend Engineer

IMPORTANT SKILLS:
Python, FastAPI, REST APIs, PostgreSQL, Backend Development,
LLMs, RAG, Vector Databases, LangChain, LangGraph,
Prompt Engineering, Claude, OpenAI, Docker, AWS, React.

TARGET EXPERIENCE:
Approximately 2-5 years.

Clearly senior, lead, principal, architect, director,
head or 8+ year roles should normally be SKIP.

For EVERY job return:

- job_id
- match_score (0-100)
- recommendation: APPLY, REVIEW, or SKIP
- role_fit (0-100)
- experience_fit (0-100)
- genai_fit (0-100)
- backend_fit (0-100)
- reason
- best_resume: GENAI, BACKEND, or FULLSTACK

Return ONLY a JSON array.

Example:

[
  {{
    "job_id": 123,
    "match_score": 91,
    "recommendation": "APPLY",
    "role_fit": 95,
    "experience_fit": 90,
    "genai_fit": 95,
    "backend_fit": 85,
    "reason": "Strong GenAI and backend alignment.",
    "best_resume": "GENAI"
  }}
]

JOBS:

{jobs_text}
"""

        try:
            response = await asyncio.wait_for(
                self.client.aio.models.generate_content(
                    model="gemini-3.6-flash",
                    contents=prompt,
                ),
                timeout=45,
            )

            text = response.text.strip()

            if text.startswith("```"):
                text = text.replace(
                    "```json",
                    "",
                )
                text = text.replace(
                    "```",
                    "",
                )
                text = text.strip()

            return json.loads(text)

        except Exception:
            raise