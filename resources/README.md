# Research Resources: Square Packing

A local, greppable archive of the primary literature behind
[research-2026-08-22-packing-11-unit-squares.md](../docs/project/research/research-2026-08-22-packing-11-unit-squares.md).

The point of this directory is that **the literature can be searched locally**, without
re-fetching, re-extracting, or fighting paywalls and bot-blocks.

## Layout

```
resources/
├── papers/   Academic papers: original .pdf + cleaned .md + faithful .raw.md
└── web/      Web sources (catalogues, surveys, encyclopedic): original .html + .md
```

Every paper is stored three ways:

| File | What it is | Use it for |
| --- | --- | --- |
| `<name>.pdf` | The original, byte-for-byte as retrieved | Authority; figures; anything the text loses |
| `<name>.md` | Cleaned Markdown, headings and LaTeX restored | Reading and quoting |
| `<name>.raw.md` | Unedited `pdfminer.six` output | **Ground truth.** Check the clean copy against this before trusting a formula |

The `.raw.md` files are deliberately retained.
Cleanup was done by language models, so the raw extraction is the fallback whenever a
formula in a `.md` looks suspicious.
Passages that could not be confidently reconstructed are marked inline as
`<!-- GARBLED: unable to reconstruct -->` rather than guessed at.

## Reconstructed passages — read this before quoting a formula

Cleanup was model-assisted, and on badly-extracted PDFs the models sometimes
**reconstructed** damaged mathematics rather than only reformatting it.
Every such passage is annotated inline with `GARBLED` or `NOTE`, and any file containing
them opens with a ⚠️ banner giving the count.

| File stem | Annotated | Notes |
| --- | --- | --- |
| `erdos-graham-1975-on-packing-squares-with-equal-squares` | 17 | **Heavily damaged** 1975 typescript scan. The central theorem was *not extracted at all* — raw shows only `Theorem.` then `(1)` — and the transcription supplies the known `w(α) = Θ(α^{7/11})` as a flagged reconstruction. A reading aid, not a source. |
| `compound-perfect-squared-squares-1303.0599` | 10 | Seven passages, nearly all **tables and matrices** scrambled by multi-column extraction: the known-perfect-squares counts, two results tables, a plantri graph-count grid, and the incidence/currents/reduction matrices for the 33×32 p-net. Best-effort reconstructions are marked. Do not cite its tables. |
| `bentz-2016-optimal-packings-22-and-33` | 3 | Includes a probable “Stromberg” → “Stromquist” correction and a reconstructed distance bound in Lemma 7. |
| `square-packing-x06-wasted-area-2508.04603` | 3 | Three cells of the Section 5 comparison table; one wholly unreconstructable, another may have lost a `log` factor. Do not cite that table. |
| `arslanov-improved-packings-n-n-1` | 1 | One orientation-constraint formula unrecoverable; its numeric value is preserved. |
| `bentz-2010-optimal-packings-13-and-46` | 1 | Corollary 7: segments reconstructed **and an inequality direction changed** (`2√2−2 > b` in raw vs `b > 2√2−2` here). Direction UNVERIFIED. The leading claim — intersection length ≥ `2√2−2 ≈ 0.828` — is unambiguous in the raw and unaffected. |
| `kearney-shiu-2002-efficient-packing-unit-squares` | 1 | One chain of inequalities not reconstructed; the conclusion is stated. |
| `mcclenagan-2026-optimally-packing-large-square` | 1 | One exponent, `(3−√3)/2`, reconstructed from fragments and flagged as possibly wrong. Independently corroborated elsewhere, so the research doc does not rely on this file for it. |

Files not listed carry no annotations.
Note that resolving `(cid:NN)` ligature artifacts, running headers and page numbers is
ordinary cleanup, not reconstruction, and is not flagged.

**The rule:** if a formula sits near an annotation, check it against the `.raw.md`
before relying on it.
That is what the raw files are for.
The research document cites only claims that are unambiguous in the raw extractions.

## Searching

```bash
# Find every mention of a bound across the whole archive
grep -rn "unavoidable" resources/ --include=*.md

# Search only cleaned papers, not raw extractions or HTML
grep -rn "3.877" resources/papers/*.md

# Check a formula in a cleaned paper against the raw extraction
grep -n "sqrt" resources/papers/stromquist-2003-*.raw.md
```

## Papers

Citation keys match those used in the research document.

| Key | Title | Authors | Year | Venue | File stem |
| --- | --- | --- | --- | --- | --- |
| **[Stromquist 2003]** | Packing 10 or 11 Unit Squares in a Square | W. Stromquist | 2003 | Electron. J. Combin. 10, #R8 | `stromquist-2003-packing-10-or-11-unit-squares` |
| **[Friedman DS7]** | Packing Unit Squares in Squares: A Survey and New Results | E. Friedman | 1998– | Electron. J. Combin., Dynamic Survey DS7 | `friedman-ds7-packing-unit-squares-in-squares` |
| **[Kearney–Shiu 2002]** | Efficient packing of unit squares in a square | M. J. Kearney, P. Shiu | 2002 | Electron. J. Combin. 9, #R14 | `kearney-shiu-2002-efficient-packing-unit-squares` |
| **[Bentz 2010]** | Optimal Packings of 13 and 46 Unit Squares in a Square | W. Bentz | 2010 | Electron. J. Combin. 17, #R126 | `bentz-2010-optimal-packings-13-and-46` |
| **[Bentz 2016]** | Optimal Packings of 22 and 33 Unit Squares in a Square | W. Bentz | 2016 | arXiv:1606.03746 | `bentz-2016-optimal-packings-22-and-33` |
| **[Erdős–Graham 1975]** | On packing squares with equal squares | P. Erdős, R. L. Graham | 1975 | JCTA 19, 119–123 (Stanford CS-TR-75-483) | `erdos-graham-1975-on-packing-squares-with-equal-squares` |
| **[Caoduro–Sebő]** | Packing, Hitting, and Colouring Squares | M. Caoduro, A. Sebő | 2022/24 | arXiv:2206.02185 | `caoduro-sebo-packing-hitting-colouring-squares` |
| **[Wegner-CE 2026]** | Counterexamples to Wegner’s Conjecture for Rectangles | see file | 2026 | arXiv:2606.17854 | `wegner-counterexamples-rectangles` |
| **[Martin 2000]** | Compactness Theorems for Geometric Packings | G. Martin | 2000 | arXiv:math/0005054 | `martin-2000-compactness-theorems-geometric-packings` |
| **[McClenagan 2026]** | Optimally Packing a Large Square by Unit Squares | R. McClenagan | 2026 | arXiv:2602.01484 | `mcclenagan-2026-optimally-packing-large-square` |
| **[Good-Squares 2025]** | Square Packing with Asymptotically Smallest Waste Only Needs Good Squares | see file | 2025 | arXiv:2504.09489 | `square-packing-good-squares-2504.09489` |
| **[Waste-0.6 2025]** | Square packing with O(x^0.6) wasted area | see file | 2025 | arXiv:2508.04603 | `square-packing-x06-wasted-area-2508.04603` |
| **[Arslanov et al.]** | Improved packings of n(n−1) unit squares in a square | M. Z. Arslanov et al. | 2021 | Electron. J. Combin. 28(4) | `arslanov-improved-packings-n-n-1` |
| **[CPSS 2013]** | Compound Perfect Squared Squares of the Order Twenties | see file | 2013 | arXiv:1303.0599 | `compound-perfect-squared-squares-1303.0599` |

## Web sources

| Key | What | Source | File stem (in `web/`) |
| --- | --- | --- | --- |
| **[Friedman Center]** | Packing Center record tables and diagrams | erich-friedman.github.io | `friedman-packing-center-squares` |
| **[Friedman DS7 html]** | 2009 HTML edition of the DS7 survey | combinatorics.org | `friedman-ds7-survey-2009-html` |
| **[Kingbird]** | Squares-in-Squares catalogue: exact minimal polynomials, rigidity flags | kingbird.myphotos.cc | `kingbird-squares-in-squares` |
| **[Kingbird-compared]** | Supersession history: which record fell to which method, when | kingbird.myphotos.cc | `kingbird-squares-in-squares-compared` |
| **[Montanher et al. 2018]** | Rigorous packing of unit squares into a circle (full text via PMC) | pmc.ncbi.nlm.nih.gov | `montanher-2018-rigorous-packing-unit-squares-circle` |
| **[squaring.net BSST]** | The Smith-diagram / Kirchhoff correspondence, in detail | squaring.net | `squaring-net-brooks-smith-stone-tutte-II` |
| **[squaring.net Sprague]** | Priority for the first published perfect squared square | squaring.net | `squaring-net-sprague` |
| **[Wikipedia]** | Square packing overview | en.wikipedia.org | `wikipedia-square-packing` |

## Special item: `papers/kingbird-square-11-provenance.svg`

Not a paper, but the single most information-dense source found on `n = 11`. Its XML
comments carry David Ellsworth’s provenance notes, the two contact equations, the
derived placement constants, and the full exact-solution history (Gensane–Ryckelynck
2004 → Ellsworth 2023 → Alexeev’s independent confirmation).
Preserved verbatim.

## Not retrievable

Recorded so nobody re-hunts them:

| Source | Obstacle |
| --- | --- |
| Gensane & Ryckelynck, *Improved Dense Packings of Congruent Squares in a Square*, DCG (2005) | Springer paywall; ResearchGate, Academia.edu and ACM DL all return 403. Its `n = 11` content is known second-hand via the Kingbird SVG notes, which cite it by page. |
| Trump, *Packing of 11 unit squares in a square with minimum size* (Mar 2023) | ResearchGate 403 |
| Roth & Vaughan, *Inefficiency in packing squares with unit squares*, JCTA (1978) | ScienceDirect 403 to automated clients |
| Nagamochi (2005), `s(m²−1) = s(m²−2) = m` | Not located as open access |
| Brooks, Smith, Stone & Tutte, *The dissection of rectangles into squares*, Duke Math. J. 7 (1940) | Project Euclid; not open access |
| Gustafsson & Thulin (1980), *Ronden* | Swedish company periodical; Ellsworth notes he has not read it directly either |

## Provenance and licence

Everything here was retrieved on **2026-08-22** from the URLs recorded in each file’s
metadata header.
The arXiv and Electronic Journal of Combinatorics items are open access;
the Stanford technical report and PMC item are publicly posted.
Retained for private research use.
Consult the original publisher before redistributing.
