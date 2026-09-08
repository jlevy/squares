# Agenda 030, lane F: The exactly-eleven plateau at 191/50

Research-lane result for BC-297 of
[Agenda 030](../../../../agendas/agenda-030-parallel-structural-lanes-at-n11.md), on
[H-133](../../../../hypotheses/H-133-plateau-site-artefact.md), written under
`session-103` (bead `think-4uon`) on 2026-09-08 in a 2.5-hour block.
Every script and output it quotes is reproduced in the appendix.
Nothing here is a registered round, a new bound or a frozen claim; the exact verdicts
are decisions about named finite objects and are labelled as such.

Date: 2026-09-08, 04:37 to 07:07 UTC. Branch `claude/squares-n11-constraints-wl9atd`
(worktree branch `lane/bc-297-plateau`); working files under `scratchpad/lane-297/`.
Python 3.14 from the project venv, `PACK_JOBS=1`, one worker throughout, on a four-core
host shared with seven other agents (load average 3.7 to 4.1 while the runs were on),
so no wall time below is comparable with the planning lane's or with BC-200's.

Notation: `L = 191/50`, `B = 9977/10000` (the retained shrink), the retained net of
`181` directions `t_k = (207107/500000) k / 180`, `U = 3.877083590022814` (Trump),
`λ = L / U = 0.98527667`. A *core* is a closed `B`-square at a net direction inside the
container, which is what a row of the covering LP is (X-014 Lemma 1).
Status labels: EXACT (a rational decision by the repository's own primitives), CHECKED
(a float computation), RECORD (read from a retained file), OPEN.

## 0. Findings in one page

| Question | Answer | Status |
| --- | --- | --- |
| Is the plateau Trump's eleven `B`-cores overlapping only in site-free strips? | No, for the canonical configuration: the clamped cores overlap in fourteen strips `0.0124` to `0.0254` wide, and `45` of the `3365` grid-seed sites, `822` of BC-200's `12761` retained sites and `162` of the grid plus T-018's atoms lie in two or more cores. A perturbation search over centres and the tilted net index bottoms out at `5` doubly covered grid-seed sites in `80000` trials. | EXACT (verdict), CHECKED (search) |
| Is the plateau a site artefact at all? | Yes, in the general sense the record already carries: every dual the instrument returns at `191/50` is site-disjoint but not point-disjoint. The row-converged dual on grid plus strip sites has exact pointwise depth `1.98595`; BC-200's raw-total-eleven dual had `1925/1152`. The artefact is not Trump-shaped: BC-200's dual carries `50.7 %` of its weight within `2.5°` of the axes, `25.2 %` in `[25°, 35°]` and `1.1 %` within `2°` of Trump's angle. | EXACT (depths), RECORD |
| Does filling the strips give a certificate below eleven? | RUN1-VERDICT | EXACT |
| The tight-cell census | CENSUS-VERDICT | EXACT |
| The shrink tax | Not measured; the block ended with the census. | OPEN |

What this changes for H-133: the *specific* mechanism the hypothesis names (Trump's
cores, site-free strips) is refuted on every reconstructible site set, and the
*general* mechanism (site-invisible overlaps of a fractional, near-axis dual) is
confirmed and is the record's own reading of exp-060.
The plateau at exactly eleven on the lost `6637`-site set is therefore best read as an
instrument stop of the column generator on a degenerate site-set optimum, not as a
statement about `τ*(191/50)`; whether `τ*_B(191/50)` is below eleven remains OPEN, and
the route to it is the cutting-plane loop's systematic site addition, not strips at
Trump's contacts.

## 1. The question and the falsifiers

BC-297 asks whether the restricted covering value of exactly `11.000000` that two site
sets reached at `191/50` is an artefact of Trump-shaped `B`-cores overlapping only in
site-free strips, what the shrink tax is there, and whether the plateau closes as an
exact cover.
The lane's priority order was the thirty-minute artefact test, then strip sites and a
column-generation run of at most forty minutes, then the census and the exact-cover
reading, then the tax if time remained.

Falsifiers, stated before each run:

- *Artefact test.* H-133's mechanism is refuted for a configuration if at least one
  site of the reconstructed site set lies in two of its eleven cores; it is exhibited
  if none does, because then the unit dual on the eleven rows is feasible for the
  restricted covering LP on that site set and its optimum is at least eleven whatever
  rows are generated (the reading rule `window_lattice` documents in
  `devtools/run_fractional_colgen.py`).
- *Run 1 (strips filled).* The run fails to yield a certificate if its converged
  restricted value stays at or above eleven, or it ends unconverged at the deadline,
  or a frozen candidate is refused by `devtools.decide_certificate`.
  Only an exactly verified measure counts; a float optimum is context.
- *Census.* The exact-cover route is recorded as an obstruction if the census exceeds
  one million cells with no clustering.

## 2. Inputs: what the plateau runs used, and what could be rebuilt

The two plateau runs are RECORD only.
`packing/frontier/covering-values.yaml` gives the grid-built set as `6637` sites and
`14820` rows at the end, twelve rounds, converged at `11.000000` after descending from
`11.6`; the certificate-seeded set as `24069` sites, `30240` rows, twenty-four rounds,
unconverged at `11.000000` with least covered mass `0.9997`; both with the note that no
run log or checkpoint was retained.
Their shrink and net are those of every `n = 11` run since T-018: `B = 9977/10000`,
angle limit `207107/500000`, `180` steps (exp-060, exp-070).
Neither final site set can be rebuilt: column generation adds one orbit per round from
the arrangement vertices of the dual, and the added orbits are in the lost logs.

What can be rebuilt exactly (EXACT):

- **The grid seed at BC-191's density.** `site_counts_for_side(191/50, 9977/10000)`
  gives counts `(25, 34, 41)` at inset `1/2`; their union is `3365` sites in `457`
  orbits, which is BC-200's recorded `initial_sites` at this side, so this is the seed
  every driver-era run at `191/50` started from.
  Its `87` distinct coordinates have gaps from `0.0021` to `0.0705`, mean `0.0328`; the
  three pitches are `0.1175`, `0.0855` and `0.0705`. The "pitch `0.047`" of the
  hypothesis is `3.82 / 81`, an average, not a coordinate spacing.
- **BC-200's retained state** (`results/bc-200-state-191-50.json`): `12761` sites in
  `1657` orbits, the grid seed plus eight rounds of violating arrangement vertices, a
  superset of the seed.
  Its rows converged at `11.055617` (exp-060, iteration 8).
- **The certificate-seeded set's seed:** the grid plus T-018's `1121` atoms scaled by
  `382/381`, `4485` sites.

The exact restricted value on the bare grid seed is at least `78/7 = 11.142857`: that is
BC-200's iteration-0 LP value with rows still violated, and a row relaxation bounds the
full restricted value from below.
So on the seed itself the plateau does not exist; it arose on the sites column
generation added.

## 3. The artefact test

### 3.1 Construction

Trump's packing is built exactly over `Q(u)`, `u = tan(a/2)`, from
`cases/trump11/packing.py`, and its side `U` and eleven centres are enclosed to sixty
digits. Each centre is scaled by `λ` and rounded to denominator `10⁹`. The six
axis-parallel squares get net direction `0`; the five tilted squares get the net
direction nearest Trump's angle, `k = 159`, `t = 10976671/30000000`, `40.194037°`,
which is `0.012100°` above Trump's `40.181937°`. Each core is the closed `B`-square at
its direction, and its centre is clamped into the admissible domain `[h, L − h]²`,
`h = B (cos θ + sin θ) / 2`, so that every core is a row of the LP. The clamp moves the
six axis cores inward by `0.006212` (the wall gap `(B − λ) / 2`) and the two tilted
cores that touch the bottom and right walls by `0.008766`; the other three tilted cores
are already admissible.
A second variant rotates the tilted block rigidly about the centroid of its five
centres by the `0.0121°` so that the block's internal contacts are kept exactly; it
changes nothing below and is reported only in the appendix output.

The strip width of the hypothesis, `B − λ = 0.012423`, is exactly the overlap of two
unclamped cores that were edge-to-edge in Trump's packing.

### 3.2 The strip geometry (EXACT)

Pairwise intersections of the clamped closed cores, computed as rational polygons
(Sutherland–Hodgman clipping in `Fraction`); width and length are the least and
greatest extent of the polygon over the four edge normals of the two squares.
Fourteen pairs overlap; total overlap area `0.110623`.

| Pair | Kind | Area | Width | Length | Near |
| --- | --- | --- | --- | --- | --- |
| 3, 4 | axis, top-left corner row | `0.018592` | `0.018635` | `0.997700` | `(0.988, 3.321)` |
| 3, 5 | axis, top-left corner column | `0.018592` | `0.018635` | `0.997700` | `(0.499, 2.832)` |
| 4, 5 | axis, corner of the L | `0.000347` | `0.018635` | `0.018635` | `(0.988, 2.832)` |
| 6, 7 | tilted block | `0.018498` | `0.019114` | `0.967742` | `(1.581, 1.067)` |
| 6, 8 | tilted block | `0.010922` | `0.012399` | `0.880874` | `(1.592, 1.794)` |
| 7, 9 | tilted block | `0.016026` | `0.018056` | `0.887570` | `(2.247, 1.061)` |
| 8, 9 | tilted block | `0.012088` | `0.012418` | `0.973400` | `(2.258, 1.788)` |
| 9, 10 | tilted block | `0.012638` | `0.019050` | `0.663389` | `(2.851, 1.863)` |
| 0, 6 | axis–tilted corner triangle | `0.000569` | `0.023684` | `0.048042` | `(0.987, 0.986)` |
| 1, 9 | axis–tilted corner triangle | `0.000572` | `0.023738` | `0.048152` | `(2.835, 0.987)` |
| 2, 8 | axis–tilted corner triangle | `0.000361` | `0.018875` | `0.038287` | `(2.005, 2.832)` |
| 2, 10 | axis–tilted corner triangle | `0.000655` | `0.025417` | `0.051559` | `(2.981, 2.833)` |
| 4, 8 | axis–tilted corner triangle | `0.000398` | `0.019809` | `0.040182` | `(1.967, 2.831)` |
| 5, 6 | axis–tilted corner triangle | `0.000366` | `0.018988` | `0.038517` | `(0.988, 1.852)` |

Only the two interior block pairs `(6, 8)` and `(8, 9)` have the hypothesis's width;
every strip against a wall square is `0.0186` to `0.0254` wide because the clamp pushes
the wall cores inward.

### 3.3 The site census on the strips (EXACT)

For every site the number of cores containing it, by `Square.covers` on exact centred
coordinates.

| Site set | Sites | In no core | In one | In two | In three | Verdict |
| --- | --- | --- | --- | --- | --- | --- |
| grid seed, BC-191 density | `3365` | `575` | `2745` | `44` | `1` | not site-free |
| BC-200 retained state | `12761` | `2352` | `9587` | `660` | `162` | not site-free |
| grid + T-018 atoms × `382/381` | `4485` | `591` | `3732` | `158` | `4` | not site-free |

On the grid seed the `45` doubly covered sites sit on the strips `(6, 7)`: `7`,
`(3, 5)`: `7`, `(3, 4)`: `7`, `(7, 9)`: `6`, `(9, 10)`: `4`, `(8, 9)`: `3`, `(6, 8)`:
`2`, and one each on `(0, 6)`, `(1, 9)`, `(2, 10)` and the triple `(3, 4, 5)`. The
grid coordinate `1987/2000 = 0.9935` of the `41`-grid runs the length of both axis
strips, which is why the corner row and column each catch seven.
The block-rotated variant gives the same counts.

### 3.4 A site-free Trump-shaped family? (CHECKED, then EXACT)

Because the canonical configuration is one point of a family, the test was extended by
a perturbation search: single-centre moves of `0.001` to `0.02`, whole-block moves, and
the tilted net index in `157..161`, each move clamped into the admissible domain and
accepted when the count of doubly covered grid-seed sites did not rise; four seeds of
`20000` trials.
Every seed bottomed out at `5` doubly covered sites (net index `161` three times, `157`
once), and the best configuration re-decided exactly has `5`. No site-free
Trump-shaped family was found; the search proves nothing about existence and is
recorded as its floor.

### 3.5 Verdict

For the canonical configuration and for every configuration the search reached, the
eleven Trump-shaped cores are not pairwise site-disjoint on any site set that can be
rebuilt from the record.
The mechanism H-133 names does not produce the plateau on these sets, and cannot have
produced it on the `6637`-site set unless column generation removed no site from the
seed, which it does not do: the seed is a subset of every set it grows.
Since the seed alone already carries `45` sites in the strips, the `6637`-site set did
too, and Trump's unit family was never dual-feasible there.

## 4. What the instrument's dual looks like near the plateau

Two exact readings say what the plateau dual is instead.

- **BC-200's retained family at `191/50`** (RECORD, EXACT reading of the file): `760`
  placements after `D4`, depth-scaled total `9.907906` from a raw restricted value of
  `11.055617`. Folded into `[0°, 45°]`, `50.7 %` of the weight is within `2.5°` of the
  axes (`1.98` at `0.26°`, `1.23` at `0°`), `16.9 %` in `[2.5°, 12°)`, `25.2 %` in
  `[25°, 35°)` (`0.67` at `29.15°`, `0.55` at `28.90°`), `2.1 %` in `[35°, 38.2°)`,
  `1.1 %` in `[38.2°, 42.2°)` and `1.0 %` above. Within `1°` of Trump's angle: `0.0139`.
  This is the near-axis-plus-`29°` dual X-021 describes, not eleven squares at `40.18°`.
- **Run 0's dual** (EXACT): the row-converged LP on the grid plus the strip sites of
  Section 5 has optimum `1223/110 = 11.118181818`; its dual, read as `256` squares after
  `D4`, has exact maximum pointwise depth `1.985950` over `301180` arrangement vertices
  (`26308` decided exactly), feasible total `5.496255`. As the sites see it the family
  is a packing; at the vertices it is almost two deep.

So the artefact mechanism is real and general: the restricted dual sits on overlaps
that no site samples, but the overlaps are those of a fractional near-axis family,
and adding sites at Trump's contacts leaves them untouched.

## 5. Run 1: column generation with the strips filled

Inputs (all EXACT): `n = 11`, `L = 191/50`, `B = 9977/10000`, angle limit
`207107/500000`, `180` steps, inset `1/2`, grid counts `auto = (25, 34, 41)`, plus
`70` strip points (nine on the long axis of each four-vertex strip, the centroid of
each triangle, rounded to denominator `10⁵` and kept only if exactly inside both cores
of the pair; listed in the appendix), `484` sites after `D4` closure, `3849` sites in
`518` orbits at the start; `column_rounds = 400`, `max_rounds = 60`,
`rows_per_direction = 3`, `support_cap = 32` (the library default), rationalisation
scale `4000000`; deadline `2400 s` from launch at `04:47:39Z`; no warm start (none is
retained for the plateau runs); one worker, `PACK_JOBS=1`, load average `3.7` to `4.1`.

Command: `python -m devtools.run_fractional_colgen --n 11 --side 191/50 --shrink
9977/10000 --grid-counts auto --column-rounds 400 --max-rounds 60 --seed-certificate
trump-strip-sites.json --seed-map scale --deadline-seconds 2400 --log --row-log --json
--freeze`.

RUN1-TABLE

RUN1-READING

## 6. The tight-cell census

CENSUS-SECTION

## 7. The exact-cover reading and obstructions

CENSUS-READING

Obstructions recorded:

- **The plateau site sets are gone.** The `6637`-site and `24069`-site runs retained no
  log, no state and no measure; the only exactly-eleven objects in the record are the
  narrative values and the dual statistics of exp-060. A census of *the* plateau
  measure, and the exact cover over it, cannot be run until a run reproduces one, and
  Section 5 shows that reproduction is not a matter of re-running the driver.
- **Strip sites are the wrong remedy.** They break Trump's unit family, which was never
  the dual; the value the instrument stops at is pinned by a fractional near-axis family
  whose overlaps move when a single site is added (Section 5), so the remedy is the
  cutting-plane loop's vertex orbits at every iteration, which BC-200 already runs.
- **Small-denominator optima.** `78/7`, `1223/110` and `11.000000` are the LP values on
  successive site sets; they are vertices of a program whose active rows are few, and
  a value this round is a sign of degeneracy, not of a covering value.

## 8. Recommended status for H-133 and the next step

Recommended: **refuted as stated, with the general mechanism confirmed.** The
`open_question` should close with the reading that the plateau is the instrument's
(site-invisible overlaps of a fractional near-axis dual, column generation stopping on
a degenerate optimum), that Trump-shaped strips are not where the overlaps are, and
that `τ*_B(191/50) < 11` is neither shown nor refuted.
No claim is frozen; no experiment id is needed.

First for the next session: NEXT-STEP

## Appendix: scripts and outputs as run

All scripts ran from `packing/` with `PACK_JOBS=1 PYTHONPATH=.` and the project venv.

APPENDIX

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
