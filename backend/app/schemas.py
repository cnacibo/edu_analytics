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
    budget_places: Optional[int] = None
    paid_places: Optional[int] = None
    url: Optional[str] = None


class VuzopediaProgramsRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    programs: list[VuzopediaProgramRead]
    page: int
    size: int
    count: int
    total: int
    total_pages: int


class HseProgramRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    code: Optional[str] = None
    cost: Optional[float] = None
    study_type: Optional[str] = None
    budget_places: Optional[int] = None
    paid_places: Optional[int] = None
    foreigners_places: Optional[int] = None
    url: Optional[str] = None


class HseProgramsRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    programs: list[HseProgramRead]
    page: int
    size: int
    count: int
    total: int
    total_pages: int


class HseCourseRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    program_id: int
    title: str
    year: Optional[str] = None
    module: Optional[str] = None
    status: Optional[str] = None
    content: Optional[str] = None
    results: Optional[str] = None
    language: Optional[str] = None
    credits: Optional[float] = None
    url: Optional[str] = None


class HseCoursesRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    courses: list[HseCourseRead]
    page: int
    size: int
    count: int
    total: int
    total_pages: int
