from fastapi import FastAPI
from sqlalchemy import text

from app.core.database import engine
from app.core.config import settings

from app.routers.resumes import router as resume_router
from app.routers.jobs import router as jobs_router

from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.services.scheduler import start_scheduler

from fastapi.middleware.cors import CORSMiddleware

@asynccontextmanager
async def lifespan(app: FastAPI):

    start_scheduler()

    yield
    
app = FastAPI(
    title=settings.APP_NAME,
    version="0.1.0",
    description="AI-powered Job Search and Application Platform",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(resume_router)
app.include_router(jobs_router)

@app.get("/health")
async def health_check():
    return {
        "status": "ok",
        "service": settings.APP_NAME,
        "environment": settings.APP_ENV,
    }

@app.get("/health/db")
async def database_health_check():
    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))

        return {
            "status": "ok",
            "database": "connected",
        }

    except Exception as e:
        return {
            "status": "error",
            "database": "disconnected",
            "detail": str(e),
        }

@app.get("/")
async def root():
    return {
        "message": "AI Job Platform API is running"
    }