from typing import Optional

from app.db.crud import get_vuzopedia_program_by_id, get_vuzopedia_programs
from app.services.shared import validate_query
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession


async def get_vuzopedia_programs_service(
    db: AsyncSession,
    max_cost: Optional[int] = None,
    max_budget_score: Optional[int] = None,
    max_paid_score: Optional[int] = None,
    study_type: Optional[str] = None,
    q: Optional[str] = None,
    page: int = 1,
    size: int = 100,
):

    if max_cost is not None and max_cost < 0:
        raise HTTPException(
            status_code=400, detail="Максимальная стоимость не может быть отрицательной"
        )

    if max_budget_score is not None and max_budget_score < 0:
        raise HTTPException(
            status_code=400, detail="Максимальный балл на бюджет не может быть отрицательным"
        )

    if max_paid_score is not None and max_paid_score < 0:
        raise HTTPException(
            status_code=400, detail="Максимальный балл на платное не может быть отрицательным"
        )

    if page < 1:
        raise HTTPException(status_code=400, detail="Номер страницы должен быть не менее 1")

    if size < 1 or size > 1000:
        raise HTTPException(status_code=400, detail="Размер страницы должен быть от 1 до 1000")

    validated_q = None
    if q:
        validated_q = validate_query(q)

    validated_study_type = None
    if study_type:
        validated_study_type = validate_query(study_type)

    if validated_study_type:
        if validated_study_type.lower() not in ["бакалавриат", "специалитет", "магистратура"]:
            raise HTTPException(
                status_code=400,
                detail="Вид образования может быть только бакалавриат, специалитет, магистратура",
            )

    response = await get_vuzopedia_programs(
        db=db,
        page=page,
        size=size,
        q=validated_q,
        max_budget_score=max_budget_score,
        max_paid_score=max_paid_score,
        max_cost=max_cost,
        study_type=validated_study_type,
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
