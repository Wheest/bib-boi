#!/usr/bin/env python3
import os
import sys
import bibtexparser
from bibtexparser.bparser import BibTexParser


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

    for i, entry in enumerate(bib_database.entries):
        key = entry["ID"]
        try:
            author = entry["author"]
        except KeyError:
            continue  # Skip this entry if it doesn't have an author

        authors = author.split(" and ")

        for a in authors:
            firstName = a.split(", ")[-1]  # Get the first name of the author.
            if len(firstName) == 1 and firstName.isalpha():
                warning = (
                    f"Warning! {key}: Author {a} only includes initial for first name."
                )
                print(warning)


if __name__ == "__main__":
    """Checks a bibtex file to see if any author first names are abbreviated"""
    if len(sys.argv) < 2:
        print("Usage: python name_check.py bibtex_file")
    else:
        bibtex_file = sys.argv[1]
        find_issues(bibtex_file)
