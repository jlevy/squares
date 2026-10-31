# Mixed cover format v1 (points + segments + polygons), 2026-09-27

Shared interface between the cover side (agent A) and the checker side (agent B).  Extends
`certificates/FORMAT.md` (read it first).  Plain text, whitespace-separated integers, `#` comments allowed
to end of line.  Everything exact.

```
mixed 1
s_num s_den        # container [0, s_num/s_den]^2 (here s = m, s_den = 1)
D                  # coordinate denominator: every coordinate is X/D
W                  # weight denominator: every mass is w/W
np                 # number of point masses
X Y w              # np lines: point (X/D, Y/D) carries mass w/W
ns                 # number of segments
X0 Y0 X1 Y1 w      # ns lines: total mass w/W spread UNIFORMLY (by length) on the closed segment (X0,Y0)-(X1,Y1)
npg                # number of polygons
k w X1 Y1 ... Xk Yk   # npg lines: convex polygon, vertices CCW, total mass w/W spread UNIFORMLY (by area)
```

Masses are given as **totals**, so every mass-in-square is rational: a segment contributes
`w/W · |seg ∩ Q| / |seg|` (the ratio is rational: parametric fraction), a polygon `w/W · area(P ∩ Q)/area(P)`.
Degenerate pieces (zero-length segment, zero-area polygon) are invalid; use a point.  All pieces in `[0,s]^2`,
all `w >= 0`.  A plain `certificates/FORMAT.md` file is a mixed file with `ns = npg = 0`.

**What the file asserts.**  For every closed unit square `Q ⊂ [0,s]^2`, at every centre and angle,
`μ(Q) >= 1`, where `μ` is the sum of the point, 1-D (segment) and 2-D (polygon) measures, `Q` closed:
a segment lying on an edge of `Q` counts in full.  With `μ([0,s]^2) = total < n` this proves `s(n) >= s`,
by the same argument as `certificates/FORMAT.md` (shrunken concentric closed unit squares are pairwise
disjoint, so `Σ μ(Q_i) <= μ(∪ Q_i) <= total`); the Lean `packing_le_weight` needs generalising from finite
point sets to finite sums of such measures (not part of this task).

**Target.**  `s(21) = 5`: a valid mixed cover of `[0,5]^2` with total `< 21`.  Calibration: `m = 4` (`s(13) = 4`,
total `< 13`; shipped point cover `12.955972`, lightest certified point cover `12.732248`, `M4_MARGIN.md`).

**Why this might help** (hypothesis to test, not a fact): 77 % of the `s(32)` cover's weight sits on interior grid
lines as 70–150 points per unit; the `m = 4/5` validity losses (`1.4–2.9 %`) are near-tile poses at `θ ≲ 1/D` that
slip between discrete line points, and the germ blow-ups in the exact checkers (S32_EXACT §1–2, S32_SHIFT §1) are
chains of discrete line points.  A uniform line density has no gaps.

Tooling contract: a reader `search/mixed_cover.py` (agent A writes it first, in the first hour; agent B imports it):
`load(path) -> dict(s, D, W, points, segments, polygons)` with exact integers, `total(cover) -> Fraction`,
`validate(cover)` (well-formedness), `mass_in_square_float(cover, cx, cy, theta)`.  Either agent may fix bugs in it;
keep the signatures.
