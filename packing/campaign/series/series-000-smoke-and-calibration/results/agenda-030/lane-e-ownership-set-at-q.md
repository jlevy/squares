# Agenda 030, lane E: A robust unavoidable set of at most eleven marks at 96/25

Retained lane report for BC-302 of
[Agenda 030](../../../../agendas/agenda-030-parallel-structural-lanes-at-n11.md),
testing [H-134](../../../../hypotheses/H-134-eleven-mark-ownership-set.md) in
session-104 on 2026-09-08, written by a research lane at maximum effort in one 2.5-hour
block on a four-core machine shared with seven other agents (load average 4 to 9; wall
times are not comparable with the planning lane’s). The report carries its own status
labels (proved, exact-verified, search reading, open); nothing here is a registered
experiment or a new bound.

## E — Is there a robust unavoidable set of at most eleven marks at 96/25?

Conventions.
`q = 96/25`, container `S = [0, q]²`, `δ = 3/500` (the transfer tolerance of
X-021’s Lemma T). A *mark* is a point or a segment; it is *thickened* by `δ`, so a
closed unit square `Q ⊂ S` *meets* the mark `m` iff `dist(Q, m) ≤ δ`. A mark set `M` is
*robustly unavoidable* iff every contained closed unit square, at every angle, meets
some mark of `M`. An *escape* of `M` is a contained closed unit square with
`dist(Q, m) > δ` for every `m ∈ M`. H-134 claims a robustly unavoidable `M` with
`|M| ≤ 11` exists. Poses are `(cx, cy, t)` with `t = tan(θ/2)` rational,
`cos θ = (1 − t²)/(1 + t²)`, `sin θ = 2t/(1 + t²)` (exp-121’s frame), corners
`(cx, cy) + ((a cos θ − b sin θ)/2, (a sin θ + b cos θ)/2)` for
`(a, b) ∈ {(−1,−1), (1,−1), (1,1), (−1,1)}`.

Thickening is on the hypothesis’s side: it enlarges every mark, so it makes covering
easier and escaping harder, and every escape below clears its marks by more than `δ`.

## 0. Findings in one page

FINDINGS_PLACEHOLDER

## 1. Falsifiers, stated before the runs

- **Falsifier of a candidate set** (every run in Section 3 and 4). A contained closed
  unit square at a rational pose with exact distance `> 3/500` to every mark, decided by
  two independent exact formulas that must agree (Section 2). A “no escape found” is a
  search reading at the stated resolution, never a theorem.
- **Falsifier of the hypothesis’s point form** (Section 5). A finite family of contained
  unit squares such that no eleven points are within `δ` of all of them, decided by an
  exact branch-and-bound whose relaxation is sound (every step enlarges the sets that
  marks may occupy). A surviving branch is not evidence for the hypothesis; a dead tree
  is a theorem.
- **Falsifier of a survivor’s proof** (Section 6). None was needed: no candidate set
  survived the first falsifier.

## 2. The engine and its verification

`escape_engine.py` (Appendix) has three stages.

1. **Grid.** Angles `0°, 1.5°, …, 88.5°`; for each, centres on a grid of step `0.02`
   over the exact containment box `[w/2, q − w/2]²`, `w = |cos θ| + |sin θ|`; the margin
   `g = min_m dist(Q, m) − δ` is evaluated in numpy for every pose (about 1.2 million
   poses for eleven marks in under a second).
   Segment marks are sampled at nine points for the float stage only.
2. **Refinement.** Nelder–Mead on `(cx, cy, θ)` from the best forty grid poses, with the
   centre projected onto the containment box at every evaluation; duplicates within
   `0.02` are merged.
3. **Exact decision.** The refined pose is snapped to rationals (`t` first, then the
   centre clipped into the exact containment box for that `t`, denominators `10³` to
   `10⁶` tried in turn) and verified: all four corners in the closed container, and for
   every mark `dist(Q, m) > δ` by two methods that must agree or the run aborts — (A)
   the local-frame formula `dist² = (|u| − ½)₊² + (|v| − ½)₊²`; (B) the separating-axis
   theorem for two convex polygons, with the square’s two edge normals, the segment’s
   normal, and every vertex-pair direction as candidates, the gap `> δ` decided as
   `gap > 0` and `gap² > δ²|d|²` in unnormalised direction `d`. For a segment mark (B)
   decides and (A) is checked at both endpoints.

Self-tests (`selftest.py`, Appendix), all passed:

| Test | Expected | Observed |
| --- | --- | --- |
| Lane C’s exact escape of P10 at `q`: centre `(73/50, 67/50)`, `t = 49/200` | escape, least margin `14979/1060025` | escape, `min dist 0.0141308` (equal to the retained value to 15 digits) |
| exp-121’s frozen square at `1939/500`, `t = 1/1000`, twelve points, `δ = 0` | strict escape | strict escape, least distance `0.000199`; against `δ = 3/500` it is *not* an escape |
| Search on P10 at `q` | finds an escape | finds four, the largest at the bottom wall (Section 4) |
| Control: points on a `0.3` grid | no escape | best float margin `−0.006`, none verified |
| Control: three full-width segments at `y = 1, q/2, q − 1` | no escape (every unit square has vertical extent `≥ 1 > 0.92`) | best float margin `−0.006`, none verified |
| Axis square `0.01` above a segment / `0.005` above it | escape / not | escape / not |

What was reused from exp-121: the rational half-angle frame, closed membership, and the
support-width containment test.
What is new: the search stages, the distance-above-`δ` decision (exp-121 decides strict
avoidance only), segment marks, and the two-method agreement check.

## 3. Structural facts proved in the block

**Lemma E.1 (no LP obstruction; proved).** The fractional relaxation of H-134 has value
at most `434547/40000 = 10.863675 < 11`. *Proof.* Scale T-018’s measure by `λ = 384/381`
from side `381/100` to `q`. Every closed square of side `λ` at any angle inside `S`
contains a `λB`-square at a net angle, hence carries mass `≥ 4001/4000`. The
`δ`-neighbourhood of a unit square `Q` contains the concentric square of side
`1 + √2·δ = 1.008485…` in `Q`’s frame (a point with `|u|, |v| ≤ ½ + δ/√2` is within
`√(2·(δ/√2)²) = δ` of `Q`), and `1 + √2·δ > λ = 1.007874…`, so every `δ`-rounded unit
square carries mass `≥ 4001/4000 ≥ 1`. ∎ Consequently no counting, pigeonhole or LP
argument can refute H-134; only the integrality gap can, and that needs a case analysis
over mark positions, which is what Section 5 mechanises.

**Lemma E.2 (ten forced marks; proved, exact-verified).** Let `G₁, …, G₁₀` be the
squares of the `n = 10` optimal packing (side `3 + 1/√2`) scaled to `q`, at the rational
poses of `tests-gobel.json` (the two `45°` squares at `t = 41/99`). They are contained
and pairwise at exact distance `> 2δ = 3/250` (`tests_gobel.py`, separating-axis
decision). Hence any robustly unavoidable set has ten distinct marks `m_i` with
`dist(m_i, G_i) ≤ δ`, and at most one further mark.
Eleven such squares cannot exist: they would be eleven squares of side `1 + 2δ` with
disjoint interiors in a container of side `q + 2δ = 3.852`, that is eleven unit squares
at side `3.852/1.012 = 3.806 < 3.81`, against T-018. So a set of eleven marks is *ten
localised marks plus one free mark*.

**Lemma E.3 (symmetry; proved).** No D4-symmetric eleven-set exists: D4 orbits in `S`
have size 1 (the centre), 4 or 8, and `11 − 1 = 10` is not a sum of 4s and 8s. Every
K4-symmetric (two centreline reflections) or C2-symmetric (half-turn) eleven-set
contains the centre, because all other orbits have even size.
Stromquist’s ten-point scheme is K4-symmetric (`2 + 4 + 4`), so its only symmetric
eleven-point extension adds the centre.

## 4. Candidate sets and the escape catalogue

All sets are point marks unless stated; coordinates are exact rationals in the JSON
files retained in the Appendix, decimals here.
Search resolution for every row: grid step `0.02`, angle step `1.5°`, forty grid poses
refined, then exact decision; wall time per set `0.6` to `1.0 s`. Every escape listed
was verified exactly by both methods.

| Set | Marks | Best escape: centre, `t`, angle | Least exact distance | Marks it clears least |
| --- | --- | --- | --- | --- |
| W11: T-018’s eleven heaviest atoms scaled by `384/381` (four corners `(0.99770·λ, …)`, centre `(48/25, 48/25)`, six of the eight atoms of the `33/500` orbit) | 11 | `(48/25, 1/2)`, `t = 0`, `0°` | `0.41449` | both bottom corner atoms at `0.41449` |
| G11: greedy set cover of a pose sample (step `0.04`, `3°`) by the 93 heaviest atoms scaled to `q` | 11 | `(1501/999, 1438/459)`, `t = 5/12`, `45.24°` | `0.06486` | `(1.0009, 2.8348)` and `(2.0045, 2.8369)` at `0.0649` |
| P10: Stromquist’s Figure-13 points at `q` | 10 | `(73/50, 1607521/2273378)`, `t = 408/985`, `45.00°` | `0.03238` | `(1, 1)` and `(48/25, 1)` at `0.03238` |
| P10C: P10 plus the centre | 11 | same as P10 | `0.03238` | same |
| P10 + one point optimised by the min–max (Section 5.1) | 11 | same as P10 | `0.03238` | same; the added point lands at `(2.31, 2.73)` and kills one of four symmetric images |

W11 fails for a structural reason: the heavy atoms of the certificate are corner and
centre atoms, and the eleven heaviest leave the whole bottom and top wall strips
`[1.42, 2.42] × [0, 1]` bare — an axis-parallel unit square there is `0.41` from every
mark. G11’s greedy cover reproduces the three-row structure (rows at `y ≈ 1, 1.92,
2.84`) but runs out of marks before the `45°` squares at the top and bottom walls are
served. P10’s four escapes are the K4 images of one `45°` square resting on a wall
between two row points `0.92` apart: a `45°` square touching the bottom wall cuts
`y = 1` in a chord of half-length `√2/2 − (1 − √2/2) = 0.4142`, so the row would need
spacing at most `0.828 + 2√2·δ = 0.845`, and Stromquist’s rows have `0.92`. One added
point cannot kill four symmetric escapes.

CATALOGUE_PLACEHOLDER

## 5. The exact branch-and-bound and the cutting-plane loop

BRANCH_PLACEHOLDER

## 6. Proved nonavoidance regions

None.
No candidate set survived the falsifier, so no region-by-region proof (Stromquist’s
Lemmas 1–4 as repaired, or an interval reader) was attempted.
The `sqpack.cover` module was read and not used: it decides point resources in triangle
meshes for open boxes, and the segment and thickened-point kinds it refuses by type are
exactly the ones this lane would have needed.

## 7. Obstructions, status of H-134, and what the next session does first

OBSTRUCTIONS_PLACEHOLDER

## 8. Inputs and resources

INPUTS_PLACEHOLDER

## Appendix: scripts and data as run

APPENDIX_PLACEHOLDER

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
