# Packing Unit Squares Inside Squares, I (Six Unit Squares)

> ⚠️ **Cleaned reading aid, not a transcription.** This memorandum is an
> image-only scan. The notes below were checked against rendered pages, but they do not
> reproduce the proof. Read the PDF for every argument, formula, and figure. The
> adjacent `.raw.md` is unedited OCR and is not mathematical ground truth.

**Author:** W. R. Stromquist
**Document:** Daniel H. Wagner, Associates internal memorandum to the 450 File
(Professional Leave)
**Date:** September 11, 1984
**Source:** https://www.walterstromquist.com/papers/squares1.pdf
**Archived:** 2026-08-24
**Pages:** 19
**Raw OCR:** Tesseract 5.5.0 English OCR of 300 dpi page images, preserved without
manual correction in
`stromquist-1984-packing-unit-squares-inside-squares-i-six-unit-squares.raw.md`.

## Result and Page Map

The memorandum proves that six unit squares fit in a square of side 3 but not in a
smaller square. It works with open **blocks** whose sides are greater than 1 so that the
impossibility statement is equivalent to the lower bound.

- pp. 1–3: formulation, preliminary definitions, and the main theorem
- pp. 3–12: nonavoidance lemmas and the cases with fewer than six squares
- pp. 13–19: the `n = 6` proof, including the key-point allocation and Figures 10–15

The introduction says that later memoranda will provide partial `n = 11` results, but
this first memorandum contains no unrestricted `n = 11` proof. Its Figure 14 on p. 19
is the remaining allocation of key points to six blocks; it is unrelated to Figure 14
in Stromquist's 2003 paper.

## The Helper Argument for Six Squares

The proof combines two point covers with a restriction on which blocks can coexist.
Lemma 6 (p. 11) gives an eight-point cover: the boundary points of the
`{1, 3/2, 2} × {1, 3/2, 2}` grid, omitting its center. Section 3 adds the center
`E = (3/2, 3/2)` and names the nine points `A` through `I` in row order from bottom
left (p. 13, Figure 10 on p. 14).

If six disjoint blocks existed, at least three would contain just one of these
points. Stromquist calls such a point isolated. The center cannot be isolated,
because the eight-point cover still applies. Lemma 8 (pp. 13–17) shows that two
adjacent key points, such as `A = (1,1)` and `B = (3/2,1)`, cannot both be isolated.
The proof compares the lengths cut from the two segments `[(1,0), A]` and `[A, B]`:
the B-block leaves less than `1/2` available near A, while the A-block would need
more than `1/2`. The raw OCR repeatedly misreads this fraction as `2`.

On p. 18, the memo reduces the remaining allocation to Figure 14, up to symmetry.
The isolated points are B, G, and I; one block contains E and H. The next geometric
step forces that block to contain `J = (1,1.7)` and `K = (2,1.7)` as well. Lemma 7
(p. 12) supplies a second unavoidable set:

```text
{G, H, I, J, K, E, (1,.9), (2,.9)}.
```

Four of these eight points are in the same block, leaving room for at most four
other blocks. This is the final contradiction. A reusable version must establish
the geometric restriction on joint allocations before using the second cover.
The memo does not state or prove a general impossibility theorem for pure
point-counting proofs, and it does not identify an intern.

## Source Formula Note

On p. 8, after rewriting the cross-section formula as
`f = 2(z-a)/(z²-1)` with `z = sin(theta) + cos(theta)`, the printed sentence calls
it increasing in z. For the displayed domain `a ≤ 1`, `z > 1`, its derivative is

```text
-2((z-a)² + 1-a²)/(z²-1)² < 0.
```

Thus decreasing is the correct direction; the stated minimum at `theta = 45°`
agrees with that direction. This is a local reading note, not an independent
verification of the complete proof. All 19 pages were visually reviewed on
2026-09-07; the PDF and raw OCR are unchanged.

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
