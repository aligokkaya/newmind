from fastapi import FastAPI, Depends, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from models.comment_model import CommentDB
from models.comment_schema import Comment
from db.database import SessionLocal

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/comments", response_model=List[Comment])
def get_comments(sentiment: Optional[str] = Query(None), db: Session = Depends(get_db)):
    query = db.query(CommentDB).order_by(CommentDB.timestamp.desc())

    if sentiment:
        query = query.filter(CommentDB.sentiment == sentiment)

    return query.all()