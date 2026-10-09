from datetime import datetime
from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from app.core.database import Base


class PerformanceData(Base):
    __tablename__ = "performance_data"

    id = Column(Integer, primary_key=True, index=True)
    content_id = Column(Integer, ForeignKey("contents.id", ondelete="CASCADE"), nullable=False, index=True)
    platform = Column(String(30), nullable=False, index=True)
    metric_name = Column(String(50), nullable=False, index=True)
    metric_value = Column(Float, nullable=False, default=0)
    captured_at = Column(DateTime, default=datetime.utcnow, nullable=False, index=True)

    content = relationship("Content", back_populates="performance_records")
