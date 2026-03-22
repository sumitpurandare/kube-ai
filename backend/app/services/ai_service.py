import requests

AI_ENGINE_URL = "http://ai-engine-service:8001/analyze"

def analyze_log(log_text: str):
    response = requests.post(
        AI_ENGINE_URL,
        json={"log": log_text}
    )
    return response.json()