import re
import bear_api
from urllib.parse import urlparse, parse_qs
from constants import BACKREFERENCES_SECTION, BACKREFERENCES_INTRO_TEXT, BACKREFERENCE_PREFIX
from links import HeaderLink


class BearNote:
    def __init__(self, sql_row):
        self.content = sql_row

    def markdown_link_list(self, links):
        already_has_a_backreference_section = BACKREFERENCES_INTRO_TEXT in self.text
        if already_has_a_backreference_section:
            intro_markdown = ""
        else:
            intro_markdown = BACKREFERENCES_SECTION + BACKREFERENCES_INTRO_TEXT
        return intro_markdown + '\n'.join(f"{BACKREFERENCE_PREFIX} {bear_api.markdown_link(l)}" for l in links) + '\n'

    def append_text(self, text):
        return bear_api.append_text_to_note(self, text)

    @property
    def outgoing_links(self):
        yield from text_links(self.text)

    @property
    def sections_outgoing_links(self):
        for title, content in self.sections:
            for link in text_links(content):
                yield title, link

    @property
    def sections(self):
        section_content = ""
        previous_section_title = ""
        for text_line in self.text.splitlines():
            title = match_section_title(text_line)
            if title:
                if previous_section_title:
                    yield previous_section_title, section_content
                previous_section_title = title
                section_content = ""
            else:
                section_content += f"\n{text_line}"
        yield previous_section_title, section_content

    @property
    def uid(self):
        return self.content['ZUNIQUEIDENTIFIER']

    @property
    def title(self):
        return self.content['ZTITLE']

    @property
    def text(self):
        return self.content['ZTEXT'].rstrip()

    # Unused for now
    @property
    def tags(self):
        pattern1 = r'(?<!\S)\#([.\w\/\-]+)[ \n]?(?!([\/ \w]+\w[#]))'
        pattern2 = r'(?<![\S])\#([^ \d][.\w\/ ]+?)\#([ \n]|$)'
        for pattern in (pattern1, pattern2):
            for matches in re.findall(pattern, self.text):
                yield matches[0]


def match_section_title(text_line):
    match = re.match(r'#+\s+([^\n]*)', text_line)
    try:
        return match[1]
    except (TypeError, IndexError):
        return None


def text_links(text):
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

        yield HeaderLink(href_id=href_id, title=link_title, header=header, reference_link_title=title)
