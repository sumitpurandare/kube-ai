def analyze_logs(parsed_logs):
    issues = []

    for log in parsed_logs:
        message = log.get("message", "")

        # Detect ERROR even if parsing imperfect
        if "ERROR" in message or log.get("level") == "ERROR":
            issues.append(log)

    return issues