from app.services import statistics_service
from fastapi import APIRouter

router = APIRouter()


@router.get("/metrics/vuz_programs_count")
async def get_vuz_programs_count():
    return await statistics_service.get_vuz_programs_count_service()


@router.get("/metrics/vuz_programs_avg_cost")
async def get_vuz_programs_avg_cost():
    return await statistics_service.get_vuz_programs_avg_cost_service()


@router.get("/metrics/vuz_programs_min_score_paid")
async def get_vuz_programs_min_score_paid():
    return await statistics_service.get_vuz_programs_min_score_paid_service()


@router.get("/metrics/vuz_programs_max_score_budget")
async def get_vuz_programs_max_score_budget():
    return await statistics_service.get_vuz_programs_max_score_budget_service()
