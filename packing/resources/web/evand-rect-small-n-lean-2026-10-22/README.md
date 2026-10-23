# Daniel’s Lean Proofs for Two to Five Squares in a Rectangle, Pinned 2026-10-22

This packet pins the part of [evand/square-packing](https://github.com/evand/square-packing)
at `7051f4e` that bears on squares in a square: Evan Daniel’s Lean proofs, from 21
October 2026, of exactly which rectangles $[0,w] \times [0,h]$ hold two, three and four
unit squares, and of the four-point lower bound for five. At $w = h$ they give
$s(2) = s(3) = s(4) = 2$ and $s(5) = 2 + 1/\sqrt{2}$, values the record holds by
published proofs (Göbel 1979; Friedman’s survey DS7): a second machine route to them,
after chelokot’s Lean proofs, which the
[chelokot small-n packet](../chelokot-small-n-lean-2026-09-05/README.md) retains.
Rectangles themselves are outside this record, and this packet keeps only what the
square case needs.

Its proposed Frontier key is **[Daniel small-n rectangles Lean 2026-10-22]**. No issue
asked for it: the intake reads of 22 October found it, and bead `think-7l2j` owns its
import with chelokot’s; which kind of register entry the two take waits on the owner
(`think-4o9c`). The claims below are stated as the source states them; nothing
here has built the proofs, and no review has read them yet.

## Source and Pin

| Field | Value |
| --- | --- |
| Source | <https://github.com/evand/square-packing> |
| Revision | `7051f4eabf7f9b2509ad1e7cc296f57d19482027`, tree `95e42aeeee83281d5f963da6f8d0ce70d1515956`, the head that the intake read of 22 October stopped at |
| Committed | 2026-10-22T01:54:20Z (19:54:20 on 21 October by the author’s clock, `-06:00`), by Evan Daniel |
| The theorems’ commits | `rect2_iff` at `74937b01` (2026-10-21T04:34:52Z), `rect3_iff` at `b7d9b1bf` (14:23:57Z), `rect4_iff` at `ee4d2cce` (16:05:00Z), and `rect5_pts_lower` with `rect5_upper` at `e96ab691` (20:10:45Z) |
| Licence | MIT, “Copyright (c) 2026 Evan Daniel” (`LICENSE`) |
| Retrieved | 2026-10-23T06:23Z, a blobless clone, head `7982d7a9`, with a sparse checkout of the pin |
| Pinned subtree | 20 files, 265,989 bytes, each by SHA-256 in [`acquisition/upstream-subtree.sha256`](acquisition/upstream-subtree.sha256) |
| Retained here | 14 files, 224,993 bytes, byte-identical under [`square-packing/`](square-packing/) |

## Credit and AI Assistance, as the Source States Them

The README at the pin credits each region’s boundary and constructions to Erich
Friedman’s *Math Magic* of June 2010 (the tilted pieces to Maurizio Morandi, with
Stenlund, Cantrell and Hosono among the solvers) and claims the proofs as new.
`Rect5Pts.lean` credits the four-point bound at $a = b$ to Göbel 1979 and piece 4.5 of
$S_4$ to Friedman. `literature/s5-proofs-2026-10-21.md`, the source’s survey of how
$s(5)$ has been proved, finds that “every proof found is the same idea: a 4-point
unavoidable set plus pigeonhole”, and that chelokot’s `s5_eq_goebel` formalized
$s(5)$, lower bound included, before this work. `CREDITS.md` says the repository’s work
was produced by Claude (Anthropic) under human direction.

## What Is Retained

Retained byte-identical, under `square-packing/`:

- **The theorem modules** `lean/Sqpack/Rect.lean` (`RectPacks`, `rect2_iff`),
  `RectChain.lean`, `Rect3.lean` (`rect3_iff`), `Rect4Core.lean` and `Rect4.lean`
  (`rect4_iff`), `Rect5Pts.lean` (`rect5_pts_lower`) and `Rect5Pack.lean`
  (`rect5_upper`);
- **the root module** `lean/Sqpack.lean` and **the axiom probe** `lean/Axioms.lean`;
- **the notes that derive them**: `literature/s5-proofs-2026-10-21.md`,
  `literature/rectangles-small-n-2026-10-20.md`, `search/rectfront/RECTFRONT.md` and
  `search/rectfront/r5pts/R5PTS.md`, the paper proofs behind `Rect5Pts.lean`;
- the root `README.md`.

Pinned by digest only: `lean/Sqpack/Basic.lean` and the three build pins, byte-identical
in the [7 October evand packet](../evand-exact-and-local-reports-2026-10-07/README.md),
and `LICENSE` and `CREDITS.md`, byte-identical in the
[12 October exact-data packet](../evand-exact-data-2026-10-12/README.md).
[`acquisition/sources.json`](acquisition/sources.json) records each file, and from
`packing/`,
`uv run --frozen --all-extras --group dev python -m devtools.acquire_source evand-rect-small-n-lean-2026-10-22 --checkout CHECKOUT`
rebuilds the packet; `--check` re-derives it without a checkout.

[`receipts/lean-closure.json`](receipts/lean-closure.json), written by
`devtools.lean_closure`, is the import closure of the five theorem modules at the pin:
eight project modules, 137,281 bytes, `Mathlib` the only import outside them, no
generated module, and no `sorry`, `axiom`, `native_decide` or other kernel escape in
their code. The build pins are `leanprover/lean4:v4.33.1` and Mathlib `0df444a3`.

Left out: the rest of the $R_5$ development (`Rect5`, `Rect5Line`, `Rect5Low`, `Rect5Mid`, the
`Rect5Hi*` modules with about 14,000 lines of generated polynomial certificates,
`Rect5Final`, `Rect5Iff` and `Rect5Thm`, whose `rect5_iff` is the exact region), which
the square case does not need; and the strip work after the pin. Both are rectangles,
outside this record.

## The Claims, as the Source States Them

`Rect.lean` defines, in namespace `SquarePacking`,

```lean
def rbox (w h : ℝ) : Set (ℝ × ℝ) := {p | 0 ≤ p.1 ∧ p.1 ≤ w ∧ 0 ≤ p.2 ∧ p.2 ≤ h}
def RectPacks (n : ℕ) (w h : ℝ) : Prop :=
  ∃ (ctr : Fin n → ℝ × ℝ) (ang : Fin n → ℝ), (∀ i, sq (ctr i) (ang i) 1 ⊆ rbox w h) ∧
    ∀ i j, i ≠ j → Disjoint (sqInt (ctr i) (ang i) 1) (sqInt (ctr j) (ang j) 1)
```

with `sq` and `sqInt` the closed and open squares of `Basic.lean`, so `RectPacks n s s`
says that $n$ closed unit squares, translated and rotated, lie in $[0,s]^2$ with
pairwise disjoint interiors. The theorems:

```lean
theorem rect2_iff {w h : ℝ} : RectPacks 2 w h ↔ 1 ≤ w ∧ 1 ≤ h ∧ (2 ≤ w ∨ 2 ≤ h)
theorem rect3_iff {w h : ℝ} : RectPacks 3 w h ↔ 1 ≤ w ∧ 1 ≤ h ∧
    ((2 ≤ w ∧ 2 ≤ h) ∨ 3 ≤ w ∨ 3 ≤ h ∨ (h < 2 ∧ 4 + 2 * Real.sqrt 2 ≤ w + 2 * h) ∨
      (w < 2 ∧ 4 + 2 * Real.sqrt 2 ≤ h + 2 * w))
theorem rect4_iff {w h : ℝ} : RectPacks 4 w h ↔ 1 ≤ w ∧ 1 ≤ h ∧
    ((2 ≤ w ∧ 2 ≤ h) ∨ 4 ≤ w ∨ 4 ≤ h ∨ (h < 2 ∧ Fried4 w h) ∨ (w < 2 ∧ Fried4 h w))
theorem rect5_pts_lower {a b : ℝ} (ha : 2 ≤ a) (hb : 2 ≤ b) (ha' : a < 2 * Real.sqrt 2)
    (hb' : b < 2 * Real.sqrt 2) (hab : a + b < 4 + Real.sqrt 2) : ¬ RectPacks 5 a b
theorem rect5_upper {w h : ℝ} (hw : 1 ≤ w) (hh : 1 ≤ h) (hc : … ∨ (2 ≤ w ∧ 2 ≤ h ∧ 4 + Real.sqrt 2 ≤ w + h) ∨ …) :
    RectPacks 5 w h
```

The source reports standard axioms only (the commit messages of `b7d9b1bf` and
`ee4d2cce`; `lean/Axioms.lean` prints each headline theorem’s axioms). No build log or
axiom output is published.

**What follows at $w = h$, read here and not stated in Lean.** No theorem states
`minSide` or $s(n)$:

- $s(2) = s(3) = s(4) = 2$: each `iff` gives `RectPacks n 2 2`, and refuses every
  $s < 2$, because then both sides are below 2, which excludes the first case, and the
  remaining cases need a side of at least 3 or 4, or, for $n = 3$, $3s \ge 4 + 2\sqrt{2}$,
  which fails for $s < 2$; for $n = 4$ the case `Fried4 s s` with $s < 2$ must be read
  from `Fried4`’s definition, which is the review’s.
- $s(5) = 2 + 1/\sqrt{2}$: `rect5_upper`’s case $2 \le w, h$, $w + h \ge 4 + \sqrt{2}$
  gives `RectPacks 5` at $w = h = 2 + 1/\sqrt{2}$, and `rect5_pts_lower` at $a = b$ refuses
  every $2 \le a < 2 + 1/\sqrt{2}$. A side below 2 is refused by `rect2_iff` applied to
  two of the five squares, a restriction no theorem in the closure states.

## The Build Plan, Priced

```sh
lake exe cache get
lake build Sqpack.Rect Sqpack.Rect3 Sqpack.Rect4 Sqpack.Rect5Pts Sqpack.Rect5Pack
lake env lean AXIOMS.lean    # #print axioms for rect2_iff, rect3_iff, rect4_iff, rect5_pts_lower, rect5_upper
```

accepted only with `propext`, `Classical.choice` and `Quot.sound`. It is eight modules
and no certificates: under 0.5 CPU-hours (an estimate from their size; the README gives
about 70 CPU-minutes for the whole $R_5$ theorem, generated certificates included), a
few GB of memory for `import Mathlib`, and about 10 GB of disk for the toolchain and
Mathlib `0df444a3`’s cache. It fits this lane’s 2 CPU-hour single run and this host’s
memory, and did not run because this host had 5.2 GB of free disk on 23 October. The
import bead holds it as a validation item.

## Limitations

- **Nothing was built or run here**, and the axiom sets are the source’s report.
- **The square-case values are read, not proved, from the rectangle theorems**, as the
  section above says; the review reads that step and `Fried4`.
- **No review has read the proofs.** The mathematical review of stage 4 starts from this
  packet.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
