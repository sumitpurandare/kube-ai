import requests
import subprocess

def get_namespaces():
    result = subprocess.run(["kubectl", "get", "ns", "-o", "jsonpath={.items[*].metadata.name}"],
                            capture_output=True, text=True)
    return result.stdout.split()

def get_pods(namespace: str):
    result = subprocess.run(
        ["kubectl", "get", "pods", "-n", namespace, "-o", "jsonpath={.items[*].metadata.name}"],
        capture_output=True, text=True
    )
    return result.stdout.split()
def fetch_logs(pod: str, namespace: str):
    result = subprocess.run(
        ["kubectl", "logs", pod, "-n", namespace],
        capture_output=True, text=True
    )
    return result.stdout
    
def analyze_logs(logs: str):
    try:
        response = requests.post(
            "http://localhost:9000/analyze",  # ✅ your working port
            json={"logs": logs}
        )
        return response.json()
    except Exception as e:
        return {
            "issue": "Backend Error",
            "root_cause": str(e),
            "fix": "Ensure backend is running",
            "confidence": 0
        }