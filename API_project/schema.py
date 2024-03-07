from fastapi import FastAPI, HTTPException, Depends
from datetime import date, timedelta, datetime
from pydantic import BaseModel
from typing import List
from loguru import logger
import psycopg2
from psycopg2.extras import RealDictCursor

app = FastAPI()


class UserGet(BaseModel):
    id: int
    gender: int
    age: int
    country: str
    city: str
    exp_group: int
    os: str
    source: str

    class Config:
        orm_mode = True


class PostGet(BaseModel):
    id: int
    text: str
    topic: str

    class Config:
        orm_mode = True


class FeedGet(BaseModel):
    action: str
    post_id: int
    time: datetime
    user_id: int
    user: UserGet
    post: PostGet

    class Config:
        orm_mode = True
