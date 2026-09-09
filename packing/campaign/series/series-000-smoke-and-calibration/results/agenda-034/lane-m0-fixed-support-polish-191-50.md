# Agenda 033, lane M0: the exact fixed-support optimum of the 3.82 fractional packing

Retained measurement-lane report for
[X-023](../../../../explorations/X-023-three-losses-and-a-new-atom.md), written by a
Fable sub-agent on 2026-09-09 under the breadth survey.
The report is reproduced as delivered, with its own status labels; X-023 carries the
coordinator’s reading.
Retained beside it: the polished depth-one family with its provenance
([`lane-m0-bc200-polished-191-50.json`](lane-m0-bc200-polished-191-50.json)) and the
diagnostics ([`lane-m0-bc200-diagnostics.json`](lane-m0-bc200-diagnostics.json)); the
tool is promoted as `packing/devtools/polish_ceiling_family.py`. Nothing here is a
registered round or a new bound.
Where the lane wrote `agenda-031`, read `agenda-034`, the directory’s name after the
reconciliation renumbering.

Sub-agent report, 2026-09-09. Everything is in `spike-m0/`; the reusable tool is the
new, uncommitted `packing/devtools/polish_ceiling_family.py`. No git state was changed.
The unit-family leg (task 2) was not run: the coordinator stopped it once spike B’s
exact 11-ceiling at 191/50 answered the plateau question.

Labels: EXACT (rational decision by repository primitives), CHECKED (float computation,
script retained), RECORD (read from a retained file), OPEN.

## 0. Findings in one page

| # | Finding | Status |
| --- | --- | --- |
| F1 | On the retained 760-placement support (`bc-200-family-191-50.json`, B = 9977/10000, N = 180) the fixed-support optimum satisfies `nu_S(191/50) >= 271428569/25000000 = 10.85714276`: the polished family `bc200-polished-191-50.json` has that total and `verify_ceiling` finds maximum depth `499999999/500000000` over 2,769,100 vertices (415,767 decided exactly). Net regime, D4-symmetric measures only. | EXACT |
| F2 | `nu_S(191/50) <= 76/7 = 10.857142857...`: an exact dual bound on the working-set program (a relaxation of the full program), rational duals on 11 priced rows, bound `sum u + sum_P max(0, c_P - (A^T u)_P)` decided in rationals. So `76/7 - nu_S < 1e-7`; the float LP optimum is `76/7` to 16 digits. **`nu_S < 11`: this support cannot witness the plateau, and the retained 9.908 was 0.95 short of what its own placements can do.** | EXACT (bracket); CHECKED (76/7 attained) |
| F3 | The float optimum is not a vertex of the program: on the closed working set (112,239 rows) the tight rows span rank 11 for its 17 free columns, and 52,692 working-set vertices (6,924 D4 orbits) are tight for it. An exact vertex could not be read from the floats; the verified family is the float weights rounded down to multiples of 1e-9. | EXACT (tightness), CHECKED (rank) |
| F4 | Denominator structure: the 76/7 solution lives on 17 of the 95 orbits (136 placements) with per-image weights in `{41/112, 9/56, 15/112, 3/56, 1/28, 1/56}`, all multiples of 1/112 (orbit totals multiples of 1/14); its duals are in `{2/7, 4/7, 8/7, 12/7}`. **Not half-integral**: in Lemma 3’s language it is a 112-fold packing, so the `k = 2` odd-cycle argument does not apply to it. | CHECKED (nearest rationals of the float LP) |
| F5 | Weight by folded angle band: `58/7 = 8.286` within 2.5 deg of the axes (76 per cent), `2/7` in [2.5, 7.5), `9/7` in [25, 27.5), `5/7` in [27.5, 30), `2/7` in [35, 38.2); nothing elsewhere. Each corner carries exactly 1 (`2 x 41/112` on the mirror pair of 0.26 deg squares plus `2 x 15/112` on the axis square). | EXACT (rounded family; sums within 1e-7 of the fractions quoted) |
| F6 | **The polished optimum violates a clique cut.** A 26-member clique of the interior-overlap graph (all 325 pairs decided exactly) carries `705357133/500000000 = 1.4107 > 1` (`79/56` at the float optimum); it has no common point (forced: depth <= 1 everywhere is exact). Its fractional piercing number is `tau*(C) = 5/3 < 2` (a 4-point measure of mass 5/3, weights (2/3, 1/3, 1/3, 1/3), covers every member -- checked exactly), so by the theory report’s F5 the cut is a rank-1 threshold atom: `(S, 3)` with `S` those four points at weights (2, 1, 1, 1), budget `floor(5/3) = 1`. Odd holes are far from tight: only 6 chordless 5-cycles exist on the support, the heaviest at 0.848 against capacity 2; the heaviest non-Helly triangle is 0.75; the heaviest triangle 0.866 is Helly. | EXACT (overlaps, weight); CHECKED (tau*, with an exact feasible piercing of mass 5/3) |
| F7 | **Spike B’s exact 11-ceiling is cut by the same language**: on `agenda-034/ceiling-family-191-50.json` (88 placements at 1/8) the interior-overlap graph (824 edges) has a maximum clique of 11 entries (10 distinct squares; the axis corner square appears as its t = 0 and t = 1 entries) of weight `11/8 = 1.375 > 1` at a corner, non-Helly, `tau* = 5/3`; 398 maximal cliques of sizes 9-11 exceed weight 1; its chordless 5-cycles carry `5/8 < 2`. | CHECKED (exact pairwise overlaps; tau* float with exact feasible piercing) |
| F8 | The LP dual is sparse and degenerate (11 atoms, none symmetric): 9.14 of its 76/7 sits exactly one B-side inside a wall, 1.71 near the centre. Pricing candidate placements against it is uninformative (coverage 0 off its support). The tight-vertex census is the informative signal: 11,455 tight vertices one B-side inside a wall, 9,015 in the wall band (< 0.5), 11,409 within 0.6 of the centre, 20,773 elsewhere in the interior, 40 at the corners. | CHECKED |
| F9 | The retained unit record `agenda-030/pr127-unit-control.json` declares `square_side` 1, so `verify_ceiling` reads it in the **net regime at B = 1**; declaring `square_side` 9977/10000 makes K0 say `unit` (B(1 + D) = 0.9999959 < 1), the stronger statement the transport was for. The polisher has `--square-side` for this. Its polish was not run. | CHECKED; OPEN (nu_S at the unit side) |
| F10 | `packing/devtools/polish_ceiling_family.py`: working-set polish with exact rows, exact rebuild or the documented rounded fallback, exact dual bound, `verify_ceiling` decision, record with provenance. Ruff and basedpyright at zero findings; `packing-validate --edit` passes its lint and type floors, and its three failing steps (a resource-usage record citing the defect id after D-488 before `defects.yaml` has it, session-close/SYNOPSIS drift, an orphaned-commit annotation in exp-002) are the concurrent integration’s, not this file’s. | tool |

## 1. The program and the method

Fix the support -- the placements of a retained family, geometry only -- and maximise
`sum_P y_P` subject to `y_P >= 0` and depth `<= 1` at every vertex of the arrangement
cut by the placements’ edge lines and the container walls (depth is upper semicontinuous
and constant on open faces, every face has a vertex in its closure, so the vertex
constraints are the whole program: `ceiling.py`). Its optimum `nu_S` is a lower bound on
`nu*(L)` and, by weak duality, on the mass of every covering measure at that
`(L, B, net)`.

Orbit variables. The support is D4-closed (95 orbits x 8 = 760, none with a stabiliser).
One variable per orbit, images tied, objective coefficient 8. This loses nothing: the
vertex set and the constraints are D4-invariant, so averaging an optimal solution over
the group keeps feasibility and the objective and yields a symmetric optimum.
(The 760-variable program was not solved; a non-symmetric vertex could have different
denominators. Not measured.)

Working set. The arrangement does not depend on the weights, so it is enumerated once
with `cutting.float_vertices` inside the checked coefficient envelope, and a loose
membership matrix (margin 2e-6, the one `screened_separation` justifies for approximate
intersections) is stored as CSR: 2,769,124 vertex pairs x 760 placements, 184.7 million
entries.
Every working-set row is an exact membership: the vertex is rebuilt as the exact
intersection of its two lines and a placement whose edge passes within 1e-8 of it is
decided by `Placement.contains`. Seed: every placement’s four corners (so no column is
unconstrained) plus the vertices the retained weights bring to float depth >= 0.98.
Loop: HiGHS dual simplex with `0 <= y <= 1` (the bound is implied by the corner
vertices); screen every vertex with the loose matrix; add every vertex with loose depth
\> 1 + 1e-9 (up to 20,000 a pass) and up to 5,000 near-tight ones; stop when no violated
vertex is new.

Exact decision.
The float solution is rebuilt as the exact vertex of a basis of its tight
rows (columns at bound 1 held at 1, a float pivoted QR choosing one tight row per free
column, the square system solved in `Fraction`s, feasibility on every working-set row
checked in integer arithmetic).
Here that failed by rank (F3), and the fallback is what any exact depth-feasible family
gives: weights rounded down to multiples of 1e-9 (the rule of `cutting.tidy_family`),
`verify_ceiling` over every vertex of the arrangement, and, had a vertex exceeded 1,
scaling by the rational `1 - 1e-6` as often as the exact maximum depth required.
No scaling was needed.
Optimality is bracketed by the exact dual bound: for any rational `u >= 0` on the rows,
`sum_P y_P <= sum u + sum_P max(0, c_P - (A^T u)_P)` because `y <= 1`; the solver’s
duals rationalised give exactly 76/7. The working-set program is a relaxation of the
full one, so `nu_S <= 76/7`.

## 2. Exact numbers

- Side `191/50`, `B = 9977/10000`, net `t_k = T k / 180`, `T = 207107/500000`, 181
  directions; regime `net`, `symmetric_only` (mirrored angles present).
- Retained family (RECORD): total `9.907905594982566`, depth exactly 1 at 16 vertices of
  2,769,100 (replay reproduced, 429 s wall on this loaded host).
- Polished family (EXACT): total `271428569/25000000 = 10.85714276`; maximum depth
  `499999999/500000000` at 2,769,100 vertices, 415,767 decided exactly; weights on 136
  placements, six distinct values: `91517857/250000000` (x8), `32142857/200000000`
  (x16), `133928571/1000000000` (x24), `13392857/250000000` (x8), `7142857/200000000`
  (x16), `8928571/500000000` (x64). `verify_ceiling`: proved = false, failure `K3` only.
- Working-set optimum: float `10.857142857142858`; exact dual bound `76/7` (11 priced
  rows, duals `8/7` x7, `12/7`, `4/7`, `2/7` x2, sum `76/7`). Bracket:
  `76/7 - 4/(7 x 25000000)
  = 271428569/25000000 <= nu_S <= 76/7`, width `1/175000000`… precisely
  `76/7 - 271428569/25000000 = 17/175000000 = 9.7e-8`.
- Support orbits (angle folded to [0, 45], a representative centre, orbit total): 0.26
  deg (0.5012, 0.5041) `41/14`; 25.67 deg (1.3438, 1.3901) `9/7`; 1.32 deg (0.5149,
  1.5894) `9/7`; 0 deg (0.4989, 1.4966) `15/14`; 0 deg (0.4989, 0.4989) `15/14`; 1.58
  deg (0.5155, 1.5101) `15/14`; 1.85 deg (1.5069, 1.5177) `3/7`; 4.74 deg (1.5283,
  1.5376) `2/7`; 1.85 deg (0.5164, 1.6722) `2/7`; and eight orbits at `1/7`: 28.91 deg
  (1.5617, 1.8140) and (1.5922, 1.8677), 29.15 deg (1.3248, 1.3869) and (1.3250,
  1.4353), 28.66 deg (1.3269, 1.4360), 35.95 deg (1.3015, 1.3938), 36.91 deg (0.6985,
  1.8717), 0.53 deg (0.5038, 1.6354). Read: corners 4 (one each), wall slots about 3.9,
  the 25-37 deg inner-corner squares 2, near-centre axis squares 0.7 -- the same
  skeleton the theory report describes for the unit family, with the corner cliques
  saturated.

## 3. Diagnostics on the polished optimum (N4)

The 26-clique (F6). Members: the two 1.32 deg wall slots at (3.305, 1.589) and (3.305,
2.231) and the two 1.58 deg slots at (3.304, 1.510), (3.304, 2.310) on the right wall,
the 25.67 deg squares at (2.476, 1.390) and (2.476, 2.430), the near-centre 1.85 and
4.74 deg squares at (2.30, 1.51), (2.30, 2.31), (2.28, 1.53), (2.28, 2.29), the 1.85 deg
slots at (3.304, 1.672), (3.304, 2.148), and twelve `1/7`-orbit tilted squares
(28.7-36.9 deg) between them.
Its piercing measure of mass 5/3 sits at (2.5264, 1.91) with weight 2/3 and at (2.8135,
1.91), (2.8154, 1.8278), (2.8154, 1.9922) with weight 1/3 each -- three points one
B-side inside the right wall and one further in.
The clique’s own point program allows `nu*(C) = 5/3`; the family uses 1.41 of it.
A threshold atom `(S, 3)` on these four points (weights 2, 1, 1, 1) charges every member
and has budget 1: adding it to the covering program cuts this family by at least 0.41 on
this clique. Whether the re-optimised support then stays below 11 is OPEN; on this
support the optimum is already below 11 without it.

Spike B’s ceiling (F7). Its maximum clique is at a corner: the axis corner square at
(0.4994, 0.4994) (two record entries), the 0.26 deg mirror pair at (0.5012, 0.5041),
(0.5041, 0.5012), the axis squares at (0.5064, 0.5513), (0.5513, 0.5064), the 1.32 deg
squares at (1.5079, 0.5161), (0.5161, 1.5079), the axis slot at (0.4989, 1.4966), and
the 29.15 deg pair at (1.3869, 1.3248), (1.3248, 1.3869): eleven entries at 1/8, weight
11/8, piercing measure of mass 5/3 at (0.0075, 0.9977) (2/3) and three points near
(0.998, 0.998). This is the corner clique the theory report’s lane-A remark says the
point constraint captures -- it does not: the eleven squares meet the corner triangle
but have no common point, and the family’s depth there is 1 while the clique carries
11/8.

Odd cycles. On the polished support (136 nodes, 3,776 edges, 59,352 triangles) there are
only 6 chordless 5-cycles, heaviest 0.848; on spike B’s family, 4,112 (with
multiplicity), all at 5/8. Against capacity 2 neither is close.
The obstruction in both witnesses is a corner or wall clique, not an odd hole.

Half-integrality.
Not present (F4); the float optimum is a 112-fold packing and its duals
have denominator 7. The prediction of the theory report’s Lemma 3 reading -- “the
denominator of the optimal dual at 3.82 is the single best predictor” -- resolves as: on
this support the denominator is 7 (dual) and 112 (primal), and the cut that bites is a
rank-1 clique atom with `tau* = 5/3`, not a `k = 2` odd-cycle atom.

Where the support is short (task 4’s second half).
The dual is too degenerate to price against (F8). The tight census says the float
optimum is pinned along the inner edge lines of the wall-flush squares (11,455 tight
vertices at distance B from a wall), in the wall band and around the centre; corners
contribute 40 tight vertices at depth exactly 1. A placement that raised the value would
have to avoid the wall-slot and corner bands and the inner-corner tilted cluster; the
interior ring at radius 0.6-1.3 from the centre, where the 76/7 solution puts only the
1.85/4.74 deg squares, is where the census is thinnest.

## 4. Timings (one core, host load 4-11)

| step | time |
| --- | --- |
| `replay_ceiling_family --check` on the retained family (2,769,100 vertices) | 429 s wall, 272 s CPU |
| arrangement enumeration + loose CSR (184.7 M entries) | 129-172 s |
| working-set loop: 7 passes, 4,756 -> 112,239 rows | 3-11 s a pass, 55 s total |
| rounding + exact dual bound | < 1 s |
| `verify_ceiling` on the polished family (415,767 exact decisions) | 1,168 s |
| diagnostics (graph, cliques, 5-cycles, dual census) | 27 s |
| exact clique check, `tau*` LP, tight census | 19 s |
| spike B clique scan | 4 s |

The polished family is tight or nearly tight on about half a million vertex pairs, which
is why its verification costs three times the retained family’s: the screen can skip
nothing.

## 5. What failed

- The first working-set program was unbounded: a placement none of whose vertices were
  in the seed had an unconstrained column.
  Fixed by seeding every placement’s corners and bounding `y <= 1`; both are implied by
  the full program.
- The first exact rebuild solved the tight system over all tight rows in the working set
  (about 10^5 rows x 95 columns in `Fraction`s); it ran 24 minutes without finishing and
  was killed. Replaced by a QR-chosen basis of at most one row per free column.
- `pkill -f` on the tool’s module name matched the shell that issued it and killed both.
  Processes were then addressed by PID with a pattern the shell’s argv cannot match.
- The QR-basis rebuild failed by rank (F3): the optimum is degenerate.
  The coordinator’s fallback (round down, verify, scale if needed) was adopted and is
  now the tool’s documented fallback; the working-set duals still give the exact upper
  bound.
- The dump-driver crashed after writing the record, zipping a dual vector shorter than
  the working set (near-tight rows added after the last solve carry no dual).
  The working-set file was rewritten with zero-padded duals; the tool’s writer was fixed
  the same way.
- Not run: the unit-family polish (task 2), the 760-variable vertex diagnostic, and a
  `replay_ceiling_family --check` of the polished record (it would repeat the 1,168 s
  verification whose verdict the record carries).
  `packing-validate --edit` (132 s wall): lint and type floors pass; the three failing
  steps are record-keeping outside this spike (`validate-edit.log`).

## 6. Next discriminating measurement

Add the clique atoms to the covering program and re-run the exact ceiling: separate
maximal non-Helly cliques of weight > 1 on the support graph (the weighted branch and
bound takes under a second on 136 nodes, 4 s on spike B’s 88), compute `tau*` per
clique, keep those with `tau* < 2` as `(S, k)` atoms from their piercing measures, and
re-solve the fixed-support program with the cuts.
If spike B’s 11-ceiling drops below 11 under its own 398 corner-clique cuts, the plateau
at 3.82 is a rank-1 clique phenomenon and the threshold-atom certificate route (M3) is
live; if a re-optimised family stays at 11 under every rank-1 clique cut, the
certificate language needs rank 2 or a different support.

## 7. Files

- `bc200-polished-191-50.json`: the verified family with provenance (program statistics,
  exact dual bound, `verify_ceiling` verdict).
  `bc200-working-set.json`: 116,275 exact vertices with their float duals.
  `bc200-dump.pkl`: working set with exact membership rows and the float solution (100
  MB).
- `bc200-diagnostics.json`, `bc200-clique-and-tight.json`, `diag-bc200.log`,
  `clique-and-tight.log`, `clique-scan-spike-b.log`.
- Scripts: `diagnose_polished_family.py`, `clique_and_tight.py`,
  `clique_scan_spike_b.py`, `fallback_from_dump.py`. Logs: `polish-bc200.log`,
  `fallback-bc200.log`, `replay-bc200-timing.log`, `validate-edit.log`.
- Tool: `packing/devtools/polish_ceiling_family.py` (new; `--square-side`,
  `--per-placement`, `--dump`, `--working-set`, `--verbose`).

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
