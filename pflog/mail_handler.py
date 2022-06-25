import os
import traceback
import email
from email.header import make_header, decode_header
from imaplib import IMAP4_SSL

from common.consts import OUTPUT_PATH
from mail.imap import fetch_unreads, mark_read


def _decode(val) -> str:
    return val.decode()


def get_email(imap_session: IMAP4_SSL):
    try:
        typ, data = fetch_unreads(imap_session)
        if data and data[0] and data[0][1]:
            id_list = [i for i in map(_decode, data[0].split()) if i]
            for i in id_list:
                typ, data = imap_session.fetch(i, '(RFC822)')
                raw_email = data[0][1]
                raw_email_string = raw_email.decode('utf-8')
                email_message = email.message_from_string(raw_email_string)
                yield email_message
                mark_read(imap_session, i)
    except Exception as e:
        traceback.print_exc()
        print(str(e))


def handle_email(email_message):
    subject = str(make_header(decode_header(email_message['subject'])))
    #print(f"{config.value1}: {subject}")
    for part in email_message.walk():
        if part.get_content_maintype() == 'multipart':
            continue
        if part.get('Content-Disposition') is None:
            continue
        file_name = part.get_filename()
        if bool(file_name):
            file_path = os.path.join(OUTPUT_PATH, file_name)
            if not os.path.isfile(file_path):
                fp = open(file_path, 'wb')
                fp.write(part.get_payload(decode=True))
                fp.close()
