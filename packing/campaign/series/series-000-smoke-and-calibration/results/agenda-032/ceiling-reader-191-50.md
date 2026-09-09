# Agenda 032, ceiling reader: an independent exact decision of the 191/50 ceiling family

Retained replay report for
[X-023](../../../../explorations/X-023-three-losses-and-a-new-atom.md), written by a
Fable sub-agent on 2026-09-09 from the statement alone: the reader imports nothing from
`sqpack` and was written before the repository’s verifier was read.
The reader is promoted as `packing/devtools/independent_ceiling_reader.py`; its result
with the three negative controls is
[`ceiling-family-191-50-independent-reader.json`](ceiling-family-191-50-independent-reader.json).
The report is reproduced as delivered, with its own status labels.

Object: `ceiling-family-191-50.json`, SHA-256
`95cf06473f185764076d21021b75cc65962ef6b68dc717c045c2c7d76ae12427` (matches; the reader
refuses any other digest when asked).

## Findings

| # | Finding | Status |
| --- | --- | --- |
| 1 | K0: all 88 placements have side B = 9977/10000, weight 1/8 ≥ 0, and a half-tangent that is a net angle (44) or the mirror (1−t)/(1+t) of one (44); six net indices used: k = 0, 1, 3, 5, 99, 113 | EXACT |
| 2 | K1: all 352 corners lie in the closed container [0, 191/50]² | EXACT |
| 3 | K2: maximum depth over the container is exactly 1, attained at 2,892 of the 20,376 distinct arrangement vertices inside the container; all 20,376 decided in integer arithmetic, no float anywhere | EXACT |
| 4 | K3: total weight 88 × 1/8 = 11 = n | EXACT |
| 5 | D4-invariant under all eight symmetries about (191/100, 191/100), decided two independent ways (corner sets; (t, x, y) triples with the half-tangent action); 88 distinct squares forming 11 free orbits of size 8, weight 1 each, one per recorded support row | EXACT |
| 6 | The net is t_k = T k/180, T = 207107/500000, k = 0..180, strictly increasing | EXACT |
| 7 | Theorem (below): no D4-symmetric measure of mass < 11 covers every closed B-square at a net angle in [0, 191/50]²; the point-atom certificate method cannot certify s(11) ≥ 191/50 at B = 9977/10000 on this net, on any net containing the six angles, at any smaller B, or at any larger side | EXACT (given 1-5) |
| 8 | Vertex count agrees with the repository replay (20,376). Its “3,675 decided exactly” is the number its float screen sent to exact arithmetic; this reader has no screen and decides all 20,376. Different bookkeeping, no disagreement. The attaining count 2,892 is new | RECORD / EXACT |
| 9 | Negative controls: weights × 8/7 → depth 8/7, total 88/7, rejected on K2+K3; one centre shifted by L → rejected on K1; one half-tangent set to 1/3 → rejected on K0 (also K1, K2 with depth 9/8) | EXACT |
| 10 | Wall time 0.87 s for the decision (0.06 s enumeration, 0.70 s depth); 3.2 s with controls; replay recorded 2.5 s | CHECKED |
| 11 | Whether tau*(3.82) < 11 for a measure with no symmetry is untouched: the mirror placements make this a statement about D4-symmetric measures, which is what C1 imposes on every certificate anyway | OPEN (as before) |

## The theorem decided

Statement written from the docstring of `packing/src/sqpack/fractional/ceiling.py`; no
code from it was read before the reader was written.
Let μ be a D4-symmetric measure on [0, L]² with μ(Q) ≥ 1 for every closed B-square Q at
a net angle inside [0, L]². For a placement P with weight y_P: at a net angle μ(P) ≥ 1
directly; at a mirror angle its reflection σP in x = L/2 is a net-angle closed B-square
inside the container (σ-invariant), so μ(P) = μ(σP) ≥ 1. Hence

```
11 = Σ y_P ≤ Σ y_P μ(P) = ∫ depth dμ ≤ μ([0, L]²)
```

using y_P ≥ 0 (K0), depth ≤ 1 on the container (K2), placements inside the container
(K1). Every such μ has mass ≥ 11 = n, so no certificate (mass < n, D4-symmetric atoms,
C1-C5) exists at (L, B, net).
Transfers: to every net containing k = 0, 1, 3, 5, 99, 113 (a finer net’s covering
measure covers those squares); to every smaller shrink B' ≤ B (a concentric B'-square
inside a net-angle B-square is inside the container, so covering all B'-squares covers
all B-squares); to every larger side L' ≥ L by embedding the family in the *concentric*
sub-square of [0, L']², whose centre is the symmetry centre of a D4-symmetric measure at
side L' — the corner embedding would not do, since a restriction to a corner is not
D4-symmetric about the corner sub-square’s centre, and the mirror placements need the
symmetry. No transfer to larger B or to a coarser net; nothing about whether 11 unit
squares fit in side 191/50.

## Reader design

`packing/devtools/independent_ceiling_reader.py`. Standard library only; imports nothing
from `sqpack`. Run from `packing/`:

```
uv run --frozen --all-extras --group dev python -m devtools.independent_ceiling_reader --expect-sha256 95cf0647…e12427 --control --output RESULT.json
```

Exit 0 only when K0-K3 hold (and with `--control`, every control is rejected as
expected); 1 otherwise; 2 on a malformed or wrong-digest record.

- Geometry: t = p/q gives cos θ = (q²−p²)/(q²+p²), sin θ = 2pq/(q²+p²), a = (cos, sin),
  b = (−sin, cos) — the same convention as `model.rotation_from_half_tangent`, confirmed
  after writing. The square is |a·p − a·c| ≤ B/2, |b·p − b·c| ≤ B/2; each slab is scaled
  to integers lo ≤ Ax + By ≤ hi.
- Vertices: 352 edge lines + 4 walls, normalised by gcd and sign → 268 distinct lines;
  every pair solved by Cramer’s rule in integers: 33,444 non-parallel pairs, 20,376
  meeting inside the closed container, 20,376 distinct after dividing by gcd(X, Y, D).
  Parallel/coincident pairs skipped.
- Depth: membership of (X/D, Y/D) is the integer test lo·D ≤ AX + BY ≤ hi·D; depth is
  the `Fraction` sum of containing weights.
  Max over vertices = max over container: depth is a finite sum of indicators of closed
  convex sets, upper semicontinuous and constant on open faces (an open edge segment on
  a square’s own edge line is either inside that edge, whose endpoints are the square’s
  corners and so vertices, or outside it); every face in the compact container is a
  bounded polygon with a vertex in its closure; a closed square containing a face
  contains its closure.
  Walls in the arrangement supply boundary vertices and the container corners.
- D4: eight maps about (L/2, L/2): rotations (L−y, x), (L−x, L−y), (y, L−x); reflections
  (L−x, y), (x, L−y), (y, x), (L−y, L−x). Check one compares weighted multisets of
  frozen corner sets (no angle algebra).
  Check two compares (t, x, y, w, s) multisets with rotations fixing t (θ+90° is the
  same square) and reflections sending t → (1−t)/(1+t) (θ → 90°−θ; tan(45°−θ/2)
  identity), folding t = 1 to t = 0: the record uses t = 1 for 20 placements and t = 0
  for 20, the same orientation, so 12 distinct half-tangents are 11 orientations.
  Both pass for all eight; no placement is fixed by a non-identity element.
- Depth histogram (eighths): 0: 756; 1/8: 1,624; 1/4: 1,000; 3/8: 1,352; 1/2: 2,592;
  5/8: 2,272; 3/4: 4,160; 7/8: 3,728; 1: 2,892. First attaining vertex in sorted order:
  (11531/220000, 11531/220000).

## Exact numbers

n, L, B = 11, 191/50, 9977/10000. Placements 88 at weight 1/8, total 11. Net/mirror
44/44. Net half-tangents used: 0, 207107/90000000, 207107/30000000, 207107/18000000,
2278177/10000000, 23403091/90000000 (k = 0, 1, 3, 5, 99, 113). Distinct lines 268 of
356; non-parallel pairs 33,444; inside pairs = distinct vertices = 20,376; max depth 1
at 2,892 vertices. 11 free D4 orbits of size 8, weight 1 each; orbit representatives are
exactly the 11 `support_rows` centres.
Regime net, symmetric_only true.
Display floats (CHECKED): angles 0°, 0.2637°, 0.7911°, 1.3184°, 25.6679°, 29.1521° plus
mirrors at 90° minus each; 11·B² = 10.9495 against L² = 14.5924 (ratio 0.7504); 14.19%
of vertices at depth 1.

## Timings

0.87 s wall in `uv run` (enumeration 0.056 s, depth 0.70 s). With three controls 3.2 s.
Faster than the replay’s 2.5 s because the inner loop builds no `Fraction` objects and
no screen is needed.

## What failed

Nothing in the decision.
Process: first ruff pass had 13 findings (line length, `TypeError` for type checks,
`pairwise`, a `raise` inside `try`), all fixed; basedpyright clean from the start;
`/usr/bin/time` is absent on this host, one timing run was repeated with the shell
builtin.

## Next discriminating measurement

The ceiling transfers to smaller B and larger L but not larger B, and a finer net raises
the admissible B toward 1. The measurement that decides whether the method can still
reach 3.82 at all is the largest side B* at which these same 11 orbits keep depth ≤ 1
and stay inside the container — an exact bisection on B through this reader at 0.8 s per
step, giving a ceiling for every shrink up to B* on any net containing the six angles;
B* ≥ 1 would put the unit regime in force and close 3.82 for every (B, net).
Second, downward in L: the 61/16 family carries 10.08, so the least L admitting a
depth-one family of weight ≥ 11 lies in (3.8125, 3.82]; the reader decides any candidate
family at any rational L in under a second.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
