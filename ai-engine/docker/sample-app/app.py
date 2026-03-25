from fastapi import FastAPI
import logging

app = FastAPI()

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")

@app.get("/")
def read_root():
    logging.info("Root endpoint called")
    logging.error("Sample error log")
    return {"message": "Hello, K8s Logs!"}