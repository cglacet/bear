import subprocess
import sqlite3
from urllib.parse import quote
from bear_note import BearNote
from constants import BEAR_DB, WRITE_API_URL


def notes():
    with sqlite3.connect(BEAR_DB) as conn:
        conn.row_factory = sqlite3.Row
        result = conn.execute("SELECT * FROM `ZSFNOTE` WHERE `ZTRASHED` LIKE '0'")
        # print(f"Database fields: {database_fields(result)}")
        return [BearNote(n) for n in result.fetchall()]


def append_text_to_note(note, text):
    x_call_text = f"{WRITE_API_URL}?mode=append&text={encode(text)}&id={note.uid}"
    return call(x_call_text)


def markdown_link(link):
    return f"[{link.title}](bear://x-callback-url/open-note?id={link.href_id})"


def call(x_call_text):
    return subprocess.call(["open", x_call_text])


def database_fields(result):
    return ', '.join(d[0] for d in result.description)


def encode(text):
    return quote(text)
