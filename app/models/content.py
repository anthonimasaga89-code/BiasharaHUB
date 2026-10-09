from datetime import datetime
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship
from app.core.database import Base


class Content(Base):
    __tablename__ = "contents"

    id = Column(Integer, primary_key=True, index=True)
    business_id = Column(Integer, ForeignKey("business.id", ondelete="CASCADE"), nullable=False, index=True)
    product_id = Column(Integer, ForeignKey("products.id", ondelete="SET NULL"), nullable=True, index=True)
    platform = Column(String(30), nullable=True, index=True)
    title = Column(String(255), nullable=True)
    body = Column(Text, nullable=False)
    media_url = Column(String(500), nullable=True)
    status = Column(String(30), nullable=False, default="DRAFT")
    scheduled_at = Column(DateTime, nullable=True)
    provider_post_id = Column(String(255), nullable=True)
    failure_reason = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    business = relationship("Business", back_populates="contents")
    product = relationship("Product", back_populates="content")
    performance_records = relationship("PerformanceData", back_populates="content", cascade="all, delete-orphan")
