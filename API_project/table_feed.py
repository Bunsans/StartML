from database import Base, SessionLocal, engine
from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    desc,
    func,
    ForeignKey,
)
from sqlalchemy.orm import relationship
from table_post import Post
from table_user import User


class Feed(Base):
    __tablename__ = "feed_action"
    action = Column(String)
    post_id = Column(Integer, ForeignKey("post.id"), primary_key=True)
    post = relationship("Post")
    time = Column(DateTime)
    user_id = Column(Integer, ForeignKey("user.id"), primary_key=True)
    user = relationship("User")


if __name__ == "__main__":
    Base.metadata.create_all(engine)
    session = SessionLocal()
    # res = [
    #     i.id
    #     for i in (
    #         session.query(Post)
    #         .filter(Post.topic == "business")
    #         .order_by(desc(Post.id))
    #         .limit(10)
    #         .all()
    #     )
    # ]
    # print(res)
