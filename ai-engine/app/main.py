from fastapi import FastAPI
from pydantic import BaseModel
from analyzer import analyze_log

app = FastAPI()

class LogRequest(BaseModel):
    log: str

@app.get("/")
def health():
    return {"status": "ai-engine running"}

@app.post("/analyze")
def analyze(request: LogRequest):
    result = analyze_log(request.log)
    return {"analysis": result}