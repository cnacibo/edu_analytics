from typing import Optional

from fastapi import APIRouter, Query

router = APIRouter()


@router.get("/universities")
async def get_all_universities():
    """Получить список всех университетов"""
    universities = [
        {"title": "university 1", "city": "Moscow"},
        {"title": "university 2", "city": "Vladimir"},
    ]

    return {"count": len(universities), "universities": universities}


@router.get("/search")
async def search_programs(
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


@router.get("/universities/{university_name}")
async def get_university_programs(university_name: str):
    """Получить все программы конкретного университета"""
    # programs = vuzopedia_service.get_programs_by_university(university_name)
    programs = [{"title": "program 1", "price": 100}, {"title": "program 2", "price": 50}]

    return {
        "university": university_name,
        "total_programs": len(programs),
        "programs": programs,
    }
