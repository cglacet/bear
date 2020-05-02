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
IN_LINKS_INTRO_TEXT = "Non-referenced incoming links"
IN_LINK_PREFIX = '\n* '
