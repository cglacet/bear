import re
import bear_api


class BearNote:
    def __init__(self, sql_row):
        self.content = sql_row

    def append_text(self, text):
        return bear_api.append_text_to_note(self, text)

    @property
    def outgoing_links(self):
        yield from bear_api.note_link(self.text)

    @property
    def sections_outgoing_links(self):
        for title, content in self.sections:
            for link in bear_api.note_link(content):
                yield title, link

    @property
    def outgoing_wiki_links(self):
        yield from bear_api.wiki_link(self.text)

    @property
    def sections_outgoing_wiki_links(self):
        for title, content in self.sections:
            for link in bear_api.wiki_link(content):
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
