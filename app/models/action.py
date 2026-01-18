# app/models/action.py
from sqlalchemy import Column, Integer, String, Date, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base

class Action(Base):
    __tablename__ = "actions"

    id = Column(Integer, primary_key=True, index=True)
    meeting_id = Column(Integer, ForeignKey("meetings.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)

    content = Column(String, nullable=False)
    due_date = Column(Date, nullable=False)
    status = Column(String, default="未着手")

    created_at = Column(DateTime, default=datetime.utcnow)

    meeting = relationship("Meeting", back_populates="actions")
