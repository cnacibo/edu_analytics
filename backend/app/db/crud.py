from typing import Any, Dict, Optional

from app.db.models import HseCourse, HseProgram, VuzopediaProgram
from sqlalchemy import and_, func, select
from sqlalchemy.ext.asyncio import AsyncSession


async def get_vuzopedia_programs(
    db: AsyncSession,
    page: int = 1,
    size: int = 100,
    q: Optional[str] = None,
    min_score: Optional[int] = None,
    max_cost: Optional[float] = None,
) -> Dict[str, Any]:
    """Получить программы Vuzopedia с фильтрацией"""
    stmt = select(VuzopediaProgram)
    filters = []

    if q:
        filters.append(VuzopediaProgram.name.ilike(f"%{q}%"))

    if min_score is not None:
        filters.append(VuzopediaProgram.min_budget_score >= min_score)

    if max_cost is not None:
        filters.append(VuzopediaProgram.cost <= max_cost)

    if filters:
        filter_condition = and_(*filters)
        stmt = stmt.where(filter_condition)
        count_stmt = select(func.count()).select_from(VuzopediaProgram).where(filter_condition)
    else:
        count_stmt = select(func.count()).select_from(VuzopediaProgram)

    total = await db.scalar(count_stmt) or 0

    offset = (page - 1) * size
    stmt = stmt.offset(offset).limit(size)
    result = await db.execute(stmt)
    programs = list(result.scalars().all())

    return {"programs": programs, "total": total}


async def get_vuzopedia_program_by_id(
    db: AsyncSession, program_id: int
) -> Optional[VuzopediaProgram]:
    """Получить программу Vuzopedia по ID"""
    stmt = select(VuzopediaProgram).where(VuzopediaProgram.id == program_id)
    result = await db.execute(stmt)
    return result.scalars().first()


async def get_hse_programs(
    db: AsyncSession,
    page: int = 1,
    size: int = 100,
    q: Optional[str] = None,
    max_cost: Optional[float] = None,
) -> Dict[str, Any]:
    """Получить программы ВШЭ ФКН с фильтрацией"""
    stmt = select(HseProgram)
    filters = []

    if q:
        filters.append(HseProgram.name.ilike(f"%{q}%"))

    if max_cost is not None:
        filters.append(HseProgram.cost <= max_cost)

    if filters:
        filter_condition = and_(*filters)
        stmt = stmt.where(filter_condition)
        count_stmt = select(func.count()).select_from(HseProgram).where(filter_condition)
    else:
        count_stmt = select(func.count()).select_from(HseProgram)

    total = await db.scalar(count_stmt) or 0

    offset = (page - 1) * size
    stmt = stmt.offset(offset).limit(size)
    result = await db.execute(stmt)
    programs = list(result.scalars().all())

    return {"programs": programs, "total": total}


async def get_hse_program_by_id(db: AsyncSession, program_id: int) -> Optional[HseProgram]:
    """Получить программу ВШЭ ФКН по ID"""
    stmt = select(HseProgram).where(HseProgram.id == program_id)
    result = await db.execute(stmt)
    return result.scalars().first()


async def get_hse_program_courses(
    db: AsyncSession,
    program_id: int,
    page: int = 1,
    size: int = 100,
) -> Dict[str, Any]:
    """Получить все дисциплины программы ВШЭ ФКН по ID программы"""
    stmt = select(HseCourse).where(HseCourse.program_id == program_id)
    count_stmt = (
        select(func.count()).select_from(HseCourse).where(HseCourse.program_id == program_id)
    )
    total = await db.scalar(count_stmt) or 0
    offset = (page - 1) * size
    stmt = stmt.offset(offset).limit(size)
    result = await db.execute(stmt)
    courses = list(result.scalars().all())
    return {"courses": courses, "total": total}


async def get_hse_course_by_id(db: AsyncSession, course_id: int) -> HseCourse:
    """Получить дисциплину ВШЭ ФКН по ID дисциплины"""
    stmt = select(HseCourse).where(HseCourse.id == course_id)
    result = await db.execute(stmt)
    return result.scalars().first()
