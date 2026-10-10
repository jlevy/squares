# Research Resources: Square Packing

This directory is a local, greppable archive of the primary literature behind
[research-2026-08-22-packing-11-unit-squares.md](../../docs/project/research/research-2026-08-22-packing-11-unit-squares.md).
It keeps the literature searchable without refetching, re-extracting, or fighting
paywalls and bot blocks.

**[Pingyou Fibonacci torus abstract 2026]** — the owner’s undated first-page
[screenshot packet](web/pingyou-fibonacci-torus-2026-10-07/README.md), received 7
October 2026: original image, raw OCR, visually corrected transcription, and explicit
source gaps. The
[X-050 audit](../campaign/explorations/X-050-fibonacci-torus-and-boundary-information.md)
contains the dispositions; no full manuscript or geometric torus inverse was supplied.

**[Berthold et al. 2026b]** — the already retained arXiv:2605.04850v1 PDF and raw
extraction were rechecked against a fresh download on October 8, 2026. The
[n17 paper review](../../docs/project/reviews/review-2026-10-08-n17-global-optimization-and-sos.md)
assesses its Farkas formulation and relevance to exact sum-of-squares certificates.
It adds no packing bound or optimality result.

**SOS certificate methods** — the
[October 8 source packet](web/n17-sos-sources-2026-10-08/README.md) records extraction
quality for the Blekherman–Parrilo–Thomas book and Laplagne’s facial-reduction paper.
The
[extended n17 review](../../docs/project/reviews/review-2026-10-08-n17-global-optimization-and-sos.md)
includes the derived exact weighted-vertex screen and conditional SOS plan.

## Layout

```
packing/resources/
├── bibliography.yaml       Citation fields for the keys something cites; see below
├── papers/                 Academic papers: original .pdf, cleaned .md, and faithful .raw.md
├── private-correspondence/ Unpublished letters and email, transcribed verbatim
└── web/                    Web sources: original .html and maintained .md capture
```

**The tables in this file are the index of citation keys; `bibliography.yaml` is the
same keys as data.** It carries only what a line of citation text is built from — each
cited source’s authors as a citation prints them, its year, a short venue, and, where a
line would otherwise run past the width the stage sets, a shorter venue still — and the
surname each credited finder is cited under.
[`devtools.build_bound_citations`](../devtools/build_bound_citations.py) reads it to
write the stage’s citation lines, and
[`tests/test_bound_citations.py`](../tests/test_bound_citations.py) checks that every
key in it is defined in bold here, that a paper’s year and authors agree with the Papers
table below, and that every source key the frontier register uses is defined here.
It is not an archived source and is edited like any other record; a key it needs that
this file does not define fails that test rather than being added silently.

**Large retained data in `web/` is stored as deterministic gzip.** A packet keeps a
retained data file (JSON, JSON Lines, a text certificate, a ledger or a log) of more
than 1,000 lines as `X.gz`, made by `gzip -9n` so no name or timestamp enters the bytes,
following the [R052 packet](web/n17-guzhou-r052-2026-09-25/README.md); source code stays
plain at any size. The packet README’s Compressed Files table gives each file’s Git blob
and the SHA-256 of its decompressed bytes, and the `gunzip -k` command that restores the
upstream tree for a manual replay.
Readers go through [`devtools.retained_data`](../devtools/retained_data.py), which reads
`X` or `X.gz`, and [`tests/test_retained_data.py`](../tests/test_retained_data.py)
re-derives every table.

The archive’s normal form stores a paper three ways; the documented exceptions follow:

| File | What it is | Use it for |
| --- | --- | --- |
| `<name>.pdf` | The original, byte-for-byte as retrieved | Authority; figures; anything the text loses |
| `<name>.md` | Cleaned Markdown, headings and LaTeX restored | Reading and quoting |
| `<name>.raw.md` | Unedited extraction or OCR output | Check the clean copy against this; for image-only scans, the PDF remains the ground truth |

The `.raw.md` files are deliberately retained.
Cleanup was done by language models, so the raw extraction is the fallback whenever a
formula in a `.md` looks suspicious.

**Transcription status, stated exactly.** The archive normally stores an original
source, a cleaned `.md` transcription, and a faithful `.raw.md` extraction.
One hundred and ten entries currently fall short in ways worth naming rather than
hiding:

- `gensane-ryckelynck-2005-improved-dense-packings`,
  `nagamochi-2005-packing-unit-squares-in-a-rectangle`,
  `wang-dong-li-2016-new-result-packing-unit-squares` and
  `basic-slivkova-2018-optimal-piercing-square`,
  `alpert-bauer-kahle-macpherson-spendlove-2023-hard-squares-configuration-spaces`,
  `alvarado-garduno-gonzalez-2025-square-section-braid-groups`,
  `el-moumni-1999-optimal-packings-unit-squares`, and
  `trump-2023-packing-11-unit-squares`, plus `bal-2026-64-rectangle-wegner-lp-gaps`,
  `dewar-2024-contacts-oriented-squares`,
  `connelly-whiteley-1996-second-order-rigidity`,
  `donev-torquato-stillinger-connelly-2004-jamming-lp`,
  `donev-connelly-stillinger-torquato-2007-underconstrained-jammed-packings`, and
  `connelly-packings-of-circles-and-spheres-lecture-notes` are **raw-only**: PDF and
  faithful extraction, no cleaned transcription yet.
  All fourteen were read directly from the PDF, and the claims resting on them were
  checked there.
- `laplagne-2018-facial-reduction-exact-polynomial-sos-1810.04215v1` is **raw-only**:
  original PDF, unedited text and original TeX, with no cleaned Markdown transcription.
  The [source packet](web/n17-sos-sources-2026-10-08/README.md) records PDF/TeX checks
  and glyph artifacts.
  The book’s full source remains outside Git; its extraction status is also recorded
  there.
- The fifteen search-method sources retained on 2026-09-08 for
  [the annealing report](../../docs/project/research/research-2026-09-08-annealing-for-square-packing.md)
  are **raw-only** on the same terms:
  `ye-huang-lu-2013-iterated-tabu-search-unequal-circles`,
  `gensane-2004-dense-packings-equal-spheres-cube`,
  `addis-locatelli-schoen-2008-disk-packing-square`,
  `grosso-jamali-locatelli-schoen-2010-packing-equal-unequal-circles`,
  `lai-hao-xiao-glover-2023-perturbation-thresholding-search`,
  `odriozola-2009-replica-exchange-hard-spheres`,
  `johnson-aragon-mcgeoch-schevon-1989-annealing-part-i`,
  `johnson-aragon-mcgeoch-schevon-1991-annealing-part-ii`,
  `blair-santangelo-machta-2012-packing-squares-in-a-torus`,
  `berthold-kamp-mexi-pokutta-polik-2026-global-optimization-combinatorial-geometry`,
  `berthold-kamp-mexi-pokutta-polik-2026-out-of-the-box-packing-problems`,
  `ninarello-berthier-coslovich-2017-next-generation-glass-transition`,
  `xu-xiao-amos-2008-simulated-annealing-weighted-polygon-packing`,
  `anderson-irrgang-glotzer-2016-scalable-metropolis-hard-shapes`, and
  `gardeyn-vandenberghe-wauters-2025-sparrow-2d-nesting`. These are method sources
  rather than results about congruent squares, and a cleaned transcription would buy
  little: the report’s readings from them are specific numbered observations and tables.
  Three of those readings were checked against the retained bytes and the check is
  recorded in
  [the acquisition packet](web/annealing-methods-audit-2026-09-08/README.md); the rest
  are cited from abstracts, tables, or the report’s own reading, and the packet says
  which.
- The **seventy-two** simulation- and physics-method sources retained on 2026-09-09 for
  [the simulation mechanisms report](../../docs/project/research/research-2026-09-09-simulation-mechanisms-for-packing.md)
  are **raw-only** on the same terms, and are listed in
  [their own table](#simulation-and-physics-method-sources) below.
  Like the 2026-09-08 batch these are method sources rather than results about congruent
  squares, and a cleaned transcription would buy little: the report’s readings from them
  are specific numbered parameters, quoted sentences and tables.
  Eight of those readings were checked against the retained bytes and the check is
  recorded in
  [the acquisition packet](web/simulation-methods-audit-2026-09-09/README.md), which
  also names every source the pass could not obtain and says what the report does and
  does not claim from it.
  One of the seventy-two, `more-wu-1997-global-continuation-distance-geometry`, is an
  **image-only raster scan**: its faithful extraction is 28 bytes of form feeds and
  `pdftotext` reported no warning at all, so an `.ocr.md` sidecar is retained beside it
  on the same terms as the Stromquist memoranda, and the formulas the report quotes were
  read off rendered page images rather than off the OCR.
- Six papers retrieved on 2026-10-05, once this environment reached their hosts, are
  **raw-only** for now: `chung-graham-2009-packing-equal-squares-into-a-large-square`
  and `chung-graham-2020-efficient-packings-unit-squares-large-square`, in the Papers
  table, and four contact-dynamics papers from HAL, in
  [the simulation table](#simulation-and-physics-method-sources).
  Each `.raw.md` is `pdftotext -layout`; no reading rests on them yet.
- `gobel-1979-geometrical-packing-and-covering-problems` is **PDF-only**: the source is
  retained, but neither a cleaned transcription nor a faithful extraction has been
  produced. Claims resting on it must be checked against the page images.
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
- The three [MacIver 2026 manuscripts](web/maciver-square-packing-2026-09-07/README.md)
  have original PDFs, faithful `pdftotext -layout` extractions, and one shared reading
  aid. They have no cleaned transcriptions.
  The packet records their source claims, incomplete local verification, and the missing
  computational artifacts for the seventeen-square proof.

Writing the missing transcriptions is deferred deliberately rather than done hastily—
model-assisted cleanup is exactly what produced the reconstruction hazards tabulated in
the next section, and Roth–Vaughan is the argument for that caution: two independent
secondary sources reported a constant the paper does not contain.

## Reconstructed Passages: Read This Before Quoting a Formula

Cleanup was model-assisted, and on badly-extracted PDFs the models sometimes
**reconstructed** damaged mathematics rather than only reformatting it.
Every such passage is annotated inline with `GARBLED` or `NOTE`, and any file containing
them opens with a ⚠️ banner giving the count.

| File stem | Annotated | Notes |
| --- | --- | --- |
| `stromquist-2003-packing-10-or-11-unit-squares` | 3 | Figure 13’s four defining coordinates were interleaved by the raw multi-column extraction and then reconstructed incorrectly. The lists are now read directly from rendered PDF page 9. A second annotation preserves but corrects the paper’s own extraneous-root error in the middle Lemma 4 table. A third gives an explicit box escaping the printed Figure 14 set and distinguishes that proof gap from the separately proposed one-coordinate repair. |
| `erdos-graham-1975-on-packing-squares-with-equal-squares` | 20 | **Heavily damaged** 1975 typescript scan. The central theorem was *not extracted at all*—raw shows only `Theorem.` then `(1)`—and until 2026-10-02 the transcription supplied `w(α) = Θ(α^{7/11})` as a flagged reconstruction, a two-sided bound the paper does not state ([D-514](../../defects.md)). Three notes of that date read the rendered pages instead: PDF page 4 prints (1) as the upper bound `W(α) = O(α^{7/11})`, and printed page 6 says the authors have no nontrivial lower estimate; the proof’s two-sided symbol is the paper’s own `Ω`, defined as bounded on both sides and restored at every occurrence where the transcription had `Θ`; and the closing “just `Ω(α^{7/11})`” is the waste of the one construction, which gives the upper bound only. Most passages still marked `GARBLED` are legible on the rendered pages and have not been re-read. A reading aid, not a source. |
| `compound-perfect-squared-squares-1303.0599` | 9 | Nine passages, nearly all **tables and matrices** scrambled by multi-column extraction. Do not cite its tables. The cell read `10` until 2026-09-21, when `check_archive_annotations` first compared it with the file: the count is of markers, and one marker repairs two objects at once — the reduction vector `R` and the reduced currents matrix `B` share a single `GARBLED` note — which is the likeliest source of the tenth. |
| `bentz-2016-optimal-packings-22-and-33` | 9 | Probable “Stromberg” → “Stromquist” correction and a reconstructed distance bound in Lemma 7. Two notes, added 2026-09-20, correct the finishing line of Theorems 9 and 11, which the interleaved extraction had turned into `(√2−1)/2 ≈ 0.2071`: the PDF prints the line at `√2 − 1/2 ≈ 0.9142` and the midpoint standoff as `½√2 − ½ ≈ 0.2071`, which are the constants the last step needs. Two more, of the same date, repair Lemma 7’s proof: its bound is `0.505√2 ≈ 0.7142`, not the transcribed `0.505/√2 ≈ 0.3571`, and the printed lemma reference “Lemma 5” is restored with the note that Lemma 4 is the applicable one, so the transcription no longer silently corrects its source. An eighth, same date, restores the factor 2 the transcription dropped from the Theorem 9 budget line: PDF page 5 prints `2(√2 − ½) + 2·0.8 + 3·½√3 ≈ 6.0265 > 6`, and without the factor the transcribed left side is `≈ 5.1123`, below 6 and so false. A ninth records a slip of the source rather than of the transcription: PDF page 8 names case 2’s end point `(0.5, √2 − ½)` where Figure 3 has `(0.5, 0.9)`, and that step holds with either value (`0.49733` against `0.48444`, both under `½`), so the text is left as printed. |
| `friedman-ds7-packing-unit-squares-in-squares` | 3 | **The “Optimal?” column of Table 1 was INFERRED, not read**—the column exists in the original but its per-row values were lost, and the transcriber deduced them from the survey’s own theorems. Both appendix tables (53 and 29 rows) were likewise reassembled from interleaved extractions. The survey predates later results, so a blank means “not proved as of that revision”. **The research doc’s proof-status claims do not rest on this file**—they use Kingbird’s explicit “Proved by” attributions and the individual papers. |
| `square-packing-x06-wasted-area-2508.04603` | 6 | Three cells of the Section 5 comparison table; two Section 5 repairs (the omitted $\nu$ condition in Proposition 7 and the lost division bar in the reduction waste term); and the omitted upper bound on Section 3.1’s replacement index. Do not cite that table. |
| `arslanov-improved-packings-n-n-1` | 1 | One orientation-constraint formula unrecoverable; its numeric value is preserved. |
| `bentz-2010-optimal-packings-13-and-46` | 2 | Corollary 7: segments reconstructed **and an inequality direction changed** (`2√2−2 > b` in raw vs `b > 2√2−2` here). Direction UNVERIFIED. The leading claim—intersection length ≥ `2√2−2 ≈ 0.828`—is unambiguous in the raw and unaffected. A second annotation, audited 2026-08-31 under BC-106, records that published Lemma 10 prints `(1, 1.74)` where the argument needs `(1.74, 1)`: the lemma is refuted as printed by an exact escape certificate and certified under the corrected reading, and the rendered PDF places the transposition in the journal rather than in the extraction, so the text is left as printed. This row read `1` until 2026-09-21. |
| `kearney-shiu-2002-efficient-packing-unit-squares` | 1 | One chain of inequalities in Theorem 2’s proof not reconstructed; the conclusion is stated. |
| `mcclenagan-2026-optimally-packing-large-square` | 4 | One exponent `(3−√3)/2` reconstructed from fragments, flagged as possibly wrong; plus a source-level contradictory chain in Section 3. H-037 gives an independent local repair of the chain; it does not certify the full theorem. Two notes of 2026-10-02 correct the introduction’s history paragraph against rendered PDF page 1 ([D-515](../../defects.md)): the transcription had swapped the paragraph’s exponents, giving Montgomery `(3+√2)/7` where the page prints `(3−√3)/2` and the restored bound `(3−√3)/2` where it prints `(3+√2)/7`, and had written `√(log x)` twice where the page prints `log x`. The flagged reconstruction was the wrong one, and the unflagged Montgomery exponent was wrong as well. |

Files not listed carry no annotations.
Resolving `(cid:NN)` ligature artifacts, running headers, and page numbers is ordinary
cleanup, not reconstruction, and is not flagged.

**The rule:** if a formula sits near an annotation, check it against the `.raw.md`
before relying on it.
The research document cites only claims that are unambiguous in the raw extractions.

## Why This Archive Is Not Auto-Formatted

The repository auto-formats maintained Markdown with Flowmark on commit.
The paper and web archives are excluded for two independent reasons.
First, `.raw.md` files are byte-level ground truth, so reflowing them would void the
comparison with the model-assisted transcriptions.
Second, the cleaned `.md` files are archival transcriptions: formatting would retype
source characters such as straight quotes and ellipses merely to make them look tidy.

Inline mathematics is no longer the reason for the exclusion.
The pinned `flowmark-rs==0.4.0` keeps every `$...$` span whole, and
`devtools.check_math_spans` remeasures that property on copies.
The archive remains excluded because source and transcription fidelity still require it.

The same byte-level rule applies to whitespace.
Some faithful `pdfminer` output contains spaces on blank lines, so the root
`.gitattributes` disables Git whitespace diagnostics only for `resources/**/*.raw.md`.
Hand-written Markdown keeps the normal check; raw extraction bytes are never normalized
to satisfy a presentation rule.

`packing/resources/README.md` is formatted normally.

## Searching

Paths below are written from the repository root.

```bash
# Find every mention of a bound across the whole archive
grep -rn "unavoidable" packing/resources/ --include=*.md

# Search only cleaned papers, not raw extractions or HTML
grep -rn "3.877" packing/resources/papers/*.md

# Check a formula in a cleaned paper against the raw extraction
grep -n "sqrt" packing/resources/papers/stromquist-2003-*.raw.md
```

## Papers

Citation keys match those used in the research document.
This table holds sources about packing congruent squares.
Two further tables below hold method analogues from adjacent problems:
[rigidity and verification](#rigidity-and-verification-method-sources), and
[search and annealing](#search-and-annealing-method-sources).

| Key | Title | Authors | Year | Venue | File stem |
| --- | --- | --- | --- | --- | --- |
| **[Stromquist Memo I]** | Packing Unit Squares Inside Squares, I (Six Unit Squares) | W. Stromquist | 1984 | Daniel H. Wagner, Associates internal memorandum, September 11 | `stromquist-1984-packing-unit-squares-inside-squares-i-six-unit-squares` |
| **[Stromquist Memo II]** | Packing Unit Squares Inside Squares, II (Ten Unit Squares) | W. Stromquist | 1984 | Daniel H. Wagner, Associates internal memorandum, October 15 | `stromquist-1984-packing-unit-squares-inside-squares-ii-ten-unit-squares` |
| **[Stromquist Memo III]** | Packing Unit Squares Inside Squares, III (Cases with n ≤ 65 and Martin Gardner’s Conjecture for n = 11) | W. Stromquist | 1984 | Daniel H. Wagner, Associates internal memorandum, November 15 | `stromquist-1984-packing-unit-squares-inside-squares-iii-cases-through-65-and-gardner-conjecture` |
| **[Stromquist 2003]** | Packing 10 or 11 Unit Squares in a Square | W. Stromquist | 2003 | Electron. J. Combin. 10, #R8 | `stromquist-2003-packing-10-or-11-unit-squares` |
| **[Friedman DS7]** | Packing Unit Squares in Squares: A Survey and New Results | E. Friedman | 1998– | Electron. J. Combin., Dynamic Survey DS7 | `friedman-ds7-packing-unit-squares-in-squares` |
| **[Kearney–Shiu 2002]** | Efficient packing of unit squares in a square | M. J. Kearney, P. Shiu | 2002 | Electron. J. Combin. 9, #R14 | `kearney-shiu-2002-efficient-packing-unit-squares` |
| **[Göbel 1979]** | Geometrical Packing and Covering Problems | F. Göbel | 1979 | *Packing and Covering in Combinatorics*, Math. Centre Tracts 106, 179–199 | `gobel-1979-geometrical-packing-and-covering-problems` |
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
| **[El Moumni 1999]** | Optimal Packings of Unit Squares in a Square | S. El Moumni | 1999 | Studia Sci. Math. Hungar. 35, 281–290 | `el-moumni-1999-optimal-packings-unit-squares` |
| **[Trump 2023]** | Packing of 11 unit squares in a square with minimum size | W. Trump | 2023 | Author preprint | `trump-2023-packing-11-unit-squares` |
| **[Bal 2026]** | A 64-Rectangle Counterexample to Wegner’s Conjecture and LP Gaps up to 5/2 | A. K. Bal | 2026 | arXiv:2607.11318v2 | `bal-2026-64-rectangle-wegner-lp-gaps` |
| **[Dewar 2024]** | How many contacts can exist between oriented squares of various sizes? | S. Dewar | 2024 | Discrete Math. 347(4), 113879; arXiv:2210.10422v2 | `dewar-2024-contacts-oriented-squares` |
| **[Karakuş 2026]** | A counterexample to Nagamochi’s scoring lemma and a new rectangle packing bound | H. Karakuş | 2026 | arXiv:2609.37410v1, 29 September 2026; CC BY 4.0; retrieved 2026-10-02, cleaned copy written from the author’s LaTeX source | `karakus-2026-counterexample-nagamochi-scoring-lemma` |
| **[Chung–Graham 2009]** | Packing equal squares into a large square | F. Chung, R. Graham | 2009 | J. Combin. Theory Ser. A 116, 1167–1175; the authors’ 14-page copy, retrieved 2026-10-05 | `chung-graham-2009-packing-equal-squares-into-a-large-square` |
| **[Chung–Graham 2020]** | Efficient packings of unit squares in a large square | F. Chung, R. Graham | 2020 | Discrete Comput. Geom.; the authors’ 13-page preprint, retrieved 2026-10-05 | `chung-graham-2020-efficient-packings-unit-squares-large-square` |

## Contributed Research Packets

The owner-supplied
[complete n=11 research bundle](papers/n11-complete-research-bundle-2026-09-07/INTAKE.md)
was received on 2026-09-07 UTC; its complete 57-file distribution remains in the local
`attic/`. The tracked archive retains its research reports, source snapshot, figures,
checkers, replay outputs and delivered PDFs.
PDF publishing helpers and original distribution-integrity files stay in the attic.
The intake note records this selection, the adapted packaging documentation and the
scope of the replayed controls.
This is a contributed analysis packet; its proposals and supplied checks are not
automatically accepted campaign results.

[X-017](../campaign/explorations/X-017-compatibility-and-complete-case-covers.md) owns
the critical adaptation and complete source-to-record map.
[Agenda 027](../campaign/agendas/agenda-027-compatibility-and-restricted-families.md)
organizes the proposed work as a separate agenda.

## Private Correspondence

`private-correspondence/` holds unpublished letters and email that bear on the
mathematics, supplied by the project owner, transcribed verbatim and named for the
correspondent and the first message in the exchange.
The transcriptions are archived source in the sense the rest of this directory uses: not
edited to read more tidily, and cited where they are used.

Correspondence is weaker evidence than a paper, and is cited as such.
It is unrefereed, often written quickly, and its author may revise or withdraw a claim
in a later message—the one file here does exactly that twice.
Cite it for what its author says, never for what this project has established.

| Source | Correspondent | Dates | File |
| --- | --- | --- | --- |
| **[Stromquist 2026]** | Walter Stromquist | 2026-09-07 and 2026-09-09 | `email-stromquist-2026-09-07.md` |

Four things arrive in that exchange, and the record already speaks to each:

- **The repair for the 2003 Figure 14 proof.** The quadrilateral southwest of point `G`
  is not covered by Lemma 4, and Stromquist gives the coordinate he intended: `G` evenly
  spaced between `F` and the leftmost `A`, so `G = (0.8, s/2 - 0.05)`—`(0.8, 1.845)`
  serves—rather than the printed `(0.8, 1.85)`, with a row for `a = 0.945, b = 0.8` in
  the table after Lemma 4. This project found the printed point set unsound
  independently on 2026-08-24 ([D-152](../../defects.md)); what the letter adds is the
  author’s own intended coordinate, which no memo supplies.
- **Fractional packings, and a conjectured duality.** Weighted collections of squares
  under a unit depth constraint at every point, which any dots proof bans at total
  weight `n` alongside genuine `n`-packings.
  If the smallest container admitting fractional weight 11 is strictly smaller than the
  smallest admitting eleven squares, no certificate of this kind can reach the packing
  bound—which makes helper arguments necessary rather than convenient.
  Stromquist expects an LP duality here, and a continuous analogue matching largest
  fractional packing to smallest measure, but states he has never written the proof.
- **“Dots proofs” and helper arguments.** The 1980s terminology for the certificates
  this project builds, the finding from that period that `n = 6` admits no pure dots
  proof but does admit one preceded by a helper argument, the same shape he used for
  `n = 11`, and the open question of making helper arguments systematic.
- **Two withdrawals.** The `n = 26` contribution, on the ground that
  `5.62132 < 5.650629`, and the `n = 18` contribution, which he reports was not new even
  in 1984.

The exchange also points at three unpublished square-packing notes on the author’s own
site, linked as `-I`, `-II` and `-III` under Geometry on his research and publications
list; those are the 1984 memoranda already archived under `papers/`.

## Rigidity and Verification Method Sources

These papers and notes support the local-rigidity and certified-search program.
They are method analogues, not direct theorems about the global optimum for eleven
congruent squares. In particular, smooth-particle or tensegrity results require their
hypotheses to be matched to the square pose chart and its nonsmooth feature changes.

| Key | Title | Authors | Year | Venue | File stem |
| --- | --- | --- | --- | --- | --- |
| **[Connelly–Whiteley 1996]** | Second-Order Rigidity and Prestress Stability for Tensegrity Frameworks | R. Connelly, W. Whiteley | 1996 | SIAM J. Discrete Math. 9(3), 453–491 | `connelly-whiteley-1996-second-order-rigidity` |
| **[Donev et al. 2004]** | A Linear Programming Algorithm to Test for Jamming in Hard-Sphere Packings | A. Donev, S. Torquato, F. H. Stillinger, R. Connelly | 2004 | J. Comput. Phys. 197, 139–166 | `donev-torquato-stillinger-connelly-2004-jamming-lp` |
| **[Donev et al. 2007]** | Underconstrained Jammed Packings of Nonspherical Hard Particles: Ellipses and Ellipsoids | A. Donev, R. Connelly, F. H. Stillinger, S. Torquato | 2007 | Phys. Rev. E 75, 051304 | `donev-connelly-stillinger-torquato-2007-underconstrained-jammed-packings` |
| **[Connelly notes]** | Packings of Circles and Spheres, Lectures III and IV | R. Connelly | undated | Institut Henri Poincaré lecture slides | `connelly-packings-of-circles-and-spheres-lecture-notes` |

## Search and Annealing Method Sources

Retained on 2026-09-08 for
[Annealing for Square Packing](../../docs/project/research/research-2026-09-08-annealing-for-square-packing.md).
Only two of them are about squares at all, and neither sets a record for `s(n)`. They
are here because the report’s argument is about **search methods**, and the methods that
set packing records were developed on circles, disks and spheres, or measured on graph
problems. Every entry is raw-only.
The retrieval receipts, the checked readings, and the sources that could not be
retrieved are in
[`web/annealing-methods-audit-2026-09-08`](web/annealing-methods-audit-2026-09-08/README.md).

| Key | Title | Authors | Year | Venue | File stem |
| --- | --- | --- | --- | --- | --- |
| **[Gensane 2004]** | Dense Packings of Equal Spheres in a Cube | T. Gensane | 2004 | Electron. J. Combin. 11, #R33 | `gensane-2004-dense-packings-equal-spheres-cube` |
| **[Addis–Locatelli–Schoen 2008]** | Disk Packing in a Square: A New Global Optimization Approach | B. Addis, M. Locatelli, F. Schoen | 2008 | INFORMS J. Comput. 20(4), 516–524 (preprint) | `addis-locatelli-schoen-2008-disk-packing-square` |
| **[Grosso et al. 2010]** | Solving the problem of packing equal and unequal circles in a circular container | A. Grosso, A. R. M. J. U. Jamali, M. Locatelli, F. Schoen | 2010 | J. Global Optim. 47, 63–81 (preprint) | `grosso-jamali-locatelli-schoen-2010-packing-equal-unequal-circles` |
| **[Ye–Huang–Lü 2013]** | Iterated Tabu Search Algorithm for Packing Unequal Circles in a Circle | F. Ye, W. Huang, Z. Lü | 2013 | arXiv:1306.0694 | `ye-huang-lu-2013-iterated-tabu-search-unequal-circles` |
| **[Lai et al. 2023]** | Perturbation-based thresholding search for packing equal circles and spheres | X. Lai, J.-K. Hao, R. Xiao, F. Glover | 2023 | INFORMS J. Comput. (accepted manuscript) | `lai-hao-xiao-glover-2023-perturbation-thresholding-search` |
| **[Odriozola 2009]** | Replica Exchange Monte Carlo applied to Hard Spheres | G. Odriozola | 2009 | J. Chem. Phys. 131, 144107; arXiv:1010.2923 | `odriozola-2009-replica-exchange-hard-spheres` |
| **[Johnson et al. Part I]** | Optimization by Simulated Annealing: An Experimental Evaluation; Part I, Graph Partitioning | D. S. Johnson, C. R. Aragon, L. A. McGeoch, C. Schevon | 1989 | Oper. Res. 37(6), 865–892 | `johnson-aragon-mcgeoch-schevon-1989-annealing-part-i` |
| **[Johnson et al. Part II]** | Optimization by Simulated Annealing: An Experimental Evaluation; Part II, Graph Coloring and Number Partitioning | D. S. Johnson, C. R. Aragon, L. A. McGeoch, C. Schevon | 1991 | Oper. Res. 39(3), 378–406 | `johnson-aragon-mcgeoch-schevon-1991-annealing-part-ii` |
| **[Blair et al. 2012]** | Packing Squares in a Torus | D. W. Blair, C. Santangelo, J. Machta | 2012 | arXiv:1110.5348; J. Stat. Mech. | `blair-santangelo-machta-2012-packing-squares-in-a-torus` |
| **[Xu–Xiao–Amos 2008]** | Simulated Annealing for Weighted Polygon Packing | Y.-C. Xu, R.-B. Xiao, M. Amos | 2008 | arXiv:0809.5005 | `xu-xiao-amos-2008-simulated-annealing-weighted-polygon-packing` |
| **[Anderson et al. 2016]** | Scalable Metropolis Monte Carlo for simulation of hard shapes (HOOMD-blue HPMC) | J. A. Anderson, M. E. Irrgang, S. C. Glotzer | 2016 | Comput. Phys. Commun. 204, 21–30; arXiv:1509.04692 | `anderson-irrgang-glotzer-2016-scalable-metropolis-hard-shapes` |
| **[Ninarello et al. 2017]** | Models and algorithms for the next generation of glass transition studies | A. Ninarello, L. Berthier, D. Coslovich | 2017 | Phys. Rev. X 7, 021039; arXiv:1704.08864 | `ninarello-berthier-coslovich-2017-next-generation-glass-transition` |
| **[Berthold et al. 2026a]** | Global Optimization for Combinatorial Geometry Problems Revisited in the Era of LLMs | T. Berthold, D. Kamp, G. Mexi, S. Pokutta, I. Pólik | 2026 | arXiv:2601.05943 | `berthold-kamp-mexi-pokutta-polik-2026-global-optimization-combinatorial-geometry` |
| **[Berthold et al. 2026b]** | Out-of-the-Box Global Optimization for Packing Problems: New Models and Improved Solutions | T. Berthold, D. Kamp, G. Mexi, S. Pokutta, I. Pólik | 2026 | arXiv:2605.04850 | `berthold-kamp-mexi-pokutta-polik-2026-out-of-the-box-packing-problems` |
| **[Sparrow 2025]** | An open-source heuristic to reboot 2D nesting research | J. Gardeyn, G. Vanden Berghe, T. Wauters | 2025 | arXiv:2509.13329 | `gardeyn-vandenberghe-wauters-2025-sparrow-2d-nesting` |

## Simulation and Physics Method Sources

Retained on 2026-09-09 for
[Physics and Simulation Mechanisms for Square Packing](../../docs/project/research/research-2026-09-09-simulation-mechanisms-for-packing.md).
None of them is about congruent squares in a square, and none sets a record for `s(n)`.
They are here because that report’s argument is about **mechanisms that move bodies
under a simulated physical or geometric rule**, and those mechanisms were developed on
disks, spheres, ellipses, polyhedra and, in the graphics half, on nothing in particular.
Every entry is raw-only, with the one image-only exception named above.
The acquisition URLs, retrieval timestamps, per-file SHA-256 hashes, the eight readings
checked against the retained bytes, the screened-out material, and every source that
could not be retrieved are in
[`web/simulation-methods-audit-2026-09-09`](web/simulation-methods-audit-2026-09-09/README.md).

### Inflation, event-driven dynamics and billiards

| Source | File stem |
| --- | --- |
| Lubachevsky, *How to Simulate Billiards and Similar Systems*, J. Comput. Phys. 94, 1991 | `lubachevsky-1991-how-to-simulate-billiards` |
| Donev, Torquato & Stillinger, *Neighbor list collision-driven molecular dynamics for nonspherical hard particles*, 2005 | `donev-torquato-stillinger-2005-neighbor-list-collision-driven-nonspherical` |
| Skoge, Donev, Stillinger & Torquato, *Packing hyperspheres in high-dimensional Euclidean spaces*, 2006 | `skoge-donev-stillinger-torquato-2006-packing-hyperspheres-high-dimensional-euclidean-spaces` |
| Torquato & Stillinger, *Jammed hard-particle packings: from Kepler to Bernal and beyond*, Rev. Mod. Phys. 82, 2010 | `torquato-stillinger-2010-jammed-hard-particle-packings-kepler-bernal` |
| Jiao, Stillinger & Torquato, *Optimal packings of superdisks*, 2008 | `jiao-stillinger-torquato-2008-dense-packings-superdisks` |
| Jiao, Stillinger & Torquato, *Maximally random jammed packings of superballs*, 2010 | `jiao-stillinger-torquato-2010-mrj-packings-superballs` |
| Klement, Lee, Anderson & Engel, *Newtonian event-chain Monte Carlo and collision prediction with polyhedral particles*, 2021 | `klement-engel-2021-newtonian-event-chain-monte-carlo-collision-prediction-polyhedra` |
| Hoover, Hoover & Bannerman, *Single-speed molecular dynamics of hard parallel squares and cubes*, 2009 | `hoover-hoover-bannerman-2009-single-speed-md-hard-parallel-squares-cubes` |
| Hoy, *Ultradense jammed ellipse packings via biased SWAP*, 2024 | `hoy-2024-ultradense-jammed-ellipse-packings-biased-swap` |
| Bannerman, Sargant & Lue, *DynamO: a free O(N) general event-driven molecular dynamics simulator*, 2011 | `bannerman-sargant-lue-2011-dynamo-free-event-driven-md-simulator` |
| Boll, Donovan, Graham & Lubachevsky, *Improving dense packings of equal disks in a square*, 2000 | `boll-donovan-graham-lubachevsky-2000-improving-dense-packings-disks-square` |
| Graham & Lubachevsky, *Repeated patterns of dense packings of equal disks in a square*, 1996 | `graham-lubachevsky-1996-repeated-patterns-dense-packings-disks-square` |
| Graham & Lubachevsky, *Dense packings of equal disks in an equilateral triangle*, 1995 | `graham-lubachevsky-1995-dense-packings-disks-equilateral-triangle` |
| Lubachevsky & Graham, *Curved hexagonal packings of equal disks in a circle*, 1997 | `lubachevsky-graham-1997-curved-hexagonal-packings-disks-circle` |

### Adaptive shrinking cell, and contact dynamics

| Source | File stem |
| --- | --- |
| Torquato & Jiao, *Dense packings of the Platonic and Archimedean solids*, Nature 460, 2009 | `torquato-jiao-2009-dense-packings-platonic-archimedean-solids` |
| Torquato & Jiao, *Dense packings of polyhedra: Platonic and Archimedean solids*, Phys. Rev. E 80, 2009 | `torquato-jiao-2009-dense-packings-polyhedra-platonic-archimedean` |
| Torquato & Jiao, *Robust algorithm to generate a diverse class of dense sphere packings via linear programming*, Phys. Rev. E 82, 2010 | `torquato-jiao-2010-robust-algorithm-sphere-packings-linear-programming` |
| Jiao, Stillinger & Torquato, *Optimal packings of superballs*, 2009 | `jiao-stillinger-torquato-2009-optimal-packings-superballs` |
| Atkinson, Jiao & Torquato, *Maximally dense packings of two-dimensional convex and concave noncircular particles*, 2012 | `atkinson-jiao-torquato-2012-maximally-dense-packings-2d-noncircular` |
| Maher, Stillinger & Torquato, *Kinetic frustration effects on dense two-dimensional packings of convex particles*, 2021 | `maher-stillinger-torquato-2021-kinetic-frustration-2d-convex-packings` |
| Fu, Steinhardt, Zhao, Socolar & Charbonneau, *Hard sphere packings within cylinders*, 2016 | `fu-steinhardt-zhao-socolar-charbonneau-2016-hard-sphere-packings-within-cylinders` |
| Fayen, Jagannathan & Foffi, *Infinite-pressure phase diagram of binary mixtures of hard disks*, 2020 | `fayen-jagannathan-foffi-2020-infinite-pressure-phase-diagram-binary-hard-disks` |
| Unger & Kertesz, *The contact dynamics method for granular media*, 2003 | `unger-kertesz-2003-contact-dynamics-method-granular-media` |
| Unger, Kertesz & Wolf, *Force indeterminacy in the jammed state of hard disks*, 2005 | `unger-kertesz-wolf-2005-force-indeterminacy-jammed-hard-disks` |
| Dubois, Acary & Jean, *The Contact Dynamics method: a nonsmooth story*, C. R. Mecanique 346, 2018 | `dubois-acary-jean-2018-contact-dynamics-method-nonsmooth-story` |
| Shaebani, Unger & Kertesz, *Generation of homogeneous granular packings: contact dynamics at constant pressure*, 2008 | `shaebani-unger-kertesz-2008-homogeneous-granular-packings-contact-dynamics-pressure-bath` |
| Shojaaee, Shaebani, Brendel, Torok & Wolf, *Parallel contact dynamics by adaptive hierarchical domain decomposition*, 2012 | `shojaaee-shaebani-brendel-torok-wolf-2012-parallel-contact-dynamics-domain-decomposition` |
| Olsen & Kamrin, *Resolving force indeterminacy in contact dynamics using compatibility conditions*, 2018 | `olsen-kamrin-2018-force-indeterminacy-contact-dynamics` |
| Preclik & Rude, *Ultrascale simulations of non-smooth granular dynamics*, 2015 | `preclik-rude-2015-ultrascale-simulations-nonsmooth-granular-dynamics` |
| Mazhar, Heyn & Pazouki et al., *Chrono: a parallel multi-physics library*, 2013 | `mazhar-heyn-pazouki-2013-chrono-parallel-multiphysics-library` |
| Azema, Estrada & Radjai, *Particle shape dependence in 2D granular media*, 2012 | `azema-estrada-radjai-2012-particle-shape-dependence-2d-granular` |
| Azema, Radjai & Saussine, *Quasistatic rheology of irregular polyhedral particles*, 2009 | `azema-radjai-saussine-2009-quasistatic-rheology-irregular-polyhedral-particles` |
| Moreau, *Some numerical methods in multibody dynamics: application to granular materials*, Eur. J. Mech. A/Solids 13, 1994; retrieved 2026-10-05 | `moreau-1994-numerical-methods-multibody-dynamics-granular-materials` |
| Jean, *The non-smooth contact dynamics method*, Comput. Methods Appl. Mech. Engrg. 177, 1999; retrieved 2026-10-05 | `jean-1999-non-smooth-contact-dynamics-method` |
| Radjai & Richefeu, *Contact dynamics as a nonsmooth discrete element method*, Mech. Mater. 41, 2009; retrieved 2026-10-05 | `radjai-richefeu-2009-contact-dynamics-nonsmooth-discrete-element-method` |
| Radjai, Jean, Moreau & Roux, *Force distributions in dense two-dimensional granular systems*, Phys. Rev. Lett. 77, 1996; retrieved 2026-10-05 | `radjai-jean-moreau-roux-1996-force-distributions-dense-2d-granular-systems` |

### Constraint projection, position-based dynamics and differentiable simulation

| Source | File stem |
| --- | --- |
| Gravel & Elser, *Divide and concur: a general approach to constraint satisfaction*, Phys. Rev. E 78, 2008 | `gravel-elser-2008-divide-and-concur` |
| Kallus, Elser & Gravel, *A method for dense packing discovery*, 2010 | `kallus-elser-gravel-2010-method-dense-packing-discovery` |
| Kallus, Elser & Gravel, *Dense periodic packings of tetrahedra with small repeating units*, 2010 | `kallus-elser-gravel-2010-dense-periodic-packings-tetrahedra` |
| Kallus, *Solving geometric puzzles with divide and concur*, Cornell thesis, 2011 | `kallus-2011-solving-geometric-puzzles-with-divide-and-concur` |
| Elser, *How densely can spheres be packed with moderate effort in high dimensions?*, 2023 | `elser-2023-how-densely-can-spheres-be-packed-moderate-effort` |
| Elser, *The complexity of bit retrieval*, 2016 | `elser-2016-complexity-of-bit-retrieval` |
| Elser, *Learning without loss*, 2019 | `elser-2019-learning-without-loss` |
| Lal, *The flow limit of reflect-reflect-relax*, 2025 | `lal-2025-flow-limit-reflect-reflect-relax` |
| Mueller, Heidelberger, Hennix & Ratcliff, *Position based dynamics*, 2007 | `muller-heidelberger-hennix-2007-position-based-dynamics` |
| Macklin, Mueller & Chentanez, *XPBD: position-based simulation of compliant constrained dynamics*, 2016 | `macklin-muller-chentanez-2016-xpbd` |
| Macklin, Storey, Lu et al., *Small steps in physics simulation*, 2019 | `macklin-storey-lu-2019-small-steps-physics-simulation` |
| Mueller, Macklin, Chentanez et al., *Detailed rigid body simulation with extended position based dynamics*, 2020 | `muller-macklin-chentanez-2020-detailed-rigid-body-xpbd` |
| Bender, Mueller & Macklin, *A survey on position based dynamics*, 2017 | `bender-muller-macklin-2017-survey-position-based-dynamics` |
| Stuyck & Chen, *DiffXPBD: differentiable position-based simulation of compliant constraint dynamics*, 2023 | `stuyck-chen-2023-diffxpbd` |
| Hu, Anderson, Li et al., *DiffTaichi: differentiable programming for physical simulation*, 2020 | `hu-anderson-li-2020-difftaichi` |
| Freeman, Frey, Raichuk et al., *Brax: a differentiable physics engine for large scale rigid body simulation*, 2021 | `freeman-frey-raichuk-2021-brax` |
| Werling, Omens, Lee et al., *Fast and feature-complete differentiable physics*, 2021 | `werling-omens-lee-2021-fast-feature-complete-differentiable-physics` |
| Howell, Le Cleac’h, Kolter et al., *Dojo: a differentiable physics engine for robotics*, 2022 | `howell-le-cleach-kolter-2022-dojo-differentiable-physics-engine` |
| Suh, Simchowitz, Zhang et al., *Do differentiable simulators give better policy gradients?*, ICML 2022 | `suh-simchowitz-zhang-2022-do-differentiable-simulators-give-better-policy-gradients` |
| Metz, Freeman, Schoenholz & Kachman, *Gradients are not all you need*, 2021 | `metz-freeman-schoenholz-2021-gradients-are-not-all-you-need` |
| Zhong, Han & Brikis, *Differentiable physics simulations with contacts: do they have correct gradients?*, 2022 | `zhong-han-brikis-2022-differentiable-physics-contacts-correct-gradients` |
| Antonova, Yang, Jatavallabhula et al., *Rethinking optimization with differentiable simulation*, 2022 | `antonova-yang-jatavallabhula-2022-rethinking-optimization-differentiable-simulation` |
| Gupta & Raman, *Differentiable packing of irregular 3D objects with adaptive container estimation*, 2026 | `gupta-raman-2026-differentiable-packing-irregular-3d-objects` |
| Wang & Lu, *Image-space collage and packing with differentiable rendering*, 2024 (screened) | `wang-lu-2024-image-space-collage-and-packing-differentiable-rendering` |
| Debnath, Tiwari, Sadekar & Raman, *RASP: shadow-guided packing*, 2025 (screened) | `debnath-tiwari-sadekar-2025-rasp-shadow-guided-packing` |
| Zhang, Lyu, Rudra et al., *Sequential object placement with convex decomposition*, 2026 (screened) | `zhang-lyu-rudra-2026-sequential-object-placement-convex-decomposition` |

### Smoothed penalties, continuation, and nonlinear-programming packing

| Source | File stem |
| --- | --- |
| Nurmela & Ostergard, *Packing up to 50 equal circles in a square*, DCG 18, 1997 | `nurmela-ostergard-1997-packing-up-to-50-equal-circles-in-a-square` |
| Nurmela & Ostergard, *More optimal packings of equal circles in a square*, DCG 22, 1999 | `nurmela-ostergard-1999-more-optimal-packings-of-equal-circles-in-a-square` |
| More & Wu, *Global continuation for distance geometry problems*, Argonne MCS-P505-0395, 1995 | `more-wu-1997-global-continuation-distance-geometry` |
| Birgin & Sobral, *Minimizing the object dimensions in circle and sphere packing problems*, 2008 | `birgin-sobral-2008-minimizing-object-dimensions-circle-sphere-packing` |
| Birgin & Gentil, *New and improved results for packing identical unitary radius circles*, 2010 | `birgin-gentil-2010-packing-unitary-radius-circles-triangles-rectangles-strips` |
| Birgin, Martinez & Nishihara, *Orthogonal packing of rectangular items within arbitrary convex regions*, 2006 | `birgin-martinez-nishihara-2006-orthogonal-packing-arbitrary-convex-regions` |
| Birgin, *Applications of nonlinear programming to packing problems*, 2016 | `birgin-2016-applications-nonlinear-programming-packing` |
| Romanova, Bennell, Stoyan & Pankratov, *Packing of concave polyhedra with continuous rotations*, EJOR, 2018 | `romanova-bennell-stoyan-2018-packing-concave-polyhedra-continuous-rotations` |
| Peralta, Andretta & Oliveira, *Solving irregular strip packing problems with free rotations using separation lines*, 2018 | `peralta-andretta-oliveira-2018-irregular-strip-packing-free-rotations-separation-lines` |
| Yaskov & Chugay, *Packing equal spheres by block coordinate descent*, 2020 | `yaskov-chugay-2020-packing-equal-spheres-block-coordinate-descent` |
| Lopez & Beasley, *Packing unequal rectangles and squares using formulation space search*, 2018 | `lopez-beasley-2018-packing-unequal-rectangles-squares-formulation-space-search` |
| He, Ye & Wang, *An efficient quasi-physical quasi-human algorithm for packing equal circles in a circular container*, 2018 | `he-ye-wang-2018-quasi-physical-quasi-human-equal-circles` |
| Zhou, He & Zheng, *Geometric batch optimization for packing equal circles*, 2023 | `zhou-he-zheng-2023-geometric-batch-optimization-equal-circles` |
| Hansmann & Wille, *Global optimization by energy landscape paving*, 2002 | `hansmann-wille-2002-global-optimization-energy-landscape-paving` |

## Web Sources

The
[September 22 external certificate packet](web/external-square-certificates-2026-09-22/README.md)
retains complete pinned Tokoharu, Kleddamag, wand125 and Guzhou source trees, the
supplied social threads, executable replay receipts and independent audit controls.
Its Frontier keys are **[Tokoharu density 2026]**, **[Kleddamag n11 2026]** and
**[wand125 point bounds 2026]**. The
[integration review](../../docs/project/reviews/review-2026-09-22-external-square-certificates-integration.md)
distinguishes literal reported bounds, verified replays and proposed native extensions.

The [Wang–Li packet](web/wang-li-n11-2026-09-29/README.md) retains Ke Wang and Can Li’s
Zenodo record 23038546: Kleddamag’s `s(11)` certificate reweighted and scaled to
`s(11) > 3875000000/999999999`, its two verifiers, the preprint, and this repository’s
full replays, native coverage and controls, under **[Wang Li n11 2026]**, T-061.

The
[September 27 wand125 rectangle packet](web/wand125-rectangle-certificates-2026-09-27/README.md)
pins wand125’s later rectangle-density certificates for 44 counts from `n = 18` to
`n = 78`, built with Tokoharu’s solver and decided by Tokoharu’s interval verifier,
under **[wand125 rectangle bounds 2026]**. It retains each standing certificate’s exact
candidate and upstream run record, digests every other file of the source tree, and
keeps the first-party preflight and coverage-replay receipts.

The [September 28 wand125 update](web/wand125-x-update-2026-09-28/README.md), under
**[wand125 X update 2026-09-28]**, keeps three messages wand125 sent the owner on X, two
on 28 September and one on 29 September, and a byte capture of the `n ≤ 100` lower-bound
table the first two link.
They report evand’s `s(21) = 5` and `s(45) = 7`, rectangle-density bounds to `n = 95`
and `s(50) ≥ 37/5`, none of it acquired here when they arrived; the packet maps each
claim to the record and to the bead that owns its intake, and each has since been
retained in its own packet.
The third announces `wand125/square-packing-tools`, the tools behind those certificates.

Four packets of 28 September retain those results:
[wand125’s 50 standing rectangle certificates at `39d8ecc`](web/wand125-rectangle-certificates-2026-09-28/README.md),
[its point-only and mixed certificates](web/wand125-point-and-mixed-2026-09-28/README.md)
for `s(21)`, `s(45)` and `s(50)`,
[Evan Daniel’s mixed covers](web/evand-square-packing-2026-09-28/README.md) for
`s(21) = 5` and `s(45) = 7`, and
[Guzhou0806’s R067 and R068](web/n17-guzhou-r068-2026-09-28/README.md) at `n = 17`.

Three packets of 29 September retain parallel upper bounds:
[Francisco Couzo’s 49 packings](web/franciscouzo-square-packing-2026-09-27/README.md)
for `n = 68…307`, which issue #227 asked this project to register,
[Joost de Winter’s `s(211) < 15`](web/de-winter-square-packing-211-2026-09-16/README.md),
and [Griffin Casson’s 39 packings](web/casson-square-packing-2026-09-23/README.md) for
`n = 103…307`, each of which Couzo’s beats.
The first two publish no licence, and their packets take the derived-only form of the
[known-best retention policy](web/known-best-packings/README.md), keeping derived facts
and metadata only; Casson’s packings are CC BY 4.0 and retained byte for byte.
Every Couzo and de Winter packing is certified here by an exact rational replay whose
certificates are under `packing/witnesses/`. A fourth, of 5 October,
[retains the seven packings Couzo lowered on 3 October](web/franciscouzo-square-packing-2026-10-03/README.md),
at `n = 208, 209, 228, 263, 272, 303` and `306`, and certifies them the same two ways
(T-092).

### Recent External GitHub Repositories

The repository links below are the moving discovery points for current work.
A branch head is not evidence for a registered claim: each claim, replay and review
cites an immutable tag or full commit and a retained packet under `web/`. When an
upstream branch moves, a dated intake may add a new pin; the older packet and citation
key remain bound to the bytes they originally named.

| Repository | Role in this record | Pinned record |
| --- | --- | --- |
| [Queuingtheorydotcom/11SquaresOptimal](https://github.com/Queuingtheorydotcom/11SquaresOptimal) | **Priority proof review:** claimed global optimality of Trump’s eleven-square packing; distinct from the `s(11) > 31/8` bound and wand125 row checks | **[Queuingtheorydotcom n11 optimality 2026]**, T-060; [29 September intake](web/n11-optimality-2026-09-29/README.md); pinned `f9e0de713a0949d1bc6a0fa6b59d96edf6c3d65c`; [GPT-6 Pro’s review evidence of 3 October](web/n11-optimality-gpt6-pro-review-2026-10-03/README.md) |
| [Queuingtheorydotcom/11SquaresFormalized](https://github.com/Queuingtheorydotcom/11SquaresFormalized) | The Lean 4 formalization of `T-060`’s proof, `ElevenSquare.optimality`, announced on 6 October 2026: the source reports a full verification run and axiom audit, private and resumed from earlier receipts, trusting Lean’s compiler for 13,308 `native_decide` axioms | **[Queuingtheorydotcom 11SquaresFormalized 2026]**, T-060; [6 October packet](web/queuingtheorydotcom-n11-lean-2026-10-06/README.md), pinned `cdc746ed907d258057c283aeb6d077cb2c27e349`; [statement audit](../../docs/project/reviews/review-2026-10-06-n11-lean-formalization-statement-audit.md) |
| [wand125/square-packing-tools](https://github.com/wand125/square-packing-tools) | MIT-licensed drivers for moving rectangle-density certificates in `n` and `L`, performance variants around Tokoharu’s solver, and the exact `general_pose_tree` checker | **[wand125 tools 2026]**; [29 September packet](web/wand125-tools-2026-09-29/README.md) |
| [wand125/square-packing-bounds](https://github.com/wand125/square-packing-bounds) | Point, rectangle-density and mixed certificate releases | **[wand125 point bounds 2026]**, **[wand125 rectangle bounds 2026-09-28]**, **[wand125 point and mixed bounds 2026-09-28]**, **[wand125 rectangle bounds 2026-10-01]**, **[wand125 exact covers 2026-10-01]**, **[wand125 mixed bounds 2026-10-01]**, **[wand125 mixed bounds 2026-10-02]**, **[wand125 mixed bounds n76 2026-10-02]**, **[wand125 point n61 2026-09-30]**, **[wand125 linear certificates 2026-10-02]**, **[wand125 mixed bounds afternoon 2026-10-02]**, **[wand125 linear n82 2026-10-02]**, **[wand125 rectangle bounds 2026-10-02]**, **[wand125 mixed bounds 2026-10-03]**, **[wand125 mixed bounds 2026-10-04]**, **[wand125 mixed bounds evening 2026-10-04]**, **[wand125 record updates 2026-10-04]**, **[wand125 mixed bounds 2026-10-05]**, **[wand125 mixed bounds finer net 2026-10-05]** and **[wand125 mixed bounds finer net 2026-10-06]** |
| [wand125/valid7-independent-check](https://github.com/wand125/valid7-independent-check) | A separately written exact-rational checker of Daniel’s Valid7, the finite premise of `s(k² − 3) = k`, and from 6 October of his ValidTilt9, the finite premise of `s(k² − 4) = k` | **[wand125 valid7 independent check 2026-10-02]**, **[wand125 valid7 independent check 2026-10-03]** and **[wand125 valid7 independent check 2026-10-06]**; [2 October packet](web/wand125-valid7-independent-check-2026-10-02/README.md), [3 October packet](web/wand125-valid7-independent-check-2026-10-03/README.md), [6 October packet](web/wand125-valid7-independent-check-2026-10-06/README.md) |
| [tokoharu/square-packing-density-bounds](https://github.com/tokoharu/square-packing-density-bounds) | Rectangle-density solver and the interval verifier used to accept its certificates | **[Tokoharu density 2026]**; [22 September packet](web/external-square-certificates-2026-09-22/README.md) |
| [evand/square-packing](https://github.com/evand/square-packing) | Weighted point, segment and area covers, exact and interval verifiers, and Lean reductions | **[evand square-packing 2026-10-01]**, **[evand square-packing 2026-10-02]**, **[evand square-packing 2026-10-03]**, **[evand square-packing 2026-10-04]**, **[evand exact optima 2026-10-05]** and, for its site, **[evand square packing atlas 2026-10-04]**; [1 October selective packet](web/evand-square-packing-2026-10-01/README.md), [2 October selective packet](web/evand-square-packing-2026-10-02/README.md), [3 October `k2m4` packet](web/evand-square-packing-2026-10-03/README.md), [4 October site packet](web/evand-square-packing-2026-10-04/README.md), [5 October exact-optima packet](web/evand-square-packing-2026-10-05/README.md), [the `zmx2` source of its `s(32)` run without the D4 fold](web/evand-zmx2-sym-atoms-2026-09-30/README.md), [source audit](../../docs/project/reviews/review-2026-10-01-evand-source-coverage.md) [mathematical review](../../docs/project/reviews/review-2026-10-01-evand-mathematical-transfer.md) and [site review](../../docs/project/reviews/review-2026-10-05-evand-square-packing-atlas.md) |
| [squarepacker/s12-lower-bound](https://github.com/squarepacker/s12-lower-bound) | Ryu Sungjoon’s `s(12) ≥ 31360/7901` (v1.0): Evan Daniel’s `s(12)` certificate with every coordinate and the side multiplied by `7902/7901`, Daniel’s verifier and the author’s own checker at the angle net `N = 24000`, archived as Zenodo [10.5281/zenodo.23106582](https://doi.org/10.5281/zenodo.23106582) and reported on jlevy/squares#309; and his `s(12) ≥ 7943/2000` (v1.1): Daniel’s points dilated and re-weighted, checked by both at `N = 96000`, with a write-up, archived as Zenodo [10.5281/zenodo.23157015](https://doi.org/10.5281/zenodo.23157015) and reported on jlevy/squares#363 | **[squarepacker s12 2026]**; [2 October packet](web/squarepacker-s12-lower-bound-2026-10-02/README.md), pinned `8c53049025b94bb589ed25a90203f0a34c2945e4`, with the replays and controls here; **[squarepacker s12 2026-10-05]**; [5 October packet](web/squarepacker-s12-lower-bound-2026-10-05/README.md), pinned `7a96bec36bc6811c3715ef581598f22ff9b7ba3a` |
| [squarepacker/k2-minus-c](https://github.com/squarepacker/k2-minus-c) | Sungjoon Ryu’s preprint `k² − M(k) ≥ 0.033 log k` for closed packings of `[0,k]²`, so `s(k² − c) = k` for every fixed `c` and all large `k`, with the ball-arithmetic certificate of its Lemma 4.10; archived as Zenodo [10.5281/zenodo.23165736](https://doi.org/10.5281/zenodo.23165736), reported on jlevy/squares#368 | **[squarepacker k2-minus-c 2026]**; [5 October packet](web/squarepacker-k2-minus-c-2026-10-05/README.md), pinned `25f645e8fcadb3c2768f4da42d80e977fb1a508d`, with the replay here and the three Zenodo records, the `v1.0` preprint PDF among them |
| [squarepacker/k2-minus-c v1.2](https://github.com/squarepacker/k2-minus-c/tree/e16a5cfa7eed489ea8d84b500e590bf6855a5f2f) | Ryu’s revised closed-packing deficiency constants; issue #368, DOI 10.5281/zenodo.23194031 | **[squarepacker k2-minus-c v1.2 2026]**; [version 1.2 packet](web/squarepacker-k2-minus-c-v12-2026-10-06/README.md), all 78 source files bound; arithmetic reviewed, independent labelling remains open |
| [squarepacker/k2-minus-c-quarter](https://github.com/squarepacker/k2-minus-c-quarter) | Ryu’s reported quarter-power deficiency theorem, with its separate analytic variant; issue #414, DOI 10.5281/zenodo.23211207 | **[squarepacker quarter-power 2026]**; [7 October packet](web/squarepacker-k2-minus-c-quarter-2026-10-07/README.md), pinned `abbedcf4bba2e4053f0278e669d84966a89c8b73`; scoped proof review and conditional interval arithmetic retained; independent box labelling remains open |
| [squarepacker/k2-minus-c-cube-root](https://github.com/squarepacker/k2-minus-c-cube-root) | Ryu’s reported cube-root deficiency theorem and intermediate square-root regimes; issue #414, DOI 10.5281/zenodo.23212059 | **[squarepacker cube-root 2026]**; [7 October packet](web/squarepacker-k2-minus-c-cube-root-2026-10-07/README.md), pinned `15045f9c6b74bd52f60394b9be593ebe4fb3debc`; scoped proof review and conditional interval arithmetic retained; independent box labelling remains open |
| [Kleddamag/11-squares-certified-bound](https://github.com/Kleddamag/11-squares-certified-bound) | The `s(11) > 31/8` certificate and its two source checkers | **[Kleddamag n11 2026]**; [retained source](web/external-square-certificates-2026-09-22/kleddamag-11/README.md) |
| [Kleddamag/17-squares-certified-bound](https://github.com/Kleddamag/17-squares-certified-bound) | The `n = 17` mixed-charge certificate line through `466001/100000` | **[Kleddamag n17 4.66001]**; [27 September packet](web/n17-kleddamag-466001-2026-09-27/README.md) |
| [Guzhou0806/n17-square-packing](https://github.com/Guzhou0806/n17-square-packing) | Parent-angle and mixed-charge certificates for `n = 17`, including R068 and R071 | **[Guzhou0806 n17 R068]**; [28 September packet](web/n17-guzhou-r068-2026-09-28/README.md); **[Guzhou0806 n17 R071]**; [30 September packet](web/n17-guzhou-r071-2026-09-30/README.md), pinned `8c11f6962506940c5de67a9fa73b3d1e2e151196` |
| [Guzhou0806/n40-square-packing](https://github.com/Guzhou0806/n40-square-packing) | The clipped-corner transfer `s(40) > 335427/50000` on wand125’s `rect_n40_L67` density, with its 401-direction nodal run and exact finite checks | **[Guzhou0806 n40 clipped corner 2026-10-10]**; [10 October packet](web/guzhou-n40-clipped-corner-2026-10-10/README.md), pinned `e5abeb4d078a5c5b35df6204dd9b93378e5a7880` |
| [Mira-acc/17squares](https://github.com/Mira-acc/17squares) | Exact point and weighted certificates used in the `n = 17` lineage | **[n17 weighted certificates 2026-09-20]**; [20 September packet](web/n17-weighted-certificates-2026-09-20/README.md) |
| [sam-bee/squarl](https://github.com/sam-bee/squarl) | Search-pipeline documentation and exact-rational lower-bound sources | **[Squarl n17 2026]**; [retained source](web/squarl-n17-2026/README.md) |

Since 22 August 2026 the archive has retained every public certificate that moved a
lower bound here. Some build on this project’s certificates or pipeline (Kleddamag,
Guzhou0806, Mira, wand125) or credit it second-hand (Tokoharu, and wand125’s point-only
and mixed certificates); others are independent of it (Evan Daniel, on Burns’s and
Massaccesi’s method).
Each key’s `credit` in [`bibliography.yaml`](bibliography.yaml) names the authors and
the work they build on, “after Levy” where the source credits this project, and its
`lineage` records how the source stands to this project, as the source says; the policy
is [epistemics.md → Results by Others](../../epistemics.md#results-by-others).

| Key | What | Source | File stem (in `web/`) |
| --- | --- | --- | --- |
| **[Friedman Center]** | Packing Center record tables and diagrams | erich-friedman.github.io | `friedman-packing-center-squares` |
| **[Guzhou R038 2026]** | The pinned R038 parent-angle certificate and verifier used in the external n17 comparison | github.com/Guzhou0806/N17 | `external-square-certificates-2026-09-22/dependencies/guzhou-n17-full/certificates/R038/` |
| **[Friedman DS7 html]** | 2009 HTML edition of the DS7 survey | combinatorics.org | `friedman-ds7-survey-2009-html` |
| **[Kingbird]** | Squares-in-Squares catalogue: exact minimal polynomials, rigidity flags; captured 2026-09-30 (page dated 2026-09-24). The capture of 2026-08-22 that the UnitSquare and certified-packet intakes read is kept byte for byte under `kingbird-squares-in-squares-2026-08-22`, whose header still names the undated files it was archived as; `devtools.diff_kingbird_catalogue` compares the two count by count. Read again on 2026-10-05 by `devtools.capture_kingbird_catalogue`, with the same bytes and the same `Last-Modified`, so the retained capture stands; the pictures behind the 98 retained Kingbird witnesses were read again the same day ([receipt](web/known-best-packings/receipts/kingbird-2026-10-05-pictures.json)) | kingbird.myphotos.cc | `kingbird-squares-in-squares` |
| **[Kingbird-compared]** | Supersession history: which record fell to which method, when, `n ≤ 100`; retrieved 2026-10-05 (page dated 2026-09-24), with the capture of 2026-08-22 kept beside it | kingbird.myphotos.cc | `kingbird-squares-in-squares-compared`, `kingbird-squares-in-squares-compared-2026-08-22` |
| **[Kingbird-rigid]** | Author-maintained rigid-packing classification | kingbird.myphotos.cc | `kingbird-squares-in-squares-rigid` |
| **[Kingbird-Göbel-squares]** | The Göbel-square family in closed form, `n = 2(a+1)a + b²` at side `a + 1 + (b/2)√2`, with its rendered members: 32 picture panels over 18 distinct `n`, from 5 to 9465; retrieved 2026-09-07 | kingbird.myphotos.cc | `kingbird-squares-in-squares-gobel-squares` |
| **[Kingbird-Göbel-strips]** | The Göbel-strip family in closed form, `n = (a+1)a + 2 + b` with `b = 1 + ⌊(a−1)√2⌋`, at side `a + 1 + (1/2)√2`, with its rendered members: 152 picture panels over 58 distinct `n`, from 5 to 2135; retrieved 2026-09-07 | kingbird.myphotos.cc | `kingbird-squares-in-squares-gobel-strips` |
| **[Kingbird analytic minimization]** | Author notes on stationary equations for underdetermined packing systems | kingbird.myphotos.cc | `kingbird-squares-in-squares-analytic-minimization` |
| **[Kingbird run statistics]** | First-party simulated-annealing basin frequencies and setup-specific search costs for `n = 51, 55` | kingbird.myphotos.cc | `kingbird-run-statistics-2026/` |
| **[Kingbird-triangular-table]** | The catalogue’s triangular table view of the same best known packings; retrieved 2026-10-02 (page dated 2026-09-24) | kingbird.myphotos.cc | `kingbird-squares-in-squares-triangular-table` |
| **[Kingbird-n²-n-1]** | DeVincentis’s 2014 `s(n² − n − 1)` pattern beside the packings that beat it; the page reports that Schadt’s annealing has shown the pattern not optimal for every `n > 3`; retrieved 2026-10-02 (page dated 2026-09-09) | kingbird.myphotos.cc | `kingbird-squares-in-squares-n2-n-1` |
| **[Kingbird-compared2]** | Older and alternative packings, `n = 101…196`, continuing **[Kingbird-compared]**; retrieved 2026-10-02 (page dated 2026-09-20) | kingbird.myphotos.cc | `kingbird-squares-in-squares-compared2` |
| **[Kingbird-compared3]** | Older and alternative packings, `n ≥ 197`; retrieved 2026-10-02 (page dated 2026-09-24) | kingbird.myphotos.cc | `kingbird-squares-in-squares-compared3` |
| **[Ellsworth DS7 edit]** | David Ellsworth’s edited copy of Friedman’s DS7 survey, linked from the catalogue as “David Ellsworth’s edit”; retrieved 2026-10-02 (page dated 2024-12-19); not compared with **[Friedman DS7 html]** | kingbird.myphotos.cc | `kingbird-squares-ellsworth-ds7-edit` |
| **[UnitSquare 2026]** | Results Release 1: six reported construction-only improvements and its public structured record | hmbelvedere.com | `unitsquare-release1-2026/` |
| **[Burns–Massaccesi n17]** | Exact-rational weighted lower-bound sources at 4.4811 and 4.5058, their public verifiers, and a distinct near-record topology; retained as method provenance and controls after later project bounds | sam-burns.com; gus-massa.blogspot.com | `n17-lower-bounds-2026/` |
| **[Brandwijk n17 capsule]** | Exact 16-point certificate capsule for `s(17) > 89/20`, offline checker, metadata, local audit, and later supersession context | zenodo.org | `literature-refresh-2026-09-05/` |
| **[Burns n17 addendum 2026-09-07]** | The rest of Burns’s series: the introduction post, the near-record arrangement’s coordinates file and five figures, the two post images, a replay receipt for the retained `4.4811` verifier, and a Squarl repository pointer; extends `[Burns–Massaccesi n17]` without editing its frozen README | sam-burns.com; github.com/sam-bee/squarl | `burns-n17-series-addendum-2026-09-07/` |
| **[GitHub n17 certificates 2026]** | Three August 2026 GitHub certificate repositories for `s(17)` found outside the indexed corpus: Mira’s exact 16-point pose-space certificates (`4.450837`, then `4.468292` with triangle-piercing leaves), Fort’s `4.456575` on the same architecture, and anabologyco-maker’s weighted-measure candidate `9141/2000 = 4.5705` with an exact orientation partition and a Lean layer; retained with their checkers, replay scripts and receipts | github.com | `n17-github-certificates-2026/` |
| **[n17 weighted certificates 2026-09-20]** | Two September 2026 GitHub repositories claiming weighted lower bounds on `s(17)` above this repository’s verified `459/100`, both descended from `T-019`: Mira’s 1620-atom certificate for `s(17) > 4.613028635886`, published hours after the 7 September check that produced `[GitHub n17 certificates 2026]`, and Guzhou0806’s R012 parent-angle catalogue for `s(17) >= 461300/99999` over Mira’s measure, with its earlier 197-direction M19 milestone; retained with their checkers, first-party replay instruments and receipts | github.com | `n17-weighted-certificates-2026-09-20/` |
| **[Kleddamag n17 certified bound]** | Kleddamag’s `v1.0.0` release claiming `s(17) > 461300/99853 = 4.61979109…` by a weighted-covering certificate with two-of-three threshold atoms over 7,853 exact angle intervals; the full release tree byte-identical with its `NOTICES/` and `LICENSE`, plus the pinned R038 checker input and its reconstruction so a replay needs no network. Replayed here in 16 min 41 s to a byte-identical `RESULT.json`; reviewed at `V4`/`C3` with `C4` blocked on method independence, and no bound moved | github.com/Kleddamag | `n17-kleddamag-certified-bound-2026-09-21/` |
| **[Guzhou0806 n17 R052]** | Guzhou0806 / N17 project’s R052 release of 2026-09-25 claiming `s(17) > 231001/50000 = 4.62002` on Kleddamag’s mixed point/threshold parent-core architecture, with 2,354 point, 514 two-of-three and 54 three-of-five orbits over 15,721 angle intervals and a counting surplus of 2 units of `10⁻¹²`; 31 files byte-identical at `3bf1095c`, the publication records of the superseded R042 (**[Guzhou0806 n17 R042]**, `115325/24963`), R043 (**[Guzhou0806 n17 R043]**, `461300/99851`) and R050 (**[Guzhou0806 n17 R050]**, `4613000/998509`), none of them replayed, and receipts for four passing source replays and the native route’s coverage refusal. Verified at `V4`/`C3`; `C4` needs a method-distinct coverage decision | github.com/Guzhou0806 | `n17-guzhou-r052-2026-09-25/` |
| **[Kleddamag n17 4.640020]** | Kleddamag, building on Squares Project (Joshua Levy), Mira and Guzhou0806: the `v1.1.0` release of 2026-09-26 claiming `s(17) > 232001/50000 = 4.640020` by a weighted-covering certificate over 2,048 exact angle intervals whose 546 charge orbits add weighted thresholds and pairwise-intersecting winning-subset rules to point and `k`-of-`m` threshold charges, with a counting surplus of 5,629 units of `10⁻⁹`; the 37 files that changed or were added since `v1.0.0`, byte-identical at `13821ddf`, the other 74 being those already retained in **[Kleddamag n17 certified bound]**, plus receipts for the full two-checker replay (36 min 44 s here, every interval ledger identical to the source’s), the integrity check and the controls. Verified at `V4`/`C3`; `C4` needs a method-distinct coverage decision that can read the new feature kinds. Superseded on 2026-09-27 by **[Kleddamag n17 4.66001]** and kept as the previous verified bound | github.com/Kleddamag | `n17-kleddamag-4640020-2026-09-26/` |
| **[Kleddamag n17 4.66001]** | Kleddamag, building on Squares Project (Joshua Levy), Mira and Guzhou0806: an exact weighted-certificate proof over 2,168 orientation intervals that `s(17) > 466001/100000 = 4.66001`, published on 2026-09-27 at the untagged commit `57519bb7` as `bounds/4.66001/` beside `v1.1.0`, whose two checkers it keeps byte for byte. Its 889 charge orbits, every rule of capacity one, combine two completed charge candidates, and eight of an original 2,048 intervals are split sixteen ways; counting surplus 54,340 units of `10⁻⁹`. The 33 files that changed or were added since `v1.1.0`, byte-identical, the other 103 being those already retained in **[Kleddamag n17 4.640020]** and **[Kleddamag n17 certified bound]**, plus receipts for the full two-checker replay (36 min 44 s here on one worker per checker, every interval ledger identical to the source’s), the integrity check and the controls. Verified at `V4`/`C3`; `C4` needs a method-distinct coverage decision that can read its feature kinds. Superseded on 2026-09-29 by **[Guzhou0806 n17 R068]** and kept as the previous verified bound | github.com/Kleddamag | `n17-kleddamag-466001-2026-09-27/` |
| **[Guzhou0806 n17 R068]** | Guzhou0806 / N17 project’s R068 release of 28 September 2026 at `815b1626`, continuing Kleddamag’s public `4.66001` charge (Kleddamag building on Squares Project (Joshua Levy), Mira and Guzhou0806) and disclosing AI assistance: `s(17) > 116511/25000 = 4.66044` from that charge’s 889 rule orbits unchanged, one zero-weight site orbit moved and one weighted four-site point orbit added, over 4,991 angle intervals, counting surplus 7,404 units of `10⁻⁹`; its publisher ran no local validation and did not observe CI. The same day’s **[Guzhou0806 n17 R067]**, `233009/50000 = 4.66018` on the unchanged charge over 2,808 intervals, is retained beside it. The 93 files that changed or were added since `6f64e4b2`, byte-identical, plus complete paired replays of both here, Guzhou0806’s own C++ checker and Kleddamag’s Node BigInt checker agreeing with the published ledgers on every row (0 of 4 × 4,991 and 4 × 2,808 differing), and a structural comparison with `4.66001`. One event-cell method, so `V4`/`C3` | github.com/Guzhou0806 | `n17-guzhou-r068-2026-09-28/` |
| **[Guzhou0806 n17 R071]** | Guzhou0806 / N17 project’s R071 release of 30 September 2026 at `8c11f696`, keeping unchanged R068’s continuation of Kleddamag’s public `4.66001` charge (Kleddamag building on Squares Project (Joshua Levy), Mira and Guzhou0806) and disclosing AI assistance: `s(17) > 18641771/4000000 = 4.66044275`, `11/4000000` above R068, from that charge at parent side `18452000/18641771` over 5,114 angle intervals, counting surplus 7,404 units of `10⁻⁹`. Its partition records are missing and a completion summary is retained; the source’s own CI replay passed and its publisher did not observe it. The previous day’s **[Guzhou0806 n17 R070]**, `46604427/10000000 = 4.6604427` over 5,107 intervals with complete four-partition ledgers, is retained beside it, with both releases’ research material that carries no bound: R070’s same-budget overlay and fixed-class obstruction and R071’s conditional joint geometry at `9321/2000`. The 45 retained of the 186 files the two commits changed or added since `815b1626`, byte-identical, the other 141 pinned by digest: 32 byte-identical to the R068 packet’s checker and notices, and 109 research files that carry no bound and that neither bound, the replay nor the audit reads; the CI run records; a pre-replay audit against R068; and the complete paired replay of R071 here on 5 October 2026, Guzhou0806’s C++ checker and Kleddamag’s Node BigInt checker agreeing on every row (0 of 4 × 5,114 differing), with two mutated certificates both checkers refuse. One event-cell method, so `V3`/`C3` | github.com/Guzhou0806 | `n17-guzhou-r071-2026-09-30/` |
| **[Guzhou0806 n40 clipped corner 2026-10-10]** | Guzhou0806’s release `n40-670854-20261010` of 10 October 2026 at `e5abeb4d`, reported on jlevy/squares#485 with AI assistance disclosed: `s(40) > 335427/50000 = 6.70854`, `427/50000` above `T-068`’s `67/10` on the same density, wand125’s `rect_n40_L67`, unchanged and pinned by digest. Every side-`9977/10000` square at each of 401 half-angle tangents of step `83/80000` captures at least `10001/10000` of the density, and a continuous-angle transfer with a clipped-corner loss bound and the density’s essential supremum carries that to every unit square; the weaker full-core bound `s(40) > 67000√6400006889/798988091` needs no peak. Twenty files retained, the density and the vendored copy of this repository’s `sqverify_fast` pinned by digest; the release ZIP’s CI receipt kept beside the tree’s local one. Replayed here on 10 October 2026: the nodal statement by `sqverify-fast` at all 401 directions, the producer’s own nodal code, and the finite steps by a first-party exact audit that shares no code with the release’s, with controls A to H; the mathematics reviewed the same day with no blocking defect | github.com/Guzhou0806 | `guzhou-n40-clipped-corner-2026-10-10/` |
| **[wand125 rectangle bounds 2026-09-28]** | wand125’s rectangle-density certificates at `39d8ecc` (28 September 2026), built with Tokoharu’s solver and decided by his unchanged interval verifier: 50 standing certificates from `n = 18` to `95`, 32 raised and six new (`n = 86, 88, 89, 91, 94, 95`) since the September 27 packet, whose 12 unchanged certificates and licence it reads rather than copies; the exact first-party preflight of all 50 passes, and coverage replays are recorded in each packet’s receipts as they complete | github.com/wand125 | `wand125-rectangle-certificates-2026-09-28/` |
| **[wand125 point and mixed bounds 2026-09-28]** | wand125’s three non-rectangle certificate families at `39d8ecc` (28 September 2026): a point-only `s(45) = 7` (12,645 `D4`-invariant points, total `12666371418707823/2^48`) decided by Evan Daniel’s unmodified `zmx2`; a point-only `s(21) = 5` on Daniel’s support (4,604 weights, threshold `249987/250000`, gap `999979/125000000000`) decided by the source’s rational replay, with a Lean 4 reduction of all but the capture step; and `s(50) ≥ 37/5` from 553 rectangle orbits, checked by a research copy of Tokoharu’s `verify.cpp` at threshold one, with the superseded `147/20` and `3659/500`. No priority claimed for `s(21)` or `s(45)`. 64 files byte-identical, MIT; the 464 MB `s(21)` bundle and the three `n = 50` tarballs pinned by SHA-256. The exact audit passes; `zmx2` re-certifies `s(45)` here with the source’s box count and depth, recorded at `V4`/`C3` as a second certificate beside Daniel’s mixed cover; the complete `s(21)` and `n = 50` replays ran here on 29 September and are in the packet’s receipts, which verifies `s(50) ≥ 37/5` (and `s(51) ≥ 37/5` by its mass) and gives `s(21) = 5` a second, point-only route | github.com/wand125 | `wand125-point-and-mixed-2026-09-28/` |
| **[wand125 rectangle bounds 2026-10-01]** | wand125’s rectangle-density certificates at `1a25a5ed` (1 October 2026), built with Tokoharu’s solver and decided by his unchanged interval verifier: the standing certificates raised or added since the September 28 packet, 34 of them requested for registration in jlevy/squares#281, with the standing certificates at `n = 59, 77, 78` that the request leaves out for exact values. The packet reads the unchanged certificates from the earlier packets; the exact first-party preflight passes, and no coverage replay of the new certificates has run | github.com/wand125 | `wand125-rectangle-certificates-2026-10-01/` |
| **[wand125 exact covers 2026-10-01]** | wand125’s mixed covers at `1a25a5ed` for `s(59) = 8` (26,308 points and 5,240 segments, total `1474762899/25000000`) and `s(77) = 9` (28,273 points and 6,420 segments, total `43347137744028965/2^49`), in Evan Daniel’s format, built from his `s(60) = 8` cover and reported accepted by his `zmx2` and `zm_mixed.py` pinned at evand/square-packing `b91d70b6`; requested in jlevy/squares#280 and #279. The `zmx2` sweeps of both covers were replayed here on 2 October 2026, which verifies `s(59) = 8` and `s(77) = s(78) = 9`. The directories’ checksum files list run logs that are not published, and the `s(59)` exact-rational evidence is two runs whose joint coverage the published files do not decide | github.com/wand125 | `wand125-point-and-mixed-2026-10-01/` |
| **[wand125 mixed bounds 2026-10-01]** | wand125’s mixed rectangle-measure certificates at `1a25a5ed` for `s(37) ≥ 161/25`, `s(65) ≥ 167/20`, `s(66) ≥ 421/50`, `s(90) ≥ 48/5` and `s(92) ≥ 969/100`: rectangle densities of mass `n − 1/100000` checked at coverage one by the research copy of Tokoharu’s `verify.cpp` that the `n = 50` certificate uses; requested in jlevy/squares#282. The complete replay of each here on 2 October 2026 matched the shipped run at all 201 directions, which verifies all five; the proof-bundle tarballs are pinned by SHA-256 and not retained | github.com/wand125 | `wand125-point-and-mixed-2026-10-01/` |
| **[wand125 mixed bounds 2026-10-02]** | wand125’s mixed rectangle-measure certificates at `52af997` (2 October 2026) for `s(84) ≥ 47/5` and `s(85) ≥ 471/50`, of the kind and checker of **[wand125 mixed bounds 2026-10-01]** and each above Green’s reported value at its count; requested in a comment on jlevy/squares#282. The complete replay of each here on 2 October 2026 matched the shipped run at all 201 directions, which verifies both, and `s(86)`, `s(87) ≥ 471/50` by the mass of the second; the proof-bundle tarballs are pinned by SHA-256 and not retained | github.com/wand125 | `wand125-mixed-bounds-2026-10-02/` |
| **[wand125 mixed bounds n76 2026-10-02]** | wand125’s mixed rectangle-measure certificate at `7975030` (2 October 2026) for `s(76) ≥ 447/50`, of the kind and checker of **[wand125 mixed bounds 2026-10-02]** and above the source’s rectangle certificate `357/40`; requested in a comment on jlevy/squares#282. Its complete replay here on 2 October 2026 matched the shipped run at all 201 directions, which verifies `s(76) ≥ 447/50`; the proof-bundle tarball is pinned by SHA-256 and not retained | github.com/wand125 | `wand125-mixed-bounds-n76-2026-10-02/` |
| **[wand125 point n61 2026-09-30]** | wand125’s point-only cover at `f8846cec` (30 September 2026) for `s(61) = 8`: 15,193 `D4`-invariant points, total `8584985072679551 / 2^47`, whose capture condition the source checks with Daniel’s `zmx2`; requested in a comment on jlevy/squares#238. Replayed here with `zmx2` `6b7f0f79`: `VERIFIED-D4`, 6,400 roots, 800,042 boxes, no uncertified box, and two mutated covers refused | github.com/wand125 | `wand125-point-n61-2026-09-30/` |
| **[wand125 linear certificates 2026-10-02]** | wand125’s linear certificates at `0c35d909` (2 October 2026) for `s(101) ≥ 257/25` and `s(83) ≥ 187/20`: measures of point masses, uniform segments and uniform rectangles in `D4` orbits, checked by `code/unified_linear_verify.cpp`, a certificate kind and checker this record had not registered; requested in jlevy/squares#294. The exact audit passes; the complete replay of the `n = 101` certificate here on 2 October 2026 matched the shipped run at all 201 directions, which verifies `s(101)` and, by its mass, `s(102)` to `s(105)`, and the `n = 83` certificate’s on 3 October did too; a negative control refused two mutated `n = 101` measures, the checker’s seven new files are retained, and the proof-bundle tarballs are pinned by SHA-256 and not retained | github.com/wand125 | `wand125-linear-certificates-2026-10-02/` |
| **[wand125 rectangle bounds 2026-10-02]** | wand125’s rectangle-density certificates at `b00fc70f` (2 October 2026), seven rungs raised since `1a25a5ed` in three commits and built with Tokoharu’s solver and decided by his unchanged interval verifier: `s(20) ≥ 49/10`, `s(42) ≥ 2731/400` and `s(70) ≥ 3451/400` raise the reported bounds there, and the rungs at `n = 59`, 77, 91 and 93 are below bounds held separately. Not requested; taken in with the afternoon’s requests. The exact preflight of all 53 standing certificates passes; none of the seven is replayed here yet | github.com/wand125 | `wand125-rectangle-certificates-2026-10-02/` |
| **[wand125 mixed bounds afternoon 2026-10-02]** | wand125’s six mixed rectangle-measure certificates of the afternoon of 2 October 2026, pinned at `b00fc70f`, for `s(83) ≥ 937/100`, `s(85) ≥ 473/50`, `s(87) ≥ 237/25`, `s(91) ≥ 97/10`, `s(92) ≥ 39/4` and `s(96) ≥ 249/25`, of the kind and checker of **[wand125 mixed bounds 2026-10-02]**; requested in four comments on jlevy/squares#282. Two supersede that key’s and the 1 October key’s certificates at `n = 85` and 92, and by mass they also bound `n = 86`, 88 and 93. The complete replay of each here on 2 and 3 October 2026 matched the shipped run at all 201 directions, which verifies all six and the three counts they carry; `sqverify-fast`, this repository’s clean-room measure verifier, also decided all six at all 201 net directions on 3 October, with controls refused on 6 October, an independent second implementation. The proof-bundle tarballs are pinned by SHA-256 and not retained | github.com/wand125 | `wand125-mixed-bounds-afternoon-2026-10-02/` |
| **[wand125 mixed bounds 2026-10-03]** | wand125’s 22 mixed rectangle-measure certificates of 3 October 2026, pinned at `2aff2076`, for `s(51) ≥ 373/50`, `s(52) ≥ 151/20`, `s(55) ≥ 966/125`, `s(58) ≥ 1581/200`, `s(69) ≥ 2153/250`, `s(70) ≥ 3459/400`, `s(71) ≥ 1741/200`, `s(73) ≥ 8809/1000`, `s(74) ≥ 3547/400`, `s(75) ≥ 223/25`, `s(76) ≥ 224/25`, `s(86) ≥ 19/2`, `s(87) ≥ 191/20`, `s(88) ≥ 48/5`, `s(89) ≥ 193/20`, `s(90) ≥ 389/40`, `s(91) ≥ 39/4`, `s(92) ≥ 977/100`, `s(93) ≥ 493/50`, `s(94) ≥ 248/25`, `s(95) ≥ 249/25` and `s(96) ≥ 997/100`, of the kind and checker of **[wand125 mixed bounds afternoon 2026-10-02]**; requested in 22 comments on jlevy/squares#282. Six supersede earlier certificates of the source at `n = 76`, 87, 90, 91, 92 and 96. Exact premises and every pre-replay check pass; on 6 October 2026 `sqverify-fast`, this repository’s clean-room measure verifier, decided all 22 at all 201 net directions, which verifies them, the one at n = 96 once the control’s repair refused its mutants (think-0uia), and the source’s own checker was not run here. The later certificates of **[wand125 mixed bounds 2026-10-04]** and **[wand125 mixed bounds evening 2026-10-04]** are higher at 16 of the counts. The proof-bundle tarballs are pinned by SHA-256 and not retained | github.com/wand125 | `wand125-mixed-bounds-2026-10-03/` |
| **[wand125 mixed bounds 2026-10-04]** | wand125’s 16 mixed rectangle-measure certificates of 3 October 19:33 UTC to 4 October 07:17 UTC, pinned at `8aa6a10b`, for `s(42) ≥ 2739/400`, `s(43) ≥ 2763/400`, `s(44) ≥ 2789/400`, `s(51) ≥ 747/100`, `s(56) ≥ 3121/400`, `s(57) ≥ 3149/400`, `s(67) ≥ 339/40`, `s(69) ≥ 431/50`, `s(72) ≥ 219/25`, `s(75) ≥ 447/50`, `s(84) ≥ 3763/400`, `s(86) ≥ 9503/1000`, `s(88) ≥ 769/80`, `s(93) ≥ 247/25`, `s(94) ≥ 497/50` and `s(95) ≥ 1993/200`, of the kind and checker of **[wand125 mixed bounds 2026-10-03]**; requested in 16 comments on jlevy/squares#282. Nine supersede earlier certificates of the source at `n = 51`, 69, 75, 84, 86, 88, 93, 94 and 95. The directories carry no `completion-audit.json`, so each tarball is bound by its digest at the pin. The packet also holds the source’s answer to review findings OC-1 and OC-2 on the 3 October key: `150939e` removes those directories’ `completion-audit.json` and nothing else. Exact premises and every pre-replay check pass; on 6 October 2026 `sqverify-fast`, this repository’s clean-room measure verifier, decided all 16 at all 201 net directions, which verifies them, and the source’s own checker was not run here. At `n = 88` and 94 **[wand125 mixed bounds evening 2026-10-04]** is higher, and at `n = 67` and 84 **[wand125 mixed bounds 2026-10-05]**. The proof-bundle tarballs are pinned by SHA-256 and not retained | github.com/wand125 | `wand125-mixed-bounds-2026-10-04/` |
| **[wand125 mixed bounds evening 2026-10-04]** | wand125’s 12 mixed rectangle-measure certificates of 4 October 07:51 to 19:03 UTC, pinned at `797bdf6e`, for `s(53) ≥ 3051/400`, `s(54) ≥ 1537/200`, `s(58) ≥ 1587/200`, `s(70) ≥ 3463/400`, `s(71) ≥ 8721/1000`, `s(73) ≥ 8813/1000`, `s(76) ≥ 1793/200`, `s(87) ≥ 479/50`, `s(88) ≥ 481/50`, `s(90) ≥ 973/100`, `s(91) ≥ 781/80` and `s(94) ≥ 199/20`, of the kind and checker of **[wand125 mixed bounds 2026-10-04]**; requested in 12 comments on jlevy/squares#282. Ten supersede earlier certificates of the source, at `n = 58`, 70, 71, 73, 76, 87, 88, 90, 91 and 94; `n = 53` and 54 are its first mixed certificates there. The directories carry no `completion-audit.json`, so each tarball is bound by its digest at the pin. The packet also pins `mixed_n69_L862` and `mixed_n86_L9503`, unchanged since **[wand125 mixed bounds 2026-10-04]** retained them. Exact premises and every pre-replay check pass; on 5 and 6 October 2026 `sqverify-fast`, this repository’s clean-room measure verifier, decided all 12 at all 201 net directions, which verifies them and the five counts they carry by mass, and the source’s own checker was not run here. The proof-bundle tarballs are pinned by SHA-256 and not retained | github.com/wand125 | `wand125-mixed-bounds-evening-2026-10-04/` |
| **[wand125 record updates 2026-10-04]** | wand125’s four updates of 4 October 2026 to certificates the record holds, pinned at `797bdf6e`: the run records, an exact record checker and a complete checksum list for the `s(59) = 8` cover, a fixed D4 check and the reference run for the `s(45) = 7` cover, run logs, a replay record and a hardened `verify.sh` for the `s(77) = 9` cover, and relativized paths and a corrected lemma-code map for the `s(21) = 5` archive. No certificate changes; each is an evidence update on its entry, retained and not run here; the `s(21) = 5` bundle parts are pinned through its archive index | github.com/wand125 | `wand125-record-updates-2026-10-04/` |
| **[wand125 mixed bounds 2026-10-05]** | wand125’s two mixed rectangle-measure certificates of 5 October 2026 at 06:06 and 06:07 UTC, pinned at `a541afbe`, for `s(67) ≥ 212/25` and `s(84) ≥ 9411/1000`, of the kind and checker of **[wand125 mixed bounds evening 2026-10-04]**; requested in two comments on jlevy/squares#282. They supersede `mixed_n67_L8475` and `mixed_n84_L94075` of **[wand125 mixed bounds 2026-10-04]**. The directories carry no `completion-audit.json`, so each tarball is bound by its digest at the pin. Exact premises and every pre-replay check pass; on 5 October 2026 `sqverify-fast`, this repository’s clean-room measure verifier, decided both at all 201 net directions, which verifies them, and the source’s own checker was not run here. The proof-bundle tarballs are pinned by SHA-256 and not retained | github.com/wand125 | `wand125-mixed-bounds-2026-10-05/` |
| **[wand125 mixed bounds finer net 2026-10-05]** | wand125’s two mixed rectangle-measure certificates added on 5 October 2026 after `a541afbe`, pinned at `43050edc`: `s(66) ≥ 843/100` (`d73ce20`, requested in a comment on jlevy/squares#282), superseding `mixed_n66_L842` of **[wand125 mixed bounds 2026-10-01]**, and `s(18) ≥ 47/10` (requested in jlevy/squares#366), the source’s first on a net its candidate declares: core `999/1000` and 416 half-angle tangents of step `1/1001`, which this repository’s `sqverify-fast` reads under its lemma N0. Same checker and driver as **[wand125 mixed bounds 2026-10-05]**. The directories carry no `completion-audit.json`, so each tarball is bound by its digest at the pin. Exact premises and every pre-replay check pass; on 6 October 2026 `sqverify-fast`, this repository’s clean-room measure verifier, decided `mixed_n66_L843` at all 201 net directions, which verifies it, and the source’s own checker ran here at 12 of its directions and not in full. The proof-bundle tarballs are pinned by SHA-256 and not retained | github.com/wand125 | `wand125-mixed-bounds-finer-net-2026-10-05/` |
| **[wand125 mixed bounds finer net 2026-10-06]** | wand125’s two mixed rectangle-measure certificates added on 6 October 2026 after `43050edc`, pinned at `65e408c9`, each on a net its candidate declares and requested in a comment on jlevy/squares#366: `s(18) ≥ 588/125` on core `1999/2000` and 832 half-angle tangents of step `1/2006`, superseding `mixed_n18_L470` of **[wand125 mixed bounds finer net 2026-10-05]**, and `s(19) ≥ 48229/10000` on that certificate’s net, superseding `rect_n19_L48175` of **[wand125 rectangle bounds 2026-10-01]**. Same checker as every earlier mixed certificate; `mixed_n18_L4704`’s driver differs from the earlier copies only in allowing more workers. The commit’s `verification/sqverify-net`, the source’s adaptation of this repository’s `sqverify_fast`, is pinned by digest and not retained. Exact premises and every pre-replay check pass; on 6 October 2026 `sqverify-fast`, this repository’s clean-room measure verifier, decided both at every direction of their declared nets, which verifies them, and the source’s own checker ran here at 10 directions of each and not in full. The proof-bundle tarballs are pinned by SHA-256 and not retained | github.com/wand125 | `wand125-mixed-bounds-finer-net-2026-10-06/` |
| **[wand125 mixed bounds check2 2026-10-06]** | wand125’s ten mixed rectangle-measure certificates added on 6 October 2026 after `65e408c9`, pinned at `2fad66e0`, each on a net its candidate declares, none requested here: `s(29) ≥ 581/100`, a complete proof bundle with the checker of every earlier mixed certificate, and nine check2 bundles, at `n = 18, 19, 20, 26, 27, 28, 30, 39, 41`, which ship no C++ record and are checked at the source by its copy of this repository’s `sqverify_fast` changed to read a declared net, pinned by digest and not retained. `s(18) ≥ 941/200` and `s(19) ≥ 193/40` are on 2073 half-angle tangents of step `1/5002` at core `4999/5000`, superseding **[wand125 mixed bounds finer net 2026-10-06]**. Exact premises and every bundle binding pass; on 6 October 2026 `sqverify-fast`, this repository’s clean-room measure verifier, decided all ten at every direction of their declared nets, which verifies them, independently of the producer’s checker for `s(29)` and sharing its components for the nine check2 bundles, whose own check is a copy of the same crate; the source’s C++ checker ran here at sampled nodes and not in full. The tarballs are pinned by SHA-256 and not retained | github.com/wand125 | `wand125-mixed-bounds-check2-2026-10-06/` |
| **[wand125 linear n82 2026-10-02]** | wand125’s linear certificate for `s(82) ≥ 233/25`, pinned at `b00fc70f` (first committed at `58f153f8`, 2 October 2026): the support of **[wand125 linear certificates 2026-10-02]**’s `n = 83` measure scaled by `932/935`, with its masses solved again, checked by the same `unified_linear_verify.cpp`; above Green’s reported value at `n = 82` and not resting on Green’s argument; requested in a comment on jlevy/squares#294. The complete replay here on 3 October 2026 matched the shipped run at all 201 directions, which verifies it; the proof-bundle tarball is pinned by SHA-256 and not retained | github.com/wand125 | `wand125-linear-n82-2026-10-02/` |
| **[wand125 valid7 independent check 2026-10-02]** | wand125’s separately written exact-rational checker of Valid7 at `38dd31b3` (2 October 2026), run on Daniel’s `k = 7` cover: 156,800 root boxes of the unreduced pose space, 9,640,060 leaves, none uncertified, about 626 core-hours; its read log says Daniel’s checker and lemma write-ups were not read. Requested in jlevy/squares#296. The code is retained and the release records pinned by SHA-256; its `verify.sh` record check and an audit passed here on 2 October, and the complete run was repeated here on 2 and 3 October 2026 with review finding D-1’s line guarded: all 156,800 roots `VERIFIED` in 9,808,968 leaves, none uncertified, each of the 124,975 roots the source ran under V2 with its published leaves | github.com/wand125 | `wand125-valid7-independent-check-2026-10-02/` |
| **[wand125 valid7 independent check 2026-10-03]** | The same checker at `da469ecf` (3 October 2026), fixing the three implementation findings of this repository’s 2 October method review: `tier_b2.nonneg_open` and `rf.nonneg_on` no longer accept a polynomial that vanishes at the sample (D-1, D-2), and `tier_b2` keys its line and value caches by exact text rather than Python’s `hash` (D-3); `check_record.py` gains `--seed` and `--claim tilt`. The release records are unchanged. Its `verify.sh` ran here on 5 October 2026 on the unchanged records, `RECORD OK`, and a probe of both revisions shows each finding present before and gone after | github.com/wand125 | `wand125-valid7-independent-check-2026-10-03/` |
| **[wand125 valid7 independent check 2026-10-06]** | The same checker at `c561dbb3` (6 October 2026), run on Daniel’s box-9 cover for ValidTilt9, the finite premise of `s(k² − 4) = k` for `k ≥ 8` (`T-081`): 28,350 root boxes over centres `[0, 9/2]²` and `u = tan(θ/2)` in `[0, 7/16]`, 9,537,343 leaves, none uncertified, about 766 core-hours, with `da469ec`’s checking modules and a driver extended mid-run; its read log says Daniel’s checker, lemma write-ups and k2m4 run records were not read. The code is retained and the release `records-tilt9-v1` pinned by SHA-256. Its `verify_tilt9.sh` and an audit of the records passed here on 6 October 2026, and a sample of roots re-ran with their published leaves; the full run was not repeated here | github.com/wand125 | `wand125-valid7-independent-check-2026-10-06/` |
| **[wand125 Green DS7 Theorem 9 2026-10-02]** | wand125’s note of 2 October 2026, a gist at `9d6de784`: the sixteen points DS7’s Figure 34 calls unavoidable for Green’s `s(17) ≥ (40√2 + 19)/17` miss a closed unit square at that side, and Green’s pattern reconstructed for every `k` fails the same way for `k ≥ 4`, so the published material does not establish DS7 Theorem 9 there; not a counterexample to the bound. Requested in jlevy/squares#308. All four files retained, no licence stated; the illustrated claude.ai page it links is not retained. `devtools.check_green_ds7` confirms the failure for `k = 4…17` in exact arithmetic and finds the pattern fails at `k = 2` too, through its side margin | gist.github.com/wand125 | `wand125-green-ds7-theorem9-2026-10-02/` |
| **[ahyangyi 17squares v1.1.1]** | ahyangyi’s `17squares` `v1.1.1` at `1a320e7f`, 23 September 2026, reporting `s(17) > 184547267428061/40000000000000 ≈ 4.6136817`, below both Guzhou0806’s R038 and the verified `n = 17` bound; its author’s commit message calls it no longer frontier. Named in the `n = 17` case file for completeness and deliberately not retained or replayed | github.com/ahyangyi | not retained |
| **[evand square-packing 2026]** | Evan Daniel’s `evand/square-packing` (formerly `square-packing-12`) at `167d842c`, 26 September 2026, building on Sam Burns’s and Gustavo Massaccesi’s weighted exact-rational covering method and, per its `CREDITS.md`, produced with an AI agent under human direction: a zero-margin weighted closed cover of `[0,6]²` for `s(32) = 6` with its two exact checkers’ run records and a Lean top theorem from one computational hypothesis; angle-net certificates for `s(12) ≥ 15680/3951`, `s(21) ≥ 5000/1001` and `s(11) ≥ 3040/797`; and a case-free closed cover for Bentz’s `s(13) = 4`. 56 files byte-identical, MIT. The Rust verifier on the `s(12)` and `s(21)` certificates passes here, registered at `V4`/`C3`, and this repository’s native parent-core interval route decides the `s(12)` certificate in full, so `s(12)` is at `V4`/`C4`; `s(32) = 6` is registered at `V4`/`C4` on a complete re-sweep here of all 7,200 roots, every census matching the source’s run, beside a complete run here of the source’s `zmx2`, from **[evand square-packing 2026-09-28]**, on the same cover; the `zmcheck` sweeps and the Lean build were not replayed, and the `s(13)` cover only by `zmx2`. Its `s(21)` bound is superseded by **[evand square-packing 2026-09-28]** | github.com/evand | `evand-square-packing-2026-09-26/` |
| **[evand square-packing 2026-09-28]** | Evan Daniel’s `evand/square-packing` at `6aa82ba4`, 28 September 2026, building on Sam Burns’s and Gustavo Massaccesi’s weighted exact-rational covering method and, per its `CREDITS.md`, produced with an AI agent under human direction: mixed covers (weighted points plus uniform mass on interior grid-line segments) for `s(21) = 5` and `s(45) = 7`, each certified at margin zero by `zm_mixed.py` (exact) and `zmx2` (Rust, binary64 enclosure), with a Lean top theorem for `s(21)` from one hypothesis; the source also reports hypothesis-free Lean checks of `s(13) = 4` and `s(32) = 6`. 91 changed files byte-identical, MIT. Both fast tiers pass here, fresh `zmx2` `--d4`/`--full` censuses equal the source’s for all 66,600 roots, and a 64-root `zm_mixed.py` sample matches, so both values are registered at `V4`/`C3`; the full `zm_mixed.py` re-sweeps run separately; Lean not built (Mathlib cache unreachable) | github.com/evand | `evand-square-packing-2026-09-28/` |
| **[evand square-packing 2026-10-01]** | Evan Daniel’s repository at `08e8a5faa54c0a7b0bb1cb0134c77d3565ce40c5`: `s(60) = 8`, its `s(61) = 8` consequence, and the periodic segment-and-area family `s(k² − 3) = k` for every `k ≥ 6`. Selective pinned source packet, citation audit and mathematical review; the `s(60)` cover’s `zmx2` sweeps were replayed here on 2 October 2026, which verifies `s(60) = s(61) = 8`. The finite family premise remains computational and the Lean reduction conditional. Recovered side-4 and side-5 fractional-dual inputs are reviewed but not freshly replayed here. The `zmx2` source that made its `s(32)` run without the D4 fold, `92a4cfe8…` at `e4af291c`, is retained in `evand-zmx2-sym-atoms-2026-09-30/`, and that run was replayed here on 2 October 2026, every root’s census equal to the source’s. See the packet for retained files and omissions. | github.com/evand | `evand-square-packing-2026-10-01/` and `evand-zmx2-sym-atoms-2026-09-30/` |
| **[evand square-packing 2026-10-02]** | Evan Daniel’s repository at `7d6f46d9`, 2 October 2026: his replay of wand125’s point-only `s(61) = 8` cover by `zeromargin.py` and `zmcheck`, with its run records; Lemma 2 of the clique family in Lean; the `dual_exact.py` fixes; and the claims audit, which restates checker independence and records a gap in Nagamochi’s Lemma 1. Selective packet, MIT; the cover and every checker its manifest names are retained here, and nothing was replayed | github.com/evand | `evand-square-packing-2026-10-02/` |
| **[evand square-packing 2026-10-03]** | Evan Daniel’s repository at `2eb15455`, 3 October 2026, the commit jlevy/squares#316 names: the `k2m4` bundle for $s(k^2 - 4) = k$ for every $k \ge 5$, with the box-9 cover and family, the `qx2_zm.py` run record over 16,200 roots, and the Lean closure of `bentz4_of_validTilt9`. MIT; the bundle’s fast `verify.sh` passed here on the retained bytes, and the full run has not been replayed | github.com/evand | `evand-square-packing-2026-10-03/` |
| **[evand square-packing 2026-10-04]** | Evan Daniel’s repository at `7ff3b211`, 4 October 2026: what it added after `2eb15455`, among it a 12,864-point cover for $s(20) > 3 + 4\sqrt{2}/3$, below this record’s verified $1959/400$, with the source’s own review of it; exact pure-cover ceilings for $n = 17$ to $20$; Lean for the LEB and CAP leaves of `ValidTilt7` and the reduction of `Valid7` to it; and a Lean bridge to chelokot’s definitions. Added on 5 October from the same commit: what earlier commits changed that no packet retained and that bears on registered entries, among it `zmx2`’s area-density run deciding `Valid7`, the source’s `k² − 3` and `k² − 4` review reports, the claims audit’s bundle READMEs, the brief of `zmx2`, and the Lean attainment theorem and specification bridges. MIT; nothing was replayed | github.com/evand | `evand-square-packing-2026-10-04/` |
| **[evand exact optima 2026-10-05]** | Evan Daniel’s repository at `13ee36e5`, 5 October 2026: an exact-contact solver run on this register’s known-best witnesses, with exact rational certificates of $s(n) \le S'$ at 321 counts. At 48 the certified side lies $3.5 \times 10^{-13}$ to $5.0 \times 10^{-11}$ below the register’s, the exact optimum of the same packing, Francisco Couzo’s at 46 counts and Joost de Winter’s at $n = 126$ and $211$ (T-098); at 77 more, $1.2 \times 10^{-16}$ to $9.8 \times 10^{-15}$ above the printed side, it lowers the verified ceiling, off the integer grid at 74 (T-101). MIT; every certificate but $n = 17$’s replayed here by the source’s two checkers and this repository’s two, the 125 the record cites retained, and the $n = 17$ certificate held | github.com/evand | `evand-square-packing-2026-10-05/` |
| **[evand square packing atlas 2026-10-04]** | Evan Daniel’s Square Packing Atlas, <https://evand.github.io/square-packing/>, as the same commit builds it: the overview, explorer, comparison, bounds, proofs, sources and `k2m4` pages, and the open-problems page <https://evand.github.io/square-packing/problems.html>, with their scripts and their floors table for $n \le 100$. The packings are David Ellsworth’s catalogue’s. The deployed site, fetched on 2026-10-05 once the egress policy allowed it, serves exactly these files: all 37 pages, scripts, data and covers the build copies are byte-identical to the commit’s. The floors table agrees with this record’s verified lower bounds at 99 of its 100 counts and at every count it marks verified; it is [reviewed](../../docs/project/reviews/review-2026-10-05-evand-square-packing-atlas.md) | evand.github.io/square-packing | `evand-square-packing-2026-10-04/` |
| **[chelokot Nagamochi counterexample 2026]** | chelokot’s note of 4 September 2026 (UTC) in `square-packing-archive`, unchanged to head `753079eb`: a square of side `1.0001` in the `4 × 4` container scoring `0.977543… < 1` under Nagamochi 2005’s Section 3 weights, against that paper’s Lemma 1, with the same Case 6 edge-incidence gap **[Karakuş 2026]** finds; CC BY 4.0, note and figure byte-identical, its checker, Lean files and the linked compensation proof of `s(n² − 2) = n` pinned by digest; the Lean development replayed at the pin for T-086 (update of 4 October 2026), not retained | github.com/chelokot | `chelokot-nagamochi-counterexample-2026-09-05/` |
| **[evand atlas explorer 2026-10-02]** | Evan Daniel’s deployed Square Packing Atlas, which colours the catalogue’s record packings by kind of packing, symmetry, free squares, year of record or wasted area and names no families; seen 2026-10-02 at 06:51 UTC (HTTP 200, `Last-Modified` 2026-10-02 00:55:33 GMT). A mutable deployment of the repository already pinned as **[evand square-packing 2026-10-01]**, so a dated reference only | evand.github.io/square-packing | not retained |
| **[Guzhou0806 n17 R052 continuation]** | Guzhou0806’s continuation of R052 at `6f64e4b2`, published 25 September 2026 (UTC), claiming `s(17) > 462003/100000 = 4.62003` from an exact `D4` site deformation of R052 and two more four-way angle splits over 15,727 rows; superseded by Kleddamag’s public `232001/50000` of 26 September. Its publication record and validation record byte-identical, plus local receipts for the records, containment and new C++ full modes; no review, no bound moved | github.com/Guzhou0806 | `n17-guzhou-r052-continuation-2026-09-26/` |
| **[MacIver 2026 papers]** | Three author-hosted manuscripts: a reported `s(17), s(18) > 4.450208382…`, the center-area lemma, and center-count bounds; original PDFs, faithful extractions, source revision, upstream CI receipt, and a reading aid with verification limits | github.com/DRMacIver; drmaciver.github.io | `maciver-square-packing-2026-09-07/` |
| **[n26 current-source audit 2026]** | Current n26 catalogues, recent solver and proof projects, and an exact comparison of MinMax Arena’s reciprocal score; no smaller public upper bound found in the scoped search | primary catalogues; GitHub; minmaxarena.com | `n26-best-known-2026-09-07/` |
| **[De Winter 2026]** | Mutable author report of proposed construction improvements at `n = 68, 126, 206`; coordinates unavailable and values unreplayed | researchgate.net | `de-winter-improved-packings-2026/` |
| **[SQUISH ten packings 2026-10-07]** | Nate Chaoweeraprasit’s SQUISH rational packing certificates for ten counts, n = 108, 126, 129, 130, 154, 155, 180, 209, 238 and 303, at `07fe6dde`, committed 7 October 2026. New upper bounds independently re-verified as T-113; no optimality claim. Credits David Ellsworth’s records and tools and states human-directed Claude Opus 5.5 assistance. No licence, so derived packing facts and source metadata only | github.com/itsnaka | `squish-401-2026-10-07/` |
| **[SQUISH n153 2026-10-07]** | Nate Chaoweeraprasit’s later rational packing certificate for n = 153, attached to issue #401 comment 6031977107 on 7 October 2026. Upper bound independently re-verified as T-114 with the same credit, AI disclosure and retention policy; the attachment is pinned by digest | github.com/itsnaka | `squish-401-2026-10-07/` |
| **[SQUISH update 2026-10-07]** | Nate Chaoweeraprasit’s thirteen pinned update certificates: seven additional counts, five tighter packings and unchanged n153. Twelve improvements were independently replayed and confirmed at V3/C3 as T-115; their evidence remains retained when later reports supersede selected poses. Per-count Couzo and SQUISH seed attribution; no licence, derived facts only | github.com/itsnaka | `squish-401-update-2026-10-07/` |
| **[SQUISH second update 2026-10-07]** | Nate Chaoweeraprasit’s nine pinned new or smaller rational packing reports at e63e4e5, V0/C0; previous verified bounds retained. Ellsworth, Couzo and SQUISH seeds; human-directed Claude Opus5.5 assistance; no licence, derived facts only | github.com/itsnaka | `squish-422-second-update-2026-10-07/` |
| **[Daniel exact and local reports 2026]** | Evan Daniel’s pinned exact-form catalogue and non-strict local-minimum reports at f58a017; four new feasible-side forms and178 source configurations retained as V0/C0. Full source metadata and Lean code, without independent geometry, minimality or Lean replay | github.com/evand | `evand-exact-and-local-reports-2026-10-07/` |
| **[franciscouzo square-packing 2026-09-27]** | Francisco Couzo’s `square-packing` at `f3c5a529`, 27 September 2026: 49 packings for `n = 68…307`, each below both this project’s recorded side and the live catalogue on 29 September. No licence, so the packet keeps each packing as derived Witness/v2 facts with the upstream digests and the per-case commit history, never the files. Every packing certifies exactly over `ℚ` here at centre dilation 1 (`packing-witness promote --strategy robust-rational`, then the independent Fraction checker), the side moving by less than `2.2e-15` either way; rounded up at the printed 15 decimals it lands one unit above the printed side at 26 counts, which the record’s agreement rule accepts, and 2–3 units above at `n = 206, 259, 305`, recorded as conflicts. Registered as T-056 at `V4`/`C3`; issue #227 | github.com/franciscouzo | `franciscouzo-square-packing-2026-09-27/` |
| **[franciscouzo square-packing 2026-10-03]** | Francisco Couzo’s `square-packing` at `6042c56b`, 3 October 2026, the revision after `f3c5a529`: it lowers seven of the 49 packings, at `n = 208, 209, 228, 263, 272, 303, 306`, each below his earlier side and the catalogue captured on 30 September. Still no licence, so the packet keeps the seven as derived Witness/v2 facts with the upstream digests of all 99 files and the per-case commit history. Each certifies exactly over `ℚ` at centre dilation 1 and again by interval arithmetic on the printed pose; rounded up at 15 decimals the certificate lands one unit above the printed side at three counts and two units above at `n = 306`, recorded as a conflict. Registered as T-092 at `V3`/`C3`; no issue | github.com/franciscouzo | `franciscouzo-square-packing-2026-10-03/` |
| **[de Winter n211 2026-09-16]** | Joost de Winter’s `square-packing-211` at `702df9bb`, 16 September 2026: 211 unit squares at side `14.99796070496771500150`, the first `s(211) < 15` on the catalogue or this record, with the author’s 80-digit interval verification summary. No licence, so derived facts only. Certified exactly over `ℚ` here, the certificate `2.1e-14` inside the printed side; registered as T-057 at `V4`/`C3` | github.com/JoostdeWinter | `de-winter-square-packing-211-2026-09-16/` |
| **[griffcass square-packing 2026-09-23]** | Griffin Casson’s `square-packing` at `82661bc`, 23 September 2026 (UTC−6): 39 SLP-polished and annealed packings for `n = 103…307`, 50-digit checked by the author, with MIT code and CC BY 4.0 packings. The packings, summary, README, LICENSE and CITATION.cff are retained byte for byte and every other file pinned by digest. Couzo’s packings are smaller at all 39, so none holds a field here; published before Couzo’s at 36 of them by the authors’ clocks, not replayed here | github.com/griffcass | `casson-square-packing-2026-09-23/` |
| **[Ellsworth n69 2026-09-24]** | David Ellsworth’s `s(69) ≤ 8.82719465572973`, a degree-38 root, as the **[Kingbird]** capture of 2026-09-30 prints it (page dated 2026-09-24; the entry says September 2026): the packing hmbelvedere’s UnitSquare release reported in July 2026, refound with his modified version of Thomas Schadt’s annealing program from Maurizio Morandi’s `s(69)` and optimized. Registered as T-088; the witness is read from Evan Daniel’s binary64 parse of the catalogue SVG at `evand/square-packing@7ff3b21`, which the registering session could not fetch; the SVG, fetched on 2026-10-05, agrees with the parse at binary64 and dates the optimization 7 September 2026 ([receipt](web/known-best-packings/receipts/kingbird-2026-10-05-pictures.json)) | kingbird.myphotos.cc | `kingbird-squares-in-squares` |
| **[Chang n83 2026-09-24]** | Allen Chang’s `s(83) ≤ 9.63475764863108`, a degree-672 root, optimized by David Ellsworth, as the same capture prints it: an improvement of the Hajba and Cantrell packing made “with GPT-5.6 Sol and GPT-6 Astra”, whose polynomial is printed only in the SVG, as a Mathematica `Root` object read on 2026-10-05, when the comment’s dates (4 to 10 September 2026) were read too. Registered as T-089, with `n = 87`; witness as for `n = 69` | kingbird.myphotos.cc | `kingbird-squares-in-squares` |
| **[Chang n87 2026-09-24]** | Allen Chang’s `s(87) ≤ 9.83881526994826`, a degree-41 root, as the same capture prints it: an improvement and optimization of Ellsworth’s and Cantrell’s packing made “working with GPT-6 Astra, with help from ‘TheMagicAnimals’”; the SVG, read on 2026-10-05, dates it 10 September 2026, says “with GPT-5.6 Sol and/or GPT-6 Astra”, and dates Ellsworth’s reconstruction 16 September. Registered as T-089, with `n = 83`; witness as for `n = 69` | kingbird.myphotos.cc | `kingbird-squares-in-squares` |
| **[Schadt n=29 repository]** | Thomas Schadt’s `n = 29` record repository: the packing, its Python verifier, the rendered SVG, and his four-sentence methodology note | github.com/BalthasarStrauss | `schadt-s29-2025/` |
| **[Squarl n17 2026]** | Sam Burns’s open `n = 17` pipeline documentation at a pinned commit: the formulation and move set, the deep-polish architecture and its tolerances, the final nine-hour production search’s own accounting, and the earlier topology drain | github.com/sam-bee/squarl | `squarl-n17-2026/` |
| **[Literature refresh 2026-09-05]** | Frozen arXiv, Crossref, OpenAlex, and Zenodo receipts; additions, currentness checks, and nearby-problem exclusions | primary sources and scholarly indexes | `literature-refresh-2026-09-05/` |
| **[Annealing methods audit 2026-09-08]** | Frozen arXiv, Crossref and OpenAlex receipts for the search-method corpus; the fifteen-paper acquisition manifest, three readings checked against the retained bytes, the screened-out adjacent problems, and the open-access verdict on every source that could not be retrieved | primary sources and scholarly indexes | `annealing-methods-audit-2026-09-08/` |
| **[Simulation methods audit 2026-09-09]** | Frozen arXiv, Crossref, OpenAlex, Semantic Scholar, GitHub and publisher receipts for the physics- and simulation-mechanism corpus, in four disjoint lanes; 101 responses, the seventy-two-paper acquisition manifest with per-file hashes, eight readings checked against the retained bytes, four searches whose zero counts are themselves findings, the screened-out adjacent problems, and every source that could not be retrieved with its obstacle | primary sources and scholarly indexes | `simulation-methods-audit-2026-09-09/` |
| **[`s(11)` lower-bound audit 2026]** | Exact-value, reciprocal, catalogue, citation-chain, and method-lineage search supporting the scoped novelty claim for `381/100` | primary papers; author pages; scholarly indexes; public catalogues | `s11-lower-bound-literature-audit-2026/` |
| **[`s(11)` exact-endpoint audit 2026-09-06]** | Dated exact-value and topic-query receipt for `38100*sqrt(8100042893309449)/899996306539`; a bounded currentness check, not absolute-priority proof | arXiv; Crossref; OpenAlex; general web index | `s11-exact-endpoint-literature-audit-2026-09-06/` |
| **[Finite-case literature audit 2026]** | Repeatable queries and bounded negative result for recent papers on the prioritized cases | arxiv.org; combinatorics.org; author pages | `finite-case-literature-audit-2026/` |
| **[`n = 54` source/formula audit 2026]** | Revision-keyed genealogy, live-SVG formula receipt, quartic-field replay, and typed pose-correspondence gap | combinatorics.org; kingbird.myphotos.cc | `n54-source-formula-audit-2026/` |
| **[Montanher et al. 2018]** | Rigorous packing of unit squares into a circle (full text via PMC) | pmc.ncbi.nlm.nih.gov | `montanher-2018-rigorous-packing-unit-squares-circle` |
| **[Markót 2021]** | Improved interval methods for circle packing in the unit square (full text via PMC) | pmc.ncbi.nlm.nih.gov | `markot-2021-improved-interval-methods-circle-packing` |
| **[squaring.net BSST]** | The Smith-diagram / Kirchhoff correspondence, in detail | squaring.net | `squaring-net-brooks-smith-stone-tutte-II` |
| **[squaring.net Sprague]** | Priority for the first published perfect squared square | squaring.net | `squaring-net-sprague` |
| **[Wikipedia]** | Square packing overview | en.wikipedia.org | `wikipedia-square-packing` |
| **[`n = 19–21` lower-bound audit 2026]** | Versioned DS7 history, evidential status, and bounded priority check for the `24/5` certificate | combinatorics.org; retained papers and web captures | `n19-n21-lower-bound-literature-audit-2026/` |

The MacIver packet preserves three separate citation identities at commit
`9e2cd597047e040a63b7dcd103e79962cfc2d781` (10 August 2026). Its
[reading aid](web/maciver-square-packing-2026-09-07/README.md) distinguishes the
manuscripts’ printed dates from that source revision and the September retrieval date.
No journal venue or DOI for them was identified in the inspected source.

| Key | Manuscript | Printed date | Retained source |
| --- | --- | --- | --- |
| **[MacIver 2026 n17]** | *An improved lower bound for packing seventeen unit squares in a square, via a deformation of Green’s scaffold with certified defect charging* | 8 August 2026 | [PDF](web/maciver-square-packing-2026-09-07/maciver-2026-seventeen-unit-squares-lower-bound.pdf) |
| **[MacIver 2026 center-area]** | *The Center-Area Lemma: Three disjoint unit squares whose centers form a non-obtuse triangle span area at least 1/2* | No date printed; present at the pinned August commit | [PDF](web/maciver-square-packing-2026-09-07/maciver-2026-center-area-lemma.pdf) |
| **[MacIver 2026 nmax]** | *Counting unit squares by their centers: sharp convex bounds and exact strip laws* | August 2026 | [PDF](web/maciver-square-packing-2026-09-07/maciver-2026-counting-unit-squares-by-centers.pdf) |

## Special Kingbird SVG Witnesses

These are not papers, but they carry the source geometry rather than a rendered picture.
Each is named by the key the frontier records cite it under.

- **[Ellsworth SVG]** `papers/kingbird-square-11-provenance.svg` is the single most
  information-dense source found on `n = 11`. Its XML comments carry David Ellsworth’s
  provenance notes, the two contact equations, the derived placement constants, and the
  full exact-solution history (Gensane–Ryckelynck 2004 → Ellsworth 2023 → Alexeev’s
  independent confirmation).
  It is preserved verbatim.
- **[Kingbird n=29 SVG]** `papers/kingbird-square-29-provenance.svg` carries Thomas
  Schadt and David Ellsworth’s `n = 29` construction, 100-digit placement constants, the
  six defining equations, and the full SVG transform tree.
  The upstream response was retrieved on 2026-08-24. The retained text differs only by
  CRLF-to-LF normalization and a terminal newline.
  The H-024 experiment records the URL, retrieval date, normalization, and retained
  path; Git retains the source bytes.
- **[Kingbird n=5 SVG]** is the catalogue’s `square-5.svg`
  (<https://kingbird.myphotos.cc/packing/square-5.svg>), the source
  `cases/gobel5/packing.py` names for Göbel’s five-square construction.
  Its bytes are **not** retained here; `web/known-best-packings/sources.json` records
  its retrieval, and the construction is replayed exactly from the case module.

## Not Retrievable

The archive records these sources to avoid duplicate searches.
**Re-test this list rather than inheriting it.** On 2026-08-22 three entries were
removed because they turned out to be freely available: Gensane–Ryckelynck (Springer
serves the PDF openly at its `/content/pdf/` URL—the earlier attempt had fetched the
article landing page), Nagamochi (open access in the *Electronic Journal of
Combinatorics*, and cited by its exact title in the archived DS7 reference list all
along), and Wang–Dong–Li (arXiv).
A “not retrievable” verdict is a negative search result, and this archive has now been
wrong about it **ten** times.
On 2026-08-27 the full El Moumni article was found inside the Hungarian Academy’s public
volume scan and Trump’s 2023 note on the author’s own site.
Earlier corrections include Markót 2021 at PMC, Roth & Vaughan (1978) supplied on
request, and Stromquist’s three memoranda on the author’s publication page.
On 2026-10-05 both Chung–Graham papers were found on Ron Graham’s publication page,
which the environment had not reached before.
Reading Roth–Vaughan produced two corrections to the published secondary literature.

[`../frontier/source-availability.yaml`](../frontier/source-availability.yaml) records
the maintained list, each obstacle, its dependants, and a route to obtaining the source;
the research document renders it as a table.
The short version below is kept for readers of this archive.

| Source | Obstacle |
| --- | --- |
| Arslanov & Bui, *Note on “efficient packings of unit squares in a large square”*, DCG (2025) | Springer; not open access. |
| Brooks, Smith, Stone & Tutte, *The dissection of rectangles into squares*, Duke Math. J. 7 (1940) | Project Euclid; not open access |
| Gustafsson & Thulin (1980), *Ronden* | Swedish company periodical; Ellsworth notes he has not read it directly either |
| MacIver (2026), supporting C1-C14 certificates and exact ledger/replay scripts | Absent from the inspected public commit of 10 August 2026; checked 7 September. The manuscript itself is archived. |

Six search-method sources were attempted on **2026-09-08** and not retrieved.
[The annealing audit packet](web/annealing-methods-audit-2026-09-08/README.md) records
each attempt, its HTTP result, and its open-access verdict from the retained OpenAlex
probe; the short version is that Basurto et al.
2024 (J. Chem. Phys.
161:044110) and Oakley et al.
2013 (Phys. Chem. Chem.
Phys. 15:3965) are nominally hybrid open access but returned HTTP 403, and that Basurto
et al. 2026 (Comput.
Phys. Commun. 320:109990), Müller et al.
2009 (Phys. Rev. E 79:021102), Gomes & Oliveira 2006 (Eur.
J. Oper. Res. 171:811) and the TAMSASS-PECS chapter are closed.
These are not in
[`../frontier/source-availability.yaml`](../frontier/source-availability.yaml), which
tracks sources bearing on square-packing bounds; these bear on search method.

Twenty further simulation-method sources or groups of them were attempted on
**2026-09-09** and not retrieved.
[The simulation methods audit packet](web/simulation-methods-audit-2026-09-09/README.md)
records each attempt, its HTTP result and its open-access verdict; these too bear on
method rather than on bounds and are not in `source-availability.yaml`. Three patterns
are worth carrying forward rather than rediscovering.
**HAL is gated from this host by an Anubis proof-of-work challenge that returns HTTP 200
with a challenge page**, which is what hides the open copies of the four foundational
contact-dynamics papers (Moreau 1994, Jean 1999, Radjai and Richefeu 2009, Radjai et al.
1996). **The American Physical Society refuses plain `curl` with HTTP 403** even on
bronze open-access articles.
And **a Cloudflare interstitial returns HTTP 200**, so a fetch can appear to succeed and
write an HTML file to a `.pdf` path; one such file was written and deleted in this pass,
and the packet says so.

## Provenance and Licence

The original archive was retrieved on **2026-08-22** from the URLs recorded in each
file’s metadata header.
The El Moumni volume scan was retrieved on **2026-08-27** from the Hungarian Academy’s
REAL-J repository; its article occupies PDF pages 287–296. Trump’s 2023 preprint was
retrieved the same day from his public author page.
The three Stromquist memoranda were retrieved on **2026-08-24** from the author’s
[official publication page](https://www.walterstromquist.com/publications.html), which
links the exact archived PDFs as `squares1.pdf`, `squares2.pdf`, and `squares3.pdf`. All
three PDFs are image-only scans; their raw aids are unedited Tesseract 5.5.0 English OCR
from 300 dpi Poppler-rendered page images, concatenated in page order with form-feed and
newline separators. All 47 pages were visually reviewed on **2026-09-07**, and the
author’s [publication page](https://walterstromquist.com/publications.html) still links
the three notes under Geometry and Topology.
The expanded reading aids describe
[Memo I’s six-square helper argument](papers/stromquist-1984-packing-unit-squares-inside-squares-i-six-unit-squares.md),
[Memo II’s forced incidences](papers/stromquist-1984-packing-unit-squares-inside-squares-ii-ten-unit-squares.md),
and
[Memo III’s historical claims and restricted proof](papers/stromquist-1984-packing-unit-squares-inside-squares-iii-cases-through-65-and-gardner-conjecture.md).
[Stromquist’s Memos and Helper Arguments](../../docs/project/research/research-2026-09-07-stromquist-memos-and-helper-arguments.md)
records their implications for the research program.
The review retains source-level formula slips as explicit reading notes and leaves the
PDFs and raw OCR unchanged.
The fifteen search-method papers and the Squarl documentation were retrieved on
**2026-09-08**; every URL, timestamp and SHA-256 is in
[the audit packet](web/annealing-methods-audit-2026-09-08/README.md), and each `.raw.md`
is `pdftotext -layout` on its retained PDF. The seventy-two simulation- and
physics-method papers were retrieved on **2026-09-09** on the same terms, from arXiv,
from open-access journal and repository mirrors, from author and institutional pages,
and in three cases from the Internet Archive’s copy of a publisher PDF; every URL,
timestamp and SHA-256 is in
[the simulation methods packet](web/simulation-methods-audit-2026-09-09/README.md).
Four contact-dynamics papers that HAL’s bot challenge had kept from that pass were
retrieved from HAL on **2026-10-05**, on the same terms; the packet records them under
“Retrieved on 2026-10-05”. The single OCR sidecar in that batch was produced with
`pdftoppm -r 300 -gray -png` and Tesseract at `--psm 6`, the same method as the
Stromquist aids. The two Chung–Graham papers were retrieved on **2026-10-05** from
<https://mathweb.ucsd.edu/~ronspubs/>, which links them as `09_03_square_packing.pdf`
(SHA-256 `77e96eb4…`, 513,202 bytes) and `pre_square_packing.pdf` (SHA-256 `bd54b4cd…`,
626,971 bytes); each `.raw.md` is `pdftotext -layout` (poppler 24.02.0) on its retained
PDF, and no cleaned transcription has been written.
Archive PDFs are marked binary in the repository’s `.gitattributes`; this prevents Git
from interpreting compressed scan streams as text without changing any source bytes.
The arXiv and Electronic Journal of Combinatorics items are open access; the Stanford
technical report and PMC item are publicly posted.
Retained for private research use.
Consult the original publisher before redistributing.

## Rational certificate refinements, 7 October 2026

- **[Rehwaldt Couzo refinements 2026-10-07]**: Seth Rehwaldt after Couzo and earlier
  contributors, with OpenAI Codex assistance.
  Finite rational ceilings from issue 425, pinned at
  `bc389ddf7d65277cd19a9b08fb285d86346d6806`;
  [packet](web/rehwaldt-couzo-refinements-2026-10-07/README.md).
- **[Rehwaldt n68 refinement 2026-10-07]**: Seth Rehwaldt after Couzo and earlier
  contributors, with OpenAI Codex assistance.
  Finite rational ceilings from issue 428, pinned at
  `fded686668e29258dad2eb29d0482fa3fd51bd6b`;
  [packet](web/rehwaldt-n68-refinement-2026-10-07/README.md).

## Three new rational arrangements, 7 October 2026

**[Daniel new arrangements 2026-10-07]**: Evan Daniel’s complete certificates for n =
266, 270 and 272, pinned at `7eef24f7221b8c3371d6171dd664b52541bbd479`;
[packet](web/evand-new-arrangements-2026-10-07/README.md).
Both project exact routes accept all three and reject all six complete-roster controls.
Source novelty and local/global optimality remain unestablished.
The source credits Ellsworth, Couzo, Cleemann, Arslanov, Mustafin, Shangitbayev and
Stead, with register data from the Squares Project (Joshua Levy) under CC BY 4.0 and
Claude assistance under Daniel’s direction.
Source MIT licences and the earlier #375 namespace remain unchanged.

## Ryan Xu’s rational and radical packings

- **[ry-xu square packing 2026]** — Ryan Xu’s complete packing reports, pinned at
  `8dc415296f697f5140caea27c7a0193d52deb4e6`;
  [packet](web/ry-xu-new-packings-2026-10-08/README.md).
  All 25 rational certificates have complete exact finite-feasibility replay (T-125).
  The separate undilated n = 51 construction in $Q(\sqrt 2)$ is confirmed by T-126. The
  atlas selects 17 rational packings and that radical construction; eight rational
  certificates remain as nonselected evidence.
  Native exact checks find 119 touching pairs at n = 51; the source’s count of 191
  remains unconfirmed.
  These results establish finite upper bounds, without local or global optimality.
  The packet preserves factual inputs and credits Xu’s direction and LLM assistance; it
  does not treat the unlicensed source programs as a licensed software bundle.

- **[Gupta rational refinements 2026-10-08]** — Siddharth Gupta’s seventeen complete
  rational source cases at `9643cb5a78c1d4dcfc867c80a6920c3a6219d05a`; fourteen selected
  finite upper-bound improvements and three withdrawals, T-127 at V3/C3.
  [Factual packet](web/gupta-square-packing-refinements-2026-10-08/README.md).
  Independently re-implemented deciding code verified every complete source certificate
  and full-roster control; actual private custody admitted the complete retained
  inputs/results without repeating geometry.
  These results establish finite feasibility, not optimality or human oversight.
  SQUISH credit remains with Nate Chaoweeraprasit, and Evan Daniel’s optimizer is
  credited. Unlicensed programs/prose remain hash-pinned; the solver MIT notice is not
  treated as a bundle licence.

## Exact-Root Report for n68, v1.2

**[Rehwaldt n68 exact-root report v1.2]**: Seth Rehwaldt after Couzo and earlier
contributors, with OpenAI Codex assistance.
The [authored packet](web/rehwaldt-n68-exact-root-2026-10-08/README.md) records
exact-root feasibility and restricted-family attainment at pinned revision
`495238e3d5a542008ff2f01a1dbbb78527cbe732`. Both claims remain unconfirmed here; the
earlier finite rational T-118 result remains unchanged.
Complete original custody is preserved outside live Git; public files contain attributed
factual metadata and external-byte identities only.

## Reported Fine-Net Lower Bounds

**[wand125 fine-net lower bounds 2026-10-08]**: wand125, using the project’s maintained
geometric kernel, reports seven finer-net measure certificates for n19, n20, n26, n27,
n28, n29 and n31. The
[authored factual packet](web/wand125-fine-net-lower-bounds-2026-10-08/README.md)
records the reported bounds and complete source references.
Independent whole-net replay and controls remain pending.

**[wand125 fine-net n29 2026-10-10]**: wand125’s later n29 certificate,
`mixed_n29_L582`, reports $s(29) \ge 291/50 = 5.82$ on the same 2,073-direction net,
superseding the 1163/200 above.
The [authored factual packet](web/wand125-fine-net-n29-2026-10-10/README.md) pins
revision `22a23c8` and its release asset by digest, with the maintained premise check
and a diagnostic eight-direction sample.
A complete replay and whole-net controls remain pending.

- **[Couzo exact refinements 2026-10-08]** — Francisco Couzo’s eight complete rational
  certificates and separate decimal context poses; T-128 remains V0/C0 pending
  historical source-house integration and confirmation.
  All 24 native jobs completed their finite-feasibility and control outcomes in 6.64
  wall minutes; actual private-worker custody passed complete stored-input and
  mutation-restoration checks.
  [Factual packet](web/couzo-exact-refinements-2026-10-08/README.md).
  Ryan Xu, Nate Chaoweeraprasit, Siddharth Gupta, David Ellsworth and Evan Daniel
  receive the source’s construction/refinement credits; no optimality is asserted.

- **[Daniel dated certificates 105 and 130 2026-10-07]** — Evan Daniel’s complete dated
  certificate reports and matching inputs for Francisco Couzo constructions at 105 and
  130, pinned at 7eef24f.
  [Historical source packet](web/evand-batch-105-130-2026-10-07/README.md).
  T-129 records V0/C0/S1; both sides are superseded by smaller currently verified
  bounds. Code is MIT; batch data credits Joshua Levy and this project under CC BY 4.0.
  No geometry replay or selected-case change.

- **[Daniel dated certificate 292 2026-10-07]** — Evan Daniel’s complete dated
  certificate report and matching input for Francisco Couzo’s 292 construction, pinned
  at f58a017. [Historical source packet](web/evand-batch-292-2026-10-07/README.md).
  T-129 records V0/C0/S1; its side is superseded by the current verified bound.
  Code is MIT; batch data credits Joshua Levy and this project under CC BY 4.0. The
  [separate wrapper correction](web/evand-batch-wrapper-2026-10-07/README.md) is pinned
  at cca7bf1; its reported rerun earns no replay credit here.

- **[Couzo extended-range reports 2026-10-08]** — Francisco Couzo’s twenty complete
  decimal poses beyond n324, retained as numerical facts and Git custody metadata.
  [Source packet](web/couzo-extended-reports-2026-10-08/README.md).
  All twenty remain author reports outside the standing-case corpus; no result row,
  geometry replay, selected bound or verification from the separate issue451
  certificates. Raw upstream text, SVGs, prose and programs remain outside Git under the
  existing retention policy; no redistribution permission is asserted.
  Since 2026-10-09 its $n = 375$ and $378$ reports are dated history, superseded in the
  source register by the later reports below.

- **[Couzo extended-range updates 2026-10-08]** — Francisco Couzo’s later decimal poses
  at $n = 375$ and $378$, pinned at 2d32a6e and retained as numerical facts and Git
  custody metadata. [Source packet](web/couzo-extended-updates-2026-10-08/README.md).
  Each side is below the same count’s ffd900d report, by exact comparison of the printed
  decimals; both remain author reports outside the standing-case corpus, with no result
  row, geometry replay or selected bound.
  No upstream byte is retained, and no redistribution permission is asserted.

- **[Couzo follow-up refinements 2026-10-08]** — Francisco Couzo’s five follow-up exact
  rational certificates at 84, 86, 105, 175 and 270, pinned at 2d32a6e and kept as
  derived exact facts with the complete pinned tree; no upstream byte is retained.
  [Derived packet](web/couzo-followup-refinements-2026-10-08/README.md).
  T-130 remains V0/C0: all five positives passed both maintained exact routes and both
  routes refused all ten controls, while independent review, historical source-house
  integration and confirmation remain pending.
  Ryan Xu, Evan Daniel and David Ellsworth receive the source’s seed and refinement
  credits; no optimality is asserted.

## Evan Daniel’s record-hunt certificates, 9 October 2026

**[Daniel record hunt 2026-10-09]**: Evan Daniel’s exact rational certificates for n =
132 and 155 from his `hunt1` record hunt, pinned at
`e0081804736a4613c2cf44c693ef1afe92518927` and retained under the source’s MIT licence
with their KKT points, inputs and solver reports;
[packet](web/evand-record-hunt-2026-10-09/README.md).
Both project exact routes accept both certificates and refuse all four controls.
T-131 records the n = 132 side at V0/C0, pending independent review and adoption.
The n = 155 side equals Couzo’s earlier issue451 certificate (T-128), with which it
shares 152 of 155 exact poses, differing only in the free and flat-motion squares the
source’s report lists; it is recorded as an evidence update to T-128. The source credits
Couzo’s and Chaoweeraprasit’s packings as starting points and discloses Claude
assistance under Daniel’s direction.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
