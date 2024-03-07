from database import Base, SessionLocal, engine
from sqlalchemy import Column, Integer, String, desc, func


class User(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True)
    gender = Column(Integer)
    age = Column(Integer)
    country = Column(String)
    city = Column(String)
    exp_group = Column(Integer)
    os = Column(String)
    source = Column(String)


if __name__ == "__main__":
    Base.metadata.create_all(engine)
    session = SessionLocal()
    res = [
        (i.country, i.os, i.count)
        for i in (
            session.query(func.count("*").label("count"), User.country, User.os)
            .filter(User.exp_group == 3)
            .group_by(User.country, User.os)
            .having(func.count("*") > 100)
            .order_by(desc("count"))
            .all()
        )
    ]
    print(res)
