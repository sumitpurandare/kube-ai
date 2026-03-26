from fastapi import FastAPI
import logging

app = FastAPI()

logging.basicConfig(level=logging.INFO)

@app.get("/")
def read_root():
    logging.info("Root endpoint called")
    logging.error("🔥 TEST ERROR FROM SAMPLE APP 🔥")  # ✅ THIS MUST BE HERE
    return {"message": "Hello, K8s Logs!"}