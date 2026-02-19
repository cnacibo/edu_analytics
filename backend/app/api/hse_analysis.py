from typing import Optional

from app.db.session import get_db
from app.services import hse_service
from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter()


@router.get("/")
async def get_hse_programs(
    db: AsyncSession = Depends(get_db),
    max_cost: Optional[int] = Query(None, description="Максимальная стоимость"),
    q: Optional[str] = Query(None, description="Поисковый запрос"),
    page: int = Query(1, description="Номер страницы"),
    size: int = Query(100, description="Размер страницы"),
):
    """Получить все программы НИУ ВШЭ с фильтрацией"""

    return await hse_service.get_hse_programs_service(
        db=db,
        max_cost=max_cost,
        q=q,
        page=page,
        size=size,
    )


@router.get("/{program_id}")
async def get_hse_program_by_id(
    program_id: int,
    db: AsyncSession = Depends(get_db),
):
    """Получить программу НИУ ВШЭ по ID"""
    return await hse_service.get_hse_program_by_id_service(program_id=program_id, db=db)


@router.get("/{program_id}/courses")
async def get_hse_program_courses(
    program_id: int,
    db: AsyncSession = Depends(get_db),
    page: int = Query(1, description="Номер страницы"),
    size: int = Query(100, description="Размер страницы"),
):
    """Получить все дисциплины программы НИУ ВШЭ по ее ID"""
    return await hse_service.get_hse_program_courses_service(
        db=db,
        program_id=program_id,
        page=page,
        size=size,
    )


@router.get("/courses/{course_id}")
async def get_hse_course_by_id(
    course_id: int,
    db: AsyncSession = Depends(get_db),
):
    """Получить данные о дисциплине НИУ ВШЭ по ID"""
    return await hse_service.get_hse_course_by_id_service(course_id=course_id, db=db)
