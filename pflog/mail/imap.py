import imaplib

from common.consts import IMAP_SERVER, IMAP_PORT


def get_imap_session(username, password) -> imaplib.IMAP4_SSL:
    imap = imaplib.IMAP4_SSL(host=IMAP_SERVER, port=IMAP_PORT)
    imap.login(username, password)
    return imap


def fetch_unreads(imap: imaplib.IMAP4_SSL):
    imap.select('inbox')
    return imap.search(None, 'UnSeen')


def mark_read(imap: imaplib.IMAP4_SSL, mail_id: str):
    return imap.store(mail_id, '+FLAGS', '\Seen')

