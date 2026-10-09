from datetime import datetime
from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from app.core.database import Base


class SocialAccount(Base):
    __tablename__ = "social_accounts"

    id = Column(Integer, primary_key=True, index=True)
    business_id = Column(Integer, ForeignKey("business.id", ondelete="CASCADE"), nullable=False, index=True)
    platform = Column(String(30), nullable=False, index=True)
    account_name = Column(String(150), nullable=False)
    account_id = Column(String(255), nullable=False)
    access_token = Column(String(2000), nullable=False)
    refresh_token = Column(String(2000), nullable=True)
    token_expires_at = Column(DateTime, nullable=True)
    is_connected = Column(Boolean, nullable=False, default=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    business = relationship("Business", back_populates="social_accounts")
