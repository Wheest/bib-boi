<!-- PROJECT LOGO -->
<br />
<div align="center">
  <a href="https://github.com/Wheest/bib-boi">
    <img src="logo.png" alt="Logo" width="80" height="80">
  </a>

  <h3 align="center">bib boi</h3>

  <p align="center">
    Tool to help with bibtex management
  </p>
</div>


## About

When I started writing my thesis, I brought together multiple papers I'd written over several years.
During this time, I'd changed my citekey format on Zotero, and also my coauthors may have provided some of the original references.
When I compiled early versions of my thesis, I had over 100 citekey warnings.
I developed these tools to help reduce the time I needed to spend manually looking for issues.

## Usage


Search for possible duplicated bibentries (this is very fuzzy, but could reveal some overlaps):
``` sh
python3 dupe_check.py $BIB_FILE
```

Search for possible arXiv papers that have a published version:
``` sh
python3 arXiv_auto_check.py $BIB_FILE
```

Search for arXiv papers that have not manually verified that there is not a published version:
``` sh
python3 arXiv_manual_check.py $BIB_FILE
```
For the above command, you should add the keys of entries that you have verified are only available on arXiv to the `verified_arxiv.txt` file.

<!-- LICENSE -->
## License

Distributed under the MIT License. See `LICENSE` for more information.

### Built With

* [arXiv.py](https://github.com/lukasschwab/arxiv.py/)
* [python-bibtexparser](https://github.com/sciunto-org/python-bibtexparser)
