import os
import search_file
from config import INSERT_OPTIONS_DICT, REPLACE_OPTIONS_DICT, TEST, USE_HEADER_LINKS

USE_HEADER_LINKS = os.getenv('BEAR_BR_SECTIONS', str(USE_HEADER_LINKS)).lower() == 'true'

WRITE_API_URL = "bear://x-callback-url/add-text"
OPEN_NOTE_API_URL = "bear://x-callback-url/open-note"

# Notes to add back-references to:
# Whitelisted notes (list of UUID's), if None -> all notes
NOTES_WHITELIST = None
# Whitelisted tags (list of tags), if None -> all tags
TAGS_WHITELIST = None
INCLUDE_SUBTAGS = False
IGNORE_TAGS_CASE = True

# You can change that (markdown rendering of links)
BACKREFERENCES_SECTION = '\n\n' + '-' * 10 + '\n'
DEFAULT_BACKREFERENCES_INTRO_TEXT = "This note is referenced in:\n"
BACKREFERENCES_INTRO_TEXT = DEFAULT_BACKREFERENCES_INTRO_TEXT
BACKREFERENCE_PREFIX = '* '

ROOT_SECTION_TEXT = "/"
ROOT_SECTION_TEXT = os.getenv('BEAR_ROOT_SECTION_TEXT', ROOT_SECTION_TEXT)

HOME = os.getenv('HOME', '')
LIBRARY = os.path.join(HOME, 'Library')
INSERT_OPTIONS = '&'.join(f'{k}={v}' for k, v in INSERT_OPTIONS_DICT.items())
REPLACE_OPTIONS = '&'.join(f'{k}={v}' for k, v in REPLACE_OPTIONS_DICT.items())

# Unique identifier that we use for backreference links
# (this is not interpreted by Bear when an ID is provided in open-note)
BACKREFMARKER = "__backreference_link__"

BEAR_DB = search_file.find_first(r'.*bear.*database\.sqlite$', LIBRARY)
# Maybe use "find ~ -iname database.sqlite | grep bear"?
BEAR_DB = os.getenv('BEAR_DB_LOCATION', BEAR_DB)

if not BEAR_DB:
    print(
        f"\n\nERROR: Couldn't locate Bear app database,"
        f"please provide a valid 'BEAR_DB_LOCATION' (as environment variable).\n\n"
    )
    exit(1)

# Just in case, this one needs to be non-empty
if not BACKREFERENCES_INTRO_TEXT:
    print("!! WARNING: This is ugly, but we need `BEAR_BACKREFERENCES_INTRO_TEXT` to be non-empty.\n"
          "It's even worse, we need it to be present in the document only if the backref section exists."
          "We used the default value instead of the empty string you provided. SOrRy.\n")
    BACKREFERENCES_INTRO_TEXT = DEFAULT_BACKREFERENCES_INTRO_TEXT


def os_env_list(env_name, default=None, seaparator=','):
    str_values = os.getenv(env_name, default)
    if str_values:
        return frozenset(str_values.split(seaparator))
    else:
        return frozenset()


def os_env_bool(env_name, default):
    return os.getenv(env_name, str(default)).lower() == 'true'


# For people that don't want to interact with python code
BACKREFERENCES_SECTION = os.getenv('BEAR_BACKREFERENCES_SEPARATOR', BACKREFERENCES_SECTION)
BACKREFERENCES_INTRO_TEXT = os.getenv('BEAR_BACKREFERENCES_INTRO_TEXT', BACKREFERENCES_INTRO_TEXT)
BACKREFERENCE_PREFIX = os.getenv('BEAR_BACKREFERENCE_PREFIX', BACKREFERENCE_PREFIX)
NOTES_WHITELIST = os_env_list('BEAR_NOTES_WHITELIST', NOTES_WHITELIST, seaparator=',')
TAGS_WHITELIST = os_env_list('BEAR_TAGS_WHITELIST', TAGS_WHITELIST, seaparator='#')
if IGNORE_TAGS_CASE:
    TAGS_WHITELIST = {t.lower() for t in TAGS_WHITELIST}
INCLUDE_SUBTAGS = os_env_bool('BEAR_INCLUDE_SUBTAGS', INCLUDE_SUBTAGS)
TEST = os_env_bool('BEAR_TEST', TEST)
