from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.db.models import EvaluationRun

router = APIRouter()

@router.get("/dashboard/summary")
def get_dashboard_summary(db: Session = Depends(get_db)):
    # Get latest run
    latest_run = db.query(EvaluationRun).order_by(EvaluationRun.started_at.desc()).first()
    
    if not latest_run or not latest_run.metrics:
        return {
            "metrics": {
                "faithfulness": 0.0,
                "answer_relevance": 0.0,
                "correctness": 0.0,
                "recall_at_5": 0.0,
                "precision_at_5": 0.0,
                "mrr": 0.0,
                "failure_rate": 0.0,
                "average_latency_ms": 0.0
            },
            "status": "no_runs"
        }
        
    return {
        "metrics": latest_run.metrics,
        "status": "success",
        "latest_run_id": latest_run.id
    }
