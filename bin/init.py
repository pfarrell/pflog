import argparse

from sqlalchemy import create_engine
from sqlalchemy.orm.session import sessionmaker
from pflog.models import Config, Base

parser = argparse.ArgumentParser(description="Initializes project data")
parser.add_argument('--db-only', action='store_true', help="only update database, skip adding emails.")
arg = parser.parse_args()

# applies any database changes
conn_string = 'sqlite:///db.sqlite3'
engine = create_engine(conn_string)
Base.metadata.create_all(engine)

# adds a email address to monitor
if not arg.db_only:
    email = input("Email address to monitor?\n")
    password = input(f"Password for {email}?\n")
    Session = sessionmaker(bind=engine)
    session = Session()
    email_address = Config(name="monitor_email", value1=email, value2=password)
    session.add(email_address)
    session.commit()
