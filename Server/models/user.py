from database import base
from sqlalchemy import Column,Integer,String


class User(base):

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True) # type: ignore
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=True)
    email = Column(String, unique=True, nullable=False, index=True)
    password =  Column(String, nullable= True)