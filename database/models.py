from datetime import datetime, timezone

from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean, Float

from .db import Base


# Модель пользователя, соответствующая таблице 'users' в базе данных
class User(Base):
    __tablename__ = "users"  # Название таблицы в БД

    # Уникальный идентификатор пользователя (первичный ключ)
    id = Column(Integer, primary_key=True, index=True)
    # Дата регистрации
    registered_at = Column(DateTime, default=datetime.now(timezone.utc))
    # Имя пользователя (уникальное и обязательное поле)
    username = Column(String, unique=True, nullable=False)
    # Хешированный пароль (не хранится в открытом виде, обязательно)
    password_hash = Column(String, nullable=False)
    # Полное имя пользователя (необязательное поле)
    full_name = Column(String, nullable=True)
    # Является ли пользователь модератором (по умолчанию — нет)
    is_moderator = Column(Boolean, default=False)

    # Отношения с другими таблицами
    preferences = relationship("UserPreferences", back_populates="user", uselist=False)  # 1:1
    history = relationship("ActivityHistory", back_populates="user")  # 1:N
    recommendations = relationship("Recommendation", back_populates="user")  # 1:N

# Модель предпочтений пользователя
class UserPreferences(Base):
    __tablename__ = "preferences"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))  # Связь с пользователем
    mood = Column(String)  # Настроение пользователя
    time_available = Column(Integer, default=0)  # Сколько времени есть
    budget = Column(Integer, default=0)  # Бюджет (низкий, средний, высокий)

    user = relationship("User", back_populates="preferences")

# Модель активностей (что можно делать)
class Activity(Base):
    __tablename__ = "activities"

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)  # Название активности
    description = Column(String, nullable=False)  # Описание
    category = Column(String, nullable=False)  # Категория (спорт, отдых, образование и т.д.)
    address = Column(String, nullable=False) # Адрес активности
    images = Column(String, nullable=False) # Ссылка на фотографию
    working_hours = Column(String, nullable=False) # Время работы
    rating = Column(Float, nullable=False)

    history = relationship("ActivityHistory", back_populates="activity")
    recommendations = relationship("Recommendation", back_populates="activity")

# История выполненных активностей
class ActivityHistory(Base):
    __tablename__ = "activity_history"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    activity_id = Column(Integer, ForeignKey("activities.id"))
    # Дата регистрации
    completed_at = Column(DateTime, default=datetime.now(timezone.utc))  # Когда выполнено

    # Обратная связь
    user = relationship("User", back_populates="history")
    activity = relationship("Activity", back_populates="history")

# Модель для хранения рекомендаций
class Recommendation(Base):
    __tablename__ = "recommendations"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    activity_id = Column(Integer, ForeignKey("activities.id"))
    recommended_at = Column(DateTime, default=datetime.now(timezone.utc))  # Когда выдана рекомендация
    accepted = Column(Boolean, default=False)  # Принял ли пользователь рекомендацию

    user = relationship("User", back_populates="recommendations")
    activity = relationship("Activity", back_populates="recommendations")
