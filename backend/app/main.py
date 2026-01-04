import uvicorn
from fastapi import FastAPI

app = FastAPI(
    title="Edu Analytics API",
    description="Веб-приложение для анализа образовательных программ",
)


@app.get("/health")
async def health_check():
    """Проверка здоровья сервиса"""
    return {"status": "healthy", "service": "edu-analytics-backend"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
