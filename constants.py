import os

HOME = os.getenv('HOME', '')
SOME_RANDOM_ID = "9K33E3U3T4"
# If you struggle finding the location of your , try to run:
#   find ~ -iname database.sqlite | grep bear
BEAR_DB = os.path.join(HOME, f'Library/Group Containers/{SOME_RANDOM_ID}.net.shinyfrog.bear/Application Data/database.sqlite')

WRITE_API_URL = "bear://x-callback-url/add-text"

# You can change that (markdown rendering of links)
IN_LINKS_SECTION = "-" * 10 + "\n"
IN_LINKS_INTRO_TEXT = "Non-referenced incoming links"
IN_LINK_PREFIX = '\n* '
