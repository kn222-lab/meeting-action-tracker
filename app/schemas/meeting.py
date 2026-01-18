# app/schemas/meeting.py
from pydantic import BaseModel
from datetime import date

class MeetingCreate(BaseModel):
    title: str
    meeting_date: date
