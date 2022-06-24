
from sqlalchemy import (
    Column,
    Integer,
    String,
)
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Config(Base):
    __tablename__ = 'config'
    id = Column(Integer, primary_key=True)
    name = Column(String(256), nullable=False, unique=False)
    value1 = Column(String, nullable=True, unique=False)
    value2 = Column(String, nullable=True, unique=False)

class Email(Base):
    __tablename__ = 'email'
    id = Column(Integer, primary_key=True)

