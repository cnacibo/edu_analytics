from ml.analysis.analysis_service import AnalysisService

_analysis_service = None


def get_analysis_service():
    global _analysis_service
    if _analysis_service is None:
        _analysis_service = AnalysisService()
    return _analysis_service


async def get_vuz_programs_count_service():
    try:
        service = get_analysis_service()
        programs_count = service.get_all_programs()
        return {"status": "success", "data": {"total_programs": programs_count, "source": "vuz"}}
    except Exception as e:
        return {"status": "error", "message": str(e)}


async def get_vuz_programs_avg_cost_service():
    try:
        service = get_analysis_service()
        avg_cost = service.get_average_cost()
        return {"status": "success", "data": {"average_cost": round(avg_cost, 0), "source": "vuz"}}
    except Exception as e:
        return {"status": "error", "message": str(e)}


async def get_vuz_programs_min_paid_score_service():
    try:
        service = get_analysis_service()
        min_paid_score = service.get_min_paid_score()
        return {"status": "success", "data": {"min_paid_score": min_paid_score, "source": "vuz"}}
    except Exception as e:
        return {"status": "error", "message": str(e)}


async def get_vuz_programs_max_budget_score_service():
    try:
        service = get_analysis_service()
        max_budget_score = service.get_max_budget_score()
        return {
            "status": "success",
            "data": {"max_budget_score": max_budget_score, "source": "vuz"},
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}


async def get_top_programs_vuz_by_cost_service():
    try:
        service = get_analysis_service()
        top_programs = service.get_top_ten_programs()  # ошибка в методе
        return {"status": "success", "data": {"top_programs": top_programs, "source": "vuz"}}
    except Exception as e:
        return {"status": "error", "message": str(e)}


async def get_avg_cost_top10_vuz_service():
    try:
        service = get_analysis_service()
        avg_cost_top10 = service.get_avg_cost_top10()
        return {
            "status": "success",
            "data": {"avg_cost_top10": round(avg_cost_top10, 0), "source": "vuz"},
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}


async def get_vuz_spheres_distribution_service():
    try:
        service = get_analysis_service()
        spheres_distribution = service.get_pie_chart()
        return {
            "status": "success",
            "data": {"spheres_distribution": spheres_distribution, "source": "vuz"},
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}
