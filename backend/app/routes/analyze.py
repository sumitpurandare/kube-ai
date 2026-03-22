from fastapi import APIRouter, UploadFile
from services.ai_service import analyze_log

router = APIRouter()

@router.post("/analyze")
async def analyze(file: UploadFile):
    content = await file.read()
    result = analyze_log(content.decode())
    return {"result": result}