from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Dict, Any
from app.db.database import get_db
from app.db.models import EvaluationRun, EvaluationResult
from app.evaluation.harness import harness

router = APIRouter()

@router.get("/evaluations")
def get_evaluations(db: Session = Depends(get_db)):
    runs = db.query(EvaluationRun).order_by(EvaluationRun.started_at.desc()).all()
    return runs
    
@router.get("/evaluations/{run_id}")
def get_evaluation_details(run_id: str, db: Session = Depends(get_db)):
    run = db.query(EvaluationRun).filter(EvaluationRun.id == run_id).first()
    if not run:
        raise HTTPException(status_code=404, detail="Run not found")
        
    results = db.query(EvaluationResult).filter(EvaluationResult.evaluation_run_id == run_id).all()
    
    return {
        "run": run,
        "results": results
    }
