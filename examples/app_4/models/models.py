from sqlalchemy import Column, Integer, String, Text, DateTime
from models.database import Base
from datetime import datetime



class Teacher(Base):
    __tablename__ = 'teachers'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    subject = Column(String)
    price = Column(String)
    time = Column(String)
    text = Column(Text)
    image = Column(Integer)
    date = Column(DateTime, default=datetime.now())

    def __init__(self, name=None, subject=None, price=None, time=None, text=None, image=None, date=None):
        self.name = name
        self.subject = subject
        self.price = price
        self.time = time
        self.text = text
        self.image = image
        self.date = date

class Review(Base):
    __tablename__ = 'reviews'
    id = Column(Integer, primary_key=True)
    teacher_id = Column(Integer)
    rating = Column(Integer)
    text = Column(Text)
    date = Column(DateTime, default=datetime.now())

    def __init__(self, teacher_id=None, rating=None, text=None, date=None):
        self.teacher_id = teacher_id
        self.rating = rating
        self.text = text

class Lecture(Base):
    __tablename__ = 'lectures'
    id = Column(Integer, primary_key=True)
    teacher_id = Column(Integer)  
    date = Column(DateTime, default=datetime.now())

    def __init__(self, teacher_id=None, date=None):
        self.teacher_id = teacher_id   
        self.date = date