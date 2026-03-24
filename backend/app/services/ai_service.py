import requests

AI_ENGINE_URL = "http://localhost:8001/analyze"

def call_ai_engine(logs: str):
    response = requests.post(
        AI_ENGINE_URL,
        json={"logs": logs},
        timeout=10
    )
    response.raise_for_status()
    return response.json()