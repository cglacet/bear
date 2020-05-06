import subprocess
import sqlite3
import re
from urllib.parse import urlparse, parse_qs, quote
from links import HeaderLink
from constants import BEAR_DB, WRITE_API_URL, OPEN_NOTE_API_URL, TEST, INSERT_OPTIONS, REPLACE_OPTIONS, ROOT_SECTION_TEXT


def notes():
    with sqlite3.connect(BEAR_DB) as conn:
        conn.row_factory = sqlite3.Row
        result = conn.execute("SELECT * FROM `ZSFNOTE` WHERE `ZTRASHED` LIKE '0'")
        # print(f"Database fields: {database_fields(result)}")
        return result.fetchall()


def test_modify_note():
    with sqlite3.connect(BEAR_DB) as conn:
        #r = conn.execute("UPDATE ZSFNOTE SET ZTEXT='# Note B\nAnother test' WHERE `ZUNIQUEIDENTIFIER`='462D4FA7-C2AA-4150-AE2A-4C5D8BB74713-60300-00009B8DECC337BB'")
        #conn.commit()
        conn.row_factory = sqlite3.Row
        result = conn.execute("SELECT * FROM `ZSFNOTE` WHERE `ZUNIQUEIDENTIFIER`='462D4FA7-C2AA-4150-AE2A-4C5D8BB74713-60300-00009B8DECC337BB'")
        print(f"Database fields: {database_fields(result)}")
        return result.fetchall()

def append_text_to_note(note, text):
    x_call_text = f"{WRITE_API_URL}?{INSERT_OPTIONS}&text={encode(text)}&id={note.uid}&new_line=no"
    if TEST:
        print("")
        print("The following would be added to your note: \n")
        print('—'*40, end="\n\n")
        print(text)
        print("")
        print('—'*40)
    else:
        return call(x_call_text)


def replace_note_text(note, text):
    x_call_text = f"{WRITE_API_URL}?{REPLACE_OPTIONS}&text={encode(text)}&id={note.uid}"
    if TEST:
        print("")
        print("The script would have replaced existing note with: \n")
        print('—'*40, end="\n\n")
        print(text)
        print("")
        print('—'*40)
    else:
        return call(x_call_text)


def note_link(text):
    pattern = r'\[([^\]]*)\]\((bear:\/\/x-callback-url\/open-note[^\)]*)\)'
    for link_title, link_url in re.findall(pattern, text):
        parsed_url = urlparse(link_url)
        try:
            title = parse_qs(parsed_url.query)['title'][0]
        except (KeyError, IndexError):
            title = None

        href_id = parse_qs(parsed_url.query)['id'][0]

        try:
            header = parse_qs(parsed_url.query)['header'][0]
        except (KeyError, IndexError):
            header = None

        yield HeaderLink(href_id=href_id, title=link_title, header=header, open_note_title=title)


def markdown_link(link):
    try:
        if link.title == link.header:
            text = f"{link.title}{ROOT_SECTION_TEXT}"
        else:
            text = f"{link.title}/{link.header}"
    except AttributeError:
        text = link.title
    url = OPEN_NOTE_API_URL
    url += f"?id={link.href_id}"
    try:
        url += f"&title={link.open_note_title}"
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


if __name__ == "__main__":
    for x in test_modify_note():
        print(x['ZMODIFICATIONDATE'])