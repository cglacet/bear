import os
import search_file
from config import INSERT_OPTIONS_DICT, MANUALLY_SET_DB_LOCATION, TEST, USE_HEADER_LINKS


WRITE_API_URL = "bear://x-callback-url/add-text"
OPEN_NOTE_API_URL = "bear://x-callback-url/open-note"

# You can change that (markdown rendering of links)
BACKREFERENCES_SECTION = "-" * 10 + "\n"
if USE_HEADER_LINKS:
    DEFAULT_BACKREFERENCES_INTRO_TEXT = "This note is referenced in the following sections:\n"
else:
    DEFAULT_BACKREFERENCES_INTRO_TEXT = "Non-referenced incoming links:\n"
BACKREFERENCES_INTRO_TEXT = DEFAULT_BACKREFERENCES_INTRO_TEXT
BACKREFERENCE_PREFIX = '* '

HOME = os.getenv('HOME', '')
LIBRARY = os.path.join(HOME, 'Library')
INSERT_OPTIONS = '&'.join(f'{k}={v}' for k, v in INSERT_OPTIONS_DICT.items())

# Unique identifier that we use for backreference links
# (this is not interpreted by Bear when an ID is provided in open-note)
BACKREFMARKER = "__backreference_link__"

BEAR_DB = search_file.find_first(r'.*bear.*database\.sqlite$', LIBRARY)
if not BEAR_DB and not MANUALLY_SET_DB_LOCATION:
    print(
        f"\n\n!!! ERROR: Couldn't locate Bear app database, please edit config.py"
        f"file to set MANUALLY_SET_DB_LOCATION this manually !!!\n\n"
    )
    exit(1)

# Just in case, this one needs to be non-empty
if not BACKREFERENCES_INTRO_TEXT:
    print("!! WARNING: This is ugly, but we need `BEAR_BACKREFERENCES_INTRO_TEXT` to be non-empty.\n"
          "It's even worse, we need it to be present in the document only if the backref section exists."
          "We used the default value instead of the empty string you provided. SOrRy.\n")
    BACKREFERENCES_INTRO_TEXT = DEFAULT_BACKREFERENCES_INTRO_TEXT


# For people that don't want to interact with python code
BACKREFERENCES_SECTION = os.getenv('BEAR_BACKREFERENCES_SECTION', BACKREFERENCES_SECTION)
BACKREFERENCES_INTRO_TEXT = os.getenv('BEAR_BACKREFERENCES_INTRO_TEXT', BACKREFERENCES_INTRO_TEXT)
BACKREFERENCE_PREFIX = os.getenv('BEAR_BACKREFERENCE_PREFIX', BACKREFERENCE_PREFIX)
TEST = os.getenv('BEAR_TEST', str(TEST)).lower() == 'true'
USE_HEADER_LINKS = os.getenv('BEAR_USE_HEADER_LINKS', str(USE_HEADER_LINKS)).lower() == 'true'
