from fastapi import APIRouter

router = APIRouter()


@router.get("/metrics/vuz_programs_count")
async def get_vuz_programs_count():
    return 100


@router.get("/metrics/vuz_programs_avg_cost")
async def get_vuz_programs_avg_cost():
    return 100000


@router.get("/metrics/vuz_programs_min_score_paid")
async def get_vuz_programs_min_score_paid():
    return 10


@router.get("/metrics/vuz_programs_max_score_budget")
async def get_vuz_programs_max_score_budget():
    return 1000
