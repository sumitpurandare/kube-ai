
import subprocess
import json

def list_pods(namespace: str):
    result = subprocess.run(
        ["kubectl", "get", "pods", "-n", namespace, "-o", "json"],
        capture_output=True,
        text=True
    )

    pods_json = json.loads(result.stdout)

    pods = []

    for item in pods_json["items"]:
        name = item["metadata"]["name"]
        status = item["status"]["phase"]

        # 🔥 Check container state
        container_statuses = item["status"].get("containerStatuses", [])

        state = "Running"

        if container_statuses:
            state_info = container_statuses[0].get("state", {})

            if "waiting" in state_info:
                state = state_info["waiting"].get("reason")
            elif "terminated" in state_info:
                state = state_info["terminated"].get("reason")

        pods.append({
            "name": name,
            "status": status,
            "state": state
        })

    return pods

# ✅ Get logs for a pod
def get_pod_logs(namespace: str, pod: str):
    result = subprocess.run(
        [
            "kubectl",
            "logs",
            pod,
            "-n",
            namespace,
            "--tail=100"   # 🔥 important
        ],
        capture_output=True,
        text=True
    )

    return result.stdout