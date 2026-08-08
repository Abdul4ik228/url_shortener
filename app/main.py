from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from .api.v1.endpoints import router as url_router, redirect_router
from .redis_client import close_redis

STATIC_DIR = Path(__file__).resolve().parent / "static"


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    await close_redis()


app = FastAPI(
    title="URL Shortener Service",
    description="Сервис сокращения ссылок с кэшированием в Redis",
    version="1.0.0",
    lifespan=lifespan
)

app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")
app.include_router(url_router)


@app.get("/")
async def root():
    return FileResponse(STATIC_DIR / "index.html")


# Регистрируется последним: "/{short_code}" перехватил бы остальные пути
app.include_router(redirect_router)
