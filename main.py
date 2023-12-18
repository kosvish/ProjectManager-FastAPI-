from fastapi import FastAPI
from src.auth.router import router as user_router
from src.verefication.router import router as verif_router
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from redis import asyncio as aioredis


app = FastAPI(title="GitHub")

app.include_router(user_router)
app.include_router(verif_router)


@app.on_event("startup")
async def startup_event():
    redis = aioredis.from_url("redis://localhost", encoding="utf-8", decode_reponse=True)
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")




