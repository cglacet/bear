# When TEST is True, instead of inserting test the script will x-callback api calls.
TEST = False

# When set to True, USE_HEADER_LINKS will generate a backreference 
# to each note/section pair that cite the current note.
USE_HEADER_LINKS = True

# Options that will be passed to the text insertion API:
#   https://bear.app/faq/X-callback-url%20Scheme%20documentation/#add-text
INSERT_OPTIONS_DICT = {
    'mode': 'append',
    'open_note': 'no',
    'show_window': 'no',
}

# If it fails and you struggle finding the location of your , try to run:
#   find ~ -iname database.sqlite | grep bear
MANUALLY_SET_DB_LOCATION = ""
