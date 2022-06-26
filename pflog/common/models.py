from datetime import datetime

from sqlalchemy import (
    Column,
    Integer,
    String, ForeignKey, Boolean, DateTime,
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class Config(Base):
    __tablename__ = 'config'
    id = Column(Integer, primary_key=True)
    name = Column(String(256), nullable=False, unique=False)
    value1 = Column(String, nullable=True, unique=False)
    value2 = Column(String, nullable=True, unique=False)
    created_at = Column('created_at', DateTime, default=datetime.now())
    updated_at = Column('updated_at', DateTime, default=datetime.now(), onupdate=datetime.now())


class Email(Base):
    __tablename__ = 'email'
    id = Column(Integer, primary_key=True)
    author_id = Column(Integer, ForeignKey("author.id"))
    external_id = Column(String, nullable = False)
    received = Column(DateTime, nullable = False)
    headers = Column(String, nullable = True)
    processed = Column(DateTime, nullable = True)
    created_at = Column('created_at', DateTime, default=datetime.now())
    updated_at = Column('updated_at', DateTime, default=datetime.now(), onupdate=datetime.now())


class Author(Base):
    __tablename__ = 'author'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable = False)
    email = Column(String, nullable = True)
    created_at = Column('created_at', DateTime, default=datetime.now())
    updated_at = Column('updated_at', DateTime, default=datetime.now(), onupdate=datetime.now())
    posts = relationship("Post")
    emails = relationship("Email")


class Image(Base):
    __tablename__ = "image"
    id = Column(Integer, primary_key=True)
    post_id = Column(Integer, ForeignKey("post.id"))
    original_file_name = Column(String, nullable = False)
    file_path = Column(String, nullable = False)
    created_at = Column('created_at', DateTime, default=datetime.now())
    updated_at = Column('updated_at', DateTime, default=datetime.now(), onupdate=datetime.now())


class Video(Base):
    __tablename__ = "video"
    id = Column(Integer, primary_key=True)
    post_id = Column(Integer, ForeignKey("post.id"))
    original_file_name = Column(String, nullable = False)
    file_path = Column(String, nullable = False)
    created_at = Column('created_at', DateTime, default=datetime.now())
    updated_at = Column('updated_at', DateTime, default=datetime.now(), onupdate=datetime.now())


class Document(Base):
    __tablename__ = "document"
    id = Column(Integer, primary_key=True)
    post_id = Column(Integer, ForeignKey("post.id"))
    original_file_name = Column(String, nullable = False)
    file_path = Column(String, nullable = False)
    created_at = Column('created_at', DateTime, default=datetime.now())
    updated_at = Column('updated_at', DateTime, default=datetime.now(), onupdate=datetime.now())


class Post(Base):
    __tablename__ = 'post'
    id = Column(Integer, primary_key=True, nullable=True)
    author_id = Column(Integer, ForeignKey("author.id"))
    email_id = Column(Integer, ForeignKey("email.id"))
    title = Column(String)
    body = Column(String, nullable=True)
    images = relationship("Image")
    images = relationship("Video")
    images = relationship("Document")
    created_at = Column('created_at', DateTime, default=datetime.now())
    updated_at = Column('updated_at', DateTime, default=datetime.now(), onupdate=datetime.now())
