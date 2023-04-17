<!-- PROJECT LOGO -->
<br />
<div align="center">
  <a href="https://github.com/Wheest/bib-boi">
    <img src="logo.png" alt="Logo" width="80" height="80">
  </a>

  <h3 align="center">bib boi</h3>

  <p align="center">
    Tools to help with bibtex management
  </p>
</div>


## About

When I started writing my thesis, I brought together multiple papers I'd written over several years.
During this time, I'd changed my citekey format on Zotero, and also my coauthors may have provided some of the original references.
When I compiled early versions of my thesis, I had over 100 citekey warnings, and I had the sneaking suspicion that many of my arXiv references would now be published.

I developed these tools to help reduce the time I needed to spend manually looking for issues.
Eventually, I bit to bullet, and made my thesis bib file a direct live export of my Zotero library.
This of course increased my warnings three-fold.
However, it encouraged me to make my fixes in my Zotero database directly.

## Usage


####  Search for possible duplicated bibentries

This approach is very fuzzy, but could reveal some overlaps.

``` sh
python3 dupe_check.py $BIB_FILE
```

#### Search for possible arXiv papers that might have a published version

This approach looks to see if the arXIv paper has a DOI, or has a comment that might suggest there is a published version

``` sh
python3 arXiv_auto_check.py $BIB_FILE
```

#### Semi-manually verify your arXiv papers

Once you have run the auto-checker script, you may still want to be sure that you haven't left any papers out.
With this script, it prints out all of your arXiv papers, and their URLs.
If you have verified that a given paper is _only_ available on arXiv, add its citekey to the `verified_arxiv.txt` file.
This will be easier than keeping a checklist yourself.

``` sh
python3 arXiv_manual_check.py $BIB_FILE
```

#### Search for possible capitalisation issues

Personally I think that paper titles should be capitalised, e.g. "Transfer-Tuning: Reusing Auto-Schedules for Efficient Tensor Program Code Generation", though common words (e.g., "for", "and", "of") shouldn't be.

Some papers don't follow that rule, but it's your bibliography and as long as the title is the same, you can use whatever capitalisation you want.
`capital_check.py` looks through your bibfile, and uses some heuristics to see if their is a capitalisation issue in the title or conference name.
It tells you what word in a title that triggered the heuristic.

You can add exceptions to the file `verified_capital.txt`, e.g. `mRNA: Enabling Efficient Mapping Space Exploration for a Reconfiguration Neural Accelerator` doesn't start with a capital letter, but is correct.

``` sh
python3 capital_check.py $BIB_FILE
```

<!-- LICENSE -->
## License

Distributed under the MIT License. See `LICENSE` for more information.

### Built With

* [arXiv.py](https://github.com/lukasschwab/arxiv.py/)
* [python-bibtexparser](https://github.com/sciunto-org/python-bibtexparser)
