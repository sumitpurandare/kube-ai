def analyze_log(log_text: str):
    issues = []

    if "CrashLoopBackOff" in log_text:
        issues.append({
            "issue": "Pod CrashLoopBackOff",
            "reason": "Container keeps restarting",
            "suggestion": "Check container logs and startup commands"
        })

    if "OOMKilled" in log_text:
        issues.append({
            "issue": "Out of Memory",
            "reason": "Container exceeded memory limits",
            "suggestion": "Increase memory limits"
        })

    if "ImagePullBackOff" in log_text:
        issues.append({
            "issue": "Image Pull Failure",
            "reason": "Container image not found or unauthorized",
            "suggestion": "Check image name and registry credentials"
        })

    if not issues:
        return {
            "summary": "No known issues detected",
            "recommendation": "Manual inspection required"
        }

    return {
        "summary": f"{len(issues)} issue(s) detected",
        "details": issues
    }