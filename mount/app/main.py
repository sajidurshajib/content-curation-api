from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from .services.connection import get_db
from .services.lifespan import lifespan
from sqlalchemy import text

from app.api.v1 import router as v1_router

app = FastAPI(lifespan=lifespan)


@app.get("/", tags=["Root"])
async def docs(db: AsyncSession = Depends(get_db)):
    try:
        await db.execute(text("SELECT 1"))
        return {"status": "🚀 DB runninng... 😄 "}
    except Exception as e:
        raise HTTPException(status_code=503, detail="Database connection failed")


app.include_router(v1_router, prefix='/api/v1')