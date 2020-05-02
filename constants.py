import os
import search_file


# If it fails and you struggle finding the location of your , try to run:
#   find ~ -iname database.sqlite | grep bear
MANUALLY_SET_DB_LOCATION = ""

HOME = os.getenv('HOME', '')
LIBRARY = os.path.join(HOME, 'Library')
BEAR_DB = search_file.find_first(r'.*bear.*database\.sqlite$', LIBRARY)

if not BEAR_DB:
    print(
        f"\n\n!!! ERROR: Couldn't locate Bear app database, please edit {__name__}.py"
        f"file to set MANUALLY_SET_DB_LOCATION this manually !!!\n\n"
    )
    exit(1)

WRITE_API_URL = "bear://x-callback-url/add-text"

# You can change that (markdown rendering of links)
IN_LINKS_SECTION = "-" * 10 + "\n"
DEFAULT_IN_LINKS_INTRO_TEXT = "Non-referenced incoming links"
IN_LINKS_INTRO_TEXT = DEFAULT_IN_LINKS_INTRO_TEXT
IN_LINK_PREFIX = '\n* '

# For people that don't want to interact with python code
IN_LINKS_SECTION = os.getenv('BEAR_IN_LINKS_SECTION', IN_LINKS_SECTION)
IN_LINKS_INTRO_TEXT = os.getenv('BEAR_IN_LINKS_INTRO_TEXT', IN_LINKS_INTRO_TEXT)
IN_LINK_PREFIX = os.getenv('BEAR_IN_LINK_PREFIX', IN_LINK_PREFIX)

# Just in case, this one needs to be non-empty
if not IN_LINKS_INTRO_TEXT:
    print("!! WARNING: This is ugly, but we need `BEAR_IN_LINKS_INTRO_TEXT` to be non-empty.\n"
          "It's even worse, we need it to be present in the document only if the backref section exists."
          "We used the default value instead of the empty string you provided. SOrRy.\n")
    IN_LINKS_INTRO_TEXT = DEFAULT_IN_LINKS_INTRO_TEXT
