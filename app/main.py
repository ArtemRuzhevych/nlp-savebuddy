from fastapi import FastAPI
from app.core.config import settings
from app.core.logging import setup_logging
from app.api.v1.routes import interpretation

setup_logging()

app = FastAPI(
    title=settings.APP_NAME,
    description="Microservice for interpreting fintech commands using QA models.",
    version="2.0.0"
)

app.include_router(interpretation.router, prefix="/api/v1", tags=["Interpretation"])

@app.get("/health")
def health_check():
    return {"status": "ok", "env": settings.APP_ENV}
