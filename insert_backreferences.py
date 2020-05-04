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


def main():
    notes = [BearNote(n) for n in bear_api.notes()]
    backreferences, out_links = find_all_links(notes)
    backreferences = filter_out_existing_links(backreferences, out_links)
    # backreferences = filter_out_self_links(backreferences, out_links)
    nb_links_inserted = 0
    for note in notes:
        try:
            nb_links_inserted += add_backreferences_to_note(note, backreferences, out_links)
        except KeyError:
            pass

    print(f"Inserted {nb_links_inserted} new links to your notes.")


def add_backreferences_to_note(note, backreferences, out_links):
    backrefs = backreferences[note.uid]
    existing_links = out_links[note.uid]
    if backrefs:
        add_intro = not any(is_a_backreference(l) for l in existing_links)
        text_to_append = markdown_link_list(note, backrefs, add_intro=add_intro)
        note.append_text(text_to_append)
        return len(backrefs)
    return 0


def markdown_link_list(note, links, add_intro=False):
    if add_intro:
        intro_markdown = BACKREFERENCES_SECTION + BACKREFERENCES_INTRO_TEXT
    else:
        intro_markdown = ""
    return intro_markdown + ''.join(f"{BACKREFERENCE_PREFIX} {bear_api.markdown_link(l)}" for l in links) + '\n'


def find_all_links(notes):
    backreferences = defaultdict(OrderedSet)
    out_links = dict()
    for note in notes:
        out_links[note.uid] = list(note.outgoing_links)
        for out_link in out_links[note.uid]:
            if not is_a_backreference(out_link):
                backref = Link(href_id=note.uid, title=note.title, open_note_title=BACKREFMARKER)
                backreferences[out_link.href_id].add(backref)
    return backreferences, out_links


def find_all_links_by_section(notes):
    backreferences = defaultdict(OrderedSet)
    out_links = dict()
    for note in notes:
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


if __name__ == "__main__":
    main()
    # notes = [BearNote(n) for n in bear_api.notes()]
    # for title, content in notes[0].sections:
    #     print(f"titre = '{title}''", content)
    #     print("-"*10)
