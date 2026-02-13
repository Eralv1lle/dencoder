from sqlalchemy import create_engine, Integer, String, Column, LargeBinary
from sqlalchemy.orm import DeclarativeBase, Session
from config import config

DATABASE_URL = f"postgresql://{config.user}:{config.password}@{config.host}:{config.port}/{config.database}"
engine = create_engine(DATABASE_URL)


class Base(DeclarativeBase):
    pass


class Data(Base):
    __tablename__ = "data"
    id = Column(Integer, primary_key=True, autoincrement=True)
    salt = Column(Integer)
    encrypted = Column(LargeBinary)

    def __repr__(self):
        return f"Data(id={self.id}, salt={self.salt})"


