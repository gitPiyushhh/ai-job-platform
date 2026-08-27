from datetime import datetime

from sqlalchemy import DateTime, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base


class Job(Base):
    __tablename__ = "jobs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    external_id: Mapped[str] = mapped_column(
        Text,
        unique=True,
        nullable=False,
        index=True,
    )   

    source: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    title: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    company: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    location: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )

    description: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    job_url: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    employment_type: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
    )

    experience_min: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
    )

    experience_max: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
    )

    salary: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )

    skills: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    match_score: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
    )

    status: Mapped[str] = mapped_column(
        String(50),
        default="DISCOVERED",
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
    )

    applications = relationship(
        "Application",
        back_populates="job",
    )

    recommendation: Mapped[str | None] = mapped_column(
        String(50),
        nullable=True,
    )

    role_fit: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
    )

    experience_fit: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
    )

    genai_fit: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
    )

    backend_fit: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
    )

    match_reason: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    best_resume: Mapped[str | None] = mapped_column(
        String(50),
        nullable=True,
    )

    applications = relationship(
        "Application",
        back_populates="job",
    )