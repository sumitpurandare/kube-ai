def analyze_logs(parsed_logs):
    issues = []

    for log in parsed_logs:
        message = log.get("message", "")
        raw = log.get("raw", "")

        if (
            "ERROR" in message
            or "ERROR" in raw
            or log.get("level") == "ERROR"
        ):
            issues.append(log)

    # -----------------------
    # 🔥 AI Logic
    # -----------------------
    ai_result = None

    if issues:
        combined = " ".join([i.get("message", "") for i in issues])

        if "CrashLoopBackOff" in combined:
            ai_result = {
                "issue": "CrashLoopBackOff",
                "root_cause": "Application failing during startup",
                "fix": "Check environment variables and startup command",
                "confidence": 90
            }

        elif "OOMKilled" in combined:
            ai_result = {
                "issue": "OOMKilled",
                "root_cause": "Container ran out of memory",
                "fix": "Increase memory limits",
                "confidence": 90
            }

        else:
            ai_result = {
                "issue": "Application error",
                "root_cause": "Runtime exception detected",
                "fix": "Check logs and stack trace",
                "confidence": 70
            }

    return issues, ai_result