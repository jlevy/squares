# Packing Unit Squares Inside Squares, III

## Cases with n ≤ 65 and Martin Gardner's Conjecture for n = 11

> ⚠️ **Cleaned reading aid, not a transcription.** This memorandum is an
> image-only scan. The notes below were checked against rendered pages, but they do not
> reproduce the proof. Read the PDF for every argument, formula, and figure. The
> adjacent `.raw.md` is unedited OCR and is not mathematical ground truth.

**Author:** W. R. Stromquist
**Document:** Daniel H. Wagner, Associates internal memorandum to the 450 File
**Date:** November 15, 1984
**Source:** https://www.walterstromquist.com/papers/squares3.pdf
**Archived:** 2026-08-24
**Pages:** 13
**Raw OCR:** Tesseract 5.5.0 English OCR of 300 dpi page images, preserved without
manual correction in
`stromquist-1984-packing-unit-squares-inside-squares-iii-cases-through-65-and-gardner-conjecture.raw.md`.

## Results and Page Map

- pp. 1–6: best-known packings for selected `n ≤ 65`, including then-new packings
  for `n = 18` and `n = 26`
- pp. 6–10: the `n = 11` argument restricted to boxes oriented at `0°` or `45°`
- pp. 10–12: a rectangle-packing digression and asymptotic results
- p. 13: references

## Historical Small-Case Evidence

Table 1 (p. 2) and Figures 3–4 (p. 5) introduce two constructions as new:
`n = 18` at side `(7 + sqrt(7))/2`, with tilt about `24.295°`, and `n = 26`
at side about `5.650629`, with tilt about `27.583°`. These are construction
claims, not proofs of optimality. The figures compare both with Göbel's
earlier `0°`/`45°` packings.

**Verification follow-up, 2026-09-07:** the
[exact reconstruction](../../cases/stromquist/memo3_n26.py) verifies all 26 unit squares,
every wall, and all 325 pairs at the unique real root of
`s^3 - 14s^2 + 67s - 112`, approximately `5.650629191439388`.
The coordinate formulas and cubic come from Ellsworth's 2023 reconstruction, rather
than an equation printed in this memo.
Its six offset dominoes match Figure 4(b).
[Ellsworth's historical catalogue](https://kingbird.myphotos.cc/packing/squares_in_squares__compared.html)
already credits Stromquist in 1984 and records Friedman's smaller 1997 side
`(7 + 3sqrt(2))/2`.
The [dedicated source review](../../../docs/project/research/research-2026-09-07-stromquist-n26-verification.md)
also resolves the `n = 18` history as an independent rediscovery, preserving
Hämäläinen's 1980 priority. The original scan and raw OCR remain unchanged.

For `n = 11`, the memo credits Mats Gustafsson and Magnus Thulin's packing,
reported by Gardner in November 1980 (pp. 2–4). It says they learned the
problem through the Swedish company periodical *Ronden*. This preserves the
memo's historical attribution; it does not establish priority over Trump's
1979 construction, distinguished in the maintained research report.

On p. 6, Stromquist says the cases `n = 14, 15, 24` can be settled by elementary
means, but provides no proofs for them here. The footnote credits G. Bajmóczy
of Budapest with the `n = 7` result, through Göbel. These are useful primary
records of earlier claims; the memo should not be cited as a complete proof of
the three larger cases.

The discussion of `n = k²+k` (pp. 3 and 6) asks when a square smaller than the
next integer side becomes possible. It records Graham's construction at
`n = 1560` and suspicion that `n = 90` may work. These are the state of the
problem in 1984, not current thresholds.

## Restricted Eleven-Square Argument

On p. 7 the theorem sets
`s = 2 + (4/3)sqrt(2)`, approximately `3.886`, and rules out eleven pairwise
nonintersecting boxes only when every box has orientation `0°` or `45°`. The proof
uses the following 12 marked points, with three points grouped under the label `A`:

```text
A = {(s-3, 1), (s-3, s/2), (1.3, 1.5)}
B = (1, s-1)        C = (s/2, s-.8)      D = (s-1, s-1)
E = (s-.8, s/2)     F = (s-1, 1)         G = (s-2, .8)
H = (1.7, 2.2)      I = (2.2, 2.2)       J = (2.2, 1.7)
```

Figures 7 and 8 on p. 9 display this point set and the distance graph used for the
restricted proof.

The preliminary ten-point set is in Figure 5 (p. 8). Eleven disjoint boxes
would force one box to avoid it. Such an avoiding box cannot be axis aligned;
at `45°`, it must occupy a restricted region up to symmetry and contain all
three A-points (p. 7, Figure 6 on p. 8). The final twelve-point cover then
allows at most `1 + 9 = 10` boxes. This is the same kind of geometric
precondition followed by point counting that appears in Memo I.

## Audit of the Later Unrestricted Bound

Memo III does **not** supply a proof of the unrestricted result later published as
Theorem 2 in 2003, and it does not supply or repair that paper's Figure 14 cover.

The only unrestricted statement is a parenthetical aside on p. 10. It begins,
"By reducing the value of s, essentially the same argument can be made to work for
general packings." It then states that 11 unit squares cannot be packed when

```text
s < 2 + (4/5)sqrt(5) ≈ 3.789,
```

which equals `2 + 4/sqrt(5)`. The memo gives no unrestricted point coordinates, no
replacement for the restricted Figure 7/8 cover, no localization proof, and no lemma
routing for this assertion. In particular, neither `.79` nor the later point
`G = (.8, 1.85)` appears in the page-checked `n = 11` argument.

The earlier two memoranda each have a local Figure 14, but those figures concern the
`n = 6` and `n = 10` proofs. Memo III has no Figure 14. None of the three memoranda
contains a coordinate correction for the printed 2003 configuration.

## Other Results and Review Scope

The rectangle example (pp. 10–11) places four unit squares in a rectangle of
height `1.9` and width approximately `3.9475`, using a tilt about `39.63°`.
The memo says a `0°`/`45°` packing cannot fit in the slightly wider `1.9 × 3.95`
rectangle. It supplies a figure and an angle equation; it does not develop an
independent global optimality proof for rectangles.

The asymptotic section (pp. 10 and 12) summarizes Erdős–Graham,
Montgomery, and Roth–Vaughan. It is a secondary account of those results;
the cited originals govern their constants and hypotheses. The closing
paragraph proposes a possible fourth memo on asymptotics or computerized
search. Only I, II, and III are linked on the author's publication page.

All 13 pages were visually reviewed on 2026-09-07, completing a review of all
47 pages in the three memoranda. This is a source review, not an independent
verification of their complete proofs. The PDF and raw OCR are unchanged.

## Extraction Limits

The PDF contains scanned page images and no usable text layer: `pdftotext` emits only
one page-break byte per page, with no text. OCR is adequate for prose search, but it
corrupts both formulas on pp. 7 and 10 and several coordinates on p. 7. The formulas
and coordinates above were read from the rendered pages. Page breaks in the raw OCR
are form-feed characters followed by newlines. Check every other mathematical hit
against the corresponding PDF page.

---

*Retained for private research use from the author's official publication archive.*

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
