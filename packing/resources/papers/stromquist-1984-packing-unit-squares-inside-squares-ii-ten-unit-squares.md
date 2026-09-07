# Packing Unit Squares Inside Squares, II (Ten Unit Squares)

> ⚠️ **Cleaned reading aid, not a transcription.** This memorandum is an
> image-only scan. The notes below were checked against rendered pages, but they do not
> reproduce the proof. Read the PDF for every argument, formula, and figure. The
> adjacent `.raw.md` is unedited OCR and is not mathematical ground truth.

**Author:** W. R. Stromquist
**Document:** Daniel H. Wagner, Associates internal memorandum to the 450 File
(Professional Leave)
**Date:** October 15, 1984
**Source:** https://www.walterstromquist.com/papers/squares2.pdf
**Archived:** 2026-08-24
**Pages:** 15
**Raw OCR:** Tesseract 5.5.0 English OCR of 300 dpi page images, preserved without
manual correction in
`stromquist-1984-packing-unit-squares-inside-squares-ii-ten-unit-squares.raw.md`.

## Result and Page Map

The memorandum proves the exact value
`s(10) = 3 + (1/2)sqrt(2)`, approximately `3.707`. As in the first memorandum, a
**block** is the open interior of a square with side greater than 1.

- pp. 1–2: statement of the `n = 10` result and three optimal packings
- pp. 2–10: four nonavoidance lemmas
- pp. 10–15: the main proof by forced incidences and point counting

This memorandum does not discuss `n = 11`. Its Figure 14 on p. 14 is a 13-point
contradiction used inside the `n = 10` proof; despite the shared figure number, it is
not the Figure 14 configuration in Stromquist's 2003 paper and supplies no repair for
that later argument.

## Forced Incidences Before the Final Cover

Section 2 begins with ten unavoidable points and ten hypothetical blocks (p. 10,
Figures 8–9 on p. 11). Every block must therefore contain exactly one point.
Stromquist repeatedly changes the cover to force additional incidences:

- Replacing the two inner points I and J by `U = (1.4,s/2)` and
  `V = (s-1.4,s/2)` forces these replacement points into the I- and J-blocks.
- Replacing `B = (s/2,.97)` by `W = (s-1.96,.75)` forces W into the B-block.
- Replacing A by `(1,1.2)` and `(.788,1)` forces at least one of the two into
  the A-block (Figure 11, p. 12).

The last disjunction, combined with nonoverlap and Lemma 4, forces the H-block
to intersect the short segment from `(1,2)` to `(.9,2.12)` (p. 13). Symmetry gives
eight such occupied points. Their exact locations need not be fixed: the required
distances to their neighbors and the container center are all below 1
(Figures 13–14, p. 14; conclusion on p. 15).

Those eight points, the four original corner points, and the center form a final
thirteen-point cover. Every point except the center is denied to the two inner
blocks; the two blocks cannot both contain the center. The method therefore uses
point ownership, alternative covers, and points chosen from forced segment
intersections. The ten-point cover alone would not give the contradiction.

## Source Formula Notes

The middle row of the Lemma 3 table (p. 6) uses
`a = 1/2 + sqrt(2)/4`, `b = .97`, and prints the stationary angle `39.514°` with
`f(theta) = .9722`. This is a different parameter value from
`a = sqrt(4/5)` in the middle row of the 2003 paper's Lemma 4 table; it does not
correct that later row by substitution.

The typed formula under Figure 6 on p. 8 has `sin(theta) + cos(theta)` in its
denominator. Equation (2) on p. 7 and the handwritten formula in Figure 6 use the
product `sin(theta) cos(theta)`, consistent with the cross-section derivation in
Memo I, pp. 5–8. The p. 8 typed denominator should therefore be read as a local
typesetting slip, not as a second formula.

All 15 pages were visually reviewed on 2026-09-07. These source comparisons do
not independently verify the numerical estimates or the complete proof. The PDF
and raw OCR are unchanged.

## Extraction Limits

The PDF contains scanned page images and no usable text layer: `pdftotext` emits only
one page-break byte per page, with no text. OCR is adequate for prose search, but it
confuses inequalities, radicals, fractions, subscripts, degree symbols, and diagram
labels. Page breaks in the raw OCR are form-feed characters followed by newlines.
Check hits against the corresponding PDF page.

---

*Retained for private research use from the author's official publication archive.*

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
