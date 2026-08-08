from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import RedirectResponse
from sqlalchemy.ext.asyncio import AsyncSession
from ...database import get_db
from ...redis_client import get_redis
from ...services.url_service import URLService
from ...schemas.url_schemas import URLCreate, URLResponse, StatsResponse
from ...core.exceptions import URLNotFoundError, URLExpiredError
from ...config import settings
import redis.asyncio as aioredis

router = APIRouter(prefix="/api/v1", tags=["url"])

# Редирект живет в корне, чтобы совпадать с short_url вида {BASE_DOMAIN}/{code}
redirect_router = APIRouter(tags=["redirect"])


@router.post("/shorten", response_model=URLResponse)
async def create_short_url(
    url_data: URLCreate,
    db: AsyncSession = Depends(get_db)
):
    """Создает короткую ссылку. Если expires_in не указан — ссылка вечная."""
    service = URLService(db)
    result = await service.create_short_url(url_data.original_url, url_data.expires_in)
    return result


@router.get("/stats/{short_code}", response_model=StatsResponse)
async def get_stats(
    short_code: str,
    db: AsyncSession = Depends(get_db)
):
    """Получает статистику по короткой ссылке."""
    service = URLService(db)
    try:
        return await service.get_stats(short_code)
    except URLNotFoundError:
        raise HTTPException(status_code=404, detail="Short URL not found")


@redirect_router.get("/{short_code}")
async def redirect_to_original(
    short_code: str,
    db: AsyncSession = Depends(get_db),
    redis: aioredis.Redis = Depends(get_redis)
):
    """
    Переходит по короткой ссылке.
    Сначала Redis (кэш URL), потом БД. Клики и expiry всегда через БД.
    """
    service = URLService(db)
    try:
        cached_url = await redis.get(f"url:{short_code}")
        if cached_url:
            await service.register_click(short_code)
            return RedirectResponse(url=cached_url, status_code=307)

        original_url = await service.get_original_url(short_code)
        await redis.setex(f"url:{short_code}", settings.REDIS_TTL, original_url)
        return RedirectResponse(url=original_url, status_code=307)

    except URLNotFoundError:
        raise HTTPException(status_code=404, detail="Short URL not found")
    except URLExpiredError:
        await redis.delete(f"url:{short_code}")
        raise HTTPException(status_code=410, detail="Short URL expired")
