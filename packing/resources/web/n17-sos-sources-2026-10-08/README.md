# n17 SOS Source Identity and Extraction Quality

**Captured:** October 8, 2026, PDT. **Status:** Original sources acquired; full raw page
coverage checked; selected mathematical pages compared visually.
The
[mathematical assessment](../../../../docs/project/reviews/review-2026-10-08-n17-global-optimization-and-sos.md)
records the implications for n17. This packet records extraction quality, not a solver
result or a claim that every formula has been transcribed correctly.

## Sources and Retention

| Source | Identity | Retention |
| --- | --- | --- |
| Blekherman, Parrilo and Thomas, editors, *Semidefinite Optimization and Convex Algebraic Geometry* | 2013 book; [MIT-hosted PDF](https://www.mit.edu/~parrilo/sdocag/MO13-Blekherman-Parrilo-Thomas.pdf), 487 PDF pages, 18,185,496 bytes | Original PDF and full raw extraction retained locally outside Git; source identity and quality audit retained here |
| Santiago Laplagne, *Facial reduction for exact polynomial sum of squares decompositions* | [arXiv:1810.04215v1](https://arxiv.org/abs/1810.04215v1), submitted October 9, 2018, 19 pages | [Original PDF](../../papers/laplagne-2018-facial-reduction-exact-polynomial-sos-1810.04215v1.pdf), [unedited raw extraction](../../papers/laplagne-2018-facial-reduction-exact-polynomial-sos-1810.04215v1.raw.md), [original TeX](../../papers/laplagne-2018-facial-reduction-exact-polynomial-sos-1810.04215v1.tex) and [source archive](laplagne-1810.04215v1-source.tar.gz) |

[source-audit.json](source-audit.json) records sizes, download identities, original-byte
SHA-256 values, extraction commands, page coverage, visual checks and source cautions.
The book PDF stays outside Git under
[OR-18](../../../../operating-rules.md#or-18-keep-bulk-data-out-of-git-and-never-bind-code-or-verdicts-to-a-git-commit-or-blob).
Its public source URL remains the retrieval location.
No bulk source was added to the branch and no snapshot cap was changed.

PDF creation timestamps do not identify publication dates: the book carries a 2013
copyright and a 2012 printer-proof footer, with 2023 PDF metadata; Laplagne’s pinned
2018 submission has 2021 PDF generation metadata.

## What the Extraction Checks Establish

Both `pdftotext -layout` extractions use Poppler 25.05.0, complete without extraction
errors, cover every PDF page, and contain no replacement characters.
Neither is a cleaned Markdown or LaTeX transcription.
Raw bytes remain unchanged.

| Check | Book | Laplagne |
| --- | ---: | ---: |
| PDF pages / nonempty raw page chunks | 487 / 487 | 19 / 19 |
| Non-whitespace control glyphs | 2,785 | 15 |
| Raw bytes | 1,947,879 | 62,596 |

The book’s raw prose supports searching.
Mathematical glyphs, powers, indices and matrix layouts require the original PDF. Visual
checks of PDF pages 65 and 131 (printed pages 49 and 115) confirm clear originals and
damaged text extraction.
There is no single printed-page offset: omitted blank pages change it.
The JSON contains the mapping ranges.
No independent extractor was already installed in the project environment; none was
installed and no OCR was needed for these clear PDFs.

Laplagne’s printed pages equal the PDF’s one-based pages.
Nine pages were checked visually.
Original TeX provides an independent equation-encoding cross-check; its title, author
and selected identities, matrix and long polynomial match the PDF. The original source
archive has two regular members, inspected before bounded extraction; no TeX or embedded
code was executed. All 15 raw control glyphs were identified as braces, parentheses or
proof squares. Superscripts and layout still require the PDF or TeX.

## Source Cautions

Laplagne’s Example 3.8 on page 9 repeats the derivative with respect to `x` three times
in both PDF and TeX. The page-15 polynomial `m2` uses `u,v` where surrounding branches
use `s,t`, also in both sources.
These are source cautions, not extraction corrections.
They remain unchanged and are not used as unchecked premises in the n17 assessment.
The TeX also contains an ordinal-character artifact after two partial-derivative
commands that is not visible in the PDF; the audit records its locations.

Mathematical claims in the assessment are checked at their cited PDF pages; page
coverage and zero replacement characters alone do not establish formula accuracy.
There is no whole-book corrected transcription or full-paper proof certification.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
