from sqlalchemy import Column, Integer, Float, String, DateTime
from datetime import datetime
from src.database import Base

class WaterLog(Base):
    __tablename__ = "water_logs"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, index=True, default="user_1")
    amount_ml = Column(Float, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)
    ai_insight = Column(String, nullable=True)
