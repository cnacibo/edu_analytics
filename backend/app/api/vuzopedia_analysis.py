from typing import Optional

from app.db.session import get_db
from app.services import vuzopedia_service
from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter()


@router.get("/")
async def get_vuzopedia_programs(
    db: AsyncSession = Depends(get_db),
    max_cost: Optional[int] = Query(None, description="Максимальная стоимость"),
    min_score: Optional[int] = Query(None, description="Минимальный проходной балл"),
    q: Optional[str] = Query(None, description="Поисковый запрос"),
    page: int = Query(1, description="Номер страницы"),
    size: int = Query(100, description="Размер страницы"),
):
    """Поиск образовательных программ"""

    return await vuzopedia_service.get_vuzopedia_programs_service(
        db=db,
        max_cost=max_cost,
        min_score=min_score,
        q=q,
        page=page,
        size=size,
    )


@router.get("/{program_id}")
async def get_vuzopedia_program_by_id(
    program_id: int,
    db: AsyncSession = Depends(get_db),
):
    """Получить программу из Vuzopedia по ID"""
    return await vuzopedia_service.get_vuzopedia_program_by_id_service(program_id=program_id, db=db)
