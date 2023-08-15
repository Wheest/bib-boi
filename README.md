<!-- PROJECT LOGO -->
<br />
<div align="center">
  <a href="https://github.com/Wheest/bib-boi">
    <img src="logo.png" alt="Logo" width="80" height="80">
  </a>

  <h3 align="center">bib boi</h3>

  <p align="center">
    Tools to help with LaTeX paper writing
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

I also brought in some LLM (large language model) based paper reviews.

## Usage

#### Give LLM reviewer feedback on the paper

This tool uses a large language model to give reviews for your text in the style of a paper reviewer.

For example:

> L12: Consider adding a citation to support the statement about bloated network architectures with diminishing returns.
>
> L15: Specify what is meant by "representational capacity".
>
> L16: It may be helpful to provide some additional context or explanation for what depthwise convolutions are and how they differ from standard convolutions, for readers who may be unfamiliar with the concept.

Right now it uses OpenAI GPT models as the backend, which may be a problem from a privacy perspective if your work in unpublished.
[OpenAI say](https://openai.com/policies/privacy-policy) that they won't use data you send them, but DYOR with regards to this point.

> What is the impact of this with regards to academic or research integrity?

You should be writing your own paper text, because 1) it is against a variety of emerging policies from academic and conference guidelines, 2) you will be cheating yourself from a valuable learning experience, and 3) the output of LLMs is inherently unreliable.

That being said, using it as a tool to get feedback on your work is acceptable, in my opinion.
Papers are reviewed by colleagues and collaborators all the time.
That being said, like suggestions from humans, you should not take LLM suggestions as gospel, they can be wrong sometimes.

To run the script in this repo, you need an OpenAI API key, then you can run the script passing you bibtex file.

``` sh
export OPENAI_API_KEY='sk-fake_key_hi_there_how_are_you_mate'
python3 reviewer_2.py $YOUR_TEX_FILE
```

Using the `gpt-3.5-turbo` model, there is a limited amount of text we can process at once.
If a file has more text, you will be prompted if you want to continue reviewing it.
Alternatively, if you want clarification on one of the points, there is an option to query the model, just be careful that you don't use it to _write_ for you.
The tool was written under the assumption that you start each sentence on a new line, which you should be doing for LaTeX files anyway.

Note that the model may be off-by-one for referencing line numbers, and may even hallucinate errors (e.g., `- L61: "opague" should be spelled "opaque".`, even though `opague` does not appear in the text).
Take it as partially reliable, but exercise your own judgement.

Features that would be nice to have in this script include:
- ✅ automated exploration of more complex LaTeX projects, for example ones with multiple files using `\input` statements. Enabled with the `--recurse_subfiles` flag, YMMV.
- reviewing with a sliding window, rather than in discrete chunks.
- more prompt configuration options, e.g., "be nice", "slag me off".
- post-processing where we pass the response through a 2nd prompt to filter unhelpful output.


####  Search for possible duplicated bibentries

This approach is very fuzzy, but could reveal some overlaps.
Your first step should probably to open up your reference manager, assuming you're using one, and sort by name.
That will reveal the most obvious overlaps.
Next, you can try this python script:

``` sh
python3 dupe_check.py $BIB_FILE
```

#### Search for possible arXiv papers that might have a published version

This approach looks to see if the arXiv paper has a DOI, or has a comment that might suggest there is a published version

``` sh
python3 arXiv_auto_check.py $BIB_FILE
```

####  Check if author names are incomplete

This tool checks if author names are left as abbreviations, e.g. `J. Blogs`.
Abbreviations should be done by the document, not the bibtex database.

``` sh
python3 name_check.py $BIB_FILE
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

*NOTE: this script is still a WIP, since bibtex capitalisation actually needs to have braces in it to work properly.*

Personally I think that paper titles should be capitalised, e.g. "Transfer-Tuning: Reusing Auto-Schedules for Efficient Tensor Program Code Generation", though common words (e.g., "for", "and", "of") shouldn't be.

Some papers don't follow that rule, but it's your bibliography and as long as the title is the same, you can use whatever capitalisation you want.
`capital_check.py` looks through your bibfile, and uses some heuristics to see if their is a capitalisation issue in the title or conference name.
It tells you what word in a title that triggered the heuristic.

You can add exceptions to the file `verified_capital.txt`, e.g. `mRNA: Enabling Efficient Mapping Space Exploration for a Reconfiguration Neural Accelerator` doesn't start with a capital letter, but is correct.

``` sh
python3 capital_check.py $BIB_FILE
```


#### Gender ratio estimator

This tool parses the authors in your bibliography and estimates what the gender ratio is.

You first need to generate a sub-bibliography of papers you _actually_ cite from your bibfile
run (assuming your main tex file is `00-main.tex` and main bib is `refs.bib`).
Generates a new bib file `extracted.bib`:

```sh
pdflatex -shell-escape 00-main.tex
biber 00-main
pdflatex -shell-escape 00-main.tex
pdflatex -shell-escape 00-main.tex

jabref -a 00-main,/tmp/extracted refs.bib
```

Then you can run `bib_stats.py`.  You will also need to set your `OPENAI_KEY`, or comment out that code.

<!-- LICENSE -->
## License

Distributed under the MIT License. See `LICENSE` for more information.

### Built With

* [arXiv.py](https://github.com/lukasschwab/arxiv.py/)
* [python-bibtexparser](https://github.com/sciunto-org/python-bibtexparser)
