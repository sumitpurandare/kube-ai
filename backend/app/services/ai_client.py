def call_ai_engine(logs: str):
    # 🔥 Simple intelligent mock (upgrade later to GPT)

    logs_lower = logs.lower()

    if "crashloopbackoff" in logs_lower:
        return {
            "issue": "CrashLoopBackOff detected",
            "root_cause": "Application is crashing repeatedly",
            "fix": "Check container startup logs and environment variables",
            "confidence": 90
        }

    elif "oomkilled" in logs_lower:
        return {
            "issue": "OOMKilled detected",
            "root_cause": "Container ran out of memory",
            "fix": "Increase memory limits in deployment",
            "confidence": 95
        }

    elif "error" in logs_lower:
        return {
            "issue": "Generic error found",
            "root_cause": "Application error detected in logs",
            "fix": "Check stack trace for more details",
            "confidence": 70
        }

    else:
        return {
            "issue": "No major issue detected",
            "root_cause": "Logs look normal",
            "fix": "No action needed",
            "confidence": 60
        }