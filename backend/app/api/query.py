from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Dict, Any, List
from app.rag.pipeline import rag_pipeline

router = APIRouter()

class QueryRequest(BaseModel):
    query: str

@router.post("/query")
def process_query(request: QueryRequest):
    try:
        result = rag_pipeline.run(request.query)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
