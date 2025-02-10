from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.bd.database import get_db
from app.bd.models import Game, Viewer
from typing import List
from pydantic import BaseModel

from sqlalchemy.sql import func

router = APIRouter()

class GameResponse(BaseModel):
    game_id: int
    game_name: str

class ViewerResponse(BaseModel):
    total_viewers: int
    date: str

@router.get("/games", response_model=List[GameResponse])
async def get_games(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Game))
    return result.scalars().all()

@router.get("/viewers", response_model=List[ViewerResponse])
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

