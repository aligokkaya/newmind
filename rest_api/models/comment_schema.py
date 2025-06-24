from pydantic import BaseModel
from datetime import datetime
from uuid import UUID

class Comment(BaseModel):
    comment_id: UUID
    text: str
    sentiment: str
    timestamp: datetime

    class Config:
        from_attributes = True