from fastapi import FastAPI
from pydantic import BaseModel
from services.ai_client import call_ai_engine

app = FastAPI()

class LogRequest(BaseModel):
    logs: str

@app.post("/analyze")
def analyze(req: LogRequest):
    result = call_ai_engine(req.logs)
    return result