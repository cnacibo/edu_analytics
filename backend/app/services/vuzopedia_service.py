from typing import Optional

from app.db.crud import get_vuzopedia_program_by_id, get_vuzopedia_programs
from app.services.shared import validate_search_query
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession


async def get_vuzopedia_programs_service(
    db: AsyncSession,
    max_cost: Optional[int] = None,
    min_score: Optional[int] = None,
    q: Optional[str] = None,
    page: int = 1,
    size: int = 100,
):

    if max_cost is not None and max_cost < 0:
        raise HTTPException(
            status_code=400, detail="Максимальная стоимость не может быть отрицательной"
        )

    if min_score is not None and min_score < 0:
        raise HTTPException(status_code=400, detail="Минимальный балл не может быть отрицательным")

    if page < 1:
        raise HTTPException(status_code=400, detail="Номер страницы должен быть не менее 1")

    if size < 1 or size > 1000:
        raise HTTPException(status_code=400, detail="Размер страницы должен быть от 1 до 1000")

    validated_q = None
    if q:
        validated_q = validate_search_query(q)

    programs = await get_vuzopedia_programs(
        db=db,
        page=page,
        size=size,
        q=validated_q,
        max_cost=max_cost,
    )

    return {
        "count": len(programs),
        "programs": programs,
        "page": page,
        "size": size,
    }


async def get_vuzopedia_program_by_id_service(
    program_id: int,
    db: AsyncSession,
):
    if program_id <= 0:
        raise HTTPException(status_code=400, detail="ID программы должен быть положительным числом")

    program = await get_vuzopedia_program_by_id(db=db, program_id=program_id)
    if not program:
        raise HTTPException(status_code=404, detail=f"Программа с ID {program_id} не найдена")

    return program
