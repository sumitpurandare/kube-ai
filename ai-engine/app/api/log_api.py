from fastapi import APIRouter, HTTPException
from app.services.aggregator.namespace_analyzer import analyze_namespace

router = APIRouter()

@router.get("/analyze-namespace/{namespace}")
def analyze_namespace_api(namespace: str):
    try:
        return analyze_namespace(namespace)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))