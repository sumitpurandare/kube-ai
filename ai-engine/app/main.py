from fastapi import FastAPI
from pydantic import BaseModel
from analyzer import analyze_log
from app.api import log_api   # ✅ ADD THIS

import os

print("🔥 RUNNING FILE:", __file__)
print("🔥 THIS MAIN.PY IS RUNNING")

app = FastAPI(title="🔥 SUMIT FINAL SERVER 🔥", version="999.0.0")

# ✅ Router registration
app.include_router(log_api.router)

class LogRequest(BaseModel):
    logs: str

print("🔥 MODEL FIELDS:", LogRequest.model_fields)

@app.post("/analyze")
def analyze(req: LogRequest):
    print("🔥 RECEIVED:", req.logs)
    result = analyze_log(req.logs)
    return {
        "issue": result.get("summary", "Unknown"),
        "root_cause": result.get("root_cause", "Not identified"),
        "fix": result.get("priority_action", "No suggestion available"),
        "confidence": 90 if result.get("severity") == "critical" else 70
    }

# Debug routes
for route in app.routes:
    print("🔥 ROUTE:", route.path, route.name)