from typing import List, Optional

from app.db.models import HseCourse, HseProgram, VuzopediaProgram
from sqlalchemy import and_, select
from sqlalchemy.ext.asyncio import AsyncSession


async def get_vuzopedia_programs(
    db: AsyncSession,
    page: int = 1,
    size: int = 100,
    q: Optional[str] = None,
    min_score: Optional[int] = None,
    max_cost: Optional[float] = None,
) -> List[VuzopediaProgram]:
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
        stmt = stmt.where(and_(*filters))

    offset = (page - 1) * size
    stmt = stmt.offset(offset).limit(size)
    result = await db.execute(stmt)

    return list(result.scalars().all())


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
) -> List[HseProgram]:
    """Получить программы ВШЭ ФКН с фильтрацией"""
    stmt = select(HseProgram)
    filters = []

    if q:
        filters.append(HseProgram.name.ilike(f"%{q}%"))

    if max_cost is not None:
        filters.append(HseProgram.cost <= max_cost)

    if filters:
        stmt = stmt.where(and_(*filters))

    offset = (page - 1) * size
    stmt = stmt.offset(offset).limit(size)
    result = await db.execute(stmt)

    return list(result.scalars().all())


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
) -> List[HseCourse]:
    """Получить все дисциплины программы ВШЭ ФКН по ID программы"""
    stmt = select(HseCourse).where(HseCourse.program_id == program_id)
    offset = (page - 1) * size
    stmt = stmt.offset(offset).limit(size)
    result = await db.execute(stmt)
    return list(result.scalars().all())


async def get_hse_course_by_id(db: AsyncSession, course_id: int) -> HseCourse:
    """Получить дисциплину ВШЭ ФКН по ID дисциплины"""
    stmt = select(HseCourse).where(HseCourse.id == course_id)
    result = await db.execute(stmt)
    return result.scalars().first()
