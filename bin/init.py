import argparse

from common.models import Base, Config
from db.sqlite import get_engine, get_session

parser = argparse.ArgumentParser(description="Initializes project data")
parser.add_argument('--db-only', action='store_true', help="only update database, skip adding emails.")
arg = parser.parse_args()

# applies any database changes
engine = get_engine()
Base.metadata.create_all(engine)

# adds a email address to monitor
if not arg.db_only:
    email = input("Email address to monitor?\n")
    password = input(f"Password for {email}?\n")
    email_address = Config(name="monitor_email", value1=email, value2=password)
    session = get_session(engine)
    session.add(email_address)
    session.commit()
