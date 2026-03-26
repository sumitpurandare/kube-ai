import re

def parse_logs(raw_logs: str):
    parsed = []

    for line in raw_logs.split("\n"):
        line = line.strip()

        if not line:
            continue

        if "ERROR" in line:
            parsed.append({
                "level": "ERROR",
                "message": line
            })
        elif "INFO" in line:
            parsed.append({
                "level": "INFO",
                "message": line
            })
        else:
            parsed.append({
                "raw": line
            })

    return parsed