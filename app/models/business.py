from datetime import datetime
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship
from app.core.database import Base


class Business(Base):
    __tablename__ = "business"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    description = Column(Text, nullable=True)
    phone = Column(String(30), nullable=True)
    location = Column(String(150), nullable=True)
    status = Column(String(20), default="active", nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    owner = relationship("User", back_populates="businesses")
    products = relationship("Product", back_populates="business", cascade="all, delete-orphan")
    social_accounts = relationship("SocialAccount", back_populates="business", cascade="all, delete-orphan")
    contents = relationship("Content", back_populates="business", cascade="all, delete-orphan")
    orders = relationship("Order", back_populates="business")
