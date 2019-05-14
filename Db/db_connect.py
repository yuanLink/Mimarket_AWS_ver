'''
author : gary wong
'''
# -*- coding:utf-8 -*-
import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

print("sqlalchemy version: "+ sqlalchemy.__version__)

'''
This string need to be configured (better store passwd in a configuration file):
    mysql+driver://root:passwd@user:port/database_name?
'''
DB_USER = "root"
DB_PASS = "TMmac8.6"
DB_HOST = "localhost"
DB_PORT = 3306
DATABASE = "aws"
connect_string = 'mysql+pymysql://{}:{}@{}:{}/{}?charset=utf8mb4'.format(DB_USER, DB_PASS, DB_HOST, DB_PORT, DATABASE)
engine = create_engine(connect_string, echo = True)
connection = engine.connect()
Base = declarative_base()
if(engine == None):
    print("can't connect to mysql")
else:
    print("connect to mysql successfully!")
    Base.metadata.create_all(engine)
    print(connection)

def get_session():
    Session = sessionmaker(bind=engine, autocommit=False, autoflush=True, expire_on_commit=False)
    return Session

