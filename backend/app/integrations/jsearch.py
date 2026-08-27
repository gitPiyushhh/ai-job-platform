import httpx

from app.core.config import settings

JSEARCH_URL = "https://jsearch.p.rapidapi.com/search-v2"


class JSearchClient:
    def __init__(self):
        self.headers = {
            "X-RapidAPI-Key": settings.JSEARCH_API_KEY,
            "X-RapidAPI-Host": "jsearch.p.rapidapi.com",
        }

    async def search_jobs(
        self,
        query: str,
        country: str = "in",
        page: int = 1,
        num_pages: int = 1,
        date_posted: str = "3days",
    ) -> list[dict]:

        params = {
            "query": query,
            "page": page,
            "num_pages": num_pages,
            "country": country,
            "date_posted": date_posted,
        }

        timeout = httpx.Timeout(
            connect=10.0,
            read=60.0,
            write=10.0,
            pool=10.0,
        )

        async with httpx.AsyncClient(timeout=timeout) as client:
            response = await client.get(
                JSEARCH_URL,
                headers=self.headers,
                params=params,
            )

            response.raise_for_status()

            data = response.json()

            print("JSEARCH RESPONSE TYPE:", type(data))
            print("JSEARCH RESPONSE:", data)

        return data.get("data", {}).get("jobs", [])