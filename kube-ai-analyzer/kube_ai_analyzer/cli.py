import sys
from .parser import parse_logs
from .analyzer import analyze_logs

def simple_ai_analysis(issues):
    if not issues:
        return None

    combined = " ".join([i.get("message", "") for i in issues])

    if "CrashLoopBackOff" in combined:
        return {
            "issue": "CrashLoopBackOff",
            "root_cause": "Application failing during startup",
            "fix": "Check environment variables and startup command",
        }

    if "OOMKilled" in combined:
        return {
            "issue": "OOMKilled",
            "root_cause": "Container ran out of memory",
            "fix": "Increase memory limits in deployment",
        }

    if "ERROR" in combined:
        return {
            "issue": "Application error",
            "root_cause": "Runtime exception detected",
            "fix": "Check stack trace and logs",
        }

    return None


def main():
    if len(sys.argv) < 3:
        print("Usage: kube-ai analyze <logfile> [--ai]")
        sys.exit(1)

    command = sys.argv[1]
    file_path = sys.argv[2]
    use_ai = "--ai" in sys.argv

    if command != "analyze":
        print("Unknown command")
        sys.exit(1)

    try:
        with open(file_path, "r") as f:
            logs = f.read()

        parsed = parse_logs(logs)
        issues = analyze_logs(parsed)

        print("\n🔍 Issues Found:\n")
        if issues:
            for issue in issues:
                print(issue)
        else:
            print("✅ No issues found")

        # 🔥 AI PART
        if use_ai and issues:
            ai_result = simple_ai_analysis(issues)

            if ai_result:
                print("\n🧠 AI Analysis:\n")
                print(f"Issue: {ai_result['issue']}")
                print(f"Root Cause: {ai_result['root_cause']}")
                print(f"Fix: {ai_result['fix']}")

    except Exception as e:
        print(f"Error: {e}")