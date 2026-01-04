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


@router.get("/compare_coures")
async def compare_hse_programs(
    program_ids: List[int] = Query(..., description="ID программ для сравнения")
):
    """Сравнить две программы НИУ ВШЭ"""
    return {"comparison": "complete"}


@router.get("/analyse_coures")
async def analyse_hse_program(program_id: int):
    """Провести анализ ПУДа программы НИУ ВШЭ"""
    return {"analysis": "complete"}


@router.get("/{program_id}")
async def get_hse_program_by_id(program_id: int):
    """Получить программу НИУ ВШЭ по ID"""
    program = {"title": "program 1", "price": 100}
    return program


@router.get("/{program_id}/courses")
async def get_hse_program_courses(program_id: int):
    """Получить все дисциплины программы НИУ ВШЭ по ее ID"""
    courses = [{"title": "course 1"}, {"title": "course 2"}]
    return courses


@router.get("/courses/{course_id}")
async def get_hse_course_by_id(course_id: int):
    """Получить данные о дисциплине НИУ ВШЭ по ID"""
    course = {"title": "course 1", "year": 1}
    return course
