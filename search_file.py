import os
import re


def find_first(pattern, path):
    for root, _, files in os.walk(path):
        for name in files:
            name = os.path.join(root, name)
            if re.match(pattern, name):
                return name
