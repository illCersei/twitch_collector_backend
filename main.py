from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.api.routes import router
import uvicorn

from redis import asyncio as aioredis
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Инициализация Redis при запуске FastAPI"""
    redis = aioredis.from_url("redis://localhost", encoding="utf8", decode_responses=True)
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")
    
    yield  # Здесь можно добавить логику остановки сервиса (если нужно)

app = FastAPI(lifespan=lifespan)

app.include_router(router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
