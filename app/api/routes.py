from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.sql import func
from app.bd.database import get_db
from app.bd.models import Viewer
from typing import List
from pydantic import BaseModel

from fastapi_cache.decorator import cache # GPT!  
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from redis import asyncio as aioredis

router = APIRouter()

@router.on_event("startup")
async def startup():
    """GPT"""
    redis = aioredis.from_url("redis://localhost", encoding="utf8", decode_responses=True)
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")


class ViewerResponse(BaseModel):
    total_viewers: int
    date: str

@router.get("/viewers", response_model=List[ViewerResponse])
@cache(expire=300)  # 300 секунд = 5 минут GPT!!
async def get_viewers(db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(
            func.sum(Viewer.viewers).label("total_viewers"),
            func.to_char(Viewer.date_time, "YYYY-MM-DD HH24:MI").label("date")
        )
        .group_by("date")
        .order_by("date")
    )
    return result.mappings().all()
