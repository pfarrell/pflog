import os
import imaplib
import email
import traceback

from sqlalchemy import select

from common.models import Config

from db.sqlite import get_session, run_query
from mail.imap import get_imap_session
from mail_handler import handle_email, get_email

session = get_session()
query = select(Config).where(Config.name.in_(["monitor_email"]))

for config in run_query(query, session=session):
    imap_session = get_imap_session(config.value1, config.value2)
    for email_message in get_email(imap_session):
        handle_email(email_message)

print("complete")
