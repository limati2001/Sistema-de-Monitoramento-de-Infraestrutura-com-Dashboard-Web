from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.sql import func
from app.core.database import Base

class CheckResult(Base):
    __tablename__ = "check_results"

    id = Column(Integer, primary_key=True, index=True)
    service_id = Column(Integer, ForeignKey("services.id"), nullable=False)
    status = Column(String, nullable=False)  # "up" ou "down"
    status_code = Column(Integer, nullable=True)
    latency_ms = Column(Float, nullable=True)
    error = Column(String, nullable=True)
    checked_at = Column(DateTime(timezone=True), server_default=func.now())