from app.services import statistics_service
from fastapi import APIRouter

router = APIRouter()


@router.get("/metrics/vuz_programs_count")
async def get_vuz_programs_count():
    return await statistics_service.get_vuz_programs_count_service()


@router.get("/metrics/vuz_programs_avg_cost")
async def get_vuz_programs_avg_cost():
    return await statistics_service.get_vuz_programs_avg_cost_service()


@router.get("/metrics/vuz_programs_min_paid_score")
async def get_vuz_programs_min_score_paid():
    return await statistics_service.get_vuz_programs_min_paid_score_service()


@router.get("/metrics/vuz_programs_max_budget_score")
async def get_vuz_programs_max_score_budget():
    return await statistics_service.get_vuz_programs_max_budget_score_service()


@router.get("/cost/vuz_top_programs_by_cost")
async def get_top_programs_vuz_by_cost():
    return await statistics_service.get_top_programs_vuz_by_cost_service()


@router.get("/cost/vuz_avg_cost_top10")
async def get_avg_cost_top10_vuz():
    return await statistics_service.get_avg_cost_top10_vuz_service()


@router.get("/spheres/vuz_spheres_distribution")
async def get_vuz_spheres_distribution():
    return await statistics_service.get_vuz_spheres_distribution_service()


@router.get("/spheres/vuz_spheres_level_cost_dist")
async def get_vuz_spheres_level_cost_dist():
    return await statistics_service.get_vuz_spheres_level_cost_dist_service()


@router.get("/map/vuz_programs_map_bachelor")
async def get_vuz_programs_map_bachelor():
    return await statistics_service.get_vuz_programs_map_bachelor_service()


@router.get("/map/vuz_programs_map_master")
async def get_vuz_programs_map_master():
    return await statistics_service.get_vuz_programs_map_master_service()


@router.get("/prospects/vuz_professions_wordcloud_data")
async def get_vuz_professions_wordcloud_data():
    return await statistics_service.get_vuz_professions_wordcloud_data_service()
