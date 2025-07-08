from sqlalchemy.orm import relationship
from sqlalchemy import Integer, String, Column, Text, ForeignKey, Date, Boolean
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, UUID

from db import Base


# Модель пользователя, соответствующая таблице 'users' в базе данных
class User(Base):
    __tablename__ = "users"  # Название таблицы в БД

    # Уникальный идентификатор пользователя (первичный ключ)
    id = Column(Integer, primary_key=True, index=True)

    # Имя пользователя (уникальное и обязательное поле)
    username = Column(String, unique=True, nullable=False)

    # Хешированный пароль (не хранится в открытом виде, обязательно)
    password_hash = Column(String, nullable=False)

    # Полное имя пользователя (необязательное поле)
    full_name = Column(String, nullable=True)

    # Возраст пользователя (необязательное поле)
    age = Column(Integer, nullable=True)

    # Настроение или статус пользователя (необязательное поле)
    mood = Column(String, nullable=True)

    # Город пользователя (необязательное поле, используется для подбора мест)
    city = Column(String, nullable=True)

    # Является ли пользователь модератором (по умолчанию — нет)
    is_moderator = Column(Boolean, default=False)