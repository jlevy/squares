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
**PDF SHA-256:** `f2034705c8c35c2bd6eaf0c075a3c45fe84d1bc73e75b839af8fd5d406129878`
**Raw OCR:** Tesseract 5.5.0 English OCR of 300 dpi page images, preserved without
manual correction in
`stromquist-1984-packing-unit-squares-inside-squares-iii-cases-through-65-and-gardner-conjecture.raw.md`
(`21ed36dfbcb4bd31afaace1ef4bba60a66583e42787d6eb1ca5de39d6dc2eb28`).

## Results and Page Map

- pp. 1–6: best-known packings for selected `n ≤ 65`, including then-new packings
  for `n = 18` and `n = 26`
- pp. 6–10: the `n = 11` argument restricted to boxes oriented at `0°` or `45°`
- pp. 10–12: a rectangle-packing digression and asymptotic results
- p. 13: references

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
