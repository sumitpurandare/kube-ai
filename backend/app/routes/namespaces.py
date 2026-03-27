from fastapi import APIRouter
import subprocess

router = APIRouter()

@router.get("/namespaces")
def get_namespaces():
    result = subprocess.run(
        [
            "kubectl",
            "get",
            "ns",
            "-o",
            "jsonpath={.items[*].metadata.name}"
        ],
        capture_output=True,
        text=True
    )

    namespaces = result.stdout.split() if result.stdout else []

    return {"namespaces": namespaces}