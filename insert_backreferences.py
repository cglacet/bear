"""We use BACKREFMARKER to mark backreference links so we don't have a loop of reference
This is a bit hacky as bear x-callback api ignores the title argument when the ID argument
is passed. THis allows to add some meta-data in the title argument of open-note:
"""

import bear_api
from collections import defaultdict
from bear_note import BearNote
from constants import USE_HEADER_LINKS, BACKREFMARKER, BACKREFERENCES_INTRO_TEXT, BACKREFERENCES_SECTION, BACKREFERENCE_PREFIX
from links import Link, HeaderLink
from ordered_set import OrderedSet


# This is the old version
def main():
    bear_notes = [BearNote(note) for note in bear_api.notes()]
    notes = {note.uid: note for note in bear_notes}
    backreferences, out_links = find_all_links(notes)
    backreferences = filter_out_existing_links(backreferences, out_links)
    # backreferences = filter_out_self_links(backreferences, out_links)
    nb_links_inserted = 0
    for note in notes.values():
        try:
            nb_links_inserted += add_backreferences_to_note(note, backreferences, out_links)
        except KeyError:
            pass

    print(f"Inserted {nb_links_inserted} new links to your notes.")


def main_test():
    bear_notes = [BearNote(note) for note in bear_api.notes()]
    notes = {note.uid: note for note in bear_notes}
    backreferences, _ = find_all_links(notes)
    for note_id, note in notes.items():
        note_back_refs = backreferences[note_id]
        if note_back_refs:
            new_note_content = ''.join(text_lines(note, backref_links=note_back_refs))
            bear_api.replace_note_text(note, new_note_content)


def add_backreferences_to_note(note, backreferences, out_links):
    backrefs = backreferences[note.uid]
    existing_links = out_links[note.uid]
    if backrefs:
        add_intro = not any(is_a_backreference(l) for l in existing_links)
        text_to_append = markdown_link_list(backrefs, add_intro=add_intro)
        note.append_text(text_to_append)
        return len(backrefs)
    return 0


def markdown_link_list(links, add_intro=False):
    if add_intro:
        intro_markdown = BACKREFERENCES_SECTION + BACKREFERENCES_INTRO_TEXT
    else:
        intro_markdown = ""
    backref_links_text = '\n'.join(f"{BACKREFERENCE_PREFIX} {bear_api.markdown_link(l)}" for l in links)
    return intro_markdown + backref_links_text


def find_all_links(notes):
    backreferences = defaultdict(OrderedSet)
    out_links = dict()
    for note in notes.values():
        out_links[note.uid] = list(note.outgoing_links)
        for out_link in out_links[note.uid]:
            if not is_a_backreference(out_link):
                backref = Link(href_id=note.uid, title=note.title, open_note_title=BACKREFMARKER)
                backreferences[out_link.href_id].add(backref)
    return backreferences, out_links


def find_all_links_by_section(notes):
    backreferences = defaultdict(OrderedSet)
    out_links = dict()
    for note in notes.values():
        out_links[note.uid] = list(note.outgoing_links)
        for header, out_link in note.sections_outgoing_links:
            if not is_a_backreference(out_link):
                backref = HeaderLink(href_id=note.uid, title=note.title, header=header, open_note_title=BACKREFMARKER)
                backreferences[out_link.href_id].add(backref)
    return backreferences, out_links


def filter_out_existing_links(backreferences, out_links):
    return {note_id: note_filter_out_existing_links(links, out_links[note_id]) for note_id, links in backreferences.items()}


def note_filter_out_existing_links(backreferences, out_links):
    return [l for l in backreferences if l.href_id not in [l.href_id for l in out_links]]


def filter_out_existing_headerlinks(backreferences, out_links):
    return {note_id: note_filter_out_existing_headerlinks(links, out_links[note_id]) for note_id, links in backreferences.items()}


def note_filter_out_existing_headerlinks(backreferences, out_links):
    existing_links = set([(l.href_id, l.header) for l in out_links])
    return [l for l in backreferences if (l.href_id, l.header) not in existing_links]


if USE_HEADER_LINKS:
    find_all_links = find_all_links_by_section
    filter_out_existing_links = filter_out_existing_headerlinks


def filter_out_self_links(backreferences, out_links):
    return {note_id: [l for l in links if l.href_id != note_id] for note_id, links in backreferences.items()}


def is_a_backreference(link):
    try:
        return link.open_note_title == BACKREFMARKER
    except AttributeError:
        return False


def is_valid_reference(notes, link):
    is_note_link = not hasattr(link, 'header')
    if is_note_link:
        return link.href_id in notes.keys()
    else:
        return link.header in set(title for title, content in notes[link.href_id].sections)


def text_lines(note, backref_links=None):
    """
        :param backref_links: add back reference links in the right place.
            The right place is defined as the place where existing back references
            were found. If no backreference was found they are just added
            at the very end of the note. (Maybe we can append them before the tags,
            just like add-text with append does in the Bear API?
            I prefer it like this personally)
    """
    lines = iter(note.text.splitlines())
    text_has_any_back_reference = False
    for line in lines:
        if BACKREFMARKER in line:
            text_has_any_back_reference = True
            break
        yield line + '\n'

    if backref_links:
        yield markdown_link_list(backref_links, add_intro=not text_has_any_back_reference)

    for line in lines:
        if BACKREFMARKER not in line:
            yield line + '\n'


if __name__ == "__main__":
    main_test()