from sqlalchemy import Column, Integer, String, Text, DateTime
from models.database import Base
from datetime import datetime

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    price = Column(String)
    time = Column(String)
    text = Column(Text)
    date = Column(DateTime, default=datetime.now())

    def __init__(self, name=None, price=None, time=None, text=None):
        self.name = name
        self.price = price
        self.time = time
        self.text = text

