def analyze_logs(parsed_logs):
    issues = []

    for log in parsed_logs:
        message = log.get("message", "")
        raw = log.get("raw", "")

        if (
            "ERROR" in message
            or log.get("level") == "ERROR"
            or "ERROR" in raw   # 🔥 THIS IS THE FIX
        ):
            issues.append(log)

    return issues