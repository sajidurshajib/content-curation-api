from fastapi import FastAPI

from app.api.v1 import router as v1_router

app = FastAPI()

@app.get("/", tags=["Root"])
def docs():
    return {"message": "Root endpoint for the API. Use /docs for documentation."}

app.include_router(v1_router, prefix='/api/v1')