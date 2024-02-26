from fastapi import FastAPI, HTTPException, Depends
from datetime import date, timedelta
from pydantic import BaseModel
from typing import List
from loguru import logger
import psycopg2
from psycopg2.extras import RealDictCursor

app = FastAPI()


class User(BaseModel):
    name: str
    surname: str
    age: int
    registration_date: date

    class Config:
        orm_mode = True


class PostResponse(BaseModel):
    id: int
    text: str
    topic: str

    class Config:
        orm_mode = True


def get_db():
    return psycopg2.connect(
        "postgresql://robot-startml-ro:pheiph0hahj1Vaif@postgres.lab.karpov.courses:6432/startml",
        cursor_factory=RealDictCursor,
    )


# @app.get("/sum_date")
# def sum_date(current_date: date, offset: int) -> date:
#     return current_date + timedelta(days=offset)

# @app.post("/user/validate") # , response_model=List[User]
# def validate(user_info: User):
#     #logger.info("OK")

#     res = f"Will add user: {user_info.name} {user_info.surname} with age {user_info.age}"

#     return res


@app.get("/post/{id}", response_model=PostResponse)
def user_id(id: int, db=Depends(get_db)) -> PostResponse:
    with db.cursor() as cursor:
        cursor.execute(
            """SELECT id, text, topic FROM "post" WHERE id=%(user_id)s""",
            {"user_id": id},
        )
        res = cursor.fetchone()
        if res != None:
            return PostResponse(**res)
        else:
            raise HTTPException(status_code=404, detail="post not found")
