from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.db.database import engine, Base

# Create tables (for production, use Alembic)
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.PROJECT_NAME,
    description="Production-Grade RAG Evaluation & Benchmarking Platform",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # In production, restrict this
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/health")
def health_check():
    return {"status": "ok", "project": settings.PROJECT_NAME, "mock_mode": settings.MOCK_MODE}

from app.api import query, dashboard, evaluations

app.include_router(query.router, prefix="/api", tags=["query"])
app.include_router(dashboard.router, prefix="/api", tags=["dashboard"])
app.include_router(evaluations.router, prefix="/api", tags=["evaluations"])
