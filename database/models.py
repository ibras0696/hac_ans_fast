from datetime import datetime, timezone

from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean, Float

from database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    registered_at = Column(DateTime, default=datetime.now(timezone.utc))
    username = Column(String, unique=True, nullable=False)
    password_hash = Column(String, nullable=False)
    full_name = Column(String, nullable=True)
    is_moderator = Column(Boolean, default=False)

    preferences = relationship("UserPreferences", back_populates="user", uselist=False)
    history = relationship("ActivityHistory", back_populates="user")
    recommendations = relationship("Recommendation", back_populates="user")
    favorites = relationship("Favorite", back_populates="user")


class UserPreferences(Base):
    __tablename__ = "preferences"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    mood = Column(String)
    time_available = Column(Integer, default=0)
    budget = Column(Integer, default=0)

    user = relationship("User", back_populates="preferences")


class Activity(Base):
    __tablename__ = "activities"

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=False)
    category = Column(String, nullable=False)
    address = Column(String, nullable=False)
    images = Column(String, nullable=False)
    working_hours = Column(String, nullable=False)
    rating = Column(Float, nullable=False)

    history = relationship("ActivityHistory", back_populates="activity")
    recommendations = relationship("Recommendation", back_populates="activity")
    favorites = relationship("Favorite", back_populates="activity")  # Add this relationship


class ActivityHistory(Base):
    __tablename__ = "activity_history"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    activity_id = Column(Integer, ForeignKey("activities.id"))
    completed_at = Column(DateTime, default=datetime.now(timezone.utc))

    user = relationship("User", back_populates="history")
    activity = relationship("Activity", back_populates="history")


class Recommendation(Base):
    __tablename__ = "recommendations"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    activity_id = Column(Integer, ForeignKey("activities.id"))
    recommended_at = Column(DateTime, default=datetime.now(timezone.utc))
    accepted = Column(Boolean, default=False)

    user = relationship("User", back_populates="recommendations")
    activity = relationship("Activity", back_populates="recommendations")


class Favorite(Base):
    __tablename__ = "favorites"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    activity_id = Column(Integer, ForeignKey("activities.id"), nullable=False)
    added_at = Column(DateTime, default=datetime.now(timezone.utc))

    user = relationship("User", back_populates="favorites")
    activity = relationship("Activity", back_populates="favorites")  # This matches the new relationship in Activity