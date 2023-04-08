#!/usr/bin/env python3

import sys
import re
import os
from tqdm import tqdm
from typing import Optional
import bibtexparser
import arxiv

ARXIV_ID_PATTERN = re.compile(r"arXiv:\s*([\w.]+)", re.IGNORECASE)


def extract_arxiv_id(entry: dict) -> Optional[str]:
    arxiv_id = None
    if "journal" in entry and "arxiv" in entry["journal"].lower():
        match = ARXIV_ID_PATTERN.search(entry["journal"])
        if match:
            arxiv_id = match.group(1)

    if "url" in entry and "arxiv.org" in entry["url"]:
        match = re.search(r"\/(\d+\.\d+)", entry["url"])
        if match:
            arxiv_id = match.group(1)

    return arxiv_id


def load_manual_data(path: os.PathLike):
    checked_keys = []

    if os.path.exists(path):
        with open(path) as f:
            while line := f.readline():
                checked_keys.append(line.rstrip())
    return checked_keys


def main(bibtex_file: str):
    with open(bibtex_file, "r") as file:
        bibtex_str = file.read()

    bib_database = bibtexparser.loads(bibtex_str)
    entries = bib_database.entries
    checked_keys = load_manual_data("verified_arxiv.txt")

    for entry in tqdm(entries):
        arxiv_id = extract_arxiv_id(entry)
        if arxiv_id:
            if entry["ID"] not in checked_keys:
                search = arxiv.Search(id_list=[arxiv_id])
                paper = next(search.results())
                print(entry["ID"], paper.links[0].href, paper.title)


if __name__ == "__main__":
    """Checks the file `verified_arxiv.txt` for cite keys.
    This should be arXiv papers that you have manually checked have not been published
    elsewhere.  It will go through your bibfile, and if there are any arXiv papers you
    have not checked, it will print their cite key, arXiv link, and paper name.
    """
    if len(sys.argv) < 2:
        print("Usage: python check_published.py bibtex_file")
    else:
        bibtex_file = sys.argv[1]
        main(bibtex_file)
