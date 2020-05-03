import subprocess
import sqlite3
from urllib.parse import quote
from constants import BEAR_DB, WRITE_API_URL, OPEN_NOTE_API_URL, TEST, INSERT_OPTIONS


def notes():
    with sqlite3.connect(BEAR_DB) as conn:
        conn.row_factory = sqlite3.Row
        result = conn.execute("SELECT * FROM `ZSFNOTE` WHERE `ZTRASHED` LIKE '0'")
        # print(f"Database fields: {database_fields(result)}")
        return result.fetchall()


def append_text_to_note(note, text):
    x_call_text = f"{WRITE_API_URL}?{INSERT_OPTIONS}&text={encode(text)}&id={note.uid}&new_line=no"
    if TEST:
        print("CLick the following link to add some backreferences: \n\t", x_call_text)
    else:
        return call(x_call_text)


def markdown_link(link):
    try:
        text = f"{link.title}/{link.header}"
    except AttributeError:
        text = link.title
    url = OPEN_NOTE_API_URL
    url += f"?id={link.href_id}"
    try:
        url += f"&title={link.reference_link_title}"
    except AttributeError:
        pass
    try:
        url += f"&header={link.header}"
    except AttributeError:
        pass
    return f"[{text}]({url})"


def call(x_call_text):
    return subprocess.call(["open", x_call_text])


def database_fields(result):
    return ', '.join(d[0] for d in result.description)


def encode(text):
    return quote(text)
