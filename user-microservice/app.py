import logging

from fastapi import FastAPI
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend

from settings import settings
from routers.user_router import router as user_router
from routers.auth_router import router as auth_router
from utils.add_begin_data import router as fixtures_router
from redis import asyncio as aioredis

logging.getLogger('passlib').setLevel(logging.ERROR)

app = FastAPI(
    title="UserService",
)


@app.on_event("startup")
async def startup():
    redis = aioredis.from_url(f"redis://{settings.REDIS_HOST}")
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")


app.include_router(user_router)
app.include_router(auth_router)
app.include_router(fixtures_router)
