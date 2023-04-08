#!/usr/bin/env python3

import sys
from collections import defaultdict
from tqdm import tqdm
import Levenshtein
import bibtexparser

MAX_LEVENSHTEIN_DISTANCE = 3


def parse_authors(entry):
    try:
        names = entry["author"].strip().split(" and ")
        authors = [name.lower().strip() for name in names]
        return set(authors)
    except:
        return set()


def similar_titles(title1, title2):
    return (
        Levenshtein.distance(title1.strip().lower(), title2.strip().lower())
        <= MAX_LEVENSHTEIN_DISTANCE
    )


def authors_overlap(authors1, authors2):
    return len(authors1.intersection(authors2)) > 0


def main(bibtex_file):
    with open(bibtex_file, "r") as file:
        bibtex_str = file.read()

    bib_database = bibtexparser.loads(bibtex_str)
    entries = bib_database.entries
    print(f"Loaded {bibtex_file}, found {len(entries)} entries")

    duplicates = defaultdict(list)

    for idx, entry1 in tqdm(enumerate(entries)):
        title1 = entry1["title"]
        authors1 = parse_authors(entry1)

        for entry2 in entries[idx + 1 :]:
            title2 = entry2["title"]
            authors2 = parse_authors(entry2)

            if (
                similar_titles(title1, title2)
                or authors_overlap(authors1, authors2)
                or (
                    title1.strip().lower() == title2.strip().lower()
                    and authors1 == authors2
                )
            ):
                duplicates[entry1["ID"]].append(entry2["ID"])

    for key, value in duplicates.items():
        print(f"{key} could be duplicated by {', '.join(value)}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python detect_duplicates.py bibtex_file")
    else:
        bibtex_file = sys.argv[1]
        main(bibtex_file)
