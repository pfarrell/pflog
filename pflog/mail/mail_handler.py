import os
import pathlib
import re
import traceback
import email
from datetime import datetime
from email.header import make_header, decode_header
from email.message import Message
from imaplib import IMAP4_SSL

from sqlalchemy.orm import Session

from common.consts import OUTPUT_PATH
from common.models import Email, Post, Author, Image, Video
from db.sqlite import get_or_create, get_session, update
from mail.imap import fetch_unreads, mark_read


def _decode(val) -> str:
    return val.decode()

def _stringify(val) -> str:
    return str(make_header(decode_header(val)))


def retrieve_emails(imap_session: IMAP4_SSL):
    try:
        typ, data = fetch_unreads(imap_session)
        if data and data[0]:
            id_list = [i for i in map(_decode, data[0].split()) if i]
            for i in id_list:
                typ, data = imap_session.fetch(i, '(RFC822)')
                raw_email = data[0][1]
                raw_email_string = raw_email.decode('utf-8')
                email_message = email.message_from_string(raw_email_string)
                yield email_message
                # mark_read(imap_session, i)
    except Exception as e:
        traceback.print_exc()
        print(str(e))

# done CREATE AUTHOR
# CREATE EMAIL
# CREATE POST
# LINK EMAIL TO POST
# CREATE IMAGE
# LINK IMAGE TO POST
def handle_email(email_message):
    session = get_session()
    author = get_author(email_message['from'], session)
    email = get_email(email_message, author, session)
    post = get_post(email_message, author, email, session)
    body = []
    part_id = 0
    for part in email_message.walk():
        part_id += 1
        if part.get_content_maintype() == 'multipart':
            continue
        if part.get_content_maintype() == 'text':
            body.append(part.get_payload())
            continue
        if part.get('Content-Disposition') is None:
            continue
        content_type = str(part.get_content_type())
        file_name = part.get_filename()
        ext = pathlib.Path(file_name).suffix
        if bool(file_name):
            file_path = os.path.join(OUTPUT_PATH, f"{email.external_id}_{part_id}{ext}")
            if not os.path.isfile(file_path):
                fp = open(file_path, 'wb')
                fp.write(part.get_payload(decode=True))
                fp.close()
            if content_type.startswith('image'):
                image = Image()
                image.original_file_name = file_name
                image.file_path = file_path
                image.post_id = post.id
                get_or_create(Image, session, obj=image, original_file_name=file_name, post_id=post.id)
            elif content_type.startswith('video'):
                video = Video()
                video.original_file_name = file_name
                video.file_path = file_path
                video.post_id = post.id
                get_or_create(Video, session, obj=video, original_file_name=file_name, post_id=post.id)
    post.body = str(body)
    update(post, session)
    # update post


def author_from_string(str: str) -> Author:
    author = Author()
    parts = re.split('[<>]', str)
    if len(parts) > 1:
        author.name = parts[0].strip()
        author.email = parts[1].strip()
    else:
        author.name = str
    return author

# parses dates like "Fri, 24 Jun 2022 20:52:02 -0400"
def to_datetime(str: str) -> datetime:
    return datetime.strptime(str, "%a, %d %b %Y %H:%M:%S %z")


def get_author(str: str, session: Session) -> Author:
    parsed = author_from_string(str)
    return get_or_create(Author, session, obj=parsed, email=parsed.email)


def get_email(msg: Message, author: Author, session: Session) -> Email:
    email = Email()
    email.author_id = author.id
    email.external_id = msg['message-id']
    email.headers = str(msg.items())
    email.received = to_datetime(_stringify(msg['date']))
    return get_or_create(Email, session, obj=email, author_id=email.author_id, external_id=email.external_id)


def get_post(msg: Message, author: Author, email: Email, session: Session) -> Post:
    post = Post()
    post.title = _stringify(msg['subject'])
    post.author_id = author.id
    post.email_id = email.id
    return get_or_create(Post, session, obj=post, author_id=post.author_id, email_id=post.email_id)


def handle_attachment():
    pass
