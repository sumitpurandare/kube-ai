from app.services.k8s.pod_service import list_pods, get_pod_logs
from app.services.k8s.log_service import get_pod_logs
from app.services.log_parser import parse_logs
from app.services.ai_analyzer import analyze_logs
from app.services.ai_client import call_ai_engine

def analyze_namespace(namespace: str):
    pod_names = list_pods(namespace)

    results = []

    for pod in pod_names:
        try:
            raw_logs = get_pod_logs(namespace, pod)
            parsed_logs = parse_logs(raw_logs)
            issues = analyze_logs(parsed_logs)

            # ✅ DEBUG (move here)
            print("\n===== POD:", pod, "=====")
            print("RAW LOGS:\n", raw_logs[:300])
            print("PARSED LOGS:\n", parsed_logs[:3])
            print("ISSUES:\n", issues)

            # 🔥 Only run AI if issues found
            if issues:
                combined_logs = " ".join(
                    [issue.get("message", "") for issue in issues]
                )

                ai_result = call_ai_engine(combined_logs)

                results.append({
                    "pod_name": pod,
                    "status": "unhealthy",
                    "issues_found": issues,
                    "ai_analysis": ai_result
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