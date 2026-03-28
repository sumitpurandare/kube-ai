from app.services.k8s.pod_service import list_pods, get_pod_logs
from kube_ai_analyzer import parse_logs, analyze_logs


def analyze_namespace(namespace: str):

    pods = list_pods(namespace)

    results = []

    for pod in pods:
        pod_name = pod["name"]
        pod_state = pod["state"]

        # 🔥 STEP 1: Check K8s state FIRST
        if pod_state in ["CrashLoopBackOff", "ImagePullBackOff", "ErrImagePull"]:
            results.append({
                "pod_name": pod_name,
                "status": "unhealthy",
                "issues_found": [{
                    "level": "CRITICAL",
                    "message": f"Pod in {pod_state}"
                }],
                "ai_analysis": {
                    "issue": pod_state,
                    "root_cause": "Container failed to start properly",
                    "fix": "Check container logs and deployment configuration",
                    "confidence": 95
                }
            })
            continue  # 🚨 skip log analysis

        try:
            # 🔧 FIX: use pod_name
            raw_logs = get_pod_logs(namespace, pod_name)

            parsed_logs = parse_logs(raw_logs)
            issues, ai_analysis = analyze_logs(parsed_logs)
            if issues:
                issues = [
                {**issue, "level": "WARNING"}
                for issue in issues
                ]

                results.append({
                    "pod_name": pod_name,
                    "status": "unhealthy",
                    "issues_found": issues,
                    "ai_analysis": ai_analysis
                })
            else:
                results.append({
                    "pod_name": pod_name,
                    "status": "healthy",
                    "issues_found": [],
                    "ai_analysis": None
                })

        except Exception as e:
            results.append({
                "pod_name": pod_name,
                "status": "error",
                "error": str(e)
            })

    return {
        "namespace": namespace,
        "total_pods": len(pods),
        "pods": results
    }