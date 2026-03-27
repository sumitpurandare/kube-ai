from fastapi import FastAPI
from app.routes import analyze   # ✅ correct path
from app.routes import namespaces

app = FastAPI()

@app.get("/")
def health():
    return {"status": "backend running"}

app.include_router(analyze.router)
app.include_router(namespaces.router)