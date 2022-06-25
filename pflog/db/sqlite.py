from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session, sessionmaker

from common.consts import CONN_STR


def get_engine(conn_string: str = None) -> Engine:
    if not conn_string:
        conn_string = CONN_STR
    return create_engine(conn_string)


def get_session(engine: Engine = None) -> Session:
    if not engine:
        engine = get_engine()
    Session = sessionmaker(bind=engine)
    return Session()
