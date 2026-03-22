from fastapi import FastAPI
from routes import analyze

app = FastAPI()

@app.get("/")
def health():
    return {"status": "backend running"}

app.include_router(analyze.router)