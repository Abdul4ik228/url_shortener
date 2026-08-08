from pydantic import AfterValidator, BaseModel, Field, HttpUrl, TypeAdapter
from datetime import datetime
from typing import Annotated, Optional

_http_url_adapter = TypeAdapter(HttpUrl)

# Проверяем значение как HttpUrl, но наружу отдаем обычную строку:
# HttpUrl нельзя ни хэшировать, ни писать в текстовую колонку напрямую.
HttpUrlStr = Annotated[
    str,
    AfterValidator(lambda value: str(_http_url_adapter.validate_python(value))),
]


class URLCreate(BaseModel):
    """
    Схема для запроса на создание короткой ссылки (POST /shorten).
    """
    original_url: HttpUrlStr
    expires_in: Optional[int] = Field(default=None, gt=0)  # Срок жизни в секундах (None — бессрочная)


class URLResponse(BaseModel):
    """
    Схема для ответа после создания ссылки.
    """

    short_url: str
    short_code: str
    expires_at: Optional[datetime]


class StatsResponse(BaseModel):
    """
    Схема для ответа со статистикой (GET /stats/{code}).
    """

    short_code: str
    original_url: str
    total_clicks: int
    created_at: datetime
    expires_at: Optional[datetime]
