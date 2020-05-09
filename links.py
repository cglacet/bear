from collections import namedtuple

Link = namedtuple('Link', ['href_id', 'title', 'open_note_title'])
HeaderLink = namedtuple('HeaderLink', ['href_id', 'title', 'header', 'open_note_title'])
Wikilink = namedtuple('Wikilink', ['title'])
