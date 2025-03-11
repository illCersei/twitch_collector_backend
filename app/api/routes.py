from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.sql import func
from app.bd.database import get_db
from app.bd.models import Viewer, Game
from typing import List
from pydantic import BaseModel

from fastapi_cache.decorator import cache

router = APIRouter()

class ViewerResponse(BaseModel):
    total_viewers: int
    date: str

class GamesResponse(BaseModel):
    game_id: int
    game_name: str

@router.get("/games", response_model=List[GamesResponse])
async def get_games(db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(
            Game.game_id.label("game_id"),
            Game.game_name.label("game_name")
        )
    )
    return result.mappings().all()

@router.get("/viewers", response_model=List[ViewerResponse])
@cache(expire=300)  # Кеширование на 5 минут
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
