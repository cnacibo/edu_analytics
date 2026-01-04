from typing import List, Optional

from fastapi import APIRouter, Query

router = APIRouter()


@router.get("/")
async def get_hse_programs(
    min_cost: Optional[int] = Query(None, description="Минимальная стоимость"),
    max_cost: Optional[int] = Query(None, description="Максимальная стоимость"),
):
    """Получить все программы НИУ ВШЭ с фильтрацией"""
    filters = {}
    if min_cost:
        filters["min_cost"] = min_cost
    if max_cost:
        filters["max_cost"] = max_cost

    programs = [{"title": "program 1", "price": 100}, {"title": "program 2", "price": 50}]

    return {"count": len(programs), "programs": programs, "filters_applied": filters}


@router.get("/compare")
async def compare_hse_programs(
    program_ids: List[int] = Query(..., description="ID программ для сравнения")
):
    """Сравнить 2 программы НИУ ВШЭ"""
    return {"comparison": "complete"}


@router.get("/{program_id}")
async def get_hse_program_by_id(program_id: int):
    """Получить программу НИУ ВШЭ по ID"""
    program = {"title": "program 1", "price": 100}
    return program
