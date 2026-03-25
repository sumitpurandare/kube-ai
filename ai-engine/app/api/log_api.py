from fastapi import APIRouter, HTTPException
from app.services.log_ingestor import get_pod_logs, get_pods
from app.services.log_parser import parse_logs
from app.services.ai_analyzer import analyze_logs

router = APIRouter()

@router.get("/analyze-namespace/{namespace}")
def analyze_namespace(namespace: str):
    try:
        pod_names = get_pods(namespace)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    results = []

    for pod in pod_names:
        try:
            raw_logs = get_pod_logs(namespace, pod)
            parsed = parse_logs(raw_logs)
            issues = analyze_logs(parsed)

            results.append({
                "pod_name": pod,
                "issues_found": issues
            })

        except Exception as e:
            results.append({
                "pod_name": pod,
                "error": str(e)
            })

    return {
        "namespace": namespace,
        "total_pods": len(pod_names),
        "pods": results
    }