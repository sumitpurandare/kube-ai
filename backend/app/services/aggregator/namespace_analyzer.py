from app.services.k8s.pod_service import list_pods, get_pod_logs
from kube_ai_analyzer import parse_logs, analyze_logs


def analyze_namespace(namespace: str):
    pod_names = list_pods(namespace)

    results = []

    for pod in pod_names:
        try:
            raw_logs = get_pod_logs(namespace, pod)
            parsed_logs = parse_logs(raw_logs)
            issues, ai_analysis = analyze_logs(parsed_logs)

            if issues:
                results.append({
                    "pod_name": pod,
                    "status": "unhealthy",
                    "issues_found": issues,
                    "ai_analysis": ai_analysis
                })
            else:
                results.append({
                    "pod_name": pod,
                    "status": "healthy",
                    "issues_found": [],
                    "ai_analysis": None
                })

        except Exception as e:
            results.append({
                "pod_name": pod,
                "status": "error",
                "error": str(e)
            })

    return {
        "namespace": namespace,
        "total_pods": len(pod_names),
        "pods": results
    }