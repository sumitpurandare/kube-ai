import subprocess

# ✅ Get all pods in namespace
def list_pods(namespace: str):
    result = subprocess.run(
        [
            "kubectl",
            "get",
            "pods",
            "-n",
            namespace,
            "-o",
            "jsonpath={.items[*].metadata.name}"
        ],
        capture_output=True,
        text=True
    )

    if result.stdout:
        return result.stdout.split()

    return []


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