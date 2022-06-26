from datetime import datetime

from sqlalchemy import (
    Column,
    Integer,
    String, ForeignKey, Boolean, DateTime,
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref

Base = declarative_base()

class BaseTable(Base):
    __abstract__ = True
    id = Column(Integer, primary_key=True)
    created_at = Column('created_at', DateTime, default=datetime.now())
    updated_at = Column('updated_at', DateTime, default=datetime.now(), onupdate=datetime.now())


class Media(BaseTable):
    __abstract__ = True
    original_file_name = Column(String, nullable = False)
    local_file_name = Column(String, nullable = False)
    src_id = Column(String, nullable=False)
    processed_at = Column(DateTime, nullable=True)


class Config(BaseTable):
    __tablename__ = 'config'
    name = Column(String(256), nullable=False, unique=False)
    value1 = Column(String, nullable=True, unique=False)
    value2 = Column(String, nullable=True, unique=False)


class Email(BaseTable):
    __tablename__ = 'email'
    author_id = Column(Integer, ForeignKey("author.id"))
    external_id = Column(String, nullable = False)
    received = Column(DateTime, nullable = False)
    headers = Column(String, nullable = True)
    processed = Column(DateTime, nullable = True)
    post = relationship("Post", backref=backref("email", uselist=False))


class Author(BaseTable):
    __tablename__ = 'author'
    name = Column(String, nullable = False)
    email = Column(String, nullable = True)
    posts = relationship("Post")
    emails = relationship("Email")


class Image(Media):
    __tablename__ = "image"
    post_id = Column(Integer, ForeignKey("post.id"))


class Video(Media):
    __tablename__ = "video"
    post_id = Column(Integer, ForeignKey("post.id"))


class Document(Media):
    __tablename__ = "document"
    post_id = Column(Integer, ForeignKey("post.id"))


class Post(BaseTable):
    __tablename__ = 'post'
    author_id = Column(Integer, ForeignKey("author.id"))
    email_id = Column(Integer, ForeignKey("email.id"))
    title = Column(String)
    body = Column(String, nullable=True)
    author = relationship("Author", viewonly=True)
    images = relationship("Image")
    videos = relationship("Video")
    docs = relationship("Document")
