import re
import bear_api


class BearNote:
    def __init__(self, sql_row, lowercase_tags=False, include_subtags=False):
        self.content = sql_row
        self._tags = set()
        self.lowercase_tags = lowercase_tags
        self.include_subtags = include_subtags

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

    @property
    def tags(self):
        if not self._tags:
            self._tags = frozenset(self.find_tags())
        return self._tags

    def find_tags(self):
        pattern1 = r'(?<!\S)\#([.\w\/\-]+)[ \n]?(?!([\/ \w]+\w[#]))'
        pattern2 = r'(?<![\S])\#([^ \d][.\w\/ ]+?)\#([ \n]|$)'
        for pattern in (pattern1, pattern2):
            for matches in re.findall(pattern, self.text):
                tag = matches[0]
                if self.lowercase_tags:
                    tag = tag.lower()
                yield tag
                if self.include_subtags:
                    yield from subtags(tag)


def match_section_title(text_line):
    match = re.match(r'#+\s+([^\n]*)', text_line)
    try:
        return match[1]
    except (TypeError, IndexError):
        return None


def subtags(tag):
    """Iterate over subtags (longer subtags come first)::
        >>> list(subtags("V/W/X/Y/Z"))
        ['V/W/X/Y', 'V/W/X', 'V/W', 'V']
    """
    subtag = tag
    try:
        while True:
            subtag, _ = subtag.rsplit('/', maxsplit=1)
            yield subtag
    except ValueError:
        pass
