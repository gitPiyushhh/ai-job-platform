from datetime import datetime

from pydantic import BaseModel, ConfigDict


class ResumeBase(BaseModel):
    name: str
    resume_type: str


class ResumeCreate(ResumeBase):
    file_url: str | None = None


class ResumeResponse(ResumeBase):
    id: int
    file_url: str | None
    resume_text: str | None
    summary: str | None
    primary_role: str | None
    experience_years: int | None
    skills: str | None
    is_active: bool
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)