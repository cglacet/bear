import re
import bear_api
from constants import IN_LINKS_SECTION, IN_LINKS_INTRO_TEXT, IN_LINK_PREFIX


class BearNote:
    def __init__(self, sql_row):
        self.content = sql_row

    def tags(self):
        pattern1 = r'(?<!\S)\#([.\w\/\-]+)[ \n]?(?!([\/ \w]+\w[#]))'
        pattern2 = r'(?<![\S])\#([^ \d][.\w\/ ]+?)\#([ \n]|$)'
        for pattern in (pattern1, pattern2):
            for matches in re.findall(pattern, self.text):
                yield matches[0]

    def markdown_link_list(self, links):
        already_has_a_in_link_section = IN_LINKS_INTRO_TEXT in self.text
        if already_has_a_in_link_section:
            intro_markdown = ""
        else:
            intro_markdown = IN_LINKS_SECTION + IN_LINKS_INTRO_TEXT
        return intro_markdown + ''.join(f"{IN_LINK_PREFIX} {bear_api.markdown_link(l)}" for l in links)

    def append_text(self, text):
        return bear_api.append_text_to_note(self, text)

    @property
    def outgoing_links_id(self):
        pattern = r'\(bear:\/\/x-callback-url\/open-note\?id=([^\)]*)\)'
        for matches in re.findall(pattern, self.text):
            yield matches

    @property
    def uid(self):
        return self.content['ZUNIQUEIDENTIFIER']

    @property
    def title(self):
        return self.content['ZTITLE']

    @property
    def text(self):
        return self.content['ZTEXT'].rstrip()
