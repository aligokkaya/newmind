from sqlalchemy import Column, String, Text, TIMESTAMP
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class CommentDB(Base):
    __tablename__ = "comments"

    comment_id = Column(UUID(as_uuid=True), primary_key=True)
    text = Column(Text, nullable=False)
    sentiment = Column(String(10), nullable=False)
    timestamp = Column(TIMESTAMP, nullable=False)