from fastapi import FastAPI
from app.routes import analyze   # ✅ correct path

app = FastAPI()

@app.get("/")
def health():
    return {"status": "backend running"}

app.include_router(analyze.router)