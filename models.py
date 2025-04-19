from database import Base
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Float

class Items(Base):
    __tablename__ = 'items'

    id=Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String)
    brand = Column(String)
    price = Column(Float)
    quantity = Column(Integer)


class Users(Base):
    __tablename__ = 'users'

    id=Column(Integer, primary_key=True, autoincrement=True)
    admin = Column(Boolean)
    username = Column(String)
    password = Column(String)
