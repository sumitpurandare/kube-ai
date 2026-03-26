from fastapi import APIRouter
from pydantic import BaseModel
from app.services.ai_client import call_ai_engine
from app.services.aggregator.namespace_analyzer import analyze_namespace

router = APIRouter()

# -----------------------
# AI Log Analysis
# -----------------------
class LogRequest(BaseModel):
    logs: str

@router.post("/analyze")
def analyze(req: LogRequest):
    return call_ai_engine(req.logs)


# -----------------------
# Namespace Analysis (K8s + AI)
# -----------------------
@router.get("/analyze-namespace/{namespace}")
def analyze_namespace_api(namespace: str):
    return analyze_namespace(namespace)