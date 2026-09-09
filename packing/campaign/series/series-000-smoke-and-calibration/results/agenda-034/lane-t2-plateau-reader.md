# Agenda 034, lane T2: the plateau reader, exact feasibility of a point dual for the rank-one cut families

Retained instrument-lane report for
[X-024](../../../../explorations/X-024-two-lines-at-eleven.md), written by a Fable
sub-agent on 2026-09-09 as slice A4 of the unconditional line, read-only on the
repository at `claude/n-11-stronger-result-d730ds`. The report is reproduced as
delivered, with its own status labels; only its file references were rewritten to name
where each file now lives, its one measured placeholder was filled from the promoted
run, and a note was added under [Promotion recipe](#5-promotion-recipe) recording which
of its steps were carried out.
X-024 carries the coordinator’s reading.
Nothing here is a registered round or a new bound.

The instrument was promoted with this report: `packing/devtools/plateau_reader.py` and
`packing/tests/test_plateau_reader.py`, ruff and basedpyright at zero findings, eighteen
tests passing with two marked `slow`. Retained beside this report:
[`plateau-reader-191-50.json`](plateau-reader-191-50.json), the full run on the 88-core
ceiling family at `191/50` — rerun from the promoted module, agreeing with the
sub-agent’s own run in every exact value, its timings its own.
That family was already retained in this directory as
[`ceiling-family-191-50.json`](ceiling-family-191-50.json).
Everything else the report names is not retained (scratch only); [Files](#6-files) lists
it.

Labels: **PROVED** (argument in the module docstring), **EXACT** (rational decision,
script retained), **SOLVER** (a HiGHS optimality claim; the returned object is verified
exactly, the claim that nothing better exists is the solver’s), **CHECKED** (float or
record reading).

## 1. What the instrument decides

Input: a family file in the ceiling-family format (`n`, `outer_side`, `square_side`,
`half_tangents`, `placements` as `[t, x, y, w, side]`), read by
`sqpack.fractional.ceiling.CeilingCertificate.from_record`; `--outer-side` and
`--square-side` re-declare the instrument the placements are read against.
Output: a JSON report (`--out`) and a printed summary, every verdict a rational.

| step | question | how | status |
| --- | --- | --- | --- |
| K0-K3 | admissible, inside, depth `<= 1`, weight | `verify_ceiling`, then the exact membership set of every arrangement vertex by integer slab tests (float screen inside `ceiling.py`’s proved envelope, each candidate confirmed in integers); the two depth readings must agree; depth above one is refused | EXACT |
| K4 | maximum two-of-three charge over all point triples | pairs of distinct membership sets in decreasing order of the bound `y(T_i ∩ T_j) + min(y(T_i Δ T_j), D)`, third set by a vectorised weighted popcount; stops when the bound is below the best; all maximisers collected, sparsest first; the witness re-verified geometrically | PROVED complete |
| K4' | three-of-five | (a) depth-first branch and bound over distinct sets with the weight-order and demand bounds, node-limited, `complete` reported; (b) the integer program of K6 with `t = 3`, multiplicity one, `a(S) = 5` | (a) EXACT when complete, (b) SOLVER |
| K5 | every budget-one atom | maximal cliques of the closed-intersection graph above weight one (separating-axis test, Bron-Kerbosch with weight pruning), `tau*` of each by a piercing LP over the clique’s restricted membership sets, certified by an exact rational primal-dual pair (fallback: an exact `Fraction` simplex); descent into sub-cliques only where `tau* >= 2`; the heaviest clique with `tau* < 2` becomes an integer-multiplicity atom verified against the whole family | PROVED complete |
| lines | wall-parallel and diagonal chords against `floor(len / c)` | the chord extent of every placement as a piecewise-linear function of the offset, solved exactly in `Q(sqrt 2)`; `count - budget` maximised over every offset of four directions at each threshold; named offsets tabulated | EXACT; violation PROVED impossible |
| K6 | rank-one Chvátal-Gomory closure | Fischetti-Lodi separation as a HiGHS integer program per threshold `t`: multiplicities `a_s in {0..t-1}` on the distinct membership sets, `f_P = floor(a(P)/t)`, `f_0 = floor(a(S)/t)`, maximise `sum y_P f_P - f_0`; the returned multiplicities are re-verified on the masks and geometrically, and the two must agree | SOLVER (cut EXACT) |

Two reductions carry the proofs and are written out in the module docstring: the
membership set of any point of the plane is contained in that of an arrangement vertex,
and every charge here is monotone in each point’s membership set, so every search runs
over the distinct membership sets of the vertices (1,541 on the 88-core family) with a
representative exact vertex each; and in K6 multiplicities may be taken below `t` and
points among the distinct sets without weakening any cut.

Two statements the work sharpened beyond the theory report:

- **Line chords are never violated by a depth-one family (PROVED).** The restriction of
  `y` to the cores with a long chord on a line is a fractional packing of an interval
  graph under all its point constraints (the cliques of an interval graph), interval
  graphs are perfect, so the restriction is a convex combination of packings, each with
  at most `floor(len / c)` members.
  Wall-line atoms are worth exactly nothing on *any* point dual, not only on the 191/50
  family; the tool measures tightness only.
- **A repeated membership set cannot violate two-of-three (PROVED)**: such a triple
  charges `y(T) <= D <= 1`. So K4 over distinct sets is complete for the feasibility
  question, and the report states the maximum over distinct sets and the depth
  separately.

Every statement in the report carries a `status`: `violated`, `feasible` (a theorem for
the class on this family), `never` (a class no depth-one family violates) or `bounded`
(a search that found nothing within its bound and proves nothing).

## 2. Control results on `ceiling-family-191-50.json`

88 placements at weight `1/8`, `L = 191/50`, `B = 9977/10000`, 181 directions; K0-K3 as
recorded (depth exactly `1`, total `11`, 20,376 vertices, 1,541 distinct nonempty
membership sets with size histogram `16, 64, 160, 224, 296, 336, 312, 133` for sizes 1
to 8, the prototype’s histogram).

| check | required | found | status |
| --- | --- | --- | --- |
| K4 two-of-three maximum | `5/4`, witness memberships `(4, 8, 8)` | **`5/4`**, 504 maximising triples, sparsest `(4, 8, 8)` (24 of them); witness re-verified geometrically at charge `5/4`, budget `1` | EXACT |
| K5 heaviest clique | corner clique, `11/8`, `tau* = 5/3` | 824 edges (lane M0’s count: closed intersection and interior overlap coincide on this family, no touching pairs); 205 maximal cliques, **52 above weight one** (sizes 9: 32, 10: 12, 11: 8; weights `9/8, 5/4, 11/8`); heaviest `11/8`, eleven entries at a corner (the axis corner square as its `t = 0` and `t = 1` entries, the `0.26°` pair, two axis squares, two `1.32°` squares, the axis slot, the `29.15°` pair), **`tau* = 5/3`** certified by an exact primal-dual pair; every overweight clique has `tau* < 2`, so no descent was needed | EXACT |
| K5 atom | the `11/8` weighted three-of-five | the LP returned the degenerate optimum with five points at `1/3`: a *plain* three-of-five `(S, 3)` with distinct points, budget `1`, charge **`11/8`** verified on the family (lane M0’s `(2/3, 1/3, 1/3, 1/3)` measure is another optimum of the same program) | EXACT |
| lines | tight at exactly `3` on the wall lines | horizontal and vertical, `c = 99/100`: maximum weight `3` over every offset against budget `3`, `max(count - budget) = 0`; named lines `y in {1/10, 1/4, 1/2, 3/4}` carry exactly `3`, `y = 1/100` `9/4`, `y = 1/20` `11/4`, `y = 1` `7/4` (the `marks_and_lines.py` table); `c = 9/10, 19/20`: `3` against `4`; diagonals `7/2` against `5` at the centre | EXACT |
| K4' three-of-five program | - | objective **`3/8`** (charge `11/8`), proved optimal by HiGHS in 14 s: the corner clique is the best plain three-of-five, agreeing with K5 by an independent route | SOLVER |
| K6 `t = 2` | at least the two-of-three cut (`1/4`) | **`1/2`**: 107 points at multiplicity one, `a(S) = 107`, budget `53`, floor charge `107/2`; proved optimal for `t = 2` in 6 s | SOLVER (cut EXACT) |
| K6 `t = 3` | - | **`5/8`**: 119 points, multiplicities `1` and `2`, `a(S) = 211`, budget `70`, floor charge `565/8`; proved optimal in 44 s | SOLVER (cut EXACT) |
| K6 `t = 4` | - | `3/8` found and verified, solver bound `3/4`, time limit reached at 60 s (K6_T4_120) | bounded |

Reading.
The K6 cuts at `t = 2, 3` are violated in the *floor* form only (their threshold
charge is `10`, far under their budgets): they are the Chvátal-Gomory cuts the threshold
language cannot state (theory report F7), and on this family they cut deeper (`1/2`,
`5/8`) than the best threshold-form atoms (two-of-three `1/4`, the three-of-five clique
`3/8`). The ranked list of the full run is therefore the `t = 3` floor atom at `5/8`,
the `t = 2` floor atom at `1/2`, the three-of-five clique at `3/8` (K5 and the shape
program agree), two-of-three at `1/4`; lines never.
The depth-first three-of-five search is incomplete at its 200,000-node budget on this
family (it finds `1`), which the report states; the complete decision for that shape is
K5’s.

Lane M0’s F7 says “398 maximal cliques of sizes 9-11 exceed weight 1”; the exact counts
are 52 maximal cliques above weight one (205 maximal in all) and 656 cliques of any size
above weight one, cross-checked by an unpruned enumeration.
The 398 is neither figure and its origin is not recorded; the clique itself, its weight
and its `tau*` agree.

Synthetic controls (quick tests): a single core and four pairwise disjoint cores return
no violated atom from every search (statuses `feasible`, `never`, `bounded`); the
planted non-Helly triple (two axis squares meeting on `[11/10, 3/2]^2` and a
`2 arctan(1/2)` square meeting both but not the box, weight `1/2` each, depth exactly
`1`) is caught by K4 (`3/2` at memberships `(2, 2, 2)`), by K5 (one clique, `tau* = 3/2`
exact, atom charge `3/2`), by K6 at `t = 2` (objective exactly `1/2`) and by the
depth-first search, while its three-of-five maximum is `1` (complete) and its lines are
slack. A family of depth `2` is refused with exit code `2`. The integer membership test
is checked against `Placement.contains` at every vertex, the pruned clique enumeration
against the unpruned one, the exact simplex on the triangle (`3/2`), and the `Q(sqrt 2)`
arithmetic on the diagonal chord of a unit square (irrational endpoints symmetric about
the centre).

## 3. Timings (this host, one process)

| stage, 88-core family | seconds |
| --- | --- |
| `verify_ceiling` + arrangement + exact membership sets (1,541) | 0.8-1.1 (the prototype: 17) |
| K4 two-of-three, all 504 maximisers (51,784 pairs expanded) | 2.5 |
| K4' depth-first three-of-five, 200,000 nodes (incomplete) | 3.3 |
| K4' three-of-five integer program (optimal) | 14 |
| K5 graph (824 edges), 52 maximal cliques, 3 piercing programs | 1.0 |
| lines, 4 directions x 3 thresholds, every offset | 2.3 |
| K6 `t = 2` (optimal) / `t = 3` (optimal) / `t = 4` (limit) | 6 / 44 / limit |
| full run with `--time-limit 120` | 196.9 (the retained run; the sub-agent’s own 195.5) |
| test file: quick subset / everything | 0.9 / 12.8 |

## 4. What the searches do not cover

- K6 is bounded: thresholds `t in {2, 3, 4}` by default, multiplicities below `t`, one
  HiGHS run per `t` under a time limit.
  “No cut found” for a `t` is the solver’s claim and is labelled `bounded`; it is not a
  theorem. Larger `t` is not searched, and a cut at `t = 4` on the 191/50 family was not
  settled within the limit.
- The depth-first three-of-five search reports `complete` honestly and is complete only
  on small families; on the 88-core family it is not.
  The exact decision for every budget-one shape is K5.
- Odd-cycle and odd-wheel atoms (two-of-five and kin) are reached only through K6 at
  `t = 2`, within its bound; no dedicated cycle enumeration was built (the 191/50
  family’s five-cycles sit at `5/8` against `2`, lane M0).
- K5’s atom uses integer multiplicities; `ThresholdAtom` refuses repeated points, so the
  loop must either drop that rule (sound, review F2) or emit near-duplicates in the same
  cell. On the 191/50 family the optimum happened to be multiplicity-free.
- The K6 cuts found are large (107 and 119 points); as floor atoms they enter the sweep
  by the count-grid route (`charge_grid_direct`), not the binomial expansion.
- Everything is one family at one `(L, B, net)`. A plateau is a theorem about a class
  only when the family read is the plateau dual itself; the tool does not find families.
- Rank-two atoms, class-indexed certificates and cuts outside the point system are
  outside the language.

## 5. Promotion recipe

Steps 1 to 3 were carried out when this report was retained; step 4 is the standing
instruction for the `383/100` dual.

1. Copy `plateau_reader.py` to `packing/devtools/plateau_reader.py` unchanged (the
   `T201` waiver for `devtools/*` covers its prints; ruff and basedpyright are at zero
   findings under `packing/pyproject.toml`, checked with `--per-file-ignores` standing
   in for that waiver).
2. Copy `test_plateau_reader.py` to `packing/tests/test_plateau_reader.py` and replace
   the `sys.path.insert(...)` line, the comment and
   `import plateau_reader as pr  # pyright: ignore[...]` by
   `from devtools import plateau_reader as pr`; drop the then-unused `sys` import.
   On promotion the `PACKING` constant was also rebased on
   `Path(__file__).resolve().parents[1]`, which is how the sibling tests find the
   project root. The 88-core tests carry `@pytest.mark.slow` (2.7 s, 1.1 s, 0.7 s and 6.2
   s) and the fixture skips when the retained family is absent.
   On promotion the marker was kept on the two that measured above the repository’s 2 s
   marking threshold (6.35 s and 2.78 s of `call`, registered with those measurements in
   `packing/tests/test_module_boundaries.py`) and dropped from the other two, which sit
   under it and would have failed the deep surface’s 1 s marker floor.
3. Validate from `packing/`: `uv run --frozen --all-extras --group dev packing-validate
   --edit` (lint and type floors), then `packing-validate --push` for the tests
   reachable from the change; the deferred tests run in the deep surface.
4. Run on the `383/100` plateau dual once it exists:
   `python -m devtools.plateau_reader FAMILY.json --out REPORT.json --time-limit 120`.
   K4 answers step 2 of the theory report’s outcome 2 (feasible: the two-of-three method
   is capped there, a theorem; violated: the loop’s generator missed the exact triple);
   K5 and K6 name the cut that moves it with its exact violation.

## 6. Files

- `packing/devtools/plateau_reader.py`: the instrument, promoted (module docstring: what
  it decides, why it is exact, what it does not protect against;
  `uv run --frozen --all-extras --group dev python -m devtools.plateau_reader --help`).
- `packing/tests/test_plateau_reader.py`: 18 tests, 2 marked `slow`.
- [`plateau-reader-191-50.json`](plateau-reader-191-50.json): the full run on the
  88-core family with `--time-limit 120 --cg-thresholds 2,3,4`, from the promoted
  module.
- The sub-agent’s own copies of the instrument and its tests, its `report-191-50.json`,
  `run-191-50.log`, `run-191-50.err` and `smoke-k6-60s.log` (K6 at 60 s): not retained
  (scratch only).

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
