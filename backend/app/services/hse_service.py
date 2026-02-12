from typing import Optional

from app.db.crud import (
    get_hse_course_by_id,
    get_hse_program_by_id,
    get_hse_program_courses,
    get_hse_programs,
)
from app.services.shared import validate_search_query
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession


async def get_hse_programs_service(
    db: AsyncSession,
    max_cost: Optional[int] = None,
    q: Optional[str] = None,
    page: int = 1,
    size: int = 100,
):

    if max_cost is not None and max_cost < 0:
        raise HTTPException(
            status_code=400, detail="Максимальная стоимость не может быть отрицательной"
        )

    if page < 1:
        raise HTTPException(status_code=400, detail="Номер страницы должен быть не менее 1")

    if size < 1 or size > 1000:
        raise HTTPException(status_code=400, detail="Размер страницы должен быть от 1 до 1000")

    validated_q = None
    if q:
        validated_q = validate_search_query(q)

    response = await get_hse_programs(
        db=db,
        page=page,
        size=size,
        q=validated_q,
        max_cost=max_cost,
    )

    programs = response["programs"]
    total = response["total"]

    return {
        "programs": programs,
        "page": page,
        "size": size,
        "count": len(programs),
        "total": total,
        "total_pages": (total + size - 1) // size if total else 0,
    }


async def get_hse_program_by_id_service(program_id: int, db: AsyncSession):
    if program_id <= 0:
        raise HTTPException(status_code=400, detail="ID программы должен быть положительным числом")

    program = await get_hse_program_by_id(db=db, program_id=program_id)
    if not program:
        raise HTTPException(status_code=404, detail=f"Программа с ID {program_id} не найдена")

    return program


async def get_hse_program_courses_service(
    db: AsyncSession,
    program_id: int,
    page: int = 1,
    size: int = 100,
):
    if program_id <= 0:
        raise HTTPException(status_code=400, detail="ID программы должен быть положительным числом")

    if page < 1:
        raise HTTPException(status_code=400, detail="Номер страницы должен быть не менее 1")

    if size < 1 or size > 1000:
        raise HTTPException(status_code=400, detail="Размер страницы должен быть от 1 до 1000")

    program = await get_hse_program_by_id(db=db, program_id=program_id)
    if not program:
        raise HTTPException(status_code=404, detail=f"Программа с ID {program_id} не найдена")

    response = await get_hse_program_courses(
        db=db,
        program_id=program_id,
        page=page,
        size=size,
    )

    courses = response["courses"]
    total = response["total"]

    return {
        "courses": courses,
        "page": page,
        "size": size,
        "count": len(courses),
        "total": total,
        "total_pages": (total + size - 1) // size if total else 0,
    }


async def get_hse_course_by_id_service(
    course_id: int,
    db: AsyncSession,
):
    if course_id <= 0:
        raise HTTPException(
            status_code=400, detail="ID дисциплины должен быть положительным числом"
        )

    course = await get_hse_course_by_id(db=db, course_id=course_id)

    if not course:
        raise HTTPException(status_code=404, detail=f"Дисциплина с ID {course_id} не найдена")

    return course
