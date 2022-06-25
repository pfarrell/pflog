
from sqlalchemy import (
    Column,
    Integer,
    String, ForeignKey, Boolean,
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
    config_id = Column(Integer, ForeignKey("config.id"))
    externalid = Column(Integer, nullable = False)
    processed = Column(Boolean, nullable = False, default = False)

