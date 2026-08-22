# Inefficiency in Packing Squares with Unit Squares

**Authors:** K. F. Roth and R. C. Vaughan
**Affiliation:** Department of Mathematics, Imperial College of Science and Technology, Huxley Building, Queen's Gate, London SW7 2BZ
**Venue:** *Journal of Combinatorial Theory, Series A* **24** (1978), 170–186
**Received:** 1 November 1976
**Communicated by:** the Managing Editors
**Source:** https://www.sciencedirect.com/science/article/pii/0097316578900055
**Archived:** 2026-08-22
**Extraction:** `pdfminer.six` from the original PDF, preserved alongside as
`roth-vaughan-1978-inefficiency-packing-squares.raw.md`.

---

> ⚠️ **Partial transcription — front matter only.**
> This paper is a 1978 scan and the OCR of its body is heavily degraded: subscripts,
> superscripts and the interval notation of Sections 2–7 do not survive extraction in a
> trustworthy form. Transcribing them would mean reconstructing mathematics rather than
> reformatting it, which this archive's policy forbids.
>
> What is transcribed below is the abstract, introduction and **Theorem**, which were
> read directly from the rendered page image and are reproduced verbatim.
> That is the part the research documents cite.
> For anything in Sections 2–7, **read the PDF**; do not rely on the `.raw.md`, which is
> retained as an extraction record rather than as usable text.

## Abstract

It is shown that, in packing a square of side `n + ½` with unit squares, the wasted space
always has area `≫ n^{1/2}`. This answers a question of Erdős and Graham.

## 1. Introduction

Following Erdős and Graham [1] we define, for each real number `α ⩾ 1`,

```
w(α) = α² − sup_𝒜 |𝒜|,                                    (1)
```

where `𝒜` ranges over all packings of unit squares into a given square `S(α)` of side `α`
and `|𝒜|` denotes the number of unit squares in `𝒜`. They show that `w(α) = O(α^{7/11})`
(Montgomery has an unpublished argument which enables him to replace the
`7/11 = 0.636363…` by `(3 − √3)/2 + ε = 0.633974… + ε`), but are unable to rule out the
possibility that `w(α) = O(1)`. They also speculate that the correct bound is
`O(α^{1/2})`. We are dubious as to the validity of such a small bound, but are unable to
prove that it is false.
However, we are able to show that if true, then it is essentially best possible.

**THEOREM.** *Suppose that* `α(α − [α]) > 1/6`. *Then*

```
w(α) ≫ (‖α‖ α)^{1/2}
```

*where* `‖α‖` *denotes the distance of* `α` *from the nearest integer.*

We remark that if `α(α − [α]) ⩽ 1/6`, then

```
α² − [α]² ⩽ 2α(α − [α]) ⩽ ⅓
```

so that `sup_𝒜 |𝒜| = [α]²`. Thus `w(α) ≫ α(α − [α])` and this is essentially best
possible. We also observe that if `α(1 + [α] − α) ⩽ 1/6`, then

```
1 > α² − ([α] + 1)² + 1 = 1 − (α + [α] + 1)(1 + [α] − α) ⩾ ½.
```

Hence the number of squares in any packing `𝒜` is at most `([α] + 1)² − 1`, and
`w(α) ⩾ ½ ⩾ (α(1 + [α] − α))^{1/2}`. Thus we assume henceforward that

```
‖α‖ α² > 1/6.                                             (2)
```

## Sections 2–7

**Not transcribed** — see the banner above.
Section 2 is *Notation and Terminology*; the remaining sections develop the proof of the
Theorem. Read the PDF for these.

## References

1. P. Erdős and R. L. Graham, On packing squares with equal squares, *J. Combin. Theory
   Ser. A* **19** (1975), 119–123.

---

*Copyright © 1978 by Academic Press, Inc. Retained for private research use.*
