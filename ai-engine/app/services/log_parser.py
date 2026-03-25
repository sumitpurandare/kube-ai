import re

def parse_logs(raw_logs: str):
    logs_list = []

    for line in raw_logs.splitlines():
        # Match: 2026-03-25 04:49:20,818 INFO message
        match = re.match(r'(\d{4}-\d{2}-\d{2}) (\S+) (INFO|ERROR|WARNING|DEBUG) (.+)', line)

        if match:
            date, time, level, message = match.groups()
            logs_list.append({
                "timestamp": f"{date} {time}",
                "level": level,
                "message": message
            })
        else:
            logs_list.append({"raw": line})

    return logs_list