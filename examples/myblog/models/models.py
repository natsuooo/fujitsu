from sqlalchemy import Column, Integer, String, Text, DateTime
from datetime import datetime
from models.database import Base

class BlogContent(Base):
    __tablename__ = "blogcontent"
    id = Column(Integer,primary_key=True)
    title = Column(String(128),unique=True)
    body = Column(Text)
    date = Column(DateTime,default=datetime.now())
    def __init__(self, title=None,body=None,date=None):
        self.title = title
        self.body = body
        self.date = date
    def __repr__(self):
        return "<BlogContent(title='%s',body='%s',date='%s')>" % (self.title, self.body,self.date)

class Users(Base):
    __tablename__ = "users"
    id = Column(Integer,primary_key=True)
    name = Column(Text,unique=True)
    password = Column(Text)
    def __init__(self,name=None,password=None):
        self.name = name
        self.password = password
    def __repr__(self):
        return "<Users(name='%s', password='%s')>" % (self.name, self.password)