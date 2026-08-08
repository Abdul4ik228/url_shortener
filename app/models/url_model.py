from sqlalchemy import Column, String, Integer, DateTime, Text, BigInteger
from sqlalchemy.sql import func
from ..database import Base

class URL(Base):
    """ Модель таблицы urls в базе данных. Хранит инфу о сокращенных ссылках"""

    __tablename__ = "urls"

    # Первичный ключ - уникальный ID записи
    id = Column(BigInteger, primary_key=True, autoincrement=True, index=True)

    # Короткий код (уникальный, по нему ищем ссылку)
    short_code = Column(String(10), unique=True, index=True, nullable=False)

    # Оригинальный длинный URL
    original_url = Column(Text, nullable=False)

    #Дата и время, когда ссылка становится не действительной
    expire_at = Column(DateTime, nullable=True)

    #Счетчик кликов по этой ссылке
    total_clicks = Column(Integer, default=0)

    #Дата создания записи (автоматически заполняется при вставке)
    created_at = Column(DateTime, server_default=func.now())