from typing import Optional

from fastapi import APIRouter, Query

router = APIRouter()


@router.get("/search")
async def search_vuzopedia_programs(
    q: Optional[str] = Query("", description="Поисковый запрос"),
    university: Optional[str] = Query(None, description="Фильтр по университету"),
    min_score: Optional[int] = Query(None, description="Минимальный проходной балл"),
    max_cost: Optional[int] = Query(None, description="Максимальная стоимость"),
):
    """Поиск образовательных программ"""
    filters = {}
    if university:
        filters["university"] = university
    if min_score:
        filters["min_score"] = min_score
    if max_cost:
        filters["max_cost"] = max_cost

    if q:
        programs = [{"title": "program 1", "price": 100}]
        # programs = vuzopedia_service.search_programs(q, filters)
    else:
        programs = [{"title": "program 1", "price": 100}, {"title": "program 2", "price": 50}]
        # programs = vuzopedia_service.get_all_programs(filters)

    return {"query": q, "count": len(programs), "programs": programs, "filters": filters}


@router.get("/visualise")
async def visualise_vuzopedia_program_feature(program_id: int, feature: str):
    """Визуализация метрики образовательной программы"""
    return {"visualisation": "complete"}


@router.get("/{program_id}")
async def get_vuzopedia_program_by_id(program_id: int):
    """Получить программу из Vuzopedia по ID"""
    program = {"title": "program 1", "price": 100}
    return program
