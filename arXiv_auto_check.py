import sys
import re
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


def comment_checker(comment):
    """Sometimes authors will add a comment that their paper has been
    published somewhere, but often the comment is just used to list other info
    """
    if comment is None:
        return False
    comment = comment.lower()
    if "published" in comment:
        return True
    elif "conference" in comment:
        return True
    elif "doi" in comment:
        return True
    elif "acm" in comment:
        return True
    elif "ieee" in comment:
        return True
    elif "accepted" in comment:
        return True
    elif "camera" in comment:
        return True
    elif bool(re.search(r"\s\d{4}\s", comment)):
        # check if something "year-like" is in the comment
        return True
    else:
        return False


def main(bibtex_file: str):
    with open(bibtex_file, "r") as file:
        bibtex_str = file.read()

    bib_database = bibtexparser.loads(bibtex_str)
    entries = bib_database.entries

    for entry in tqdm(entries):
        arxiv_id = extract_arxiv_id(entry)
        if arxiv_id:
            search = arxiv.Search(id_list=[arxiv_id])
            try:
                paper = next(search.results())
                if paper.doi or comment_checker(paper.comment):
                    print(
                        f"{paper.title} {paper.links[0].href}, {paper.comment}, doi: {paper.doi}"
                    )
                else:
                    ...
                    # print(
                    #     f"{entry['title']} (arXiv ID: {arxiv_id}) has not been published elsewhere."
                    # )
            except StopIteration:
                ...
                # print(f"{entry['title']} (arXiv ID: {arxiv_id}) not found on arXiv")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python check_published.py bibtex_file")
    else:
        bibtex_file = sys.argv[1]
        main(bibtex_file)
