#!/usr/bin/env python3

import os
import sys
import bibtexparser
from bibtexparser.bparser import BibTexParser


common_words = [
    "in",
    "and",
    "of",
    "on",
    "with",
    "at",
    "to",
    "for",
    "from",
    "the",
    "or",
    "via",
]


def strip(title):
    for s in ["{", "}", "(", ")"]:
        title = title.replace(s, "")
    return title


def check_capitalization(title):
    title = strip(title)
    words = title.split()

    start_rule = (
        True  # starts of titles, or parts followed by a `:` have different rules
    )
    for i, word in enumerate(words[1:]):
        if start_rule and not words[0][0].isupper() and not words[0][0].isnumeric():
            # expect first word to be uppercase, or a number
            return False, words[0]
        else:
            start_rule = False
            continue
        if word[-1] == ":":
            start_rule = True
        if word in ":":
            # a standalone `:` usually means incorrect spacing
            return False, word

        if word in common_words:
            continue
        if word.lower() in common_words:
            # common words should be lower-case
            return False, word
        if word[0].isnumeric():
            # numbers are fine
            continue
        if not word[0].isupper():
            # check all other words
            return False, word
    return True, None


def load_manual_data(path: os.PathLike):
    checked_keys = []

    if os.path.exists(path):
        with open(path) as f:
            while line := f.readline():
                checked_keys.append(line.rstrip())
    return checked_keys


def find_issues(filename):
    with open(filename) as bibtex_file:
        parser = BibTexParser()
        bib_database = bibtexparser.load(bibtex_file, parser=parser)

    checked_keys = load_manual_data("verified_capital.txt")

    for i, entry in enumerate(bib_database.entries):
        key = entry["ID"]
        if key in checked_keys:
            continue

        if entry.get("title"):
            title_pass, word = check_capitalization(entry["title"])
            if not title_pass:
                print(
                    f"Capitalization issue in paper title: {strip(entry['title'])}, trigger: `{word}`, citekey: {key}"
                )

        if entry.get("booktitle"):
            title_pass, word = check_capitalization(entry["title"])
            if not title_pass:
                print(
                    f"Capitalization issue in conference title: {strip(entry['booktitle'])}, trigger: `{word}`, citekey: {key}"
                )


if __name__ == "__main__":
    """Checks the file `verified_capital.txt` for cite keys.
    Checks a bibtex file for possible captialization issues in the
    paper or conference title.
    """
    if len(sys.argv) < 2:
        print("Usage: python check_published.py bibtex_file")
    else:
        bibtex_file = sys.argv[1]
        find_issues(bibtex_file)
