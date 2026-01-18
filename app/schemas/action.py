# app/schemas/action.py
from pydantic import BaseModel
from datetime import date

class ActionCreate(BaseModel):
    meeting_id: int
    content: str
    due_date: date


from pydantic import BaseModel
from datetime import date, datetime
from typing import Optional

class ActionResponse(BaseModel):
    id: int
    meeting_id: int
    user_id: Optional[int]
    content: str
    status: str
    due_date: date
    created_at: datetime

    class Config:
        orm_mode = True

from typing import Optional
from datetime import date
from pydantic import BaseModel

class ActionUpdate(BaseModel):
    content: Optional[str] = None
    due_date: Optional[date] = None
    status: Optional[str] = None
