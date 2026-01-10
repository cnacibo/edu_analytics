from typing import Optional

from pydantic import BaseModel, ConfigDict


class VuzopediaProgramRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    cost: Optional[float] = None
    study_type: Optional[str] = None
    min_budget_score: Optional[int] = None
    min_paid_score: Optional[int] = None
    code: Optional[str] = None
    sphere: Optional[str] = None
    career_prospects: Optional[str] = None


class HseProgramRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    code: Optional[str] = None
    cost: Optional[float] = None
    study_type: Optional[str] = None
    budget_places: int = 0
    paid_places: int = 0
    foreigners_places: int = 0


class HseCourseRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    program_id: int
    title: str
    year: Optional[int] = None
    module: Optional[str] = None
    status: Optional[str] = None
    track: Optional[str] = None
    content: Optional[str] = None
    results: Optional[str] = None
    language: Optional[str] = None
    credits: Optional[int] = None
