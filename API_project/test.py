from fastapi import FastAPI, HTTPException, Depends
from datetime import date, timedelta
from typing import List
from database import Base, SessionLocal, engine
from sqlalchemy.orm import Session
from sqlalchemy import desc
from table_post import Post
from table_user import User
from table_feed import Feed

from schema import UserGet, PostGet, FeedGet

if __name__ == "__main__":
    id = 201
    limit = 10
    Base.metadata.create_all(engine)
    session = SessionLocal()
    res = [
        (i.action, i.post_id, i.time, i.user_id)
        for i in (
            session.query(Feed)
            .filter(Feed.user_id == id)
            .order_by(desc(Feed.time))
            .limit(limit)
            .all()
        )
    ]
    print(res)
