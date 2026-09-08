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
host shared with seven other agents (load average 3.7 to 4.1 while the runs were on), so
no wall time below is comparable with the planning lane’s or with BC-200’s.

Notation: `L = 191/50`, `B = 9977/10000` (the retained shrink), the retained net of
`181` directions `t_k = (207107/500000) k / 180`, `U = 3.877083590022814` (Trump),
`λ = L / U = 0.98527667`. A *core* is a closed `B`-square at a net direction inside the
container, which is what a row of the covering LP is (X-014 Lemma 1). Status labels:
EXACT (a rational decision by the repository’s own primitives), CHECKED (a float
computation), RECORD (read from a retained file), OPEN.

## 0. Findings in one page

| Question | Answer | Status |
| --- | --- | --- |
| Is the plateau Trump’s eleven `B`-cores overlapping only in site-free strips? | No, for the canonical configuration: the clamped cores overlap in fourteen strips `0.0124` to `0.0254` wide, and `45` of the `3365` grid-seed sites, `822` of BC-200’s `12761` retained sites and `162` of the grid plus T-018’s atoms lie in two or more cores. A perturbation search over centres and the tilted net index bottoms out at `5` doubly covered grid-seed sites in `80000` trials. | EXACT (verdict), CHECKED (search) |
| Is the plateau a site artefact at all? | Yes, in the general sense the record already carries: every dual the instrument returns at `191/50` is site-disjoint but not point-disjoint. The row-converged dual on grid plus strip sites has exact pointwise depth `1.98595`; BC-200’s raw-total-eleven dual had `1925/1152`. The artefact is not Trump-shaped: BC-200’s dual carries `50.7 %` of its weight within `2.5°` of the axes, `25.2 %` in `[25°, 35°]` and `1.1 %` within `2°` of Trump’s angle. | EXACT (depths), RECORD |
| Does filling the strips give a certificate below eleven? | No. Column generation from the grid plus `484` strip sites ran `66` column rounds in `2080 s` and stopped by its own criterion at `11.072443` (rationalised `553677/50000` over `384` atoms; exactly swept, a valid measure with least cell mass `40003/40000`, failing only Condition 2). The objective descended in seven steps from `1223/110` and never approached eleven; the last priced dual’s heaviest `32` rows carry `9.26` of its `11.07` units and screen as a packing, so the stop is the pricing’s truncated view, the same shape as the plateau run’s stop. | EXACT (values), RECORD (table) |
| The tight-cell census | On the one exactly decided measure of this block (mass `11.118805`, valid, `213` atoms): `0` cells exactly tight, `442292` within `1/1000` of one in `6000` components, `1934092` within the gap `13/110` in `18440` components over `21997353` reachable cells and the whole centre domain; at directions `0` and `159` under `5 %` of the tight cells lie within `0.05` of a Trump core. Above the agenda’s one-million threshold; recorded as the obstruction to the exact cover. | EXACT |
| The shrink tax | Not measured; the block ended with the census. | OPEN |

What this changes for H-133: the *specific* mechanism the hypothesis names (Trump’s
cores, site-free strips) is refuted on every reconstructible site set, and the *general*
mechanism (site-invisible overlaps of a fractional, near-axis dual) is confirmed and is
the record’s own reading of exp-060. The plateau at exactly eleven on the lost
`6637`-site set is therefore best read as an instrument stop of the column generator on
a degenerate site-set optimum, not as a statement about `τ*(191/50)`; whether
`τ*_B(191/50)` is below eleven remains OPEN, and the route to it is the cutting-plane
loop’s systematic site addition, not strips at Trump’s contacts.

## 1. The question and the falsifiers

BC-297 asks whether the restricted covering value of exactly `11.000000` that two site
sets reached at `191/50` is an artefact of Trump-shaped `B`-cores overlapping only in
site-free strips, what the shrink tax is there, and whether the plateau closes as an
exact cover. The lane’s priority order was the thirty-minute artefact test, then strip
sites and a column-generation run of at most forty minutes, then the census and the
exact-cover reading, then the tax if time remained.

Falsifiers, stated before each run:

- *Artefact test.* H-133’s mechanism is refuted for a configuration if at least one site
  of the reconstructed site set lies in two of its eleven cores; it is exhibited if none
  does, because then the unit dual on the eleven rows is feasible for the restricted
  covering LP on that site set and its optimum is at least eleven whatever rows are
  generated (the reading rule `window_lattice` documents in
  `devtools/run_fractional_colgen.py`).
- *Run 1 (strips filled).* The run fails to yield a certificate if its converged
  restricted value stays at or above eleven, or it ends unconverged at the deadline, or
  a frozen candidate is refused by `devtools.decide_certificate`. Only an exactly
  verified measure counts; a float optimum is context.
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
angle limit `207107/500000`, `180` steps (exp-060, exp-070). Neither final site set can
be rebuilt: column generation adds one orbit per round from the arrangement vertices of
the dual, and the added orbits are in the lost logs.

What can be rebuilt exactly (EXACT):

- **The grid seed at BC-191’s density.** `site_counts_for_side(191/50, 9977/10000)`
  gives counts `(25, 34, 41)` at inset `1/2`; their union is `3365` sites in `457`
  orbits, which is BC-200’s recorded `initial_sites` at this side, so this is the seed
  every driver-era run at `191/50` started from.
  Its `87` distinct coordinates have gaps from `0.0021` to `0.0705`, mean `0.0328`; the
  three pitches are `0.1175`, `0.0855` and `0.0705`. The “pitch `0.047`” of the
  hypothesis is `3.82 / 81`, an average, not a coordinate spacing.
- **BC-200’s retained state** (`results/bc-200-state-191-50.json`): `12761` sites in
  `1657` orbits, the grid seed plus eight rounds of violating arrangement vertices, a
  superset of the seed.
  Its rows converged at `11.055617` (exp-060, iteration 8).
- **The certificate-seeded set’s seed:** the grid plus T-018’s `1121` atoms scaled by
  `382/381`, `4485` sites.

The exact restricted value on the bare grid seed is at least `78/7 = 11.142857`: that is
BC-200’s iteration-0 LP value with rows still violated, and a row relaxation bounds the
full restricted value from below.
So on the seed itself the plateau does not exist; it arose on the sites column
generation added.

## 3. The artefact test

### 3.1 Construction

Trump’s packing is built exactly over `Q(u)`, `u = tan(a/2)`, from
`cases/trump11/packing.py`, and its side `U` and eleven centres are enclosed to sixty
digits. Each centre is scaled by `λ` and rounded to denominator `10⁹`. The six
axis-parallel squares get net direction `0`; the five tilted squares get the net
direction nearest Trump’s angle, `k = 159`, `t = 10976671/30000000`, `40.194037°`, which
is `0.012100°` above Trump’s `40.181937°`. Each core is the closed `B`-square at its
direction, and its centre is clamped into the admissible domain `[h, L − h]²`,
`h = B (cos θ + sin θ) / 2`, so that every core is a row of the LP. The clamp moves the
six axis cores inward by `0.006212` (the wall gap `(B − λ) / 2`) and the two tilted
cores that touch the bottom and right walls by `0.008766`; the other three tilted cores
are already admissible.
A second variant rotates the tilted block rigidly about the centroid of its five centres
by the `0.0121°` so that the block’s internal contacts are kept exactly; it changes
nothing below and is reported only in the appendix output.

The strip width of the hypothesis, `B − λ = 0.012423`, is exactly the overlap of two
unclamped cores that were edge-to-edge in Trump’s packing.

### 3.2 The strip geometry (EXACT)

Pairwise intersections of the clamped closed cores, computed as rational polygons
(Sutherland–Hodgman clipping in `Fraction`); width and length are the least and greatest
extent of the polygon over the four edge normals of the two squares.
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

Only the two interior block pairs `(6, 8)` and `(8, 9)` have the hypothesis’s width;
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
`2`, and one each on `(0, 6)`, `(1, 9)`, `(2, 10)` and the triple `(3, 4, 5)`. The grid
coordinate `1987/2000 = 0.9935` of the `41`-grid runs the length of both axis strips,
which is why the corner row and column each catch seven.
The block-rotated variant gives the same counts.

### 3.4 A site-free Trump-shaped family? (CHECKED, then EXACT)

Because the canonical configuration is one point of a family, the test was extended by a
perturbation search: single-centre moves of `0.001` to `0.02`, whole-block moves, and
the tilted net index in `157..161`, each move clamped into the admissible domain and
accepted when the count of doubly covered grid-seed sites did not rise; four seeds of
`20000` trials. Every seed bottomed out at `5` doubly covered sites (net index `161`
three times, `157` once), and the best configuration re-decided exactly has `5`. No
site-free Trump-shaped family was found; the search proves nothing about existence and
is recorded as its floor.

### 3.5 Verdict

For the canonical configuration and for every configuration the search reached, the
eleven Trump-shaped cores are not pairwise site-disjoint on any site set that can be
rebuilt from the record.
The mechanism H-133 names does not produce the plateau on these sets, and, if the
`6637`-site run grew from the grid at BC-191’s density as exp-060 records for the dual
it regenerated, it cannot have produced it there either: column generation only adds
orbits, so the seed’s `45` strip sites were in that set too and Trump’s unit family was
never dual-feasible on it.

## 4. What the instrument’s dual looks like near the plateau

Two exact readings say what the plateau dual is instead.

- **BC-200’s retained family at `191/50`** (RECORD, EXACT reading of the file): `760`
  placements after `D4`, depth-scaled total `9.907906` from a raw restricted value of
  `11.055617`. Folded into `[0°, 45°]`, `50.7 %` of the weight is within `2.5°` of the
  axes (`1.98` at `0.26°`, `1.23` at `0°`), `16.9 %` in `[2.5°, 12°)`, `25.2 %` in
  `[25°, 35°)` (`0.67` at `29.15°`, `0.55` at `28.90°`), `2.1 %` in `[35°, 38.2°)`,
  `1.1 %` in `[38.2°, 42.2°)` and `1.0 %` above.
  Within `1°` of Trump’s angle: `0.0139`. This is the near-axis-plus-`29°` dual X-021
  describes, not eleven squares at `40.18°`.
- **Run 0’s dual** (EXACT): the row-converged LP on the grid plus the strip sites of
  Section 5 has optimum `1223/110 = 11.118181818`; its dual, read as `256` squares after
  `D4`, has exact maximum pointwise depth `1.985950` over `301180` arrangement vertices
  (`26308` decided exactly), feasible total `5.496255`. As the sites see it the family
  is a packing; at the vertices it is almost two deep.

So the artefact mechanism is real and general: the restricted dual sits on overlaps that
no site samples, but the overlaps are those of a fractional near-axis family, and adding
sites at Trump’s contacts leaves them untouched.

## 5. Run 1: column generation with the strips filled

Inputs (all EXACT): `n = 11`, `L = 191/50`, `B = 9977/10000`, angle limit
`207107/500000`, `180` steps, inset `1/2`, grid counts `auto = (25, 34, 41)`, plus `70`
strip points (nine on the long axis of each four-vertex strip, the centroid of each
triangle, rounded to denominator `10⁵` and kept only if exactly inside both cores of the
pair; listed in the appendix), `484` sites after `D4` closure, `3849` sites in `518`
orbits at the start; `column_rounds = 400`, `max_rounds = 60`, `rows_per_direction = 3`,
`support_cap = 32` (the library default), rationalisation scale `4000000`; deadline
`2400 s` from launch at `04:47:39Z`; no warm start (none is retained for the plateau
runs); one worker, `PACK_JOBS=1`, load average `3.7` to `4.1`.

Command: `python -m devtools.run_fractional_colgen --n 11 --side 191/50 --shrink
9977/10000 --grid-counts auto --column-rounds 400 --max-rounds 60 --seed-certificate
trump-strip-sites.json --seed-map scale --deadline-seconds 2400 --log --row-log --json
--freeze`.

The run ran `66` column rounds (`0` to `65`) in `2080.3 s` of wall and stopped by the
generator’s own criterion, “no candidate orbit has averaged depth above 1”, before its
deadline; the row loop converged at every round (least covered mass `1 − 10⁻¹⁰` or
closer in floats). One orbit of negative reduced cost was added per round, and the
objective moved in seven steps:

| Rounds | Sites | Rows | LP objective | Depth at the priced vertex |
| --- | --- | --- | --- | --- |
| `0`–`12` | `3849`–`3933` | `5732`–`6926` | `11.118181818` (`1223/110`) | `1.07`–`1.92` |
| `13`–`30` | `3941`–`4073` | `8294`–`9073` | `11.098818475` | `1.01`–`1.27` |
| `31`–`36` | `4081`–`4117` | `9456`–`9641` | `11.095119344` | `1.20`–`1.41` |
| `37` | `4121` | `9763` | `11.093829679` | `1.13` |
| `38`–`40` | `4129`–`4141` | `9958`–`9983` | `11.082608208` | `1.00`–`1.62` |
| `41`–`59` | `4145`–`4277` | `10038`–`10469` | `11.082501622` | `1.02`–`1.50` |
| `60`–`64` | `4285`–`4317` | `10478`–`10480` | `11.072443466` | `1.02`–`1.14` |
| `65` | `4325` | `10480` | `11.072443466` | none above `1` |

Final state: `4325` sites in `583` orbits, `10480` rows.
The frozen candidate is `553677/50000 = 11.073540` over `384` atoms; swept exactly with
one worker its least cell mass is `40003/40000 = 1.000075` at direction `0`, so it is a
valid measure that fails only Condition 2 (EXACT). Nothing was below eleven at any
round, so `decide_certificate` was not run on a claim and no identifier is needed.

Reading (EXACT where the depths are named, otherwise RECORD of the driver’s table):

- **The objective is degenerate.** Every added orbit had strictly negative reduced cost
  against the dual of the moment (`−0.02` to `−7.3`), yet the objective stayed fixed for
  runs of thirteen, eighteen and nineteen rounds: the LP has many optimal duals of the
  same value, and a site that breaks one is invisible to the next.
  The plateau at `1223/110` on the strip-filled seed is the same phenomenon as the
  plateau at eleven on the lost set, one site set earlier.
- **The strips did nothing.** The seventy strip points break Trump’s unit family, but
  the dual at every round was a fractional family whose deepest vertex sat elsewhere
  (`(2.817, 1.003)`, `(1.005, 2.817)`, `(2.821, 0.997)`, ... in the driver’s notes,
  wall-hugging placements near the container’s mid-walls, not the tilted block).
- **The stop is the pricing’s, not the site set’s.** The generator prices from the
  arrangement vertices of the dual’s heaviest `32` rows (`dual_squares` with
  `support_cap = 32`, `256` squares after `D4`). At round `65` that truncated dual
  totals `9.263227` of the `11.072443` units of dual weight and screens with no vertex
  above depth one among `272536`, so the criterion fires while `1.81` units of dual
  weight, in rows the pricing never sees, remain free to overlap.
  A run that stops this way reports whatever value the LP has at that moment; on the
  lost `6637`-site set that value was `11.000000`, here it is `11.072443`, and neither
  is a converged site-set optimum in the sense the register’s `converged: true`
  suggests.

Not run: the warm-started continuation of BC-200’s cutting-plane loop from its retained
state, which adds vertex orbits from the exact depth check over the full dual and is the
route Section 8 recommends; when run 1 ended at `05:28Z` the host’s load average was `8`
to `9`, and an iteration on `12761` sites costs about `400 s` at load `4` (exp-060), so
two iterations would have fitted and measured nothing the record does not already hold.

## 6. The tight-cell census

The object is run 0’s measure, the only exactly decided measure at `191/50` this block
produced: the row-converged restricted LP on the grid seed plus the strip sites (one
column round, `23` LP rounds, `5732` rows, optimum `1223/110`), rationalised at scale
`4000000` to `213` atoms of total mass `2223761/200000 = 11.118805`, swept exactly with
one worker: least cell mass `200009/200000 = 1.000045` at direction `0`, so it is a
valid measure failing only Condition 2 (its mass gap is `ε = 23761/200000 = 0.118805`).
The census is `devtools.census_tight_cells` on that file (SHA-256 `29d3c78c…80cb84`),
complete over the `181` directions, margins `0, 1/1000, 1/100, 1/20, 1/10, 13/110`;
every count is an integer comparison on the weights’ common scale `200000` (EXACT).

| Margin above `1` | Tight cells | Of reachable | Components | Most per direction | Largest component |
| --- | --- | --- | --- | --- | --- |
| `0` | `0` | `0` | `0` | `0` | `0` |
| `1/1000` | `442292` | `2.01 %` | `6000` | `68` | `856` |
| `1/100` | `545584` | `2.48 %` | `7812` | `76` | `865` |
| `1/20` | `795384` | `3.62 %` | `11876` | `116` | `879` |
| `1/10` | `1463492` | `6.65 %` | `18100` | — | — |
| `13/110` | `1934092` | `8.79 %` | `18440` | — | — |

Reachable cells: `21997353` over the net, `8281` at direction `0` and about `106000` to
`121000` at every tilted direction.
No cell is exactly tight, which is what a rationalised LP vertex looks like: the minimum
sits `9/200000` above one.
At the gap margin `13/110` (just below `ε`) the near-tight set is `1.93` million cells
in `18440` components and its bounding box at direction `0` is the whole centre domain.

Where the tight cells are (`tight_locality.py`, the same grid, EXACT selection with a
float readout):

- Direction `0`: `80` cells within `1/1000` of one, `440` within `13/110`. One of the
  `80` lies within `0.05` of one of Trump’s six axis cores; the dense bins are the
  wall-middle placements `(0.5, 2.1)`, `(2.1, 0.5)`, `(2.1, 3.1)`, `(3.1, 2.1)` and the
  wall run `(0.5, 1.6)` to `(0.5, 2.2)`: axis squares flush against a wall near its
  middle, not in the corners where Trump’s are.
- Direction `159`: `468` cells within `1/1000`, `7436` within `13/110`. `4.7 %` of the
  former and `4.0 %` of the latter lie within `0.05` of a tilted Trump core; the dense
  bins are the four corners `(0.7, 0.7)`, `(0.8, 3.0)`, `(3.1, 0.7)`, `(3.0, 3.0)`:
  tilted squares snug in the container’s corners, where Trump has axis squares.

So the tight set is the support of the near-axis fractional dual of Section 4 seen from
the primal side, and it does not cluster on Trump’s cores.

## 7. The exact-cover reading and obstructions

Corollary 1a at this measure says: every atom heavier than `ε = 0.118805` lies in
exactly one core of any packing at `191/50`, and each core is an event cell of mass at
most `1 + ε`. Of the `213` atoms, `8` (all at `30001/200000`) weigh more than `ε`, so
the ownership skeleton is small; but the cells that could own them are the `1.93`
million near-tight cells above, in `18440` components spread over the whole centre
domain at every direction, and the exact cover would branch over them.
That is the census the agenda names as the obstruction: above one million cells, and
clustered only in the weak sense that a direction’s tight set falls into a few dozen
connected components, none of which sits on Trump’s cores.
At `ε = 0`, the plateau certificate’s regime, the tight set would be the cells of mass
exactly one, which for a rationalised measure is empty; the exact-cover reading needs an
exact optimum at exactly eleven, and the block found none: the optimum on every site set
it built is a rational strictly above eleven (`78/7`, `1223/110`, and run 1’s
`11.072443` whose candidate is `553677/50000`).

Obstructions recorded:

- **The plateau site sets are gone.** The `6637`-site and `24069`-site runs retained no
  log, no state and no measure; the only exactly-eleven objects in the record are the
  narrative values and the dual statistics of exp-060. A census of *the* plateau
  measure, and the exact cover over it, cannot be run until a run reproduces one, and
  Section 5 shows that reproduction is not a matter of re-running the driver.
- **Strip sites are the wrong remedy.** They break Trump’s unit family, which was never
  the dual; the value the instrument stops at is pinned by a fractional near-axis family
  whose overlaps move when a single site is added (Section 5), so the remedy is the
  cutting-plane loop’s vertex orbits at every iteration, which BC-200 already runs.
- **Small-denominator optima.** `78/7`, `1223/110` and `11.000000` are the LP values on
  successive site sets; they are vertices of a program whose active rows are few, and a
  value this round is a sign of degeneracy, not of a covering value.

## 8. Recommended status for H-133 and the next step

Recommended: **refuted as stated, with the general mechanism confirmed.** The
`open_question` should close with the reading that the plateau is the instrument’s
(site-invisible overlaps of a fractional near-axis dual, column generation stopping on a
degenerate optimum), that Trump-shaped strips are not where the overlaps are, and that
`τ*_B(191/50) < 11` is neither shown nor refuted.
No claim is frozen; no experiment id is needed.

First for the next session: re-run run 1’s final site set with the column generator
pricing on the full dual (`support_cap` raised past the support, a one-line library
parameter that the driver does not expose) and see whether the generator’s stop moves;
if it does, the exactly-eleven stop of the lost run was the cap’s and the register’s
`converged: true` for that row should be read as “the pricing stopped”.
Then continue BC-200’s cutting-plane loop from `results/bc-200-state-191-50.json`
(`--warm`, the exp-060 settings) on an unloaded core and retain its state at every
iteration, so that the next plateau, if one appears, is an object and not a narrative.

## Appendix: scripts and outputs as run

All scripts ran from `packing/` with `PACK_JOBS=1 PYTHONPATH=.` and the project venv.

### `artefact_test.py`

The exact artefact test.

```text
"""BC-297 artefact test: are Trump's eleven B-cores at 191/50 pairwise site-free?

Construction (exact, rational): Trump's packing over Q(u) is scaled by
lambda = (191/50) / U to side 191/50; each square's centre is rounded to a rational
with denominator 10^9; each core is the closed B-square (B = 9977/10000) at the
nearest net direction (t_k = (207107/500000) k / 180, k = 0 .. 180), with its centre
clamped into the admissible centre domain [h, L - h]^2, h = B (cos + sin) / 2, so
that every core is an admissible row of the covering LP. Two variants of the tilted
block: (a) centres kept at the scaled positions; (b) the block rotated rigidly about
the centroid of its five centres by (theta_k - a) so the intra-block geometry is kept.

Decision (exact): for every reconstructible site set, the multiplicity of each site
over the eleven closed cores. If no site has multiplicity >= 2, the unit dual on the
eleven rows is feasible for the restricted covering LP on that site set and its
optimum is >= 11 whatever rows are generated (window_lattice's reading rule).
Also reported exactly: every pairwise intersection polygon (area; width and length as
the least and greatest extent over the two squares' edge normals).
"""

from __future__ import annotations

import json
import math
import sys
from fractions import Fraction
from pathlib import Path

from cases.trump11.packing import build
from sqpack.fractional.colgen import (
    Square,
    site_counts_for_side,
    site_set_from_grids,
    site_set_from_points,
    square_at,
)
from sqpack.fractional.generate import direction_net, net_half_tangents
from sqpack.fractional.model import Direction

L = Fraction(191, 50)
B = Fraction(9977, 10000)
ANGLE_LIMIT = Fraction(207107, 500000)
STEPS = 180
DEN = 10**9
RESULTS = Path(
    "scratchpad/"
    "wt-lane-297/packing/campaign/series/series-000-smoke-and-calibration/results"
)
T018 = Path(
    "scratchpad/"
    "wt-lane-297/packing/cases/n11_fractional_certificate/certificate.json"
)


def mid(field, e, den: int = DEN) -> Fraction:
    lo, hi = field.enclose(e)
    return Fraction(round((lo + hi) / 2 * den), den)


def clip(poly: list[tuple[Fraction, Fraction]], a: Fraction, b: Fraction, c: Fraction):
    """Keep the part of the convex polygon with a x + b y <= c (Sutherland-Hodgman)."""

    out: list[tuple[Fraction, Fraction]] = []
    n = len(poly)
    for i in range(n):
        p, q = poly[i], poly[(i + 1) % n]
        fp, fq = a * p[0] + b * p[1] - c, a * q[0] + b * q[1] - c
        if fp <= 0:
            out.append(p)
        if (fp < 0 < fq) or (fq < 0 < fp):
            t = fp / (fp - fq)
            out.append((p[0] + t * (q[0] - p[0]), p[1] + t * (q[1] - p[1])))
    return out


def corners_of(sq: Square) -> list[tuple[Fraction, Fraction]]:
    """The square's corners in centred coordinates, counter-clockwise."""

    pts = []
    for su, sv in ((-1, -1), (1, -1), (1, 1), (-1, 1)):
        u = sq.u + su * sq.half
        v = sq.v + sv * sq.half
        # solve [ax ay; bx by] q = (u, v); the matrix is a rotation, so inverse = transpose
        x = sq.ax * u + sq.bx * v
        y = sq.ay * u + sq.by * v
        pts.append((x, y))
    return pts


def half_planes(sq: Square):
    for (a, b, c) in sq.lines():
        yield (a, b, c)


def intersection(s1: Square, s2: Square) -> list[tuple[Fraction, Fraction]]:
    poly = corners_of(s1)
    (ax, ay, lo1), (_, _, hi1), (bx, by, lo2), (_, _, hi2) = s2.lines()
    for a, b, c in ((ax, ay, hi1), (-ax, -ay, -lo1), (bx, by, hi2), (-bx, -by, -lo2)):
        poly = clip(poly, a, b, c)
        if not poly:
            return []
    return poly


def area(poly) -> Fraction:
    s = Fraction(0)
    for i in range(len(poly)):
        p, q = poly[i], poly[(i + 1) % len(poly)]
        s += p[0] * q[1] - q[0] * p[1]
    return abs(s) / 2


def extents(poly, s1: Square, s2: Square) -> tuple[Fraction, Fraction]:
    widths = []
    for sq in (s1, s2):
        for nx, ny in ((sq.ax, sq.ay), (sq.bx, sq.by)):
            vals = [nx * p[0] + ny * p[1] for p in poly]
            widths.append(max(vals) - min(vals))
    return min(widths), max(widths)


def main() -> None:
    squares, side, field = build()
    field.refine_to(60)
    U = side
    u = field.alpha
    lam = field.rational(L) / U
    tangents = net_half_tangents(ANGLE_LIMIT, STEPS)
    net = direction_net(tangents)
    u_mid = mid(field, u, 10**15)
    k = round(u_mid / (ANGLE_LIMIT / STEPS))
    print(f"U = {field.decimal(U, 20)}  lambda = {field.decimal(lam, 20)}")
    print(f"u = tan(a/2) = {field.decimal(u, 20)}; nearest net index k = {k}, t_k = {tangents[k]} = {float(tangents[k]):.9f}")
    a_deg = math.degrees(2 * math.atan(float(u_mid)))
    ak_deg = math.degrees(2 * math.atan(float(tangents[k])))
    print(f"Trump angle = {a_deg:.6f} deg; net angle = {ak_deg:.6f} deg; difference = {ak_deg - a_deg:+.6f} deg")
    print(f"strip width B - lambda = {float(B - mid(field, lam, 10**15)):.6f}")

    centres = []
    for idx, sq in enumerate(squares):
        cx = sum((p[0] for p in sq), field.zero) / field.rational(4)
        cy = sum((p[1] for p in sq), field.zero) / field.rational(4)
        centres.append((mid(field, lam * cx), mid(field, lam * cy)))
    tilted = list(range(6, 11))

    def clamp(c: tuple[Fraction, Fraction], d: Direction) -> tuple[tuple[Fraction, Fraction], Fraction]:
        h = B * (d.ux + d.uy) / 2
        x = min(max(c[0], h), L - h)
        y = min(max(c[1], h), L - h)
        shift = max(abs(x - c[0]), abs(y - c[1]))
        return (x, y), shift

    variants: dict[str, list[tuple[Direction, tuple[Fraction, Fraction]]]] = {}
    # (a) centres as scaled
    placements_a = []
    for idx in range(11):
        d = net[0] if idx < 6 else net[k]
        placements_a.append((d, centres[idx]))
    variants["a-scaled-centres"] = placements_a
    # (b) tilted block rotated rigidly about its centroid by (theta_k - a)
    cxm = sum(centres[i][0] for i in tilted) / 5
    cym = sum(centres[i][1] for i in tilted) / 5
    dth = 2 * math.atan(float(tangents[k])) - 2 * math.atan(float(u_mid))
    placements_b = []
    for idx in range(11):
        if idx < 6:
            placements_b.append((net[0], centres[idx]))
        else:
            dx, dy = float(centres[idx][0] - cxm), float(centres[idx][1] - cym)
            rx = float(cxm) + dx * math.cos(dth) - dy * math.sin(dth)
            ry = float(cym) + dx * math.sin(dth) + dy * math.cos(dth)
            placements_b.append((net[k], (Fraction(round(rx * DEN), DEN), Fraction(round(ry * DEN), DEN))))
    variants["b-block-rotated"] = placements_b

    # site sets
    counts = site_counts_for_side(L, B)
    grid = site_set_from_grids(L, counts, Fraction(1, 2))
    print(f"grid counts at BC-191's density: {counts}; grid seed sites = {grid.size} (orbits {len(grid.orbits)})")
    state = json.loads((RESULTS / "bc-200-state-191-50.json").read_text())
    bc200_pts = {(Fraction(x), Fraction(y)) for x, y in state["sites"]}
    bc200 = site_set_from_points(L, bc200_pts)
    print(f"BC-200 retained state sites = {bc200.size} (orbits {len(bc200.orbits)}); grid subset of it: {set(grid.positions()) <= bc200_pts}")
    t018 = json.loads(T018.read_text())
    ratio = L / Fraction(t018["outer_side"])
    seed_pts = {(Fraction(x) * ratio, Fraction(y) * ratio) for x, y, _ in t018["atoms"]}
    seeded = site_set_from_points(L, set(grid.positions()) | seed_pts)
    print(f"T-018 atoms scaled by {ratio}: {len(seed_pts)} points; grid + seed sites = {seeded.size}")
    site_sets = {"grid-seed-3365": grid, "bc200-state": bc200, "grid+T018x382/381": seeded}

    report = {}
    for name, placements in variants.items():
        print(f"\n=== variant {name} ===")
        sqs = []
        for idx, (d, c) in enumerate(placements):
            cc, shift = clamp(c, d)
            sq = square_at(d, cc, L, B)
            sqs.append(sq)
            print(f"  core {idx:2d}: dir {d.label:>3} centre ({float(c[0]):.6f},{float(c[1]):.6f}) -> ({float(cc[0]):.6f},{float(cc[1]):.6f}) clamped shift {float(shift):.6f}  exact centre {cc[0]},{cc[1]}")
        # admissibility check: every corner inside the closed container
        half = L / 2
        for idx, sq in enumerate(sqs):
            for x, y in corners_of(sq):
                assert -half <= x <= half and -half <= y <= half, (idx, x, y)
        print("  all eleven cores admissible (inside the closed container): True")
        pairs = []
        total_area = Fraction(0)
        for i in range(11):
            for j in range(i + 1, 11):
                poly = intersection(sqs[i], sqs[j])
                if not poly:
                    continue
                ar = area(poly)
                if ar == 0:
                    continue
                w, ln = extents(poly, sqs[i], sqs[j])
                total_area += ar
                # polygon centroid in absolute coordinates, as a float for reading
                gx = sum(p[0] for p in poly) / len(poly) + half
                gy = sum(p[1] for p in poly) / len(poly) + half
                pairs.append((i, j, ar, w, ln, float(gx), float(gy)))
                print(f"  overlap ({i:2d},{j:2d}): area {float(ar):.6f} width {float(w):.6f} length {float(ln):.6f} near ({float(gx):.4f},{float(gy):.4f}) vertices {len(poly)}")
        print(f"  {len(pairs)} overlapping pairs; total overlap area {float(total_area):.6f}")
        for sname, sset in site_sets.items():
            mult = {}
            doubles = []
            for (x, y) in sset.positions():
                cx, cy = x - half, y - half
                hits = [idx for idx, sq in enumerate(sqs) if sq.covers(cx, cy)]
                mult[len(hits)] = mult.get(len(hits), 0) + 1
                if len(hits) >= 2:
                    doubles.append(((x, y), hits))
            verdict = "SITE-FREE overlaps: unit dual feasible, restricted optimum >= 11" if not doubles else "NOT site-free"
            print(f"  site set {sname}: multiplicities {dict(sorted(mult.items()))}; sites in >=2 cores: {len(doubles)} -> {verdict}")
            for (pt, hits) in doubles[:40]:
                print(f"      site ({float(pt[0]):.6f},{float(pt[1]):.6f}) = ({pt[0]},{pt[1]}) in cores {hits}")
            report[(name, sname)] = len(doubles)
        # dump the placements for reuse
        out = {
            "variant": name,
            "outer_side": str(L),
            "square_side": str(B),
            "placements": [
                {"k": int(d.label), "half_tangent": str(tangents[int(d.label)]), "centre": [str(c[0]), str(c[1])]}
                for (d, c) in [(p[0], clamp(p[1], p[0])[0]) for p in placements]
            ],
            "overlaps": [
                {"pair": [i, j], "area": str(ar), "width": str(w), "length": str(ln), "near": [gx, gy]}
                for (i, j, ar, w, ln, gx, gy) in pairs
            ],
        }
        Path(__file__).with_name(f"cores-{name}.json").write_text(json.dumps(out, indent=1))
    print("\nsummary (variant, site set) -> sites in >= 2 cores:")
    for key, val in report.items():
        print(f"  {key}: {val}")


if __name__ == "__main__":
    sys.setrecursionlimit(10000)
    main()
```

### `artefact_test.out`

Its output, both variants (the per-site listings are cut to the first eight of each
block).

```text
U = 3.877083590022814177307897060100962706376  lambda = 0.9852766677072138450864799770252624816125
u = tan(a/2) = 0.3657693076046772933885450181433113152391; nearest net index k = 159, t_k = 10976671/30000000 = 0.365889033
Trump angle = 40.181937 deg; net angle = 40.194037 deg; difference = +0.012100 deg
strip width B - lambda = 0.012423
grid counts at BC-191's density: (25, 34, 41); grid seed sites = 3365 (orbits 457)
BC-200 retained state sites = 12761 (orbits 1657); grid subset of it: True
T-018 atoms scaled by 382/381: 1121 points; grid + seed sites = 4485

=== variant a-scaled-centres ===
  core  0: dir   0 centre (0.492638,0.492638) -> (0.498850,0.498850) clamped shift 0.006212  exact centre 9977/20000,9977/20000
  core  1: dir   0 centre (3.327362,0.492638) -> (3.321150,0.498850) clamped shift 0.006212  exact centre 66423/20000,9977/20000
  core  2: dir   0 centre (2.495271,3.327362) -> (2.495271,3.321150) clamped shift 0.006212  exact centre 2495270617/1000000000,66423/20000
  core  3: dir   0 centre (0.492638,3.327362) -> (0.498850,3.321150) clamped shift 0.006212  exact centre 9977/20000,66423/20000
  core  4: dir   0 centre (1.477915,3.327362) -> (1.477915,3.321150) clamped shift 0.006212  exact centre 738957501/500000000,66423/20000
  core  5: dir   0 centre (0.492638,2.342085) -> (0.498850,2.342085) clamped shift 0.006212  exact centre 9977/20000,1171042499/500000000
  core  6: dir 159 centre (1.253522,1.431172) -> (1.253522,1.431172) clamped shift 0.000000  exact centre 1253522079/1000000000,1431171677/1000000000
  core  7: dir 159 centre (1.907964,0.694234) -> (1.907964,0.703000) clamped shift 0.008766  exact centre 190796353/100000000,14348052939641161543/20409746124844820000
  core  8: dir 159 centre (1.930761,2.156303) -> (1.930761,2.156303) clamped shift 0.000000  exact centre 1930760797/1000000000,2156302511/1000000000
  core  9: dir 159 centre (2.585202,1.419365) -> (2.585202,1.419365) clamped shift 0.000000  exact centre 323150281/125000000,1419364823/1000000000
  core 10: dir 159 centre (3.125766,2.306332) -> (3.117000,2.306332) clamped shift 0.008766  exact centre 63617177257266050857/20409746124844820000,1153166043/500000000
  all eleven cores admissible (inside the closed container): True
  overlap ( 0, 6): area 0.000569 width 0.023684 length 0.048042 near (0.9874,0.9855) vertices 3
  overlap ( 1, 9): area 0.000572 width 0.023738 length 0.048152 near (2.8346,0.9873) vertices 3
  overlap ( 2, 8): area 0.000361 width 0.018875 length 0.038287 near (2.0047,2.8320) vertices 3
  overlap ( 2,10): area 0.000655 width 0.025417 length 0.051559 near (2.9810,2.8334) vertices 3
  overlap ( 3, 4): area 0.018592 width 0.018635 length 0.997700 near (0.9884,3.3211) vertices 4
  overlap ( 3, 5): area 0.018592 width 0.018635 length 0.997700 near (0.4989,2.8316) vertices 4
  overlap ( 4, 5): area 0.000347 width 0.018635 length 0.018635 near (0.9884,2.8316) vertices 4
  overlap ( 4, 8): area 0.000398 width 0.019809 length 0.040182 near (1.9665,2.8309) vertices 3
  overlap ( 5, 6): area 0.000366 width 0.018988 length 0.038517 near (0.9879,1.8515) vertices 3
  overlap ( 6, 7): area 0.018498 width 0.019114 length 0.967742 near (1.5807,1.0671) vertices 4
  overlap ( 6, 8): area 0.010922 width 0.012399 length 0.880874 near (1.5921,1.7937) vertices 4
  overlap ( 7, 9): area 0.016026 width 0.018056 length 0.887570 near (2.2466,1.0612) vertices 4
  overlap ( 8, 9): area 0.012088 width 0.012418 length 0.973400 near (2.2580,1.7878) vertices 4
  overlap ( 9,10): area 0.012638 width 0.019050 length 0.663389 near (2.8511,1.8628) vertices 4
  14 overlapping pairs; total overlap area 0.110623
  site set grid-seed-3365: multiplicities {0: 575, 1: 2745, 2: 44, 3: 1}; sites in >=2 cores: 45 -> NOT site-free
      site (0.500000,2.826500) = (1/2,5653/2000) in cores [3, 5]
      site (0.993500,3.320000) = (1987/2000,83/25) in cores [3, 4]
      site (0.570500,2.826500) = (1141/2000,5653/2000) in cores [3, 5]
      site (0.993500,3.249500) = (1987/2000,6499/2000) in cores [3, 4]
      site (0.641000,2.826500) = (641/1000,5653/2000) in cores [3, 5]
      site (0.993500,3.179000) = (1987/2000,3179/1000) in cores [3, 4]
      site (0.711500,2.826500) = (1423/2000,5653/2000) in cores [3, 5]
      site (0.993500,3.108500) = (1987/2000,6217/2000) in cores [3, 4]
  site set bc200-state: multiplicities {0: 2352, 1: 9587, 2: 660, 3: 162}; sites in >=2 cores: 822 -> NOT site-free
      site (0.435872,2.822827) = (1680939256193018441441026731923751580469759599/3856498684820246735369735746441071966900468750,5232968494745922583967186596474122007561/1853804405773580846235297175325476140000) in cores [3, 5]
      site (0.997173,3.384128) = (1848564335309156248651648613269196847239/1853804405773580846235297175325476140000,6525442859910162043835681909740571666545015513/1928249342410123367684867873220535983450234375) in cores [3, 4]
      site (0.439175,2.822811) = (288962677721318222149870593446528267099738782704455603/657966568321940843653442684274573495263404800000000000,49821685443863034443021614282259693575499/17649668161920082202636068534476636480000) in cores [3, 5]
      site (0.997189,3.380825) = (17600046934671679571048167519441057778101/17649668161920082202636068534476636480000,2224469613268495800606280460482342484806467553295544397/657966568321940843653442684274573495263404800000000000) in cores [3, 4]
      site (0.439680,2.822574) = (434835304890252865872639497518209329642716458221/988981399398220406203959798478428464860000000000,148262535099063905703157942070981887063/52527415265444550248149786261510780000) in cores [3, 5]
      site (0.997426,3.380320) = (52392191214934276244774241447989292537/52527415265444550248149786261510780000,3343073640810949085826486932669387406122483541779/988981399398220406203959798478428464860000000000) in cores [3, 4]
      site (0.440035,2.822807) = (15136822678495893532766471760866804185327067/34399151804644926984287522978254597800000000,5209448022843345412859788355739169/1845484690664188451395629794060000) in cores [3, 5]
      site (0.997193,3.379965) = (1840303495493854471471517457570031/1845484690664188451395629794060000,116267937215247727547211866016065759410672933/34399151804644926984287522978254597800000000) in cores [3, 4]
  site set grid+T018x382/381: multiplicities {0: 591, 1: 3732, 2: 158, 3: 4}; sites in >=2 cores: 162 -> NOT site-free
      site (0.431129,2.827402) = (8213/19050,8977/3175) in cores [3, 5]
      site (0.992598,3.388871) = (6303/6350,32279/9525) in cores [3, 4]
      site (0.481260,2.837428) = (1528/3175,54053/19050) in cores [3, 5]
      site (0.982572,3.338740) = (9359/9525,21201/6350) in cores [3, 4]
      site (0.500000,2.826500) = (1/2,5653/2000) in cores [3, 5]
      site (0.993500,3.320000) = (1987/2000,83/25) in cores [3, 4]
      site (0.570500,2.826500) = (1141/2000,5653/2000) in cores [3, 5]
      site (0.993500,3.249500) = (1987/2000,6499/2000) in cores [3, 4]

=== variant b-block-rotated ===
  core  0: dir   0 centre (0.492638,0.492638) -> (0.498850,0.498850) clamped shift 0.006212  exact centre 9977/20000,9977/20000
  core  1: dir   0 centre (3.327362,0.492638) -> (3.321150,0.498850) clamped shift 0.006212  exact centre 66423/20000,9977/20000
  core  2: dir   0 centre (2.495271,3.327362) -> (2.495271,3.321150) clamped shift 0.006212  exact centre 2495270617/1000000000,66423/20000
  core  3: dir   0 centre (0.492638,3.327362) -> (0.498850,3.321150) clamped shift 0.006212  exact centre 9977/20000,66423/20000
  core  4: dir   0 centre (1.477915,3.327362) -> (1.477915,3.321150) clamped shift 0.006212  exact centre 738957501/500000000,66423/20000
  core  5: dir   0 centre (0.492638,2.342085) -> (0.498850,2.342085) clamped shift 0.006212  exact centre 9977/20000,1171042499/500000000
  core  6: dir 159 centre (1.253558,1.430980) -> (1.253558,1.430980) clamped shift 0.000000  exact centre 1253558067/1000000000,357745027/250000000
  core  7: dir 159 centre (1.908155,0.694181) -> (1.908155,0.703000) clamped shift 0.008819  exact centre 381631027/200000000,14348052939641161543/20409746124844820000
  core  8: dir 159 centre (1.930644,2.156254) -> (1.930644,2.156254) clamped shift 0.000000  exact centre 1930643631/1000000000,43125079/20000000
  core  9: dir 159 centre (2.585241,1.419454) -> (2.585241,1.419454) clamped shift 0.000000  exact centre 2585240699/1000000000,1419454489/1000000000
  core 10: dir 159 centre (3.125617,2.306536) -> (3.117000,2.306536) clamped shift 0.008617  exact centre 63617177257266050857/20409746124844820000,2306535893/1000000000
  all eleven cores admissible (inside the closed container): True
  overlap ( 0, 6): area 0.000574 width 0.023780 length 0.048237 near (0.9873,0.9854) vertices 3
  overlap ( 1, 9): area 0.000569 width 0.023694 length 0.048063 near (2.8345,0.9874) vertices 3
  overlap ( 2, 8): area 0.000357 width 0.018754 length 0.038042 near (2.0046,2.8320) vertices 3
  overlap ( 2,10): area 0.000663 width 0.025573 length 0.051875 near (2.9809,2.8335) vertices 3
  overlap ( 3, 4): area 0.018592 width 0.018635 length 0.997700 near (0.9884,3.3211) vertices 4
  overlap ( 3, 5): area 0.018592 width 0.018635 length 0.997700 near (0.4989,2.8316) vertices 4
  overlap ( 4, 5): area 0.000347 width 0.018635 length 0.018635 near (0.9884,2.8316) vertices 4
  overlap ( 4, 8): area 0.000400 width 0.019848 length 0.040261 near (1.9665,2.8310) vertices 3
  overlap ( 5, 6): area 0.000359 width 0.018818 length 0.038173 near (0.9880,1.8514) vertices 3
  overlap ( 6, 7): area 0.018537 width 0.019160 length 0.967500 near (1.5809,1.0670) vertices 4
  overlap ( 6, 8): area 0.010941 width 0.012423 length 0.880666 near (1.5921,1.7936) vertices 4
  overlap ( 7, 9): area 0.016075 width 0.018115 length 0.887403 near (2.2467,1.0612) vertices 4
  overlap ( 8, 9): area 0.012090 width 0.012423 length 0.973192 near (2.2579,1.7879) vertices 4
  overlap ( 9,10): area 0.012606 width 0.019006 length 0.663277 near (2.8511,1.8630) vertices 4
  14 overlapping pairs; total overlap area 0.110703
  site set grid-seed-3365: multiplicities {0: 575, 1: 2745, 2: 44, 3: 1}; sites in >=2 cores: 45 -> NOT site-free
      site (0.500000,2.826500) = (1/2,5653/2000) in cores [3, 5]
      site (0.993500,3.320000) = (1987/2000,83/25) in cores [3, 4]
      site (0.570500,2.826500) = (1141/2000,5653/2000) in cores [3, 5]
      site (0.993500,3.249500) = (1987/2000,6499/2000) in cores [3, 4]
      site (0.641000,2.826500) = (641/1000,5653/2000) in cores [3, 5]
      site (0.993500,3.179000) = (1987/2000,3179/1000) in cores [3, 4]
      site (0.711500,2.826500) = (1423/2000,5653/2000) in cores [3, 5]
      site (0.993500,3.108500) = (1987/2000,6217/2000) in cores [3, 4]
  site set bc200-state: multiplicities {0: 2352, 1: 9587, 2: 660, 3: 162}; sites in >=2 cores: 822 -> NOT site-free
      site (0.435872,2.822827) = (1680939256193018441441026731923751580469759599/3856498684820246735369735746441071966900468750,5232968494745922583967186596474122007561/1853804405773580846235297175325476140000) in cores [3, 5]
      site (0.997173,3.384128) = (1848564335309156248651648613269196847239/1853804405773580846235297175325476140000,6525442859910162043835681909740571666545015513/1928249342410123367684867873220535983450234375) in cores [3, 4]
      site (0.439175,2.822811) = (288962677721318222149870593446528267099738782704455603/657966568321940843653442684274573495263404800000000000,49821685443863034443021614282259693575499/17649668161920082202636068534476636480000) in cores [3, 5]
      site (0.997189,3.380825) = (17600046934671679571048167519441057778101/17649668161920082202636068534476636480000,2224469613268495800606280460482342484806467553295544397/657966568321940843653442684274573495263404800000000000) in cores [3, 4]
      site (0.439680,2.822574) = (434835304890252865872639497518209329642716458221/988981399398220406203959798478428464860000000000,148262535099063905703157942070981887063/52527415265444550248149786261510780000) in cores [3, 5]
      site (0.997426,3.380320) = (52392191214934276244774241447989292537/52527415265444550248149786261510780000,3343073640810949085826486932669387406122483541779/988981399398220406203959798478428464860000000000) in cores [3, 4]
      site (0.440035,2.822807) = (15136822678495893532766471760866804185327067/34399151804644926984287522978254597800000000,5209448022843345412859788355739169/1845484690664188451395629794060000) in cores [3, 5]
      site (0.997193,3.379965) = (1840303495493854471471517457570031/1845484690664188451395629794060000,116267937215247727547211866016065759410672933/34399151804644926984287522978254597800000000) in cores [3, 4]
  site set grid+T018x382/381: multiplicities {0: 591, 1: 3732, 2: 158, 3: 4}; sites in >=2 cores: 162 -> NOT site-free
      site (0.431129,2.827402) = (8213/19050,8977/3175) in cores [3, 5]
      site (0.992598,3.388871) = (6303/6350,32279/9525) in cores [3, 4]
      site (0.481260,2.837428) = (1528/3175,54053/19050) in cores [3, 5]
      site (0.982572,3.338740) = (9359/9525,21201/6350) in cores [3, 4]
      site (0.500000,2.826500) = (1/2,5653/2000) in cores [3, 5]
      site (0.993500,3.320000) = (1987/2000,83/25) in cores [3, 4]
      site (0.570500,2.826500) = (1141/2000,5653/2000) in cores [3, 5]
      site (0.993500,3.249500) = (1987/2000,6499/2000) in cores [3, 4]

summary (variant, site set) -> sites in >= 2 cores:
  ('a-scaled-centres', 'grid-seed-3365'): 45
  ('a-scaled-centres', 'bc200-state'): 822
  ('a-scaled-centres', 'grid+T018x382/381'): 162
  ('b-block-rotated', 'grid-seed-3365'): 45
  ('b-block-rotated', 'bc200-state'): 822
  ('b-block-rotated', 'grid+T018x382/381'): 162
```

### `strip_sites.py`

The strip sites.

```text
"""Exact sites inside the fourteen overlap strips of Trump's clamped B-cores at 191/50.

Reads the placements written by artefact_test.py (variant a), rebuilds the pairwise
intersection polygons exactly, and puts sites on each polygon's long axis: nine
equally spaced points for a four-vertex strip, the centroid for a triangle. Each
site is rounded to denominator 10^5 and kept only if it lies (exactly) in both cores
of its pair, so every site written breaks that pair's site-disjointness. Written in
the retained-certificate shape so run_fractional_colgen --seed-certificate can union
them with the grid (weights are placeholders; a seed is a site set).
"""

from __future__ import annotations

import json
import sys
from fractions import Fraction
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from artefact_test import B, L, area, corners_of, intersection  # noqa: E402

from sqpack.fractional.colgen import d4_orbit, square_at  # noqa: E402
from sqpack.fractional.generate import direction_net, net_half_tangents  # noqa: E402

HERE = Path(__file__).parent
ROUND = 10**5


def main() -> None:
    data = json.loads((HERE / "cores-a-scaled-centres.json").read_text())
    tangents = net_half_tangents(Fraction(207107, 500000), 180)
    net = direction_net(tangents)
    sqs = []
    for p in data["placements"]:
        c = (Fraction(p["centre"][0]), Fraction(p["centre"][1]))
        sqs.append(square_at(net[p["k"]], c, L, B))
    half = L / 2
    sites: set[tuple[Fraction, Fraction]] = set()
    per_pair = []
    for i in range(11):
        for j in range(i + 1, 11):
            poly = intersection(sqs[i], sqs[j])
            if not poly or area(poly) == 0:
                continue
            cx = sum(p[0] for p in poly) / len(poly)
            cy = sum(p[1] for p in poly) / len(poly)
            # long axis: the edge direction of square i or j with the greatest extent
            best = None
            for sq in (sqs[i], sqs[j]):
                for (nx, ny) in ((sq.ax, sq.ay), (sq.bx, sq.by)):
                    vals = [nx * p[0] + ny * p[1] for p in poly]
                    ext = max(vals) - min(vals)
                    if best is None or ext > best[0]:
                        best = (ext, nx, ny, min(vals), max(vals))
            ext, nx, ny, lo, hi = best
            candidates = []
            if len(poly) >= 4 and ext > Fraction(1, 10):
                for m in range(1, 10):
                    s = lo + (hi - lo) * m / 10
                    # point on the long axis through the centroid: centroid shifted along (nx, ny)
                    proj_c = nx * cx + ny * cy
                    px = cx + (s - proj_c) * nx
                    py = cy + (s - proj_c) * ny
                    candidates.append((px, py))
            candidates.append((cx, cy))
            kept = 0
            for (px, py) in candidates:
                rx = Fraction(round((px + half) * ROUND), ROUND)
                ry = Fraction(round((py + half) * ROUND), ROUND)
                if sqs[i].covers(rx - half, ry - half) and sqs[j].covers(rx - half, ry - half):
                    sites.add((rx, ry))
                    kept += 1
            per_pair.append((i, j, len(candidates), kept))
    closed: set[tuple[Fraction, Fraction]] = set()
    for (x, y) in sites:
        closed.update(d4_orbit(x, y, L))
    print(f"strip sites: {len(sites)} distinct points, {len(closed)} after D4 closure")
    for row in per_pair:
        print("  pair %2d,%2d: %d candidates, %d kept" % row)
    record = {
        "id": "bc-297-trump-strip-sites",
        "n": 11,
        "outer_side": str(L),
        "square_side": str(B),
        "note": "sites inside the pairwise overlap strips of Trump's clamped B-cores; weights are placeholders",
        "atoms": [[str(x), str(y), "1"] for (x, y) in sorted(sites)],
    }
    (HERE / "trump-strip-sites.json").write_text(json.dumps(record, indent=1))
    (HERE / "trump-strip-sites.txt").write_text("\n".join(f"{x} {y}" for (x, y) in sorted(sites)) + "\n")


if __name__ == "__main__":
    main()
```

### `trump-strip-sites.txt`

The seventy strip points, exact, before D4 closure.

```text
9977/100000 141581/50000
9977/50000 141581/50000
29931/100000 141581/50000
9977/25000 141581/50000
9977/20000 141581/50000
29931/50000 141581/50000
69839/100000 141581/50000
9977/12500 141581/50000
89793/100000 141581/50000
6171/6250 98547/100000
98789/100000 5786/3125
49419/50000 141581/50000
49419/50000 292207/100000
49419/50000 37773/12500
49419/50000 312161/100000
49419/50000 161069/50000
49419/50000 66423/20000
49419/50000 85523/25000
49419/50000 352069/100000
49419/50000 181023/50000
49419/50000 372023/100000
25701/20000 40863/50000
67949/50000 21993/25000
68237/50000 12893/6250
142159/100000 4989/2500
14329/10000 94217/100000
36961/25000 192831/100000
75341/50000 100463/100000
153529/100000 93051/50000
79037/50000 106709/100000
79607/50000 89687/50000
164899/100000 34529/20000
165467/100000 56477/50000
21323/12500 41479/25000
172859/100000 149/125
176269/100000 39797/25000
180251/100000 25089/20000
90977/50000 152459/100000
187643/100000 131691/100000
24507/12500 30731/20000
196653/100000 141547/50000
100233/50000 56641/20000
100873/50000 66619/50000
50873/25000 159937/100000
103737/50000 63229/50000
210927/100000 166219/100000
106601/50000 59839/50000
218363/100000 172501/100000
21893/10000 56449/50000
112329/50000 53059/50000
112899/50000 178783/100000
115193/50000 49669/50000
116617/50000 37013/20000
47223/20000 92559/100000
240669/100000 47837/25000
241843/100000 85779/100000
247571/100000 78999/100000
31013/12500 19763/10000
12777/5000 25489/12500
53597/20000 103277/50000
136133/50000 201487/100000
276547/100000 9821/5000
280829/100000 23919/12500
8858/3125 49367/50000
28511/10000 37257/20000
289391/100000 181217/100000
293673/100000 3523/2000
148977/50000 171083/100000
298099/100000 283339/100000
75559/25000 33203/20000
```

### `sitefree_search.py`

The perturbation search.

```text
"""Search for a site-free Trump-shaped family of eleven admissible B-cores at 191/50.

Starts from the clamped canonical configuration of artefact_test.py (variant a) and
perturbs single centres (steps 0.001, 0.003, 0.01, 0.02) and the common net index of
the tilted block (157 .. 161), accepting any move that does not increase the number of
grid-seed sites lying in two or more closed cores, for a fixed number of trials per
seed. Floats rank the moves; the configuration reported is re-decided exactly
(rational centres, exact Square.covers). A count of zero would exhibit the artefact
family; a positive minimum found proves nothing about existence and is reported as
the search's floor.
"""

from __future__ import annotations

import json
import random
import sys
from fractions import Fraction
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).parent))
from artefact_test import B, L  # noqa: E402

from sqpack.fractional.colgen import site_counts_for_side, site_set_from_grids, square_at  # noqa: E402
from sqpack.fractional.generate import direction_net, net_half_tangents  # noqa: E402

HERE = Path(__file__).parent
DEN = 10**6


def main(trials: int = 20000, seeds: int = 4) -> None:
    data = json.loads((HERE / "cores-a-scaled-centres.json").read_text())
    tangents = net_half_tangents(Fraction(207107, 500000), 180)
    net = direction_net(tangents)
    grid = site_set_from_grids(L, site_counts_for_side(L, B), Fraction(1, 2))
    pts = grid.points()  # absolute coordinates
    Lf, Bf = float(L), float(B)
    ks = [int(p["k"]) for p in data["placements"]]
    centres0 = np.array([[float(Fraction(p["centre"][0])), float(Fraction(p["centre"][1]))] for p in data["placements"]])
    tilted = [i for i in range(11) if ks[i] != 0]

    def frame(k: int) -> tuple[float, float]:
        d = net[k]
        return float(d.ux), float(d.uy)

    def count_doubles(centres: np.ndarray, k: int) -> int:
        mult = np.zeros(len(pts), dtype=int)
        for i in range(11):
            c, s = frame(k) if ks[i] else (1.0, 0.0)
            dx = pts[:, 0] - centres[i, 0]
            dy = pts[:, 1] - centres[i, 1]
            u = c * dx + s * dy
            v = -s * dx + c * dy
            inside = (np.abs(u) <= Bf / 2 + 1e-12) & (np.abs(v) <= Bf / 2 + 1e-12)
            mult += inside
        return int((mult >= 2).sum())

    def admissible(centres: np.ndarray, k: int) -> bool:
        for i in range(11):
            c, s = frame(k) if ks[i] else (1.0, 0.0)
            h = Bf * (c + s) / 2
            if not (h - 1e-12 <= centres[i, 0] <= Lf - h + 1e-12 and h - 1e-12 <= centres[i, 1] <= Lf - h + 1e-12):
                return False
        return True

    best_overall = None
    for seed in range(seeds):
        rng = random.Random(seed)
        centres = centres0.copy()
        k = ks[tilted[0]]
        cur = count_doubles(centres, k)
        start = cur
        for t in range(trials):
            trial = centres.copy()
            kk = k
            r = rng.random()
            if r < 0.08:
                kk = min(161, max(157, k + rng.choice((-1, 1))))
            elif r < 0.2:
                # move the whole tilted block
                step = rng.choice((0.001, 0.003, 0.01))
                dx, dy = rng.choice(((step, 0), (-step, 0), (0, step), (0, -step)))
                for i in tilted:
                    trial[i] += (dx, dy)
            else:
                i = rng.randrange(11)
                step = rng.choice((0.001, 0.003, 0.01, 0.02))
                dx, dy = rng.choice(((step, 0), (-step, 0), (0, step), (0, -step), (step, step), (-step, -step), (step, -step), (-step, step)))
                trial[i] += (dx, dy)
            # clamp into the admissible domain
            for i in range(11):
                c, s = frame(kk) if ks[i] else (1.0, 0.0)
                h = Bf * (c + s) / 2
                trial[i, 0] = min(max(trial[i, 0], h), Lf - h)
                trial[i, 1] = min(max(trial[i, 1], h), Lf - h)
            val = count_doubles(trial, kk)
            if val <= cur:
                centres, k, cur = trial, kk, val
                if cur == 0:
                    break
        print(f"seed {seed}: start {start} doubles -> best {cur} (k = {k}) after {t + 1} trials")
        if best_overall is None or cur < best_overall[0]:
            best_overall = (cur, centres.copy(), k)

    cur, centres, k = best_overall
    # exact re-decision of the best configuration
    half = L / 2
    sqs = []
    exact_centres = []
    for i in range(11):
        d = net[k] if ks[i] else net[0]
        h = B * (d.ux + d.uy) / 2
        x = Fraction(round(centres[i, 0] * DEN), DEN)
        y = Fraction(round(centres[i, 1] * DEN), DEN)
        x = min(max(x, h), L - h)
        y = min(max(y, h), L - h)
        exact_centres.append((x, y))
        sqs.append(square_at(d, (x, y), L, B))
    doubles = 0
    for (x, y) in grid.positions():
        hits = sum(1 for sq in sqs if sq.covers(x - half, y - half))
        if hits >= 2:
            doubles += 1
    print(f"exact re-decision of the best configuration: {doubles} grid-seed sites in >= 2 cores (float search said {cur}); tilted net index k = {k}")
    for i, (x, y) in enumerate(exact_centres):
        print(f"  core {i:2d}: k={k if ks[i] else 0:3d} centre ({float(x):.6f},{float(y):.6f}) = ({x},{y})")
    out = {"doubles": doubles, "k": k, "centres": [[str(x), str(y)] for (x, y) in exact_centres]}
    (HERE / "sitefree-best.json").write_text(json.dumps(out, indent=1))


if __name__ == "__main__":
    main(trials=int(sys.argv[1]) if len(sys.argv) > 1 else 20000, seeds=int(sys.argv[2]) if len(sys.argv) > 2 else 4)
```

### `sitefree_search.out`

Its output.

```text
seed 0: start 45 doubles -> best 5 (k = 161) after 20000 trials
seed 1: start 45 doubles -> best 5 (k = 161) after 20000 trials
seed 2: start 45 doubles -> best 5 (k = 157) after 20000 trials
seed 3: start 45 doubles -> best 5 (k = 161) after 20000 trials
exact re-decision of the best configuration: 5 grid-seed sites in >= 2 cores (float search said 5); tilted net index k = 161
  core  0: k=  0 centre (0.498850,0.522850) = (9977/20000,10457/20000)
  core  1: k=  0 centre (3.267150,0.509850) = (65343/20000,10197/20000)
  core  2: k=  0 centre (2.483271,3.319150) = (2483271/1000000,66383/20000)
  core  3: k=  0 centre (0.499850,3.313150) = (9997/20000,66263/20000)
  core  4: k=  0 centre (1.523915,3.316150) = (304783/200000,66323/20000)
  core  5: k=  0 centre (0.508850,2.309085) = (10177/20000,461817/200000)
  core  6: k=161 centre (1.251522,1.459172) = (625761/500000,364793/250000)
  core  7: k=161 centre (1.898964,0.703456) = (474741/250000,129602461019851943167/184236749484550580000)
  core  8: k=161 centre (1.935761,2.188303) = (1935761/1000000,2188303/1000000)
  core  9: k=161 centre (2.590202,1.431365) = (1295101/500000,286273/200000)
  core 10: k=161 centre (3.116544,2.350332) = (574181922011131272433/184236749484550580000,587583/250000)
```

### `family_angles.py`

BC-200’s family by folded angle.

```text
"""Angular support of BC-200's retained dual family at 191/50 (exp-060, iteration 8).

The family is the depth-scaled, D4-symmetrised dual of the restricted covering LP on
12761 sites (rows converged at 11.055617). Reports the weight by folded angle and the
weight within 1 degree of Trump's 40.18 degrees, so the reader can see whether the
instrument's dual near the plateau is Trump-shaped.
"""

from __future__ import annotations

import json
import math
from collections import Counter
from fractions import Fraction
from pathlib import Path

FAMILY = Path(
    "scratchpad/"
    "wt-lane-297/packing/campaign/series/series-000-smoke-and-calibration/results/bc-200-family-191-50.json"
)


def main() -> None:
    d = json.loads(FAMILY.read_text())
    total = Fraction(0)
    by_bin: Counter[str] = Counter()
    by_angle: dict[float, Fraction] = {}
    distinct = set()
    for t, x, y, w, _side in d["placements"]:
        t = Fraction(t)
        w = Fraction(w)
        theta = math.degrees(2 * math.atan(float(t))) % 90
        theta = min(theta, 90 - theta)
        total += w
        key = round(theta, 2)
        by_angle[key] = by_angle.get(key, Fraction(0)) + w
        distinct.add((t, Fraction(x), Fraction(y)))
        if theta < 2.5:
            by_bin["[0, 2.5)"] += w
        elif theta < 12:
            by_bin["[2.5, 12)"] += w
        elif theta < 25:
            by_bin["[12, 25)"] += w
        elif theta < 35:
            by_bin["[25, 35)"] += w
        elif theta < 38.2:
            by_bin["[35, 38.2)"] += w
        elif theta < 42.2:
            by_bin["[38.2, 42.2) (Trump 40.18 +- 2)"] += w
        else:
            by_bin["[42.2, 45]"] += w
    print(f"placements {len(d['placements'])} (distinct {len(distinct)}), total weight {float(total):.6f} (depth-scaled)")
    for key, w in sorted(by_bin.items()):
        print(f"  {key:>32}: {float(w):8.4f} ({float(w / total) * 100:5.1f}%)")
    print("weight by angle (top 12):")
    for theta, w in sorted(by_angle.items(), key=lambda kv: -kv[1])[:12]:
        print(f"  {theta:6.2f} deg: {float(w):.4f}")
    near = sum(w for th, w in by_angle.items() if abs(th - 40.18) <= 1)
    print(f"weight within 1 degree of Trump's angle: {float(near):.4f}")


if __name__ == "__main__":
    main()
```

### `family_angles.out`

Its output.

```text
placements 760 (distinct 760), total weight 9.907906 (depth-scaled)
                          [0, 2.5):   5.0278 ( 50.7%)
                          [12, 25):   0.2927 (  3.0%)
                         [2.5, 12):   1.6753 ( 16.9%)
                          [25, 35):   2.4969 ( 25.2%)
                        [35, 38.2):   0.2053 (  2.1%)
   [38.2, 42.2) (Trump 40.18 +- 2):   0.1063 (  1.1%)
                        [42.2, 45]:   0.1036 (  1.0%)
weight by angle (top 12):
    0.26 deg: 1.9841
    0.00 deg: 1.2289
    0.79 deg: 0.6762
   29.15 deg: 0.6650
    2.37 deg: 0.5712
   28.90 deg: 0.5503
    3.69 deg: 0.5079
    3.43 deg: 0.5071
   25.67 deg: 0.3595
   26.17 deg: 0.2361
    0.53 deg: 0.2322
    4.74 deg: 0.1720
weight within 1 degree of Trump's angle: 0.0139
```

### `grid_gaps.out`

The grid seed’s coordinate gaps (inline script, quoted in Section 2).

```text
distinct coordinates 87 min gap 0.0021363636363636363 max gap 0.0705 mean gap 0.032790697674418605
pitches: 25 -> 0.1175 34 -> 0.08545454545454545 41 -> 0.0705
coordinates in [0.97,1.01]: ['97/100=0.97000', '1987/2000=0.99350']
coordinates within B-lambda of a wall (x <= 0.0124 from 0 or L): []
```

### `run0/run.log`

Run 0 (one column round, freeze): the driver’s log.

```text
round 0: rows=5732 orbits=518 sites=3849 lp_rounds=23 objective=11.118181818 depth=1.558161157 cost=-2.232644628 least_covered=1.000000000 seconds=94.5 | adding 1 orbits, deepest at (Fraction(1812103, 643300), Fraction(645303, 643300))
ceiling: proved=False total 10.915289 over 256 squares, max pointwise depth 1.985950 at 301180 vertices (26308 decided exactly), feasible total 5.496255
rationalised total 2223761/200000 = 11.118805000 against LP optimum 11.118181818 over 213 atoms
```

### `fill_least.py`

The exact sweep that fills least_cell_mass on the candidate.

```text
"""Sweep a frozen colgen candidate exactly and write a copy carrying its least cell mass.

The census tool loads certificates through the retention gate's loader, which requires
`least_cell_mass` as an exact rational; run_fractional_colgen leaves it null unless
--verify-serial was passed. This runs the exact event-cell sweep (one worker) on the
candidate's atoms and net, prints the verdict, and writes <name>-swept.json with the
sweep's minimum filled in. Nothing here decides a bound; the mass is above eleven.
"""

from __future__ import annotations

import json
import sys
from fractions import Fraction
from pathlib import Path

from sqpack.fractional.certificate import Certificate, verify
from sqpack.fractional.generate import net_half_tangents
from sqpack.fractional.model import Atom


def main(path: Path) -> None:
    record = json.loads(path.read_text())
    atoms = tuple(
        Atom(f"a{i}", Fraction(x), Fraction(y), Fraction(w)) for i, (x, y, w) in enumerate(record["atoms"])
    )
    cert = Certificate(
        n=int(record["n"]),
        outer_side=Fraction(record["outer_side"]),
        square_side=Fraction(record["square_side"]),
        atoms=atoms,
        half_tangents=net_half_tangents(Fraction(record["angle_limit"]), int(record["direction_steps"])),
    )
    verdict = verify(cert, workers=1)
    print(f"total mass {cert.total_mass} = {float(cert.total_mass):.9f}; least cell mass {verdict.minimum_cell_mass} = {float(verdict.minimum_cell_mass):.9f} at direction {verdict.worst_direction}")
    print(f"accepted {verdict.accepted}; failures {verdict.failures}")
    record["least_cell_mass"] = str(verdict.minimum_cell_mass)
    out = path.with_name(path.stem + "-swept.json")
    out.write_text(json.dumps(record, indent=1) + "\n")
    print(f"wrote {out}")


if __name__ == "__main__":
    main(Path(sys.argv[1]))
```

### `run0/fill_least.out`

Its output.

```text
total mass 2223761/200000 = 11.118805000; least cell mass 200009/200000 = 1.000045000 at direction 0
accepted False; failures ('Condition 2 total mass below n',)
wrote scratchpad/lane-297/run0/candidate-swept.json
```

### `census/stdout.txt`

The census, per direction and totals.

```text
direction   0 t=0 reachable      8281 min 200009/200000 [margin:cells/components] 0:0/0 1/1000:80/16 1/100:80/16 1/20:136/24 1/10:360/36 13/110:440/32
direction   1 t=207107/90000000 reachable    106345 min 200009/200000 [margin:cells/components] 0:0/0 1/1000:720/16 1/100:880/16 1/20:1260/24 1/10:3272/36 13/110:4344/36
direction   2 t=207107/45000000 reachable    108381 min 200009/200000 [margin:cells/components] 0:0/0 1/1000:1132/16 1/100:1332/16 1/20:1752/24 1/10:3940/36 13/110:5144/36
direction   3 t=207107/30000000 reachable    110309 min 200009/200000 [margin:cells/components] 0:0/0 1/1000:1544/16 1/100:1756/16 1/20:2248/24 1/10:4748/32 13/110:6132/36
direction   4 t=207107/22500000 reachable    110945 min 200009/200000 [margin:cells/components] 0:0/0 1/1000:1804/16 1/100:2024/16 1/20:2532/24 1/10:5184/32 13/110:6752/36
direction   5 t=207107/18000000 reachable    111349 min 200009/200000 [margin:cells/components] 0:0/0 1/1000:2072/16 1/100:2308/16 1/20:2860/24 1/10:5648/32 13/110:7288/36
direction   6 t=207107/15000000 reachable    111773 min 200009/200000 [margin:cells/components] 0:0/0 1/1000:2516/16 1/100:2764/16 1/20:3336/24 1/10:5940/32 13/110:7756/36
direction   7 t=1449749/90000000 reachable    112189 min 200009/200000 [margin:cells/components] 0:0/0 1/1000:2752/16 1/100:3012/16 1/20:3632/24 1/10:6572/32 13/110:8200/36
direction   8 t=207107/11250000 reachable    112473 min 200009/200000 [margin:cells/components] 0:0/0 1/1000:2908/16 1/100:3176/16 1/20:3804/24 1/10:6684/32 13/110:8392/32
direction   9 t=207107/10000000 reachable    112769 min 200009/200000 [margin:cells/components] 0:0/0 1/1000:3296/16 1/100:3584/16 1/20:4040/20 1/10:7124/32 13/110:9036/36
direction  10 t=207107/9000000 reachable    113321 min 200009/200000 [margin:cells/components] 0:0/0 1/1000:3544/16 1/100:3848/16 1/20:4324/20 1/10:7612/32 13/110:9512/36
direction  11 t=2278177/90000000 reachable    113805 min 200009/200000 [margin:cells/components] 0:0/0 1/1000:3708/16 1/100:4012/16 1/20:4484/20 1/10:7860/28 13/110:9724/36
direction  12 t=207107/7500000 reachable    114385 min 200009/200000 [margin:cells/components] 0:0/0 1/1000:3980/16 1/100:4288/16 1/20:4760/20 1/10:8604/28 13/110:10516/36
direction  13 t=2692391/90000000 reachable    115025 min 200009/200000 [margin:cells/components] 0:0/0 1/1000:4104/16 1/100:4412/16 1/20:4892/20 1/10:8792/28 13/110:10740/36
direction  14 t=1449749/45000000 reachable    115761 min 200009/200000 [margin:cells/components] 0:0/0 1/1000:4300/16 1/100:4612/16 1/20:5256/20 1/10:9368/28 13/110:11532/40
direction  15 t=207107/6000000 reachable    116373 min 200009/200000 [margin:cells/components] 0:0/0 1/1000:4460/16 1/100:4776/16 1/20:5456/20 1/10:9960/24 13/110:11816/40
direction  16 t=207107/5625000 reachable    116817 min 200009/200000 [margin:cells/components] 0:0/0 1/1000:4692/16 1/100:5024/16 1/20:5768/20 1/10:10360/24 13/110:12128/40
direction  17 t=3520819/90000000 reachable    117213 min 200009/200000 [margin:cells/components] 0:0/0 1/1000:5112/16 1/100:5464/16 1/20:6252/20 1/10:10700/24 13/110:12544/40
direction  18 t=207107/5000000 reachable    117601 min 200009/200000 [margin:cells/components] 0:0/0 1/1000:5264/16 1/100:5656/16 1/20:6284/20 1/10:10852/24 13/110:12788/36
direction  19 t=3935033/90000000 reachable    117933 min 200009/200000 [margin:cells/components] 0:0/0 1/1000:5656/16 1/100:6028/16 1/20:7168/20 1/10:11528/24 13/110:13660/36
direction  20 t=207107/4500000 reachable    118277 min 200009/200000 [margin:cells/components] 0:0/0 1/1000:5808/16 1/100:6180/16 1/20:7376/20 1/10:11648/24 13/110:13808/36
direction  21 t=1449749/30000000 reachable    118693 min 200009/200000 [margin:cells/components] 0:0/0 1/1000:5864/16 1/100:6284/16 1/20:7956/20 1/10:11692/28 13/110:13872/40
direction  22 t=2278177/45000000 reachable    118941 min 200009/200000 [margin:cells/components] 0:0/0 1/1000:5864/16 1/100:6296/16 1/20:8120/20 1/10:12084/32 13/110:14152/44
direction  23 t=4763461/90000000 reachable    119113 min 200009/200000 [margin:cells/components] 0:0/0 1/1000:5840/16 1/100:6232/16 1/20:8096/24 1/10:12500/36 13/110:14460/48
direction  24 t=207107/3750000 reachable    119473 min 200009/200000 [margin:cells/components] 0:0/0 1/1000:5988/20 1/100:6384/20 1/20:8496/28 1/10:12692/44 13/110:14640/44
direction  25 t=207107/3600000 reachable    119765 min 200009/200000 [margin:cells/components] 0:0/0 1/1000:6164/20 1/100:6556/20 1/20:8656/28 1/10:12996/44 13/110:15124/44
direction  26 t=2692391/45000000 reachable    120073 min 200009/200000 [margin:cells/components] 0:0/0 1/1000:6240/20 1/100:6688/20 1/20:8764/28 1/10:13112/44 13/110:15420/48
direction  27 t=621321/10000000 reachable    120405 min 200009/200000 [margin:cells/components] 0:0/0 1/1000:6296/20 1/100:6740/20 1/20:8660/32 1/10:12932/48 13/110:15308/52
direction  28 t=1449749/22500000 reachable    120741 min 200009/200000 [margin:cells/components] 0:0/0 1/1000:6424/20 1/100:6828/20 1/20:8980/32 1/10:13344/48 13/110:15800/52
direction  29 t=6006103/90000000 reachable    121093 min 200009/200000 [margin:cells/components] 0:0/0 1/1000:6272/24 1/100:6708/24 1/20:8824/36 1/10:13516/52 13/110:16000/52
direction  30 t=207107/3000000 reachable    121449 min 200009/200000 [margin:cells/components] 0:0/0 1/1000:6088/24 1/100:6488/28 1/20:8688/40 1/10:13672/48 13/110:16024/48
direction  31 t=6420317/90000000 reachable    121849 min 200009/200000 [margin:cells/components] 0:0/0 1/1000:6112/24 1/100:6512/28 1/20:8580/44 1/10:13860/48 13/110:16052/48
direction  32 t=207107/2812500 reachable    122117 min 200009/200000 [margin:cells/components] 0:0/0 1/1000:6180/24 1/100:6584/28 1/20:8476/44 1/10:14068/48 13/110:16300/52
direction  33 t=2278177/30000000 reachable    122429 min 200009/200000 [margin:cells/components] 0:0/0 1/1000:6268/24 1/100:6696/28 1/20:8544/44 1/10:14240/48 13/110:16688/56
direction  34 t=3520819/45000000 reachable    122713 min 200009/200000 [margin:cells/components] 0:0/0 1/1000:5648/24 1/100:6376/28 1/20:8528/40 1/10:14076/52 13/110:16276/64
direction  35 t=1449749/18000000 reachable    122877 min 200009/200000 [margin:cells/components] 0:0/0 1/1000:5536/24 1/100:6252/28 1/20:8460/40 1/10:14076/52 13/110:16272/64
direction  36 t=207107/2500000 reachable    123021 min 200009/200000 [margin:cells/components] 0:0/0 1/1000:5268/24 1/100:5684/28 1/20:8640/40 1/10:13900/48 13/110:16196/56
direction  37 t=7662959/90000000 reachable    123217 min 200009/200000 [margin:cells/components] 0:0/0 1/1000:5488/28 1/100:5872/28 1/20:8884/40 1/10:14336/52 13/110:16556/60
direction  38 t=3935033/45000000 reachable    123401 min 200009/200000 [margin:cells/components] 0:0/0 1/1000:5068/28 1/100:5752/28 1/20:8676/40 1/10:14244/52 13/110:16512/60
direction  39 t=2692391/30000000 reachable    123601 min 200009/200000 [margin:cells/components] 0:0/0 1/1000:4500/28 1/100:5428/28 1/20:8124/40 1/10:13436/56 13/110:15920/64
direction  40 t=207107/2250000 reachable    123725 min 200009/200000 [margin:cells/components] 0:0/0 1/1000:4284/28 1/100:5504/28 1/20:8256/40 1/10:13980/56 13/110:16180/68
direction  41 t=8491387/90000000 reachable    123873 min 200009/200000 [margin:cells/components] 0:0/0 1/1000:4264/28 1/100:5100/28 1/20:7920/40 1/10:13364/60 13/110:15616/68
direction  42 t=1449749/15000000 reachable    124005 min 200009/200000 [margin:cells/components] 0:0/0 1/1000:4240/28 1/100:4820/28 1/20:7812/40 1/10:12988/60 13/110:15800/68
direction  43 t=8905601/90000000 reachable    124173 min 200009/200000 [margin:cells/components] 0:0/0 1/1000:3980/28 1/100:4820/28 1/20:7792/40 1/10:12784/64 13/110:15868/64
direction  44 t=2278177/22500000 reachable    124301 min 200009/200000 [margin:cells/components] 0:0/0 1/1000:3996/28 1/100:4548/36 1/20:8004/52 1/10:12732/76 13/110:16584/76
direction  45 t=207107/2000000 reachable    124425 min 200009/200000 [margin:cells/components] 0:0/0 1/1000:3780/28 1/100:4336/36 1/20:7656/56 1/10:12276/72 13/110:15996/88
direction  46 t=4763461/45000000 reachable    124517 min 200009/200000 [margin:cells/components] 0:0/0 1/1000:3692/28 1/100:4232/36 1/20:7232/56 1/10:12468/72 13/110:15832/92
direction  47 t=9734029/90000000 reachable    124509 min 200009/200000 [margin:cells/components] 0:0/0 1/1000:3552/28 1/100:3884/36 1/20:6828/56 1/10:12120/68 13/110:15472/88
direction  48 t=207107/1875000 reachable    124585 min 200009/200000 [margin:cells/components] 0:0/0 1/1000:3592/28 1/100:3968/40 1/20:6824/60 1/10:11952/64 13/110:15140/80
direction  49 t=10148243/90000000 reachable    124629 min 200009/200000 [margin:cells/components] 0:0/0 1/1000:3504/36 1/100:3884/40 1/20:6676/56 1/10:11960/64 13/110:14708/80
direction  50 t=207107/1800000 reachable    124661 min 200009/200000 [margin:cells/components] 0:0/0 1/1000:3444/36 1/100:4012/40 1/20:6812/52 1/10:12020/64 13/110:15108/80
direction  51 t=3520819/30000000 reachable    124745 min 200009/200000 [margin:cells/components] 0:0/0 1/1000:3564/32 1/100:4292/40 1/20:6960/56 1/10:12160/64 13/110:15444/80
direction  52 t=2692391/22500000 reachable    124777 min 200009/200000 [margin:cells/components] 0:0/0 1/1000:3556/32 1/100:4480/40 1/20:6868/56 1/10:11892/68 13/110:15100/80
direction  53 t=10976671/90000000 reachable    124837 min 200009/200000 [margin:cells/components] 0:0/0 1/1000:3532/32 1/100:4556/40 1/20:6784/52 1/10:11212/72 13/110:14328/92
direction  54 t=621321/5000000 reachable    124985 min 200009/200000 [margin:cells/components] 0:0/0 1/1000:3480/36 1/100:4324/44 1/20:6884/48 1/10:10584/80 13/110:13872/92
direction  55 t=2278177/18000000 reachable    125093 min 200009/200000 [margin:cells/components] 0:0/0 1/1000:3616/36 1/100:4260/44 1/20:7008/48 1/10:11156/80 13/110:14448/96
direction  56 t=1449749/11250000 reachable    125237 min 200009/200000 [margin:cells/components] 0:0/0 1/1000:3676/36 1/100:4408/44 1/20:6952/48 1/10:11168/92 13/110:14384/116
direction  57 t=3935033/30000000 reachable    125417 min 200009/200000 [margin:cells/components] 0:0/0 1/1000:3764/36 1/100:4308/44 1/20:6784/48 1/10:11188/88 13/110:14432/96
direction  58 t=6006103/45000000 reachable    125521 min 200009/200000 [margin:cells/components] 0:0/0 1/1000:3624/32 1/100:4120/44 1/20:6428/52 1/10:10444/76 13/110:14052/92
direction  59 t=12219313/90000000 reachable    125661 min 200009/200000 [margin:cells/components] 0:0/0 1/1000:3940/32 1/100:4488/44 1/20:6824/48 1/10:10808/76 13/110:14460/96
direction  60 t=207107/1500000 reachable    125721 min 200009/200000 [margin:cells/components] 0:0/0 1/1000:3812/32 1/100:4264/44 1/20:6284/48 1/10:10836/76 13/110:14304/92
direction  61 t=12633527/90000000 reachable    125841 min 200009/200000 [margin:cells/components] 0:0/0 1/1000:3948/28 1/100:4412/40 1/20:6560/40 1/10:10988/92 13/110:14332/100
direction  62 t=6420317/45000000 reachable    125925 min 200009/200000 [margin:cells/components] 0:0/0 1/1000:4180/32 1/100:4604/40 1/20:6728/48 1/10:11320/88 13/110:14460/80
direction  63 t=1449749/10000000 reachable    125953 min 200009/200000 [margin:cells/components] 0:0/0 1/1000:4260/32 1/100:4668/40 1/20:6772/52 1/10:11504/88 13/110:14620/80
direction  64 t=207107/1406250 reachable    126033 min 200009/200000 [margin:cells/components] 0:0/0 1/1000:4372/32 1/100:4616/40 1/20:6800/52 1/10:11300/96 13/110:15052/80
direction  65 t=2692391/18000000 reachable    126089 min 200009/200000 [margin:cells/components] 0:0/0 1/1000:4156/32 1/100:4512/40 1/20:6748/52 1/10:11152/96 13/110:14976/84
direction  66 t=2278177/15000000 reachable    126137 min 200009/200000 [margin:cells/components] 0:0/0 1/1000:4328/40 1/100:4688/48 1/20:7084/64 1/10:11208/96 13/110:14992/72
direction  67 t=13876169/90000000 reachable    126145 min 200009/200000 [margin:cells/components] 0:0/0 1/1000:4132/40 1/100:4492/48 1/20:6448/64 1/10:10584/96 13/110:14020/72
direction  68 t=3520819/22500000 reachable    126157 min 200009/200000 [margin:cells/components] 0:0/0 1/1000:4136/36 1/100:4736/48 1/20:6616/64 1/10:10240/96 13/110:13440/72
direction  69 t=4763461/30000000 reachable    126193 min 200009/200000 [margin:cells/components] 0:0/0 1/1000:3948/36 1/100:4596/48 1/20:6556/64 1/10:10732/96 13/110:14488/72
direction  70 t=1449749/9000000 reachable    126181 min 200009/200000 [margin:cells/components] 0:0/0 1/1000:4028/36 1/100:4604/48 1/20:6524/64 1/10:10416/92 13/110:14216/72
direction  71 t=14704597/90000000 reachable    126193 min 200009/200000 [margin:cells/components] 0:0/0 1/1000:3764/36 1/100:4340/48 1/20:6120/64 1/10:10420/96 13/110:14220/80
direction  72 t=207107/1250000 reachable    126177 min 200009/200000 [margin:cells/components] 0:0/0 1/1000:3488/36 1/100:4088/48 1/20:5788/64 1/10:9676/96 13/110:13280/80
direction  73 t=15118811/90000000 reachable    126129 min 200009/200000 [margin:cells/components] 0:0/0 1/1000:3456/28 1/100:4104/40 1/20:5804/64 1/10:9716/108 13/110:13244/104
direction  74 t=7662959/45000000 reachable    126065 min 200009/200000 [margin:cells/components] 0:0/0 1/1000:3428/28 1/100:4188/40 1/20:5980/64 1/10:9748/108 13/110:12832/104
direction  75 t=207107/1200000 reachable    126013 min 200009/200000 [margin:cells/components] 0:0/0 1/1000:3344/28 1/100:3964/40 1/20:5584/60 1/10:9076/104 13/110:12192/104
direction  76 t=3935033/22500000 reachable    125953 min 200009/200000 [margin:cells/components] 0:0/0 1/1000:3200/28 1/100:3872/40 1/20:5252/60 1/10:8688/108 13/110:11640/104
direction  77 t=15947239/90000000 reachable    125913 min 200009/200000 [margin:cells/components] 0:0/0 1/1000:3176/32 1/100:3792/44 1/20:5332/64 1/10:8692/124 13/110:11652/112
direction  78 t=2692391/15000000 reachable    125837 min 200009/200000 [margin:cells/components] 0:0/0 1/1000:2976/36 1/100:3572/48 1/20:4832/68 1/10:8248/120 13/110:11060/108
direction  79 t=16361453/90000000 reachable    125741 min 200009/200000 [margin:cells/components] 0:0/0 1/1000:2812/36 1/100:3412/52 1/20:4552/68 1/10:7956/116 13/110:10752/100
direction  80 t=207107/1125000 reachable    125689 min 200009/200000 [margin:cells/components] 0:0/0 1/1000:2900/36 1/100:3532/48 1/20:4692/56 1/10:8296/116 13/110:10940/100
direction  81 t=1863963/10000000 reachable    125593 min 200009/200000 [margin:cells/components] 0:0/0 1/1000:2748/40 1/100:3376/48 1/20:4516/56 1/10:8092/112 13/110:10876/96
direction  82 t=8491387/45000000 reachable    125473 min 200009/200000 [margin:cells/components] 0:0/0 1/1000:2628/40 1/100:3224/48 1/20:4340/56 1/10:8032/128 13/110:10804/100
direction  83 t=17189881/90000000 reachable    125453 min 200009/200000 [margin:cells/components] 0:0/0 1/1000:2580/40 1/100:3128/48 1/20:4268/56 1/10:8096/116 13/110:10600/100
direction  84 t=1449749/7500000 reachable    125377 min 200009/200000 [margin:cells/components] 0:0/0 1/1000:2500/44 1/100:3004/48 1/20:4152/56 1/10:8260/112 13/110:10500/96
direction  85 t=3520819/18000000 reachable    125305 min 200009/200000 [margin:cells/components] 0:0/0 1/1000:2296/48 1/100:2748/48 1/20:3812/56 1/10:7708/104 13/110:9804/96
direction  86 t=8905601/45000000 reachable    125209 min 200009/200000 [margin:cells/components] 0:0/0 1/1000:2180/48 1/100:2692/48 1/20:3828/56 1/10:7604/104 13/110:9600/100
direction  87 t=6006103/30000000 reachable    125121 min 200009/200000 [margin:cells/components] 0:0/0 1/1000:2056/44 1/100:2616/48 1/20:4044/72 1/10:7844/120 13/110:10152/124
direction  88 t=2278177/11250000 reachable    125057 min 200009/200000 [margin:cells/components] 0:0/0 1/1000:2076/44 1/100:2632/48 1/20:3940/72 1/10:7580/116 13/110:9836/120
direction  89 t=18432523/90000000 reachable    125021 min 200009/200000 [margin:cells/components] 0:0/0 1/1000:1940/44 1/100:2632/56 1/20:4160/76 1/10:7960/112 13/110:10272/120
direction  90 t=207107/1000000 reachable    124897 min 200009/200000 [margin:cells/components] 0:0/0 1/1000:2060/44 1/100:2600/56 1/20:3928/76 1/10:7768/112 13/110:9968/120
direction  91 t=18846737/90000000 reachable    124801 min 200009/200000 [margin:cells/components] 0:0/0 1/1000:1860/40 1/100:2556/56 1/20:4036/76 1/10:7660/112 13/110:9848/120
direction  92 t=4763461/22500000 reachable    124709 min 200009/200000 [margin:cells/components] 0:0/0 1/1000:1888/40 1/100:2496/52 1/20:3792/76 1/10:7304/116 13/110:9544/116
direction  93 t=6420317/30000000 reachable    124633 min 200009/200000 [margin:cells/components] 0:0/0 1/1000:1896/40 1/100:2500/52 1/20:3812/76 1/10:7364/116 13/110:9688/112
direction  94 t=9734029/45000000 reachable    124577 min 200009/200000 [margin:cells/components] 0:0/0 1/1000:1812/36 1/100:2364/52 1/20:3580/76 1/10:7156/120 13/110:9420/112
direction  95 t=3935033/18000000 reachable    124493 min 200009/200000 [margin:cells/components] 0:0/0 1/1000:1640/36 1/100:2336/52 1/20:3460/76 1/10:6860/120 13/110:9256/116
direction  96 t=207107/937500 reachable    124365 min 200009/200000 [margin:cells/components] 0:0/0 1/1000:1748/36 1/100:2276/56 1/20:3384/80 1/10:6488/120 13/110:9064/116
direction  97 t=20089379/90000000 reachable    124217 min 200009/200000 [margin:cells/components] 0:0/0 1/1000:1688/40 1/100:2172/56 1/20:3140/76 1/10:6400/116 13/110:8736/108
direction  98 t=10148243/45000000 reachable    124189 min 200009/200000 [margin:cells/components] 0:0/0 1/1000:1660/40 1/100:2152/56 1/20:3064/76 1/10:6232/112 13/110:8632/108
direction  99 t=2278177/10000000 reachable    124185 min 200009/200000 [margin:cells/components] 0:0/0 1/1000:1584/40 1/100:2020/60 1/20:2984/76 1/10:6300/108 13/110:8620/104
direction 100 t=207107/900000 reachable    124153 min 200009/200000 [margin:cells/components] 0:0/0 1/1000:1596/44 1/100:2012/60 1/20:2984/76 1/10:6160/104 13/110:8592/104
direction 101 t=20917807/90000000 reachable    124089 min 200009/200000 [margin:cells/components] 0:0/0 1/1000:1408/36 1/100:2124/60 1/20:3012/72 1/10:6156/96 13/110:8464/96
direction 102 t=3520819/15000000 reachable    123933 min 200009/200000 [margin:cells/components] 0:0/0 1/1000:1432/36 1/100:2156/60 1/20:3020/72 1/10:6180/100 13/110:8456/100
direction 103 t=21332021/90000000 reachable    123877 min 200009/200000 [margin:cells/components] 0:0/0 1/1000:1372/36 1/100:1776/56 1/20:2516/72 1/10:5368/104 13/110:7864/100
direction 104 t=2692391/11250000 reachable    123813 min 200009/200000 [margin:cells/components] 0:0/0 1/1000:1268/32 1/100:1700/52 1/20:2416/64 1/10:5188/100 13/110:7532/100
direction 105 t=1449749/6000000 reachable    123761 min 200009/200000 [margin:cells/components] 0:0/0 1/1000:1240/32 1/100:1696/52 1/20:2508/64 1/10:5452/100 13/110:7688/100
direction 106 t=10976671/45000000 reachable    123665 min 200009/200000 [margin:cells/components] 0:0/0 1/1000:1288/32 1/100:1712/52 1/20:2536/64 1/10:5508/104 13/110:7876/104
direction 107 t=22160449/90000000 reachable    123641 min 200009/200000 [margin:cells/components] 0:0/0 1/1000:1312/32 1/100:1732/52 1/20:2452/68 1/10:5228/104 13/110:7600/100
direction 108 t=621321/2500000 reachable    123593 min 200009/200000 [margin:cells/components] 0:0/0 1/1000:1392/32 1/100:1788/52 1/20:2428/68 1/10:5296/100 13/110:7720/100
direction 109 t=22574663/90000000 reachable    123457 min 200009/200000 [margin:cells/components] 0:0/0 1/1000:1364/32 1/100:1764/52 1/20:2400/68 1/10:5328/104 13/110:7868/96
direction 110 t=2278177/9000000 reachable    123397 min 200009/200000 [margin:cells/components] 0:0/0 1/1000:1412/32 1/100:1864/52 1/20:2512/68 1/10:5384/104 13/110:7676/100
direction 111 t=7662959/30000000 reachable    123413 min 200009/200000 [margin:cells/components] 0:0/0 1/1000:1432/32 1/100:1936/52 1/20:2548/72 1/10:5448/100 13/110:7976/108
direction 112 t=1449749/5625000 reachable    123389 min 200009/200000 [margin:cells/components] 0:0/0 1/1000:1352/32 1/100:1836/52 1/20:2408/72 1/10:5308/100 13/110:7812/108
direction 113 t=23403091/90000000 reachable    123277 min 200009/200000 [margin:cells/components] 0:0/0 1/1000:1352/36 1/100:1816/48 1/20:2348/80 1/10:5312/100 13/110:7788/104
direction 114 t=3935033/15000000 reachable    123165 min 200009/200000 [margin:cells/components] 0:0/0 1/1000:1308/32 1/100:1856/48 1/20:2348/76 1/10:5168/96 13/110:7768/108
direction 115 t=4763461/18000000 reachable    123053 min 200009/200000 [margin:cells/components] 0:0/0 1/1000:1188/32 1/100:1804/48 1/20:2288/68 1/10:5280/100 13/110:7840/104
direction 116 t=6006103/22500000 reachable    122945 min 200009/200000 [margin:cells/components] 0:0/0 1/1000:1220/32 1/100:1996/48 1/20:2508/68 1/10:5204/100 13/110:7508/104
direction 117 t=2692391/10000000 reachable    122825 min 200009/200000 [margin:cells/components] 0:0/0 1/1000:1208/32 1/100:1988/48 1/20:2472/68 1/10:5360/100 13/110:7648/104
direction 118 t=12219313/45000000 reachable    122717 min 200009/200000 [margin:cells/components] 0:0/0 1/1000:1344/32 1/100:1996/48 1/20:2584/68 1/10:5988/100 13/110:8380/104
direction 119 t=24645733/90000000 reachable    122621 min 200009/200000 [margin:cells/components] 0:0/0 1/1000:1308/32 1/100:1964/48 1/20:2540/68 1/10:5884/100 13/110:8376/108
direction 120 t=207107/750000 reachable    122549 min 200009/200000 [margin:cells/components] 0:0/0 1/1000:1164/32 1/100:1764/48 1/20:2336/68 1/10:5828/100 13/110:8484/108
direction 121 t=25059947/90000000 reachable    122481 min 200009/200000 [margin:cells/components] 0:0/0 1/1000:1172/32 1/100:1804/48 1/20:2428/68 1/10:5928/100 13/110:8364/108
direction 122 t=12633527/45000000 reachable    122401 min 200009/200000 [margin:cells/components] 0:0/0 1/1000:1096/28 1/100:1700/48 1/20:2268/64 1/10:5864/104 13/110:8236/112
direction 123 t=8491387/30000000 reachable    122393 min 200009/200000 [margin:cells/components] 0:0/0 1/1000:1220/28 1/100:1840/48 1/20:2376/64 1/10:5756/104 13/110:8208/112
direction 124 t=6420317/22500000 reachable    122353 min 200009/200000 [margin:cells/components] 0:0/0 1/1000:1272/32 1/100:1920/48 1/20:2584/68 1/10:6200/112 13/110:8836/128
direction 125 t=207107/720000 reachable    122337 min 200009/200000 [margin:cells/components] 0:0/0 1/1000:1196/32 1/100:1856/44 1/20:2544/64 1/10:6248/104 13/110:9028/120
direction 126 t=1449749/5000000 reachable    122293 min 200009/200000 [margin:cells/components] 0:0/0 1/1000:1164/36 1/100:1824/48 1/20:2464/68 1/10:5940/100 13/110:8584/120
direction 127 t=26302589/90000000 reachable    122225 min 200009/200000 [margin:cells/components] 0:0/0 1/1000:1072/36 1/100:1688/48 1/20:2316/68 1/10:5768/100 13/110:8472/120
direction 128 t=207107/703125 reachable    122157 min 200009/200000 [margin:cells/components] 0:0/0 1/1000:1044/36 1/100:1636/48 1/20:2448/68 1/10:5816/100 13/110:8560/120
direction 129 t=8905601/30000000 reachable    122141 min 200009/200000 [margin:cells/components] 0:0/0 1/1000:1044/36 1/100:1600/48 1/20:2464/68 1/10:5932/100 13/110:8756/120
direction 130 t=2692391/9000000 reachable    122145 min 200009/200000 [margin:cells/components] 0:0/0 1/1000:1140/44 1/100:1860/60 1/20:2728/84 1/10:5996/96 13/110:8968/108
direction 131 t=27131017/90000000 reachable    122085 min 200009/200000 [margin:cells/components] 0:0/0 1/1000:1120/40 1/100:1816/56 1/20:2648/76 1/10:5856/96 13/110:8796/116
direction 132 t=2278177/7500000 reachable    122025 min 200009/200000 [margin:cells/components] 0:0/0 1/1000:1036/40 1/100:1644/56 1/20:2376/84 1/10:5852/108 13/110:8988/112
direction 133 t=27545231/90000000 reachable    122057 min 200009/200000 [margin:cells/components] 0:0/0 1/1000:940/40 1/100:1544/56 1/20:2252/84 1/10:5908/120 13/110:8952/136
direction 134 t=13876169/45000000 reachable    122021 min 200009/200000 [margin:cells/components] 0:0/0 1/1000:808/40 1/100:1540/52 1/20:2312/84 1/10:5900/120 13/110:8752/140
direction 135 t=621321/2000000 reachable    122033 min 200009/200000 [margin:cells/components] 0:0/0 1/1000:916/40 1/100:1760/52 1/20:2452/84 1/10:6156/120 13/110:8936/140
direction 136 t=3520819/11250000 reachable    122053 min 200009/200000 [margin:cells/components] 0:0/0 1/1000:956/40 1/100:1836/52 1/20:2780/84 1/10:6352/132 13/110:9292/140
direction 137 t=28373659/90000000 reachable    122025 min 200009/200000 [margin:cells/components] 0:0/0 1/1000:960/40 1/100:1944/52 1/20:2808/84 1/10:6188/132 13/110:9132/140
direction 138 t=4763461/15000000 reachable    122017 min 200009/200000 [margin:cells/components] 0:0/0 1/1000:964/40 1/100:1944/52 1/20:3068/84 1/10:6432/140 13/110:9352/140
direction 139 t=28787873/90000000 reachable    122001 min 200009/200000 [margin:cells/components] 0:0/0 1/1000:944/40 1/100:1928/52 1/20:3044/92 1/10:6392/140 13/110:9392/148
direction 140 t=1449749/4500000 reachable    121965 min 200009/200000 [margin:cells/components] 0:0/0 1/1000:880/40 1/100:1868/48 1/20:2708/100 1/10:5920/140 13/110:8984/144
direction 141 t=9734029/30000000 reachable    121953 min 200009/200000 [margin:cells/components] 0:0/0 1/1000:880/40 1/100:1860/48 1/20:2812/100 1/10:6396/148 13/110:9620/148
direction 142 t=14704597/45000000 reachable    121937 min 200009/200000 [margin:cells/components] 0:0/0 1/1000:864/40 1/100:1892/48 1/20:2928/100 1/10:6876/152 13/110:10260/152
direction 143 t=29616301/90000000 reachable    121925 min 200009/200000 [margin:cells/components] 0:0/0 1/1000:832/40 1/100:1876/48 1/20:2920/104 1/10:6532/156 13/110:9824/156
direction 144 t=207107/625000 reachable    121897 min 200009/200000 [margin:cells/components] 0:0/0 1/1000:844/36 1/100:1812/40 1/20:2996/108 1/10:6264/168 13/110:9972/168
direction 145 t=6006103/18000000 reachable    121813 min 200009/200000 [margin:cells/components] 0:0/0 1/1000:808/40 1/100:1480/44 1/20:3020/112 1/10:6620/164 13/110:10240/164
direction 146 t=15118811/45000000 reachable    121761 min 200009/200000 [margin:cells/components] 0:0/0 1/1000:784/40 1/100:1448/44 1/20:2908/112 1/10:6036/160 13/110:9420/160
direction 147 t=10148243/30000000 reachable    121749 min 200009/200000 [margin:cells/components] 0:0/0 1/1000:768/40 1/100:1412/44 1/20:2824/112 1/10:5844/160 13/110:9408/160
direction 148 t=7662959/22500000 reachable    121717 min 200009/200000 [margin:cells/components] 0:0/0 1/1000:552/28 1/100:1252/36 1/20:2300/92 1/10:5412/160 13/110:8724/160
direction 149 t=30858943/90000000 reachable    121693 min 200009/200000 [margin:cells/components] 0:0/0 1/1000:520/28 1/100:1284/36 1/20:2424/92 1/10:5528/156 13/110:8952/156
direction 150 t=207107/600000 reachable    121661 min 200009/200000 [margin:cells/components] 0:0/0 1/1000:512/32 1/100:1244/40 1/20:2244/92 1/10:5488/148 13/110:8904/156
direction 151 t=31273157/90000000 reachable    121645 min 200009/200000 [margin:cells/components] 0:0/0 1/1000:524/48 1/100:1240/52 1/20:2284/100 1/10:5596/172 13/110:8692/160
direction 152 t=3935033/11250000 reachable    121549 min 200009/200000 [margin:cells/components] 0:0/0 1/1000:484/52 1/100:1144/52 1/20:2136/100 1/10:5508/172 13/110:8604/156
direction 153 t=3520819/10000000 reachable    121469 min 200009/200000 [margin:cells/components] 0:0/0 1/1000:476/52 1/100:1168/52 1/20:2132/108 1/10:5324/168 13/110:7968/156
direction 154 t=15947239/45000000 reachable    121441 min 200009/200000 [margin:cells/components] 0:0/0 1/1000:448/52 1/100:1124/52 1/20:2176/112 1/10:5572/184 13/110:8488/152
direction 155 t=6420317/18000000 reachable    121369 min 200009/200000 [margin:cells/components] 0:0/0 1/1000:432/48 1/100:1156/48 1/20:2116/104 1/10:5280/192 13/110:8012/168
direction 156 t=2692391/7500000 reachable    121361 min 200009/200000 [margin:cells/components] 0:0/0 1/1000:460/64 1/100:1188/60 1/20:2316/112 1/10:5900/172 13/110:8552/148
direction 157 t=32515799/90000000 reachable    121365 min 200009/200000 [margin:cells/components] 0:0/0 1/1000:524/64 1/100:1296/60 1/20:2428/112 1/10:5916/172 13/110:8324/144
direction 158 t=16361453/45000000 reachable    121321 min 200009/200000 [margin:cells/components] 0:0/0 1/1000:472/64 1/100:1148/64 1/20:2276/112 1/10:5360/168 13/110:7580/144
direction 159 t=10976671/30000000 reachable    121269 min 200009/200000 [margin:cells/components] 0:0/0 1/1000:468/64 1/100:1124/64 1/20:2316/96 1/10:5508/160 13/110:7436/144
direction 160 t=207107/562500 reachable    121341 min 200009/200000 [margin:cells/components] 0:0/0 1/1000:408/68 1/100:1128/76 1/20:2280/96 1/10:5340/132 13/110:7456/152
direction 161 t=33344227/90000000 reachable    121345 min 200009/200000 [margin:cells/components] 0:0/0 1/1000:384/48 1/100:996/72 1/20:2088/96 1/10:5332/136 13/110:7412/160
direction 162 t=1863963/5000000 reachable    121333 min 200009/200000 [margin:cells/components] 0:0/0 1/1000:412/48 1/100:1008/72 1/20:2076/100 1/10:5180/140 13/110:7124/164
direction 163 t=33758441/90000000 reachable    121333 min 200009/200000 [margin:cells/components] 0:0/0 1/1000:488/48 1/100:1036/72 1/20:2284/100 1/10:5092/156 13/110:7300/168
direction 164 t=8491387/22500000 reachable    121337 min 200009/200000 [margin:cells/components] 0:0/0 1/1000:512/44 1/100:1040/72 1/20:2316/112 1/10:5488/172 13/110:7784/160
direction 165 t=2278177/6000000 reachable    121393 min 200009/200000 [margin:cells/components] 0:0/0 1/1000:564/48 1/100:1036/72 1/20:2332/112 1/10:5252/172 13/110:7600/144
direction 166 t=17189881/45000000 reachable    121385 min 200009/200000 [margin:cells/components] 0:0/0 1/1000:612/44 1/100:1132/72 1/20:2460/112 1/10:5808/180 13/110:8308/148
direction 167 t=34586869/90000000 reachable    121437 min 200009/200000 [margin:cells/components] 0:0/0 1/1000:504/44 1/100:960/72 1/20:2184/112 1/10:5168/172 13/110:7588/148
direction 168 t=1449749/3750000 reachable    121489 min 200009/200000 [margin:cells/components] 0:0/0 1/1000:464/40 1/100:904/68 1/20:2232/116 1/10:5072/164 13/110:7460/152
direction 169 t=35001083/90000000 reachable    121517 min 200009/200000 [margin:cells/components] 0:0/0 1/1000:572/44 1/100:992/68 1/20:2568/116 1/10:5920/160 13/110:8400/152
direction 170 t=3520819/9000000 reachable    121601 min 200009/200000 [margin:cells/components] 0:0/0 1/1000:472/44 1/100:1016/68 1/20:2468/112 1/10:5812/148 13/110:8332/156
direction 171 t=3935033/10000000 reachable    121645 min 200009/200000 [margin:cells/components] 0:0/0 1/1000:432/44 1/100:1124/68 1/20:2880/112 1/10:6316/156 13/110:8812/164
direction 172 t=8905601/22500000 reachable    121613 min 200009/200000 [margin:cells/components] 0:0/0 1/1000:456/44 1/100:1132/68 1/20:2968/112 1/10:6296/160 13/110:8596/164
direction 173 t=35829511/90000000 reachable    121593 min 200009/200000 [margin:cells/components] 0:0/0 1/1000:400/44 1/100:1076/68 1/20:2720/112 1/10:6020/160 13/110:8672/164
direction 174 t=6006103/15000000 reachable    121641 min 200009/200000 [margin:cells/components] 0:0/0 1/1000:440/36 1/100:1124/60 1/20:2808/108 1/10:6080/172 13/110:8416/168
direction 175 t=1449749/3600000 reachable    121689 min 200009/200000 [margin:cells/components] 0:0/0 1/1000:404/28 1/100:1008/52 1/20:2516/104 1/10:5252/172 13/110:7520/172
direction 176 t=2278177/5625000 reachable    121717 min 200009/200000 [margin:cells/components] 0:0/0 1/1000:376/24 1/100:1032/52 1/20:2416/104 1/10:5072/168 13/110:7388/180
direction 177 t=12219313/30000000 reachable    121733 min 200009/200000 [margin:cells/components] 0:0/0 1/1000:392/24 1/100:1112/52 1/20:2588/108 1/10:5480/168 13/110:7984/180
direction 178 t=18432523/45000000 reachable    121865 min 200009/200000 [margin:cells/components] 0:0/0 1/1000:368/20 1/100:1040/36 1/20:2364/104 1/10:5116/184 13/110:7700/188
direction 179 t=37072153/90000000 reachable    122065 min 200009/200000 [margin:cells/components] 0:0/0 1/1000:396/20 1/100:1156/36 1/20:2504/104 1/10:5076/172 13/110:7664/172
direction 180 t=207107/500000 reachable    122113 min 200009/200000 [margin:cells/components] 0:0/0 1/1000:356/12 1/100:1052/32 1/20:2172/56 1/10:3636/140 13/110:5512/140
scratchpad/lane-297/run0/candidate-swept.json: 181 directions, 21997353 reachable cells
  margin 0: 0 cells (0.000000 of reachable) in 0 components
  margin 1/1000: 442292 cells (0.020107 of reachable) in 6000 components
  margin 1/100: 545584 cells (0.024802 of reachable) in 7812 components
  margin 1/20: 795384 cells (0.036158 of reachable) in 11876 components
  margin 1/10: 1463492 cells (0.066530 of reachable) in 18100 components
  margin 13/110: 1934092 cells (0.087924 of reachable) in 18440 components
```

### `tight_locality.py`

Tight cells against Trump’s cores.

```text
"""Where the near-tight cells of run 0's measure sit, against Trump's clamped cores.

For directions 0 (the six axis cores) and 159 (the five tilted cores) the dense mass
grid is filled by sweep.scaled_mass_grid exactly as the census reads it; every cell at
or below 1 + margin is mapped back from the rotated frame to an absolute centre (the
cell's lower-left event corner), and the distance to the nearest Trump core centre at
that direction is taken. Reported: the number of tight cells, how many lie within 0.05
and within 0.15 of a Trump core centre, and the ten heaviest clusters by a coarse
0.1-bin histogram of centres. Floats only in the readout; the tightness is exact.
"""

from __future__ import annotations

import json
import math
import sys
from collections import Counter
from fractions import Fraction
from pathlib import Path

import numpy as np

from devtools.census_tight_cells import scaled_threshold, tight_cells
from sqpack.fractional.certificate import Certificate
from sqpack.fractional.generate import direction_net, net_half_tangents
from sqpack.fractional.model import Atom
from sqpack.fractional.sweep import scaled_mass_grid, weight_scale

HERE = Path(__file__).parent


def main(path: Path) -> None:
    record = json.loads(path.read_text())
    atoms = tuple(Atom(f"a{i}", Fraction(x), Fraction(y), Fraction(w)) for i, (x, y, w) in enumerate(record["atoms"]))
    L = Fraction(record["outer_side"])
    B = Fraction(record["square_side"])
    tangents = net_half_tangents(Fraction(record["angle_limit"]), int(record["direction_steps"]))
    net = direction_net(tangents)
    scale = weight_scale(atoms)
    cores = json.loads((HERE / "cores-a-scaled-centres.json").read_text())["placements"]
    for k in (0, 159):
        d = net[k]
        c, s = float(d.ux), float(d.uy)
        trump = np.array([[float(Fraction(p["centre"][0])), float(Fraction(p["centre"][1]))] for p in cores if int(p["k"]) == k])
        filled = scaled_mass_grid(atoms, d, L, B, scale)
        u_ev = np.array([float(v) for v in filled.reduction.u_events])
        v_ev = np.array([float(v) for v in filled.reduction.v_events])
        print(f"direction {k} (t = {tangents[k]}): {len(trump)} Trump cores at this direction")
        for margin in (Fraction(1, 1000), Fraction(1, 100), Fraction(13, 110)):
            rows, cols, masses = tight_cells(filled, scaled_threshold(margin, scale))
            if rows.size == 0:
                print(f"  margin {margin}: no tight cells")
                continue
            u = u_ev[rows]
            v = v_ev[cols]
            x = c * u - s * v
            y = s * u + c * v
            pts = np.stack([x, y], axis=1)
            dist = np.min(np.linalg.norm(pts[:, None, :] - trump[None, :, :], axis=2), axis=1)
            near05 = int((dist <= 0.05).sum())
            near15 = int((dist <= 0.15).sum())
            hist = Counter((round(float(px), 1), round(float(py), 1)) for px, py in pts)
            top = hist.most_common(8)
            print(f"  margin {margin}: {rows.size} tight cells; within 0.05 of a Trump core centre: {near05} ({near05 / rows.size * 100:.1f}%), within 0.15: {near15} ({near15 / rows.size * 100:.1f}%); least distance {dist.min():.4f}")
            print(f"    densest 0.1-bins of tight-cell centres (x, y): count -> {top}")
            print(f"    Trump core centres here: {[tuple(round(float(t), 3) for t in row) for row in trump]}")


if __name__ == "__main__":
    main(Path(sys.argv[1]))
```

### `tight_locality.out`

Its output.

```text
direction 0 (t = 0): 6 Trump cores at this direction
  margin 1/1000: 80 tight cells; within 0.05 of a Trump core centre: 1 (1.2%), within 0.15: 2 (2.5%); least distance 0.0000
    densest 0.1-bins of tight-cell centres (x, y): count -> [((0.5, 2.1), 3), ((2.1, 0.5), 3), ((2.1, 3.1), 3), ((3.1, 2.1), 3), ((0.5, 1.6), 2), ((0.5, 1.7), 2), ((0.5, 2.2), 2), ((1.6, 0.5), 2)]
    Trump core centres here: [(0.499, 0.499), (3.321, 0.499), (2.495, 3.321), (0.499, 3.321), (1.478, 3.321), (0.499, 2.342)]
  margin 1/100: 80 tight cells; within 0.05 of a Trump core centre: 1 (1.2%), within 0.15: 2 (2.5%); least distance 0.0000
    densest 0.1-bins of tight-cell centres (x, y): count -> [((0.5, 2.1), 3), ((2.1, 0.5), 3), ((2.1, 3.1), 3), ((3.1, 2.1), 3), ((0.5, 1.6), 2), ((0.5, 1.7), 2), ((0.5, 2.2), 2), ((1.6, 0.5), 2)]
    Trump core centres here: [(0.499, 0.499), (3.321, 0.499), (2.495, 3.321), (0.499, 3.321), (1.478, 3.321), (0.499, 2.342)]
  margin 13/110: 440 tight cells; within 0.05 of a Trump core centre: 1 (0.2%), within 0.15: 3 (0.7%); least distance 0.0000
    densest 0.1-bins of tight-cell centres (x, y): count -> [((2.1, 2.9), 9), ((2.9, 2.1), 9), ((0.9, 2.1), 6), ((1.6, 2.9), 6), ((1.7, 2.9), 6), ((2.1, 0.9), 6), ((2.2, 2.9), 6), ((2.9, 1.6), 6)]
    Trump core centres here: [(0.499, 0.499), (3.321, 0.499), (2.495, 3.321), (0.499, 3.321), (1.478, 3.321), (0.499, 2.342)]
direction 159 (t = 10976671/30000000): 5 Trump cores at this direction
  margin 1/1000: 468 tight cells; within 0.05 of a Trump core centre: 22 (4.7%), within 0.15: 38 (8.1%); least distance 0.0171
    densest 0.1-bins of tight-cell centres (x, y): count -> [((0.7, 0.7), 28), ((0.8, 3.0), 28), ((3.1, 0.7), 28), ((3.0, 3.0), 27), ((0.7, 2.9), 25), ((2.9, 3.1), 25), ((3.1, 0.9), 16), ((0.9, 0.7), 15)]
    Trump core centres here: [(1.254, 1.431), (1.908, 0.703), (1.931, 2.156), (2.585, 1.419), (3.117, 2.306)]
  margin 1/100: 1124 tight cells; within 0.05 of a Trump core centre: 45 (4.0%), within 0.15: 68 (6.0%); least distance 0.0171
    densest 0.1-bins of tight-cell centres (x, y): count -> [((3.0, 3.0), 51), ((0.8, 3.0), 45), ((2.9, 3.1), 38), ((1.7, 0.7), 37), ((0.7, 2.1), 34), ((3.1, 1.7), 34), ((0.7, 2.9), 31), ((3.1, 0.9), 30)]
    Trump core centres here: [(1.254, 1.431), (1.908, 0.703), (1.931, 2.156), (2.585, 1.419), (3.117, 2.306)]
  margin 13/110: 7436 tight cells; within 0.05 of a Trump core centre: 297 (4.0%), within 0.15: 1054 (14.2%); least distance 0.0042
    densest 0.1-bins of tight-cell centres (x, y): count -> [((2.6, 2.4), 156), ((2.1, 3.1), 150), ((1.4, 2.6), 145), ((3.1, 1.7), 145), ((0.7, 2.1), 136), ((1.2, 1.4), 131), ((2.4, 1.2), 127), ((1.7, 0.7), 126)]
    Trump core centres here: [(1.254, 1.431), (1.908, 0.703), (1.931, 2.156), (2.585, 1.419), (3.117, 2.306)]
```

### `run1/run.log`

Run 1 (strips filled, 2400 s deadline): the driver’s round log.

```text
round 0: rows=5732 orbits=518 sites=3849 lp_rounds=23 objective=11.118181818 depth=1.558161157 cost=-2.232644628 least_covered=1.000000000 seconds=63.0 | adding 1 orbits, deepest at (Fraction(1812103, 643300), Fraction(645303, 643300))
round 1: rows=5792 orbits=519 sites=3853 lp_rounds=4 objective=11.118181818 depth=1.564691558 cost=-4.517532468 least_covered=1.000000000 seconds=11.6 | adding 1 orbits, deepest at (Fraction(982489, 977900), Fraction(2238377, 794700))
round 2: rows=6083 orbits=520 sites=3861 lp_rounds=7 objective=11.118181818 depth=1.915483785 cost=-7.323870282 least_covered=1.000000000 seconds=31.7 | adding 1 orbits, deepest at (Fraction(927799, 328900), Fraction(133797, 134200))
round 3: rows=6431 orbits=521 sites=3869 lp_rounds=2 objective=11.118181818 depth=1.532954545 cost=-2.131818182 least_covered=1.000000000 seconds=8.4 | adding 1 orbits, deepest at (Fraction(185605347, 65780000), Fraction(185605347, 65780000))
round 4: rows=6475 orbits=522 sites=3873 lp_rounds=3 objective=11.118181818 depth=1.319008264 cost=-2.552066116 least_covered=1.000000000 seconds=14.7 | adding 1 orbits, deepest at (Fraction(214583, 211300), Fraction(91689, 91900))
round 5: rows=6688 orbits=523 sites=3881 lp_rounds=2 objective=11.118181818 depth=1.514726792 cost=-4.117814338 least_covered=1.000000000 seconds=14.1 | adding 1 orbits, deepest at (Fraction(889947, 891700), Fraction(202999, 203900))
round 6: rows=6726 orbits=524 sites=3889 lp_rounds=2 objective=11.118181818 depth=1.340240642 cost=-2.721925134 least_covered=1.000000000 seconds=9.3 | adding 1 orbits, deepest at (Fraction(627019, 620900), Fraction(92971, 32900))
round 7: rows=6726 orbits=525 sites=3897 lp_rounds=1 objective=11.118181818 depth=1.282960590 cost=-2.263684720 least_covered=1.000000000 seconds=6.1 | adding 1 orbits, deepest at (Fraction(36023, 36100), Fraction(9957, 10000))
round 8: rows=6755 orbits=526 sites=3905 lp_rounds=2 objective=11.118181818 depth=1.242740093 cost=-0.970960370 least_covered=1.000000000 seconds=12.4 | adding 1 orbits, deepest at (Fraction(40423503, 40513300), Fraction(40423503, 40513300))
round 9: rows=6926 orbits=527 sites=3909 lp_rounds=3 objective=11.118181818 depth=1.189204545 cost=-1.513636364 least_covered=1.000000000 seconds=21.3 | adding 1 orbits, deepest at (Fraction(183143, 183300), Fraction(348111, 190100))
round 10: rows=6926 orbits=528 sites=3917 lp_rounds=1 objective=11.118181818 depth=1.417846400 cost=-3.342771199 least_covered=1.000000000 seconds=6.8 | adding 1 orbits, deepest at (Fraction(75027, 26575), Fraction(493237, 174700))
round 11: rows=6926 orbits=529 sites=3925 lp_rounds=1 objective=11.118181818 depth=1.067045455 cost=-0.536363636 least_covered=1.000000000 seconds=5.0 | adding 1 orbits, deepest at (Fraction(180607, 179700), Fraction(685119, 243400))
round 12: rows=6926 orbits=530 sites=3933 lp_rounds=1 objective=11.118181818 depth=1.279822616 cost=-2.238580931 least_covered=1.000000000 seconds=6.7 | adding 1 orbits, deepest at (Fraction(91053, 45800), Fraction(148961, 52725))
round 13: rows=8294 orbits=531 sites=3941 lp_rounds=16 objective=11.098818475 depth=1.210392052 cost=-1.683136412 least_covered=1.000000000 seconds=148.6 | adding 1 orbits, deepest at (Fraction(496153, 175800), Fraction(546807, 193700))
round 14: rows=8335 orbits=532 sites=3949 lp_rounds=2 objective=11.098818475 depth=1.236439313 cost=-1.891514501 least_covered=1.000000000 seconds=18.6 | adding 1 orbits, deepest at (Fraction(130771677237901998063401765781788015268359, 131055765475038455269664762017248024660000), Fraction(892423083497913771968397123972072170044703559613271, 488566195564298208399620277607911359578655160000000))
round 15: rows=8335 orbits=533 sites=3957 lp_rounds=1 objective=11.098818475 depth=1.006444683 cost=-0.051557465 least_covered=1.000000000 seconds=7.6 | adding 1 orbits, deepest at (Fraction(1375319, 380900), Fraction(702183, 248800))
round 16: rows=8340 orbits=534 sites=3965 lp_rounds=2 objective=11.098818475 depth=1.017051557 cost=-0.068206230 least_covered=1.000000000 seconds=16.0 | adding 1 orbits, deepest at (Fraction(248233, 248800), Fraction(248233, 248800))
round 17: rows=8409 orbits=535 sites=3969 lp_rounds=4 objective=11.098818475 depth=1.040547798 cost=-0.324382385 least_covered=1.000000000 seconds=38.5 | adding 1 orbits, deepest at (Fraction(100062409, 99559900), Fraction(221147, 220000))
round 18: rows=8409 orbits=536 sites=3977 lp_rounds=1 objective=11.098818475 depth=1.274704619 cost=-2.197636950 least_covered=1.000000000 seconds=9.8 | adding 1 orbits, deepest at (Fraction(49615667, 17580000), Fraction(640153153, 3324938300))
round 19: rows=8689 orbits=537 sites=3985 lp_rounds=2 objective=11.098818475 depth=1.191846805 cost=-1.534774436 least_covered=1.000000000 seconds=20.2 | adding 1 orbits, deepest at (Fraction(570993, 572300), Fraction(73417, 73700))
round 20: rows=8749 orbits=538 sites=3993 lp_rounds=2 objective=11.098818475 depth=1.224970909 cost=-1.799767275 least_covered=1.000000000 seconds=22.4 | adding 1 orbits, deepest at (Fraction(697491, 700100), Fraction(51186, 51475))
round 21: rows=8749 orbits=539 sites=4001 lp_rounds=1 objective=11.098818475 depth=1.122986037 cost=-0.983888292 least_covered=1.000000000 seconds=7.1 | adding 1 orbits, deepest at (Fraction(4772232773, 4783195300), Fraction(3185217689, 1128532900))
round 22: rows=8785 orbits=540 sites=4009 lp_rounds=3 objective=11.098818475 depth=1.195018797 cost=-1.560150376 least_covered=1.000000000 seconds=27.4 | adding 1 orbits, deepest at (Fraction(9159874371, 3245540000), Fraction(104966338492577210276663321837, 29056137145362654198075000000))
round 23: rows=8843 orbits=541 sites=4017 lp_rounds=5 objective=11.098818475 depth=1.193071966 cost=-1.544575725 least_covered=1.000000000 seconds=46.2 | adding 1 orbits, deepest at (Fraction(48410297, 48521700), Fraction(326371029, 89371900))
round 24: rows=8843 orbits=542 sites=4025 lp_rounds=1 objective=11.098818475 depth=1.108754028 cost=-0.870032223 least_covered=1.000000000 seconds=8.9 | adding 1 orbits, deepest at (Fraction(75963, 41800), Fraction(965579, 341900))
round 25: rows=8976 orbits=543 sites=4033 lp_rounds=3 objective=11.098818475 depth=1.026852846 cost=-0.214822771 least_covered=1.000000000 seconds=28.6 | adding 1 orbits, deepest at (Fraction(145552293, 51572300), Fraction(115269101, 40831100))
round 26: rows=8976 orbits=544 sites=4041 lp_rounds=1 objective=11.098818475 depth=1.042024705 cost=-0.336197637 least_covered=1.000000000 seconds=10.0 | adding 1 orbits, deepest at (Fraction(69311, 38100), Fraction(1307553, 463300))
round 27: rows=8976 orbits=545 sites=4049 lp_rounds=1 objective=11.098818475 depth=1.073979592 cost=-0.591836735 least_covered=1.000000000 seconds=9.9 | adding 1 orbits, deepest at (Fraction(51453893, 51572300), Fraction(136942597, 48521700))
round 28: rows=8978 orbits=546 sites=4057 lp_rounds=2 objective=11.098818475 depth=1.103651987 cost=-0.829215897 least_covered=1.000000000 seconds=23.7 | adding 1 orbits, deepest at (Fraction(48410297, 48521700), Fraction(115269101, 40831100))
round 29: rows=8995 orbits=547 sites=4065 lp_rounds=2 objective=11.098818475 depth=1.266648765 cost=-2.133190118 least_covered=1.000000000 seconds=19.0 | adding 1 orbits, deepest at (Fraction(960721, 963100), Fraction(151289, 151900))
round 30: rows=9073 orbits=548 sites=4073 lp_rounds=2 objective=11.098818475 depth=1.166084855 cost=-1.328678840 least_covered=1.000000000 seconds=21.5 | adding 1 orbits, deepest at (Fraction(2119637, 750700), Fraction(396601, 199100))
round 31: rows=9456 orbits=549 sites=4081 lp_rounds=9 objective=11.095119344 depth=1.335693504 cost=-1.342774017 least_covered=1.000000000 seconds=97.6 | adding 1 orbits, deepest at (Fraction(253117, 253700), Fraction(253117, 253700))
round 32: rows=9576 orbits=550 sites=4085 lp_rounds=8 objective=11.095119344 depth=1.233523335 cost=-1.868186676 least_covered=1.000000000 seconds=121.5 | adding 1 orbits, deepest at (Fraction(38225617, 38313700), Fraction(90748349, 90973900))
round 33: rows=9620 orbits=551 sites=4093 lp_rounds=2 objective=11.095119344 depth=1.204188190 cost=-1.633505522 least_covered=1.000000000 seconds=34.7 | adding 1 orbits, deepest at (Fraction(2432083, 861300), Fraction(215931, 489100))
round 34: rows=9637 orbits=552 sites=4101 lp_rounds=2 objective=11.095119344 depth=1.412406484 cost=-3.299251870 least_covered=1.000000000 seconds=26.8 | adding 1 orbits, deepest at (Fraction(2543078719, 2548940000), Fraction(10391944667, 10416580000))
round 35: rows=9638 orbits=553 sites=4109 lp_rounds=2 objective=11.095119344 depth=1.211747417 cost=-1.693979337 least_covered=1.000000000 seconds=27.0 | adding 1 orbits, deepest at (Fraction(4809040339, 4821860000), Fraction(2543078719, 2548940000))
round 36: rows=9641 orbits=554 sites=4117 lp_rounds=2 objective=11.095119344 depth=1.296847168 cost=-1.187388671 least_covered=1.000000000 seconds=23.3 | adding 1 orbits, deepest at (Fraction(1308817, 463700), Fraction(462517, 463700))
round 37: rows=9763 orbits=555 sites=4121 lp_rounds=8 objective=11.093829679 depth=1.125191229 cost=-1.001529832 least_covered=1.000000000 seconds=63.4 | adding 1 orbits, deepest at (Fraction(1084667, 383700), Fraction(514047, 181700))
round 38: rows=9958 orbits=556 sites=4129 lp_rounds=7 objective=11.082608208 depth=1.137384449 cost=-1.099075595 least_covered=1.000000000 seconds=85.3 | adding 1 orbits, deepest at (Fraction(125709, 68900), Fraction(52777, 18700))
round 39: rows=9983 orbits=557 sites=4137 lp_rounds=2 objective=11.082608208 depth=1.616423582 cost=-2.465694328 least_covered=1.000000000 seconds=28.5 | adding 1 orbits, deepest at (Fraction(7193872081, 2548940000), Fraction(2543078719, 2548940000))
round 40: rows=9983 orbits=558 sites=4141 lp_rounds=1 objective=11.082608208 depth=1.004069789 cost=-0.016279157 least_covered=1.000000000 seconds=22.6 | adding 1 orbits, deepest at (Fraction(933487, 935700), Fraction(2640887, 935700))
round 41: rows=10038 orbits=559 sites=4145 lp_rounds=5 objective=11.082506157 depth=1.489635421 cost=-3.917083364 least_covered=1.000000000 seconds=73.3 | adding 1 orbits, deepest at (Fraction(2767247381314886356927635916668967, 2773632226655157787448122557420000), Fraction(2543078719, 2548940000))
round 42: rows=10044 orbits=560 sites=4153 lp_rounds=2 objective=11.082506157 depth=1.502254521 cost=-2.009018086 least_covered=1.000000000 seconds=24.5 | adding 1 orbits, deepest at (Fraction(68941, 69100), Fraction(68941, 69100))
round 43: rows=10251 orbits=561 sites=4157 lp_rounds=4 objective=11.082501622 depth=1.214219685 cost=-1.713757478 least_covered=1.000000000 seconds=61.6 | adding 1 orbits, deepest at (Fraction(80274677, 79774700), Fraction(100296943, 35537300))
round 44: rows=10262 orbits=562 sites=4165 lp_rounds=2 objective=11.082501622 depth=1.162213169 cost=-1.297705348 least_covered=1.000000000 seconds=28.3 | adding 1 orbits, deepest at (Fraction(2557251, 906100), Fraction(175403, 175800))
round 45: rows=10262 orbits=563 sites=4173 lp_rounds=1 objective=11.082501622 depth=1.180938891 cost=-0.723755562 least_covered=1.000000000 seconds=18.4 | adding 1 orbits, deepest at (Fraction(191, 100), Fraction(5953, 5660))
round 46: rows=10262 orbits=564 sites=4177 lp_rounds=1 objective=11.082501622 depth=1.072232751 cost=-0.577862008 least_covered=1.000000000 seconds=18.7 | adding 1 orbits, deepest at (Fraction(287129, 101900), Fraction(178379, 178900))
round 47: rows=10268 orbits=565 sites=4185 lp_rounds=2 objective=11.082501622 depth=1.095181431 cost=-0.761451446 least_covered=1.000000000 seconds=47.2 | adding 1 orbits, deepest at (Fraction(711067, 713700), Fraction(393703, 197300))
round 48: rows=10318 orbits=566 sites=4193 lp_rounds=2 objective=11.082501622 depth=1.164008355 cost=-1.312066837 least_covered=1.000000000 seconds=38.1 | adding 1 orbits, deepest at (Fraction(560333, 158300), Fraction(828191, 830100))
round 49: rows=10320 orbits=567 sites=4201 lp_rounds=3 objective=11.082501622 depth=1.024166463 cost=-0.193331702 least_covered=1.000000000 seconds=57.1 | adding 1 orbits, deepest at (Fraction(291667, 293700), Fraction(18657, 18700))
round 50: rows=10320 orbits=568 sites=4209 lp_rounds=1 objective=11.082501622 depth=1.037597017 cost=-0.300776138 least_covered=1.000000000 seconds=14.3 | adding 1 orbits, deepest at (Fraction(2343761, 827100), Fraction(2275111, 802100))
round 51: rows=10336 orbits=569 sites=4217 lp_rounds=2 objective=11.082501622 depth=1.170724539 cost=-1.365796309 least_covered=1.000000000 seconds=25.9 | adding 1 orbits, deepest at (Fraction(1381347, 486700), Fraction(658137, 233200))
round 52: rows=10336 orbits=570 sites=4225 lp_rounds=1 objective=11.082501622 depth=1.119839252 cost=-0.958714014 least_covered=1.000000000 seconds=30.4 | adding 1 orbits, deepest at (Fraction(828191, 830100), Fraction(2400463, 849300))
round 53: rows=10372 orbits=571 sites=4233 lp_rounds=2 objective=11.082501622 depth=1.059727470 cost=-0.477819759 least_covered=1.000000000 seconds=36.3 | adding 1 orbits, deepest at (Fraction(191963843, 68017300), Fraction(252080587, 89175700))
round 54: rows=10389 orbits=572 sites=4241 lp_rounds=3 objective=11.082501622 depth=1.038776658 cost=-0.310213267 least_covered=1.000000000 seconds=48.1 | adding 1 orbits, deepest at (Fraction(25853703, 25913300), Fraction(50327411, 14250100))
round 55: rows=10402 orbits=573 sites=4249 lp_rounds=2 objective=11.082501622 depth=1.074808882 cost=-0.598471054 least_covered=1.000000000 seconds=36.3 | adding 1 orbits, deepest at (Fraction(1856407, 657700), Fraction(48473, 17175))
round 56: rows=10402 orbits=574 sites=4257 lp_rounds=1 objective=11.082501622 depth=1.088272866 cost=-0.353091464 least_covered=1.000000000 seconds=21.1 | adding 1 orbits, deepest at (Fraction(493163, 494300), Fraction(493163, 494300))
round 57: rows=10416 orbits=575 sites=4261 lp_rounds=2 objective=11.082501622 depth=1.041253834 cost=-0.330030670 least_covered=1.000000000 seconds=39.6 | adding 1 orbits, deepest at (Fraction(661529, 234400), Fraction(87161, 88100))
round 58: rows=10469 orbits=576 sites=4269 lp_rounds=2 objective=11.082501622 depth=1.051585444 cost=-0.412683555 least_covered=1.000000000 seconds=28.3 | adding 1 orbits, deepest at (Fraction(1373033, 486300), Fraction(147041, 365100))
round 59: rows=10469 orbits=577 sites=4277 lp_rounds=1 objective=11.082501622 depth=1.034845469 cost=-0.278763756 least_covered=1.000000000 seconds=13.9 | adding 1 orbits, deepest at (Fraction(857699, 303900), Fraction(470071, 473100))
round 60: rows=10478 orbits=578 sites=4285 lp_rounds=2 objective=11.072443466 depth=1.135309757 cost=-1.082478058 least_covered=1.000000000 seconds=19.6 | adding 1 orbits, deepest at (Fraction(17254920447, 6113780000), Fraction(130028456787840066580078065287, 130931314778435874496056000000))
round 61: rows=10480 orbits=579 sites=4293 lp_rounds=3 objective=11.072443466 depth=1.030633598 cost=-0.245068780 least_covered=1.000000000 seconds=25.9 | adding 1 orbits, deepest at (Fraction(691703, 693300), Fraction(608809, 609900))
round 62: rows=10480 orbits=580 sites=4301 lp_rounds=1 objective=11.072443466 depth=1.022061314 cost=-0.176490510 least_covered=1.000000000 seconds=7.9 | adding 1 orbits, deepest at (Fraction(209819, 114650), Fraction(824603, 823300))
round 63: rows=10480 orbits=581 sites=4309 lp_rounds=1 objective=11.072443466 depth=1.082482823 cost=-0.659862584 least_covered=1.000000000 seconds=12.7 | adding 1 orbits, deepest at (Fraction(24768733, 8776300), Fraction(33675419, 11892150))
round 64: rows=10480 orbits=582 sites=4317 lp_rounds=1 objective=11.072443466 depth=1.032636248 cost=-0.261089987 least_covered=1.000000000 seconds=9.8 | adding 1 orbits, deepest at (Fraction(28856457717769000055620599, 28923147160855781922260000), Fraction(184270661782261071711388137, 65291367746668010798380000))
round 65: rows=10480 orbits=583 sites=4325 lp_rounds=1 objective=11.072443466 depth=nan cost=nan least_covered=1.000000000 seconds=8.5 | no candidate orbit has averaged depth above 1
ceiling: proved=False total 9.263227 over 256 squares, max pointwise depth 0.000000 at 272536 vertices (0 decided exactly), feasible total 9.263227
rationalised total 553677/50000 = 11.073540000 against LP optimum 11.072443466 over 384 atoms
```

### `run1/rows.log`

Run 1: the LP-round log.

```text
   lp    rows  added violated  support     objective    sep_s     lp_s
    0     505    505      543        0      9.000000    21.30     0.13
    1     881    376      543      100      9.666667     0.14     0.27
    2    1149    268      543       96     10.600000     0.12     0.25
    3    1485    336      543       72     11.000000     0.09     0.39
    4    1875    390      543      132     11.000000     0.23     0.45
    5    2305    430      543      152     11.000000     0.29     0.71
    6    2604    299      492      160     11.000000     0.32     0.91
    7    2947    343      543      180     11.026144     0.38     0.99
    8    3288    341      513      176     11.054054     0.36     1.17
    9    3542    254      426      144     11.073072     0.26     1.15
   10    3773    231      411      240     11.080000     0.60     1.44
   11    4000    227      369      184     11.096154     0.39     1.83
   12    4197    197      354      208     11.115385     0.51     2.06
   13    4557    360      543      288     11.118182     0.78     2.09
   14    4881    324      462      233     11.118182     0.61     2.06
   15    5039    158      258      257     11.118182     0.78     2.09
   16    5279    240      360      237     11.118182     0.60     1.90
   17    5300     21       54      417     11.118182     0.73     1.73
   18    5370     70      147      393     11.118182     0.91     1.95
   19    5618    248      411      421     11.118182     0.86     1.79
   20    5659     41      114      497     11.118182     1.59     1.65
   21    5732     73      138      385     11.118182     0.95     2.18
   22    5732      0        0      417     11.118182     1.05     0.00
   -1    5732      0        0       70     11.118182     0.00     2.39
    0    5745     13       30      497     11.118182     1.36     1.54
    1    5768     23       27      341     11.118182     0.89     1.72
    2    5792     24       42      437     11.118182     0.83     2.07
    3    5792      0        0      397     11.118182     0.83     0.00
   -1    5792      0        0       65     11.118182     0.00     1.59
    0    5796      4       15      473     11.118182     1.35     1.87
    1    5909    113      267      321     11.118182     0.90     2.72
    2    5912      3       12      501     11.118182     1.71     3.30
    3    5972     60      114      521     11.118182     1.69     3.77
    4    6040     68      165      469     11.118182     2.54     3.51
    5    6083     43       93      445     11.118182     2.01     3.37
    6    6083      0        0      453     11.118182     1.35     0.00
   -1    6083      0        0       47     11.057088     0.00     2.78
    0    6431    348      492      336     11.118182     0.98     2.87
    1    6431      0        0      501     11.118182     1.78     0.00
   -1    6431      0        0       71     11.118182     0.00     2.86
    0    6455     24       42      517     11.118182     1.48     2.82
    1    6475     20       42      361     11.118182     1.12     4.14
    2    6475      0        0      453     11.118182     2.29     0.00
   -1    6475      0        0       68     11.118078     0.00     4.45
    0    6688    213      423      485     11.118182     3.28     3.68
    1    6688      0        0      629     11.118182     2.73     0.00
   -1    6688      0        0       69     11.117276     0.00     3.21
    0    6726     38       75      501     11.118182     1.61     2.83
    1    6726      0        0      529     11.118182     1.60     0.00
   -1    6726      0        0       81     11.118182     0.00     3.92
    0    6726      0        0      593     11.118182     2.13     0.00
   -1    6726      0        0       77     11.118182     0.00     3.39
    0    6755     29       66      561     11.118182     3.88     3.04
    1    6755      0        0      489     11.118182     2.13     0.00
   -1    6755      0        0       69     11.116953     0.00     3.53
    0    6899    144      264      497     11.118182     1.65     4.15
    1    6926     27       45      629     11.118182     2.70     6.39
    2    6926      0        0      557     11.118182     2.88     0.00
   -1    6926      0        0       82     11.118182     0.00     4.86
    0    6926      0        0      573     11.118182     1.87     0.00
   -1    6926      0        0       70     11.118182     0.00     3.44
    0    6926      0        0      497     11.118182     1.54     0.00
   -1    6926      0        0       74     11.118182     0.00     4.76
    0    6926      0        0      529     11.118182     1.96     0.00
   -1    6926      0        0       53     11.061741     0.00     4.31
    0    7190    264      543      376     11.077418     1.62     4.65
    1    7428    238      426      472     11.086957     2.31     5.41
    2    7468     40       72      504     11.090592     1.81     6.56
    3    7648    180      369      540     11.095155     4.11     6.60
    4    7835    187      357      596     11.096175     4.93     4.33
    5    7908     73      168      528     11.098164     2.99     5.13
    6    8045    137      258      416     11.098567     2.25     5.88
    7    8108     63      132      600     11.098768     6.56     5.44
    8    8134     26       57      428     11.098818     2.51     4.81
    9    8167     33       75      429     11.098818     2.48     4.38
   10    8241     74      150      536     11.098818     3.07     6.78
   11    8255     14       42      652     11.098818     5.99     6.62
   12    8281     26       57      584     11.098818     4.86     7.19
   13    8293     12       33      620     11.098818     3.61     6.18
   14    8294      1        3      640     11.098818     4.92     6.11
   15    8294      0        0      608     11.098818     4.14     0.00
   -1    8294      0        0       73     11.093308     0.00     5.83
    0    8335     41       72      528     11.098818     3.06     6.96
    1    8335      0        0      536     11.098818     2.76     0.00
   -1    8335      0        0       77     11.098818     0.00     5.16
    0    8335      0        0      569     11.098818     2.45     0.00
   -1    8335      0        0       66     11.098818     0.00     5.13
    0    8340      5       18      476     11.098818     1.68     5.99
    1    8340      0        0      564     11.098818     3.15     0.00
   -1    8340      0        0       67     11.098818     0.00     5.52
    0    8357     17       39      496     11.098818     2.24     5.68
    1    8393     36       99      548     11.098818     2.71     6.03
    2    8409     16       27      532     11.098818     4.07     7.73
    3    8409      0        0      600     11.098818     4.55     0.00
   -1    8409      0        0       79     11.098818     0.00     6.47
    0    8409      0        0      580     11.098818     3.34     0.00
   -1    8409      0        0       65     11.089563     0.00     5.84
    0    8689    280      543      476     11.098818     3.60     6.02
    1    8689      0        0      624     11.098818     4.71     0.00
   -1    8689      0        0       72     11.098528     0.00     6.45
    0    8749     60      108      532     11.098818     3.94     6.75
    1    8749      0        0      616     11.098818     5.26     0.00
   -1    8749      0        0       61     11.098818     0.00     4.61
    0    8749      0        0      452     11.098818     2.52     0.00
   -1    8749      0        0       69     11.094066     0.00     5.79
    0    8760     11       21      504     11.098818     3.48     5.49
    1    8785     25       54      620     11.098818     4.15     5.80
    2    8785      0        0      564     11.098818     2.64     0.00
   -1    8785      0        0       63     11.098818     0.00     7.03
    0    8797     12       30      468     11.098818     2.36     5.90
    1    8809     12       30      601     11.098818     3.20     9.00
    2    8810      1        3      436     11.098818     2.27     5.86
    3    8843     33       51      524     11.098818     3.52     4.57
    4    8843      0        0      484     11.098818     2.52     0.00
   -1    8843      0        0       55     11.098818     0.00     6.58
    0    8843      0        0      400     11.098818     2.35     0.00
   -1    8843      0        0       68     11.097826     0.00     7.10
    0    8970    127      243      496     11.098818     3.64     5.52
    1    8976      6       12      540     11.098818     3.23     6.52
    2    8976      0        0      572     11.098818     2.63     0.00
   -1    8976      0        0       81     11.098818     0.00     6.06
    0    8976      0        0      608     11.098818     3.92     0.00
   -1    8976      0        0       74     11.098818     0.00     6.70
    0    8976      0        0      552     11.098818     3.19     0.00
   -1    8976      0        0       87     11.098818     0.00     6.19
    0    8978      2        6      648     11.098818     6.01     8.23
    1    8978      0        0      624     11.098818     3.25     0.00
   -1    8978      0        0       66     11.094074     0.00     6.09
    0    8995     17       39      488     11.098818     2.78     6.05
    1    8995      0        0      604     11.098818     4.10     0.00
   -1    8995      0        0       76     11.098259     0.00     7.45
    0    9073     78      135      556     11.098818     4.22     7.19
    1    9073      0        0      536     11.098818     2.59     0.00
   -1    9073      0        0       68     11.092914     0.00     8.30
    0    9288    215      357      492     11.093261     3.20     7.10
    1    9334     46      108      524     11.094070     3.36     7.27
    2    9340      6       12      592     11.094203     3.13     6.63
    3    9394     54       87      620     11.095104     6.65     6.77
    4    9437     43       77      608     11.095119     3.86     8.34
    5    9444      7       18      468     11.095119     3.18     7.01
    6    9446      2        6      496     11.095119     4.30     6.66
    7    9456     10       42      440     11.095119     2.20     4.77
    8    9456      0        0      616     11.095119     4.86     0.00
   -1    9456      0        0       75     11.089597     0.00     6.81
    0    9531     75      177      544     11.095119     3.13     6.23
    1    9536      5       15      532     11.095119     3.07     7.13
    2    9544      8       24      592     11.095119     3.56     7.14
    3    9551      7       18      648     11.095119     5.64     8.42
    4    9553      2        6      584     11.095119     8.18    14.76
    5    9557      4       12      700     11.095119    12.95    10.48
    6    9576     19       42      624     11.095119    11.81     7.75
    7    9576      0        0      560     11.095119     4.43     0.00
   -1    9576      0        0       77     11.091340     0.00    10.66
    0    9620     44       90      580     11.095119     6.84     8.43
    1    9620      0        0      628     11.095119     8.78     0.00
   -1    9620      0        0       65     11.095119     0.00     9.74
    0    9637     17       30      476     11.095119     4.07     7.20
    1    9637      0        0      560     11.095119     5.79     0.00
   -1    9637      0        0       82     11.095119     0.00     8.00
    0    9638      1        3      588     11.095119     5.10     8.82
    1    9638      0        0      580     11.095119     5.05     0.00
   -1    9638      0        0       59     11.095119     0.00     9.00
    0    9641      3        9      436     11.095119     2.42     8.25
    1    9641      0        0      572     11.095119     3.62     0.00
   -1    9641      0        0       87     11.092393     0.00     6.35
    0    9652     11       27      644     11.092706     3.46     5.87
    1    9675     23       66      565     11.093410     2.44     4.90
    2    9687     12       24      556     11.093444     2.32     4.17
    3    9759     72      129      544     11.093750     2.35     5.42
    4    9760      1        3      536     11.093811     1.87     4.94
    5    9761      1        3      632     11.093819     3.84     4.56
    6    9763      2        3      556     11.093830     3.19     5.77
    7    9763      0        0      556     11.093830     1.98     0.00
   -1    9763      0        0       81     11.080394     0.00     5.29
    0    9800     37       99      600     11.081845     3.36     6.52
    1    9888     88      207      556     11.082271     3.83     7.58
    2    9905     17       27      697     11.082593     3.49     7.79
    3    9928     23       66      657     11.082600     6.08     6.36
    4    9932      4        9      601     11.082608     3.82     7.61
    5    9958     26       60      709     11.082608     9.98     8.03
    6    9958      0        0      641     11.082608     5.54     0.00
   -1    9958      0        0       81     11.082608     0.00     7.63
    0    9983     25       63      581     11.082608     7.02     8.33
    1    9983      0        0      553     11.082608     5.51     0.00
   -1    9983      0        0       85     11.082608     0.00    11.95
    0    9983      0        0      625     11.082608    10.62     0.00
   -1    9983      0        0       76     11.082455     0.00     7.69
    0    9993     10       21      553     11.082506     7.02    10.14
    1   10030     37       60      601     11.082506     5.83    10.36
    2   10031      1        3      629     11.082506     5.48     9.56
    3   10038      7       15      625     11.082506     3.24     7.22
    4   10038      0        0      577     11.082506     6.72     0.00
   -1   10038      0        0       81     11.082506     0.00     8.63
    0   10044      6       18      593     11.082506     3.53     7.64
    1   10044      0        0      597     11.082506     4.65     0.00
   -1   10044      0        0       71     11.066714     0.00     7.76
    0   10215    171      381      520     11.082466     3.67     9.02
    1   10231     16       27      641     11.082499     8.36     9.07
    2   10251     20       39      717     11.082502     9.95     6.84
    3   10251      0        0      657     11.082502     6.91     0.00
   -1   10251      0        0       89     11.082502     0.00     5.67
    0   10262     11       18      649     11.082502     7.90     6.88
    1   10262      0        0      645     11.082502     7.80     0.00
   -1   10262      0        0       86     11.082502     0.00     9.04
    0   10262      0        0      625     11.082502     9.32     0.00
   -1   10262      0        0      104     11.082502     0.00     7.63
    0   10262      0        0      761     11.082502    11.09     0.00
   -1   10262      0        0       95     11.082502     0.00    14.75
    0   10268      6       15      681     11.082502    12.45    12.65
    1   10268      0        0      533     11.082502     7.33     0.00
   -1   10268      0        0       89     11.079168     0.00    10.44
    0   10318     50       96      660     11.082502     9.11     8.98
    1   10318      0        0      689     11.082502     9.51     0.00
   -1   10318      0        0      105     11.082502     0.00    11.35
    0   10319      1        3      765     11.082502     8.89     9.04
    1   10320      1        3      713     11.082502    10.87     8.52
    2   10320      0        0      657     11.082502     8.42     0.00
   -1   10320      0        0       88     11.082502     0.00     8.93
    0   10320      0        0      633     11.082502     5.32     0.00
   -1   10320      0        0       94     11.081755     0.00     7.74
    0   10336     16       42      688     11.082502     5.91     5.67
    1   10336      0        0      681     11.082502     6.62     0.00
   -1   10336      0        0       97     11.082502     0.00    15.08
    0   10336      0        0      709     11.082502    15.31     0.00
   -1   10336      0        0       82     11.062470     0.00     9.65
    0   10372     36       84      604     11.082502     6.64    10.85
    1   10372      0        0      729     11.082502     9.10     0.00
   -1   10372      0        0       93     11.082502     0.00     9.88
    0   10388     16       48      685     11.082502     7.07     6.97
    1   10389      1        3      709     11.082502     7.36     8.54
    2   10389      0        0      705     11.082502     8.25     0.00
   -1   10389      0        0       97     11.082502     0.00     8.97
    0   10402     13       30      705     11.082502    10.08     7.47
    1   10402      0        0      725     11.082502     9.72     0.00
   -1   10402      0        0       99     11.082502     0.00     9.88
    0   10402      0        0      733     11.082502    11.25     0.00
   -1   10402      0        0      101     11.082502     0.00    11.06
    0   10416     14       24      725     11.082502    11.71     7.78
    1   10416      0        0      737     11.082502     9.03     0.00
   -1   10416      0        0       89     11.082502     0.00     7.21
    0   10469     53       84      645     11.082502     7.43     7.64
    1   10469      0        0      653     11.082502     5.99     0.00
   -1   10469      0        0       95     11.082502     0.00     7.44
    0   10469      0        0      697     11.082502     6.47     0.00
   -1   10469      0        0       80     11.072349     0.00     6.93
    0   10478      9       15      584     11.072443     4.21     6.33
    1   10478      0        0      412     11.072443     2.13     0.00
   -1   10478      0        0       57     11.072443     0.00     8.69
    0   10479      1        3      420     11.072443     1.50     5.29
    1   10480      1        3      728     11.072443     3.27     5.16
    2   10480      0        0      540     11.072443     2.01     0.00
   -1   10480      0        0       70     11.072443     0.00     5.23
    0   10480      0        0      516     11.072443     2.63     0.00
   -1   10480      0        0       96     11.072443     0.00     8.02
    0   10480      0        0      712     11.072443     4.69     0.00
   -1   10480      0        0       85     11.072443     0.00     7.59
    0   10480      0        0      616     11.072443     2.25     0.00
   -1   10480      0        0       66     11.072443     0.00     5.81
    0   10480      0        0      488     11.072443     2.64     0.00
```

### `run1/stdout.txt`

Run 1: the driver’s summary.

```text
warning: The `UV_NATIVE_TLS` environment variable is deprecated and will be removed in a future release. Use `UV_SYSTEM_CERTS` instead.
{
 "n": 11,
 "outer_side": "191/50",
 "square_side": "9977/10000",
 "grid_counts": [
  25,
  34,
  41
 ],
 "inset": "1/2",
 "angle_limit": "207107/500000",
 "direction_steps": 180,
 "scale": 200000,
 "column_rounds": 400,
 "max_rounds": 60,
 "rows_per_direction": 3,
 "seed_certificate": "scratchpad/lane-297/trump-strip-sites.json",
 "seed_map": "scale",
 "seed_windows": 0
}
round    rows  orbits   sites lp_rounds     objective least_covered      depth   seconds  note
----------------------------------------------------------------------------------------------
    0    5732     518    3849        23     11.118182      1.000000   1.558161      63.0  adding 1 orbits, deepest at (Fraction(1812103, 643300), Fraction(645303, 643300))
    1    5792     519    3853         4     11.118182      1.000000   1.564692      11.6  adding 1 orbits, deepest at (Fraction(982489, 977900), Fraction(2238377, 794700))
    2    6083     520    3861         7     11.118182      1.000000   1.915484      31.7  adding 1 orbits, deepest at (Fraction(927799, 328900), Fraction(133797, 134200))
    3    6431     521    3869         2     11.118182      1.000000   1.532955       8.4  adding 1 orbits, deepest at (Fraction(185605347, 65780000), Fraction(185605347, 65780000))
    4    6475     522    3873         3     11.118182      1.000000   1.319008      14.7  adding 1 orbits, deepest at (Fraction(214583, 211300), Fraction(91689, 91900))
    5    6688     523    3881         2     11.118182      1.000000   1.514727      14.1  adding 1 orbits, deepest at (Fraction(889947, 891700), Fraction(202999, 203900))
    6    6726     524    3889         2     11.118182      1.000000   1.340241       9.3  adding 1 orbits, deepest at (Fraction(627019, 620900), Fraction(92971, 32900))
    7    6726     525    3897         1     11.118182      1.000000   1.282961       6.1  adding 1 orbits, deepest at (Fraction(36023, 36100), Fraction(9957, 10000))
    8    6755     526    3905         2     11.118182      1.000000   1.242740      12.4  adding 1 orbits, deepest at (Fraction(40423503, 40513300), Fraction(40423503, 40513300))
    9    6926     527    3909         3     11.118182      1.000000   1.189205      21.3  adding 1 orbits, deepest at (Fraction(183143, 183300), Fraction(348111, 190100))
   10    6926     528    3917         1     11.118182      1.000000   1.417846       6.8  adding 1 orbits, deepest at (Fraction(75027, 26575), Fraction(493237, 174700))
   11    6926     529    3925         1     11.118182      1.000000   1.067045       5.0  adding 1 orbits, deepest at (Fraction(180607, 179700), Fraction(685119, 243400))
   12    6926     530    3933         1     11.118182      1.000000   1.279823       6.7  adding 1 orbits, deepest at (Fraction(91053, 45800), Fraction(148961, 52725))
   13    8294     531    3941        16     11.098818      1.000000   1.210392     148.6  adding 1 orbits, deepest at (Fraction(496153, 175800), Fraction(546807, 193700))
   14    8335     532    3949         2     11.098818      1.000000   1.236439      18.6  adding 1 orbits, deepest at (Fraction(130771677237901998063401765781788015268359, 131055765475038455269664762017248024660000), Fraction(892423083497913771968397123972072170044703559613271, 488566195564298208399620277607911359578655160000000))
   15    8335     533    3957         1     11.098818      1.000000   1.006445       7.6  adding 1 orbits, deepest at (Fraction(1375319, 380900), Fraction(702183, 248800))
   16    8340     534    3965         2     11.098818      1.000000   1.017052      16.0  adding 1 orbits, deepest at (Fraction(248233, 248800), Fraction(248233, 248800))
   17    8409     535    3969         4     11.098818      1.000000   1.040548      38.5  adding 1 orbits, deepest at (Fraction(100062409, 99559900), Fraction(221147, 220000))
   18    8409     536    3977         1     11.098818      1.000000   1.274705       9.8  adding 1 orbits, deepest at (Fraction(49615667, 17580000), Fraction(640153153, 3324938300))
   19    8689     537    3985         2     11.098818      1.000000   1.191847      20.2  adding 1 orbits, deepest at (Fraction(570993, 572300), Fraction(73417, 73700))
   20    8749     538    3993         2     11.098818      1.000000   1.224971      22.4  adding 1 orbits, deepest at (Fraction(697491, 700100), Fraction(51186, 51475))
   21    8749     539    4001         1     11.098818      1.000000   1.122986       7.1  adding 1 orbits, deepest at (Fraction(4772232773, 4783195300), Fraction(3185217689, 1128532900))
   22    8785     540    4009         3     11.098818      1.000000   1.195019      27.4  adding 1 orbits, deepest at (Fraction(9159874371, 3245540000), Fraction(104966338492577210276663321837, 29056137145362654198075000000))
   23    8843     541    4017         5     11.098818      1.000000   1.193072      46.2  adding 1 orbits, deepest at (Fraction(48410297, 48521700), Fraction(326371029, 89371900))
   24    8843     542    4025         1     11.098818      1.000000   1.108754       8.9  adding 1 orbits, deepest at (Fraction(75963, 41800), Fraction(965579, 341900))
   25    8976     543    4033         3     11.098818      1.000000   1.026853      28.6  adding 1 orbits, deepest at (Fraction(145552293, 51572300), Fraction(115269101, 40831100))
   26    8976     544    4041         1     11.098818      1.000000   1.042025      10.0  adding 1 orbits, deepest at (Fraction(69311, 38100), Fraction(1307553, 463300))
   27    8976     545    4049         1     11.098818      1.000000   1.073980       9.9  adding 1 orbits, deepest at (Fraction(51453893, 51572300), Fraction(136942597, 48521700))
   28    8978     546    4057         2     11.098818      1.000000   1.103652      23.7  adding 1 orbits, deepest at (Fraction(48410297, 48521700), Fraction(115269101, 40831100))
   29    8995     547    4065         2     11.098818      1.000000   1.266649      19.0  adding 1 orbits, deepest at (Fraction(960721, 963100), Fraction(151289, 151900))
   30    9073     548    4073         2     11.098818      1.000000   1.166085      21.5  adding 1 orbits, deepest at (Fraction(2119637, 750700), Fraction(396601, 199100))
   31    9456     549    4081         9     11.095119      1.000000   1.335694      97.6  adding 1 orbits, deepest at (Fraction(253117, 253700), Fraction(253117, 253700))
   32    9576     550    4085         8     11.095119      1.000000   1.233523     121.5  adding 1 orbits, deepest at (Fraction(38225617, 38313700), Fraction(90748349, 90973900))
   33    9620     551    4093         2     11.095119      1.000000   1.204188      34.7  adding 1 orbits, deepest at (Fraction(2432083, 861300), Fraction(215931, 489100))
   34    9637     552    4101         2     11.095119      1.000000   1.412406      26.8  adding 1 orbits, deepest at (Fraction(2543078719, 2548940000), Fraction(10391944667, 10416580000))
   35    9638     553    4109         2     11.095119      1.000000   1.211747      27.0  adding 1 orbits, deepest at (Fraction(4809040339, 4821860000), Fraction(2543078719, 2548940000))
   36    9641     554    4117         2     11.095119      1.000000   1.296847      23.3  adding 1 orbits, deepest at (Fraction(1308817, 463700), Fraction(462517, 463700))
   37    9763     555    4121         8     11.093830      1.000000   1.125191      63.4  adding 1 orbits, deepest at (Fraction(1084667, 383700), Fraction(514047, 181700))
   38    9958     556    4129         7     11.082608      1.000000   1.137384      85.3  adding 1 orbits, deepest at (Fraction(125709, 68900), Fraction(52777, 18700))
   39    9983     557    4137         2     11.082608      1.000000   1.616424      28.5  adding 1 orbits, deepest at (Fraction(7193872081, 2548940000), Fraction(2543078719, 2548940000))
   40    9983     558    4141         1     11.082608      1.000000   1.004070      22.6  adding 1 orbits, deepest at (Fraction(933487, 935700), Fraction(2640887, 935700))
   41   10038     559    4145         5     11.082506      1.000000   1.489635      73.3  adding 1 orbits, deepest at (Fraction(2767247381314886356927635916668967, 2773632226655157787448122557420000), Fraction(2543078719, 2548940000))
   42   10044     560    4153         2     11.082506      1.000000   1.502255      24.5  adding 1 orbits, deepest at (Fraction(68941, 69100), Fraction(68941, 69100))
   43   10251     561    4157         4     11.082502      1.000000   1.214220      61.6  adding 1 orbits, deepest at (Fraction(80274677, 79774700), Fraction(100296943, 35537300))
   44   10262     562    4165         2     11.082502      1.000000   1.162213      28.3  adding 1 orbits, deepest at (Fraction(2557251, 906100), Fraction(175403, 175800))
   45   10262     563    4173         1     11.082502      1.000000   1.180939      18.4  adding 1 orbits, deepest at (Fraction(191, 100), Fraction(5953, 5660))
   46   10262     564    4177         1     11.082502      1.000000   1.072233      18.7  adding 1 orbits, deepest at (Fraction(287129, 101900), Fraction(178379, 178900))
   47   10268     565    4185         2     11.082502      1.000000   1.095181      47.2  adding 1 orbits, deepest at (Fraction(711067, 713700), Fraction(393703, 197300))
   48   10318     566    4193         2     11.082502      1.000000   1.164008      38.1  adding 1 orbits, deepest at (Fraction(560333, 158300), Fraction(828191, 830100))
   49   10320     567    4201         3     11.082502      1.000000   1.024166      57.1  adding 1 orbits, deepest at (Fraction(291667, 293700), Fraction(18657, 18700))
   50   10320     568    4209         1     11.082502      1.000000   1.037597      14.3  adding 1 orbits, deepest at (Fraction(2343761, 827100), Fraction(2275111, 802100))
   51   10336     569    4217         2     11.082502      1.000000   1.170725      25.9  adding 1 orbits, deepest at (Fraction(1381347, 486700), Fraction(658137, 233200))
   52   10336     570    4225         1     11.082502      1.000000   1.119839      30.4  adding 1 orbits, deepest at (Fraction(828191, 830100), Fraction(2400463, 849300))
   53   10372     571    4233         2     11.082502      1.000000   1.059727      36.3  adding 1 orbits, deepest at (Fraction(191963843, 68017300), Fraction(252080587, 89175700))
   54   10389     572    4241         3     11.082502      1.000000   1.038777      48.1  adding 1 orbits, deepest at (Fraction(25853703, 25913300), Fraction(50327411, 14250100))
   55   10402     573    4249         2     11.082502      1.000000   1.074809      36.3  adding 1 orbits, deepest at (Fraction(1856407, 657700), Fraction(48473, 17175))
   56   10402     574    4257         1     11.082502      1.000000   1.088273      21.1  adding 1 orbits, deepest at (Fraction(493163, 494300), Fraction(493163, 494300))
   57   10416     575    4261         2     11.082502      1.000000   1.041254      39.6  adding 1 orbits, deepest at (Fraction(661529, 234400), Fraction(87161, 88100))
   58   10469     576    4269         2     11.082502      1.000000   1.051585      28.3  adding 1 orbits, deepest at (Fraction(1373033, 486300), Fraction(147041, 365100))
   59   10469     577    4277         1     11.082502      1.000000   1.034845      13.9  adding 1 orbits, deepest at (Fraction(857699, 303900), Fraction(470071, 473100))
   60   10478     578    4285         2     11.072443      1.000000   1.135310      19.6  adding 1 orbits, deepest at (Fraction(17254920447, 6113780000), Fraction(130028456787840066580078065287, 130931314778435874496056000000))
   61   10480     579    4293         3     11.072443      1.000000   1.030634      25.9  adding 1 orbits, deepest at (Fraction(691703, 693300), Fraction(608809, 609900))
   62   10480     580    4301         1     11.072443      1.000000   1.022061       7.9  adding 1 orbits, deepest at (Fraction(209819, 114650), Fraction(824603, 823300))
   63   10480     581    4309         1     11.072443      1.000000   1.082483      12.7  adding 1 orbits, deepest at (Fraction(24768733, 8776300), Fraction(33675419, 11892150))
   64   10480     582    4317         1     11.072443      1.000000   1.032636       9.8  adding 1 orbits, deepest at (Fraction(28856457717769000055620599, 28923147160855781922260000), Fraction(184270661782261071711388137, 65291367746668010798380000))
   65   10480     583    4325         1     11.072443      1.000000        nan       8.5  no candidate orbit has averaged depth above 1
stopped: converged: every placement covers mass 1
objective: 11.072443466079633
least covered mass: 0.999999999999948
total mass: 553677/50000 = 11.07354
least cell mass: None
atoms: 384
seed sites: 70
frozen: scratchpad/lane-297/run1/candidate.json
seconds: 2080.3
```

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
