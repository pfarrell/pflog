import os
import imaplib
import email
import traceback

from sqlalchemy import select

from common.consts import IMAP_PORT, IMAP_SERVER, OUTPUT_PATH
from common.models import Config
from email.header import decode_header, make_header

from db.sqlite import get_session


def get_email(username, password):
    try:
        mail = imaplib.IMAP4_SSL(host=IMAP_SERVER, port=IMAP_PORT)
        mail.login(username, password)
        mail.select('inbox')

        data = mail.search(None, 'ALL')
        mail_ids = data[1]
        id_list = mail_ids[0].split()
        first_email_id = int(id_list[0])
        latest_email_id = int(id_list[-1])

        for i in range(latest_email_id, first_email_id, -1):
            typ, data = mail.fetch(str(i), '(RFC822)')
            raw_email = data[0][1]
            raw_email_string = raw_email.decode('utf-8')
            email_message = email.message_from_string(raw_email_string)
            yield email_message
    except Exception as e:
        traceback.print_exc()
        print(str(e))


def handle_email(email_message):
    subject = str(make_header(decode_header(email_message['subject'])))
    print(f"{config.value1}: {subject}")
    for part in email_message.walk():
        if part.get_content_maintype() == 'multipart':
            continue
        if part.get('Content-Disposition') is None:
            continue
        fileName = part.get_filename()
        if bool(fileName):
            filePath = os.path.join(OUTPUT_PATH, fileName)
            if not os.path.isfile(filePath):
                fp = open(filePath, 'wb')
                fp.write(part.get_payload(decode=True))
                fp.close()


session = get_session()
query = select(Config).where(Config.name.in_(["monitor_email"]))
for config in session.scalars(query):
    for email_message in get_email(config.value1, config.value2):
        handle_email(email_message)
