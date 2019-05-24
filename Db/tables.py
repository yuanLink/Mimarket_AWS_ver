# -*- coding: utf-8 -*-
from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import VARCHAR

from Db.db_connect import Base


class Phone(Base):
    __tablename__ = 'Phone'
    phone_name = Column(VARCHAR(255), nullable=False, primary_key=True,default="Xiaomi-9")
    phone_num = Column(Integer, default=10000)

class User(Base):
    __tablename__ = 'User'
    User_phone = Column(VARCHAR(255), nullable=False, primary_key=True, default='')
    User_location = Column(VARCHAR(255), nullable=False, default=' ')

