import re


def extract_details(log_text: str):
    pod_match = re.search(r"pod[ /]([a-z0-9-]+)", log_text)
    namespace_match = re.search(r"namespace[ /]([a-z0-9-]+)", log_text)

    pod = pod_match.group(1) if pod_match else "unknown"
    namespace = namespace_match.group(1) if namespace_match else None

    return {
        "pod": pod,
        "namespace": namespace
    }


def build_kubectl_logs_command(pod: str, namespace: str):
    """
    Build safe kubectl logs command
    """
    if pod == "unknown":
        return "Pod name not found in logs. Run: kubectl get pods -A"

    if namespace and namespace != "unknown":
        return f"Run: kubectl logs {pod} -n {namespace} (verify namespace exists)"
    
    return f"Run: kubectl logs {pod}"


def detect_issues(log_text: str, details: dict):
    """
    Detect known Kubernetes issues
    """
    issues = []

    pod = details["pod"]
    namespace = details["namespace"]

    if "CrashLoopBackOff" in log_text:
        issues.append({
            "issue": "CrashLoopBackOff",
            "severity": "critical",
            "reason": "Container keeps restarting repeatedly",
            "suggestion": build_kubectl_logs_command(pod, namespace)
        })

    if "OOMKilled" in log_text:
        issues.append({
            "issue": "OOMKilled",
            "severity": "critical",
            "reason": "Container exceeded memory limits",
            "suggestion": "Increase memory limits in deployment"
        })

    if "ImagePullBackOff" in log_text or "ErrImagePull" in log_text:
        issues.append({
            "issue": "Image Pull Error",
            "severity": "high",
            "reason": "Container image not found or access denied",
            "suggestion": "Check image name, tag, and registry credentials"
        })

    if "FailedScheduling" in log_text:
        issues.append({
            "issue": "Failed Scheduling",
            "severity": "high",
            "reason": "Pod cannot be scheduled on any node",
            "suggestion": "Check node resources, taints, and tolerations"
        })

    return issues


def calculate_severity(issues: list):
    """
    Determine overall severity
    """
    if any(i["severity"] == "critical" for i in issues):
        return "critical"
    if any(i["severity"] == "high" for i in issues):
        return "high"
    return "low"


def generate_root_cause(issues: list):
    """
    Generate human-readable root cause summary
    """
    names = [i["issue"] for i in issues]
    return f"Issues detected: {', '.join(names)}"


def get_priority_action(issues: list):
    """
    Suggest most important immediate action
    """
    for i in issues:
        if i["issue"] == "CrashLoopBackOff":
            return "Check application logs immediately using kubectl logs"
        if i["issue"] == "OOMKilled":
            return "Increase memory limits urgently"
        if i["issue"] == "Image Pull Error":
            return "Fix image name or registry access first"

    return "Investigate logs and cluster state"


def analyze_log(log_text: str):
    """
    Main analysis function
    """
    details = extract_details(log_text)
    issues = detect_issues(log_text, details)

    if not issues:
        return {
            "summary": "No known issues detected",
            "severity": "low",
            "details": [],
            "metadata": details,
            "recommendation": "Manual investigation required"
        }

    return {
        "summary": f"{len(issues)} issue(s) detected",
        "severity": calculate_severity(issues),
        "root_cause": generate_root_cause(issues),
        "priority_action": get_priority_action(issues),
        "details": issues,
        "metadata": details
    }