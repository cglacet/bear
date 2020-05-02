import bear_api
from collections import defaultdict, namedtuple


Link = namedtuple('Link', ['href_id', 'title'])


def main():
    notes = bear_api.notes()
    in_links, out_links = find_all_links(notes)
    in_links = filter_out_existing_links(in_links, out_links)
    nb_links_inserted = 0
    for note in notes:
        try:
            links = in_links[note.uid]
            if links:
                note.append_text(note.markdown_link_list(links))
                nb_links_inserted += len(links)
        except KeyError:
            pass

    print(f"Inserted {nb_links_inserted} new links to your notes.")


def find_all_links(notes):
    in_links = defaultdict(set)
    out_links = dict()
    for note in notes:
        out_links[note.uid] = list(note.outgoing_links_id)
        for href_note_id in out_links[note.uid]:
            link_back_to_self = Link(href_id=note.uid, title=note.title)
            in_links[href_note_id].add(link_back_to_self)
    return in_links, out_links


def filter_out_existing_links(in_links, out_links):
    return {note_id: [l for l in links if l.href_id not in out_links[note_id]] for note_id, links in in_links.items()}


if __name__ == "__main__":
    main()
