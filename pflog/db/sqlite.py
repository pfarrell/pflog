from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.sql import expression

from common.consts import CONN_STR


def get_engine(conn_string: str = None) -> Engine:
    if not conn_string:
        conn_string = CONN_STR
    return create_engine(conn_string)


def get_session(engine: Engine = None) -> Session:
    if not engine:
        engine = get_engine()
    return sessionmaker(bind=engine)()


def run_query(query: expression, session: Session = None):
    if not session:
        session = get_session()
    return session.scalars(query)
