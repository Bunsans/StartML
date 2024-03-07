from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, text
from typing import List
from datetime import datetime
from catboost import CatBoostClassifier
import pandas as pd
import os
from pydantic import BaseModel
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, Integer, String, desc, func


from heapq import nlargest
import random
import numpy as np
import pandas as pd


# from database import SessionLocal
### database
SQLALCHEMY_DATABASE_URL = "postgresql://robot-startml-ro:pheiph0hahj1Vaif@postgres.lab.karpov.courses:6432/startml"

engine = create_engine(SQLALCHEMY_DATABASE_URL)  # ,  pool_size=0, max_overflow=20)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


# from table_post import Post
# Post
class Post(Base):
    __tablename__ = "post"
    id = Column(Integer, primary_key=True)
    text = Column(String)
    topic = Column(String)


# from finder import recomend_finder
### finder
# def find_neighb(user_target, user_post_like, posts, NUMBER_OF_REC=50):
#     NUMBER_OF_NEIGHB = 100
#     SMALLEST_NUMBER_OF_INTER = 10

#     list_neighb = []
#     user_check = set()

#     user_target_likes_posts = eval(user_post_like.loc[user_target, "post_like"])
#     # can be before
#     all_posts = set(posts.unique())
#     not_liked_before = all_posts - user_target_likes_posts
#     ### should think about posts which user have been viewed, but not liked

#     # choice random users for next check
#     while len(user_check) < NUMBER_OF_NEIGHB:
#         x = random.choice(user_post_like.index)
#         if x not in user_check:
#             user_check.add(x)

#     # There we will know how close user_1 to usr in user_check
#     for user_1 in user_check:
#         list_neighb.append(
#             (
#                 len(
#                     user_target_likes_posts
#                     & eval(user_post_like.loc[user_1, "post_like"])
#                 ),
#                 user_1,
#             )
#         )
#     # if they intersection is small it is good. Take
#     res_nearest = nlargest(SMALLEST_NUMBER_OF_INTER, list_neighb, key=lambda x: x[0])
#     res_recom_posts = set()
#     count = 0
#     for _, neighb in res_nearest:
#         # user targ not liked but can be interested
#         try:
#             post = (
#                 eval(user_post_like.loc[neighb, "post_like"]) - user_target_likes_posts
#             ).pop()
#             if post not in res_recom_posts and post in not_liked_before:
#                 res_recom_posts.add(post)
#                 count += 1
#             if count >= NUMBER_OF_REC:
#                 return res_recom_posts
#         except KeyError:
#             pass

#     # count < NUMBER_OF_REC take not liked posts
#     while count < NUMBER_OF_REC:

#         post_not_liked = random.choice(posts)
#         if post_not_liked not in res_recom_posts and post in not_liked_before:
#             res_recom_posts.add(post_not_liked)
#             count += 1

#     return res_recom_posts


# def recomend_finder(
#     test_user_id, user_post_like, res_user, res_post_text, time_diff, catboost_model
# ):
#     NUMBER_OF_REC = 50
#     posts = res_post_text["post_id"]

#     ### making dframe to model

#     possible_posts = list(
#         find_neighb(test_user_id, user_post_like, posts, NUMBER_OF_REC=50)
#     )

#     pair_user_posts = np.array([[test_user_id] * NUMBER_OF_REC, possible_posts]).T
#     pair_user_posts = pd.DataFrame(pair_user_posts, columns=["user_id", "post_id"])
#     data_to_model = pair_user_posts.merge(res_user, on="user_id", how="left").merge(
#         res_post_text, on="post_id", how="left"
#     )
#     time_delta = np.array([time_diff] * NUMBER_OF_REC)
#     data_to_model.columns
#     data_to_model.insert(len(data_to_model.columns), "time_delta", time_delta)

#     ### think about time but later
#     # обработать время
#     # data_to_model['time_delta']=[80] * NUMBER_OF_REC
#     ##################

#     data_to_model = data_to_model.drop(["user_id", "post_id"], axis=1)
#     predict_model = catboost_model.predict_proba(data_to_model).tolist()
#     for i in range(len(predict_model)):
#         predict_model[i][0] = possible_posts[i]
#     predict_model.sort(reverse=True, key=(lambda x: x[1]))
#     result_rec = []
#     for preds in predict_model[:5]:
#         result_rec.append(preds[0])

#     return tuple(result_rec)


def recomend_finder(test_user_id, res_user, res_post_text, time_diff, catboost_model):
    posts_filter = res_post_text["post_id"].unique().tolist()
    random.shuffle(posts_filter)
    posts_filter = posts_filter[:3000]

    pair_user_posts = np.array(
        [
            [test_user_id] * len(posts_filter),
            posts_filter,
        ]
    ).T
    pair_user_posts = pd.DataFrame(pair_user_posts, columns=["user_id", "post_id"])
    data_to_model = pair_user_posts.merge(res_user, on="user_id", how="left").merge(
        res_post_text, on="post_id", how="left"
    )
    time_delta = np.array([time_diff] * len(posts_filter))
    # data_to_model.columns
    data_to_model.insert(len(data_to_model.columns), "time_delta", time_delta)
    data_to_model = data_to_model.drop(["user_id", "post_id"], axis=1)
    predict_model = catboost_model.predict_proba(data_to_model).tolist()
    for i in range(len(predict_model)):
        predict_model[i][0] = posts_filter[i]
    predict_model.sort(reverse=True, key=(lambda x: x[1]))
    result_rec = []
    for preds in predict_model[:5]:
        result_rec.append(preds[0])

    return result_rec

    # pair_user_posts = np.array(
    #     [
    #         [test_user_id] * len(res_post_text["post_id"].unique()),
    #         res_post_text["post_id"].unique(),
    #     ]
    # ).T
    # pair_user_posts = pd.DataFrame(pair_user_posts, columns=["user_id", "post_id"])
    # data_to_model = pair_user_posts.merge(res_user, on="user_id", how="left").merge(
    #     res_post_text, on="post_id", how="left"
    # )
    # time_delta = np.array([time_diff] * len(res_post_text["post_id"].unique()))
    # data_to_model.columns
    # data_to_model.insert(len(data_to_model.columns), "time_delta", time_delta)
    # data_to_model = data_to_model.drop(["user_id", "post_id"], axis=1)
    # predict_model = catboost_model.predict_proba(data_to_model).tolist()
    # for i in range(len(predict_model)):
    #     predict_model[i][0] = res_post_text["post_id"].unique()[i]
    # predict_model.sort(reverse=True, key=(lambda x: x[1]))
    # result_rec = []
    # for preds in predict_model[:5]:
    #     result_rec.append(preds[0])

    # return result_rec


from schema import PostGet

# class PostGet(BaseModel):
#     id: int
#     text: str
#     topic: str

#     class Config:
#         orm_mode = True


def get_db():
    with SessionLocal() as db:
        return db


def get_model_path(path: str) -> str:
    if (
        os.environ.get("IS_LMS") == "1"
    ):  # проверяем где выполняется код в лмс, или локально. Немного магии
        MODEL_PATH = "/workdir/user_input/model"
    else:
        MODEL_PATH = path
    return MODEL_PATH


def load_models():
    model_path = get_model_path(
        "./catboost_model_250_remove_col"
    )  # Assuming the model file is in the same directory
    from_file = CatBoostClassifier()
    model = from_file.load_model(model_path)
    return model


def batch_load_sql(query: str) -> pd.DataFrame:
    CHUNKSIZE = 200000
    # engine = create_engine(
    #     "postgresql://robot-startml-ro:pheiph0hahj1Vaif@"
    #     "postgres.lab.karpov.courses:6432/startml"
    # )
    conn = engine.connect().execution_options(stream_results=True)
    chunks = []
    for chunk_dataframe in pd.read_sql(text(query), conn, chunksize=CHUNKSIZE):
        chunks.append(chunk_dataframe)
    conn.close()
    return pd.concat(chunks, ignore_index=True)


### existing tables
### ale_kim_features_user_post_like
### ale_kim_features_res_user_last
### ale_kim_features_res_posts_last


def load_features_user() -> pd.DataFrame:
    return batch_load_sql("SELECT * FROM ale_kim_features_res_user_remove_col")


def load_features_posts() -> pd.DataFrame:
    return batch_load_sql(
        "SELECT * FROM ale_kim_features_res_posts_remove_col_remove_tf"
    )


# def load_user_post_like() -> pd.DataFrame:
#     return batch_load_sql("SELECT * FROM ale_kim_features_user_post_like").set_index(
#         "user_id"
#     )


# global
# user_post_like = load_user_post_like()
res_user = load_features_user()
res_post_text = load_features_posts()
res_post = res_post_text.drop("text", axis=1)
catboost_model = load_models()
START = datetime.strptime("2021-10-01 06:05:25", "%Y-%m-%d %H:%M:%S")


app = FastAPI()


@app.get("/post/recommendations/")  # , response_model=List[PostGet])
def recommended_posts(
    id: int, time: datetime, limit: int = 10, db: Session = Depends(get_db)
) -> List[PostGet]:

    time_diff = (time - START).days
    result_recs_post = recomend_finder(
        id, res_user, res_post, time_diff, catboost_model
    )
    result_recs_post = [int(i) for i in result_recs_post]
    # res = db.query(Post).filter(Post.id.in_((result_recs_post))).all()
    res = []  # 'post_id'  'topic'  'text'
    for i in result_recs_post:
        res.append(
            {
                "id": i,
                "topic": res_post_text.loc[
                    res_post_text["post_id"] == i, "topic"
                ].values[0],
                "text": res_post_text.loc[res_post_text["post_id"] == i, "text"].values[
                    0
                ],
            }
        )
    return res
