from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update
from datetime import datetime, timedelta, timezone
from ..models.url_model import URL
from ..core.generator import generate_short_code
from ..core.exceptions import URLNotFoundError, URLExpiredError
from ..config import settings


def _utcnow() -> datetime:
    """Наивный UTC-момент: колонка expire_at объявлена как DateTime без таймзоны."""
    return datetime.now(timezone.utc).replace(tzinfo=None)


class URLService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_short_url(self, original_url: str, expires_in: int = None) -> dict:
        """
        Создает короткую ссылку.
        Если ссылка с таким URL уже есть — возвращаем существующий код (идемпотентность).
        """
        original_url = str(original_url)

        # 1. Генерируем код
        short_code = generate_short_code(original_url)

        # 2. Проверяем, нет ли уже такой ссылки в БД (чтобы не плодить дубли)
        stmt = select(URL).where(URL.original_url == original_url)
        result = await self.db.execute(stmt)
        existing = result.scalar_one_or_none()

        if existing:
            # Если уже есть, возвращаем старую ссылку (так делают все сервисы типа Bitly)
            return {
                "short_url": f"{settings.BASE_DOMAIN}/{existing.short_code}",
                "short_code": existing.short_code,
                "expires_at": existing.expire_at
            }

        # 3. Если такой ссылки нет — создаем новую
        expire_at = None
        if expires_in:
            expire_at = _utcnow() + timedelta(seconds=expires_in)

        new_url = URL(
            short_code=short_code,
            original_url=original_url,
            expire_at=expire_at
        )
        self.db.add(new_url)
        await self.db.commit()
        await self.db.refresh(new_url)

        return {
            "short_url": f"{settings.BASE_DOMAIN}/{short_code}",
            "short_code": short_code,
            "expires_at": expire_at
        }

    async def _get_active_url(self, short_code: str) -> URL:
        """Достаёт запись и проверяет, что ссылка существует и не просрочена."""
        stmt = select(URL).where(URL.short_code == short_code)
        result = await self.db.execute(stmt)
        url_entry = result.scalar_one_or_none()

        if not url_entry:
            raise URLNotFoundError(f"Short URL with code '{short_code}' not found")

        if url_entry.expire_at and url_entry.expire_at < _utcnow():
            raise URLExpiredError(f"Short URL '{short_code}' has expired")

        return url_entry

    async def _increment_clicks(self, url_id: int) -> None:
        await self.db.execute(
            update(URL)
            .where(URL.id == url_id)
            .values(total_clicks=URL.total_clicks + 1)
        )
        await self.db.commit()

    async def register_click(self, short_code: str) -> None:
        """Проверяет expiry и увеличивает счётчик (для hit в Redis-кэше)."""
        url_entry = await self._get_active_url(short_code)
        await self._increment_clicks(url_entry.id)

    async def get_original_url(self, short_code: str) -> str:
        """
        Ищет оригинальный URL по короткому коду в БД.
        Проверяет, не истек ли срок годности.
        """
        url_entry = await self._get_active_url(short_code)
        await self._increment_clicks(url_entry.id)
        return url_entry.original_url

    async def get_stats(self, short_code: str) -> dict:
        """
        Возвращает статистику по ссылке (количество кликов, дата создания и т.д.).
        """
        stmt = select(URL).where(URL.short_code == short_code)
        result = await self.db.execute(stmt)
        url_entry = result.scalar_one_or_none()

        if not url_entry:
            raise URLNotFoundError(f"Short URL with code '{short_code}' not found")

        return {
            "short_code": url_entry.short_code,
            "original_url": url_entry.original_url,
            "total_clicks": url_entry.total_clicks,
            "created_at": url_entry.created_at,
            "expires_at": url_entry.expire_at
        }
