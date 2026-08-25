# Research Resources: Square Packing

A local, greppable archive of the primary literature behind
[research-2026-08-22-packing-11-unit-squares.md](../docs/project/research/research-2026-08-22-packing-11-unit-squares.md).

The point of this directory is that **the literature can be searched locally**, without
re-fetching, re-extracting, or fighting paywalls and bot-blocks.

## Layout

```
explorations/packing/resources/
├── papers/   Academic papers: original .pdf + cleaned .md + faithful .raw.md
└── web/      Web sources (catalogues, surveys, encyclopedic): original .html + .md
```

Every paper is stored three ways:

| File | What it is | Use it for |
| --- | --- | --- |
| `<name>.pdf` | The original, byte-for-byte as retrieved | Authority; figures; anything the text loses |
| `<name>.md` | Cleaned Markdown, headings and LaTeX restored | Reading and quoting |
| `<name>.raw.md` | Unedited extraction or OCR output | Check the clean copy against this; for image-only scans, the PDF remains the ground truth |

The `.raw.md` files are deliberately retained.
Cleanup was done by language models, so the raw extraction is the fallback whenever a
formula in a `.md` looks suspicious.

**Transcription status, stated exactly.** The archive’s discipline is original + cleaned
`.md` + faithful `.raw.md`, and ten entries currently fall short of it in ways worth
naming rather than hiding:

- `gensane-ryckelynck-2005-improved-dense-packings`,
  `nagamochi-2005-packing-unit-squares-in-a-rectangle`,
  `wang-dong-li-2016-new-result-packing-unit-squares` and
  `basic-slivkova-2018-optimal-piercing-square`,
  `alpert-bauer-kahle-macpherson-spendlove-2023-hard-squares-configuration-spaces` and
  `alvarado-garduno-gonzalez-2025-square-section-braid-groups` are **raw-only**: PDF and
  faithful extraction, no cleaned transcription yet.
  All six were read directly from the PDF, and the claims resting on them were checked
  there.
- `roth-vaughan-1978-inefficiency-packing-squares` carries a **partial** cleaned
  transcription: abstract, introduction and Theorem, read from the rendered page image
  and reproduced verbatim; Sections 2–7 are not transcribed.
  The 1978 scan’s OCR loses subscripts, superscripts and interval notation, and
  transcribing it would mean reconstructing mathematics rather than reformatting it.
  The file opens with a banner saying so.
- The three `stromquist-1984-packing-unit-squares-inside-squares-*` memoranda are
  **image-only scans with concise reading aids**, not cleaned transcriptions.
  Their `.raw.md` files are unedited page-ordered Tesseract OCR for search, not source
  ground truth; formulas and figures must be checked against the PDFs.

Writing the missing transcriptions is deferred deliberately rather than done hastily —
model-assisted cleanup is exactly what produced the reconstruction hazards tabulated in
the next section, and Roth–Vaughan is the argument for that caution: two independent
secondary sources reported a constant the paper does not contain.

## Reconstructed passages — read this before quoting a formula

Cleanup was model-assisted, and on badly-extracted PDFs the models sometimes
**reconstructed** damaged mathematics rather than only reformatting it.
Every such passage is annotated inline with `GARBLED` or `NOTE`, and any file containing
them opens with a ⚠️ banner giving the count.

| File stem | Annotated | Notes |
| --- | --- | --- |
| `stromquist-2003-packing-10-or-11-unit-squares` | 3 | Figure 13’s four defining coordinates were interleaved by the raw multi-column extraction and then reconstructed incorrectly. The lists are now read directly from rendered PDF page 9. A second annotation preserves but corrects the paper’s own extraneous-root error in the middle Lemma 4 table. A third gives an explicit box escaping the printed Figure 14 set and distinguishes that proof gap from the separately proposed one-coordinate repair. |
| `erdos-graham-1975-on-packing-squares-with-equal-squares` | 17 | **Heavily damaged** 1975 typescript scan. The central theorem was *not extracted at all* — raw shows only `Theorem.` then `(1)` — and the transcription supplies the known `w(α) = Θ(α^{7/11})` as a flagged reconstruction. A reading aid, not a source. |
| `compound-perfect-squared-squares-1303.0599` | 10 | Ten passages, nearly all **tables and matrices** scrambled by multi-column extraction. Do not cite its tables. |
| `bentz-2016-optimal-packings-22-and-33` | 3 | Probable “Stromberg” → “Stromquist” correction and a reconstructed distance bound in Lemma 7. |
| `friedman-ds7-packing-unit-squares-in-squares` | 3 | **The “Optimal?” column of Table 1 was INFERRED, not read** — the column exists in the original but its per-row values were lost, and the transcriber deduced them from the survey’s own theorems. Both appendix tables (53 and 29 rows) were likewise reassembled from interleaved extractions. The survey predates later results, so a blank means “not proved as of that revision”. **The research doc’s proof-status claims do not rest on this file** — they use Kingbird’s explicit “Proved by” attributions and the individual papers. |
| `square-packing-x06-wasted-area-2508.04603` | 5 | Three cells of the Section 5 comparison table; plus two Section 5 repairs (the omitted $\nu$ condition in Proposition 7 and the lost division bar in the reduction waste term). Do not cite that table. |
| `arslanov-improved-packings-n-n-1` | 1 | One orientation-constraint formula unrecoverable; its numeric value is preserved. |
| `bentz-2010-optimal-packings-13-and-46` | 1 | Corollary 7: segments reconstructed **and an inequality direction changed** (`2√2−2 > b` in raw vs `b > 2√2−2` here). Direction UNVERIFIED. The leading claim — intersection length ≥ `2√2−2 ≈ 0.828` — is unambiguous in the raw and unaffected. |
| `kearney-shiu-2002-efficient-packing-unit-squares` | 1 | One chain of inequalities in Theorem 2’s proof not reconstructed; the conclusion is stated. |
| `mcclenagan-2026-optimally-packing-large-square` | 2 | One exponent `(3−√3)/2` reconstructed from fragments, flagged as possibly wrong; plus a source-level contradictory chain in Section 3. Independently corroborated elsewhere, so the research doc does not rely on this file for it. |

Files not listed carry no annotations.
Note that resolving `(cid:NN)` ligature artifacts, running headers and page numbers is
ordinary cleanup, not reconstruction, and is not flagged.

**The rule:** if a formula sits near an annotation, check it against the `.raw.md`
before relying on it.
That is what the raw files are for.
The research document cites only claims that are unambiguous in the raw extractions.

## Why this archive is not auto-formatted

The repository auto-formats all Markdown with flowmark on commit.
This directory is excluded, deliberately and for a measured reason.

The `.raw.md` files must stay byte-exact to serve as ground truth.
But the cleaned `.md` transcriptions are excluded too, because flowmark inserts line
breaks **inside** `$...$` math spans when it rewraps.
Measured 2026-08-22: 31 of 339 spans broken in the Stromquist transcription, 101 of 1236
in Caoduro–Sebő, 5 of 433 in the Kingbird capture.
A newline in the middle of a formula defeats `grep`, which is what this archive exists
for.

The same byte-level rule applies to whitespace.
Some faithful `pdfminer` output contains spaces on blank lines, so the root
`.gitattributes` disables Git whitespace diagnostics only for `resources/**/*.raw.md`.
Hand-written Markdown keeps the normal check; raw extraction bytes are never normalized
to satisfy a presentation rule.

`explorations/packing/resources/README.md` — this file — is *not* excluded, and is
formatted normally.

## Searching

Paths below are written from the repository root.

```bash
# Find every mention of a bound across the whole archive
grep -rn "unavoidable" explorations/packing/resources/ --include=*.md

# Search only cleaned papers, not raw extractions or HTML
grep -rn "3.877" explorations/packing/resources/papers/*.md

# Check a formula in a cleaned paper against the raw extraction
grep -n "sqrt" explorations/packing/resources/papers/stromquist-2003-*.raw.md
```

## Papers

Citation keys match those used in the research document.

| Key | Title | Authors | Year | Venue | File stem |
| --- | --- | --- | --- | --- | --- |
| **[Stromquist Memo I]** | Packing Unit Squares Inside Squares, I (Six Unit Squares) | W. Stromquist | 1984 | Daniel H. Wagner, Associates internal memorandum, September 11 | `stromquist-1984-packing-unit-squares-inside-squares-i-six-unit-squares` |
| **[Stromquist Memo II]** | Packing Unit Squares Inside Squares, II (Ten Unit Squares) | W. Stromquist | 1984 | Daniel H. Wagner, Associates internal memorandum, October 15 | `stromquist-1984-packing-unit-squares-inside-squares-ii-ten-unit-squares` |
| **[Stromquist Memo III]** | Packing Unit Squares Inside Squares, III (Cases with n ≤ 65 and Martin Gardner’s Conjecture for n = 11) | W. Stromquist | 1984 | Daniel H. Wagner, Associates internal memorandum, November 15 | `stromquist-1984-packing-unit-squares-inside-squares-iii-cases-through-65-and-gardner-conjecture` |
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
| **[Gensane–Ryckelynck 2005]** | Improved Dense Packings of Congruent Squares in a Square | T. Gensane, P. Ryckelynck | 2005 | Discrete Comput. Geom. 34, 97–109 | `gensane-ryckelynck-2005-improved-dense-packings` |
| **[Nagamochi 2005]** | Packing Unit Squares in a Rectangle | H. Nagamochi | 2005 | Electron. J. Combin. 12, #R37 | `nagamochi-2005-packing-unit-squares-in-a-rectangle` |
| **[Wang–Dong–Li 2016]** | A New Result on Packing Unit Squares into a Large Square | S. Wang, T. Dong, J. Li | 2016 | arXiv:1603.02368 | `wang-dong-li-2016-new-result-packing-unit-squares` |
| **[Basic-Slivkova 2018]** | On optimal piercing of a square | B. Bašić, A. Slivková | 2018 | Discrete Applied Mathematics 247 | `basic-slivkova-2018-optimal-piercing-square` |
| **[Alpert et al. 2023]** | Homology of configuration spaces of hard squares in a rectangle | H. Alpert, U. Bauer, M. Kahle, R. MacPherson, K. Spendlove | 2023 | Algebraic & Geometric Topology 23, 2593–2626; arXiv:2010.14480 | `alpert-bauer-kahle-macpherson-spendlove-2023-hard-squares-configuration-spaces` |
| **[Alvarado-Garduño–González 2025]** | Square-section braid groups and Higman–Neumann–Neumann extensions | O. Alvarado-Garduño, J. González | 2025 | arXiv:2510.17707 | `alvarado-garduno-gonzalez-2025-square-section-braid-groups` |
| **[Roth–Vaughan 1978]** | Inefficiency in Packing Squares with Unit Squares | K. F. Roth, R. C. Vaughan | 1978 | JCTA 24, 170–186 | `roth-vaughan-1978-inefficiency-packing-squares` |

## Web sources

| Key | What | Source | File stem (in `web/`) |
| --- | --- | --- | --- |
| **[Friedman Center]** | Packing Center record tables and diagrams | erich-friedman.github.io | `friedman-packing-center-squares` |
| **[Friedman DS7 html]** | 2009 HTML edition of the DS7 survey | combinatorics.org | `friedman-ds7-survey-2009-html` |
| **[Kingbird]** | Squares-in-Squares catalogue: exact minimal polynomials, rigidity flags | kingbird.myphotos.cc | `kingbird-squares-in-squares` |
| **[Kingbird-compared]** | Supersession history: which record fell to which method, when | kingbird.myphotos.cc | `kingbird-squares-in-squares-compared` |
| **[Montanher et al. 2018]** | Rigorous packing of unit squares into a circle (full text via PMC) | pmc.ncbi.nlm.nih.gov | `montanher-2018-rigorous-packing-unit-squares-circle` |
| **[Markót 2021]** | Improved interval methods for circle packing in the unit square (full text via PMC) | pmc.ncbi.nlm.nih.gov | `markot-2021-improved-interval-methods-circle-packing` |
| **[squaring.net BSST]** | The Smith-diagram / Kirchhoff correspondence, in detail | squaring.net | `squaring-net-brooks-smith-stone-tutte-II` |
| **[squaring.net Sprague]** | Priority for the first published perfect squared square | squaring.net | `squaring-net-sprague` |
| **[Wikipedia]** | Square packing overview | en.wikipedia.org | `wikipedia-square-packing` |

## Special Kingbird SVG witnesses

These are not papers, but they carry the source geometry rather than a rendered picture.

- `papers/kingbird-square-11-provenance.svg` is the single most information-dense source
  found on `n = 11`. Its XML comments carry David Ellsworth’s provenance notes, the two
  contact equations, the derived placement constants, and the full exact-solution
  history (Gensane–Ryckelynck 2004 → Ellsworth 2023 → Alexeev’s independent
  confirmation). It is preserved verbatim.
- `papers/kingbird-square-29-provenance.svg` carries Thomas Schadt and David Ellsworth’s
  `n = 29` construction, 100-digit placement constants, the six defining equations, and
  the full SVG transform tree.
  The upstream response was retrieved on 2026-08-24. The retained text differs only by
  CRLF-to-LF normalization and a terminal newline.
  The H-024 experiment records the URL, retrieval date, normalization, and retained
  path; Git retains the source bytes.

## Not retrievable

Recorded so nobody re-hunts them.
**Re-test this list rather than inheriting it.** On 2026-08-22 three entries were
removed because they turned out to be freely available: Gensane–Ryckelynck (Springer
serves the PDF openly at its `/content/pdf/` URL — the earlier attempt had fetched the
article landing page), Nagamochi (open access in the *Electronic Journal of
Combinatorics*, and cited by its exact title in the archived DS7 reference list all
along), and Wang–Dong–Li (arXiv).
A “not retrievable” verdict is a negative search result, and this archive has now been
wrong about it **six** times: Markót 2021 was open access at PMC the whole time, Roth &
Vaughan (1978) was supplied on request, and Stromquist’s three memoranda were linked
directly from the author’s publication page.
Reading Roth–Vaughan produced two corrections to the published secondary literature.

**The canonical list now lives in
[`../frontier/source-availability.yaml`](../frontier/source-availability.yaml)**, with
the obstacle, what depends on each source, and a route to obtaining it; the research
document renders it as a table.
The short version below is kept for readers of this archive.

| Source | Obstacle |
| --- | --- |
| Trump, *Packing of 11 unit squares in a square with minimum size* (Mar 2023) | ResearchGate 403 |
| El Moumni, *Optimal Packings of Unit Squares in a Square*, Studia Sci. Math. Hungar. 35 (1999) | Print-only; no digital copy located. Holds published priority for `s(7) = s(8) = 3` and `s(15) = 4`. |
| Arslanov & Bui, *Note on “efficient packings of unit squares in a large square”*, DCG (2025) | Springer; not open access. |
| Brooks, Smith, Stone & Tutte, *The dissection of rectangles into squares*, Duke Math. J. 7 (1940) | Project Euclid; not open access |
| Gustafsson & Thulin (1980), *Ronden* | Swedish company periodical; Ellsworth notes he has not read it directly either |

## Provenance and licence

The original archive was retrieved on **2026-08-22** from the URLs recorded in each
file’s metadata header.
The three Stromquist memoranda were retrieved on **2026-08-24** from the author’s
[official publication page](https://www.walterstromquist.com/publications.html), which
links the exact archived PDFs as `squares1.pdf`, `squares2.pdf`, and `squares3.pdf`. All
three PDFs are image-only scans; their raw aids are unedited Tesseract 5.5.0 English OCR
from 300 dpi Poppler-rendered page images, concatenated in page order with form-feed and
newline separators. Archive PDFs are marked binary in the repository’s `.gitattributes`;
this prevents Git from interpreting compressed scan streams as text without changing any
source bytes. The arXiv and Electronic Journal of Combinatorics items are open access;
the Stanford technical report and PMC item are publicly posted.
Retained for private research use.
Consult the original publisher before redistributing.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
