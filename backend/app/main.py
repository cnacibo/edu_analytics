import uvicorn
from app.api import hse_analysis, vuzopedia_analysis
from fastapi import FastAPI

app = FastAPI(
    title="Edu Analytics API",
    description="Веб-приложение для анализа образовательных программ",
)

app.include_router(hse_analysis.router, prefix="/hse", tags=["HSE Analysis"])
app.include_router(vuzopedia_analysis.router, prefix="/vuzopedia", tags=["Vuzopedia Analysis"])


@app.get("/health", tags=["Health"])
async def health_check():
    """Проверка здоровья сервиса"""
    return {"status": "healthy", "service": "edu-analytics-backend"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
