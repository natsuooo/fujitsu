import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

engine = sqlalchemy.create_engine("sqlite:///"+os.path.join(os.path.abspath(os.path.dirname(__file__)),"myblog.db"))

Base = declarative_base()

from models.models import BlogContent,Users

Base.metadata.create_all(bind=engine)

db_session = sessionmaker(bind=engine)()