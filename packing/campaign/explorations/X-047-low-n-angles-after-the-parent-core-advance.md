---
title: X-047 — low-n angles after the parent-core advance
softschema:
  contract: packing.squares:Exploration/v1
  schema: ../schemas/exploration.schema.yaml
  envelope: exploration
  status: enforced
exploration:
  id: X-047
  title: Low-n Angles After the Parent-Core Advance
  date: '2026-09-23'
  author: Fable at extra-high reasoning (W3 low-n lane); not yet reviewed
  campaign: packing.squares
  brief: >-
    W3 low-n lane of the overnight insight-iteration block. For each open low case other
    than n11 (which another agent owns), find the most creative credible angle to a
    material bound move or a settlement, its first sub-two-hour discriminator with a
    machine-checkable exit, and the distinct lane it belongs to. Specify the shared
    ParentClip and freeze-to-parent-core W7 instrument that several lanes consume, and
    say which angles are dead on arrival. Generate hypotheses; certify nothing; keep
    computation small and bounded. Assign lanes so agents can run them in parallel
    without shared files.
  sources:
  - operating-rules.md
  - packing/campaign/explorations/X-042-what-is-left-at-low-n.md
  - packing/campaign/explorations/X-043-new-lower-bound-proof-directions.md
  - packing/campaign/explorations/X-044-low-n-certificate-transfer.md
  - packing/frontier/n-012.md
  - packing/frontier/n-017.md
  - packing/frontier/n-018.md
  - packing/frontier/n-019.md
  - packing/frontier/n-020.md
  - packing/frontier/n-021.md
  - packing/frontier/n-026.md
  - packing/frontier/n-029.md
  - packing/frontier/RESULTS.md
  - packing/src/sqpack/fractional/colgen.py
  - packing/src/sqpack/fractional/corner_clip.py
  - packing/src/sqpack/fractional/parent_core.py
  - packing/src/sqpack/fractional/parent_core_interval.py
  - packing/src/sqpack/fractional/sweep.py
  - packing/cases/n12_fractional_certificate/certificate.json
  - packing/cases/n20_fractional_certificate/certificate.json
  - packing/cases/n18_fractional_certificate/certificate-4679-1000.json
  - packing/campaign/hypotheses/H-226-n21-one-spare-wall-charge-lemma.md
  - packing/campaign/series/series-000-smoke-and-calibration/results/agenda-040/bentz2016-one-spare-receipt.md
  - packing/resources/papers/bentz-2016-optimal-packings-22-and-33.md
  - packing/resources/papers/bentz-2010-optimal-packings-13-and-46.md
  proposes: [H-240, H-241]
---
# X-047: Low-n Angles After the Parent-Core Advance

**The single most useful fact for triage is where the additive route dies.** Every
retained low-n lower bound is a nonnegative measure charging at least 1 to every
`B`-square placement, with total mass below `n`. Such a measure exists only up to a hard
ceiling, and for four of the five bands that ceiling is a hair above the current bound.
The one exception is **n21**, whose budget sits far enough above its certificate mass
that pure additive covering has real headroom left.
That reorders the night: n21 first on the stock instrument, n12 turned over to a
kill-switch that would close its additive route for good, and the shared parent-core
instrument built to reach the cases where additive is genuinely spent.

This is a W3 exploration.
It proposes hypotheses and lanes; it decides nothing and promotes no bound.
Session 156 codified its selected rows as H-240 and H-241. n11 belongs to X-046.

## The Additive-Ceiling Map

For the fixed shrunk core `B = 9977/10000` the covering value of the unrestricted
program is bounded below by an elementary **grid obstruction** (X-044 §"A fixed-shrink
grid obstruction", X-042 §"Two Findings That Change the Slate"): if `L > kB` the `k^2`
axis-parallel `B`-squares on a small-gap lattice are pairwise disjoint closed sets, so
every additive measure charging each at least 1 has mass at least `k^2`. Once `k^2 >= n`
the additive route cannot certify `s(n)` at all.
This is proved; the strict case `L > kB` is what it needs, and equality wants a boundary
convention.

Below that hard ceiling the covering value climbs continuously toward `k^2` as the side
grows; the additive route dies at the **crossing side** where the value first reaches
`n`. The crossing is not proved — it is estimated here from the retained certificate
masses and X-042’s own measurement that the value is `~19.81` at `4.85` and reaches the
grid `25` at `5B` — but its message is robust: the additive headroom is `current bound`
to `crossing`.

| Case | Verified lower | Grid ceiling `kB` | Est. additive crossing (value = n) | Additive headroom |
| --- | --- | --- | --- | --- |
| n12 | 99/25 = 3.96 | 4B = 3.9908 | ~3.961 (T-017 mass 11.99897) | **~0.001, effectively closed** |
| n18 | 4679/1000 = 4.679 | 5B = 4.9885 | ~4.69 (mass 17.8934) | ~0.01 |
| n19 | 24/5 = 4.80 | 5B = 4.9885 | ~4.81 (mass 18.9200) | ~0.01 |
| n20 | 97/20 = 4.85 | 5B = 4.9885 | ~4.86 | ~0.01 |
| **n21** | 97/20 = 4.85 | 5B = 4.9885 | **~4.886** (mass 19.8487, budget 21) | **~0.036** |
| n26–29 | 5.508 / 5.71 (external density) | 6B = 5.9862 | not first-party reachable near here | see §n26–29 |

The arithmetic behind this table (grid `kB`, the per-target charge slacks of X-044’s
table 5, the linear crossing estimate, and the parent-centre insets below) is recomputed
in `attic/x047/checks.py` and reproduces X-044’s slack figures exactly: n12 loss
`< 0.0167%`, n18 `< 0.593%`, n19 `< 0.421%`, n20 `< 0.757%`, **n21 `< 5.483%`**.

**Why n21 is the outlier (proved-arithmetic, not a bound):** its budget 21 sits
`19.8487` above the same T-021 mass that pins n20’s budget 20 only `0.1513` above it.
The covering value must climb much further to reach 21, so the crossing is much higher,
and the per-parent charge tolerance is `36x` n20’s. n21 is `5^2 - 4`, one count below
the solved n22; that spare unit of allowance is exactly what buys the headroom.

## n12: Additive Is Spent — Turn the Case Over to a Kill and to Structure

Proved: additive dies above `4B = 3.9908`. T-017 already reaches `3.96` with mass
`11.99897`, `~0.0009` below the crossing.
So the additive window is at most `[3.96, 3.9908]` and probably `~0.001` wide.
Two consequences:

- **The kill-switch discriminator (cheap, decisive negative).** Run
  `run_fractional_cutting --n 12 --side 39609/10000 --shrink 9977/10000`, seeded from
  T-017’s atoms, and read `colgen.check_ceiling` (`colgen.py:969`). A depth-one family
  with `total / maxdepth >= 12` proves the covering value is at least 12 at `3.9609`,
  and by monotonicity in `L` at every larger side — killing every additive/point/density
  route to `s(12) > ~3.961`. Machine-checkable exit: `CeilingResult.proved` with
  `feasible_total >= 12`. Falsifier: converged value `< 12`, which would mean additive
  headroom survives and a window-enriched point run should be retried.
  **Not run by this lane; presented as the discriminator, not a result.**
- **Exact four is a structural program, not an additive one.** `s(12) = 4` needs either
  a certificate family at side `4 - eps` with a uniform positive budget gap
  `12*Gamma(eps) - M(eps) >= c*eps^p` (the hard premise is uniform coverage, not the
  arithmetic), or a Bentz-style occupancy count.
  The count route has a known obstruction: n12 is `4^2 - 4`, and the excess `t - n` in
  Bentz’s identity `u + sum(r_i - 1) = t - n` rises to 4 for the 16-point figure-2 set,
  and X-044 exhibits a purely combinatorial allocation of four coincidences among the 16
  points that fills 12 boxes and defeats the counting inference.
  **Cheap discriminator:** enumerate the excess-4 occupancy patterns of the 16-point set
  and test each survivor against an exact parent-footprint / maximal box-diagonal
  (`1.01*sqrt(2)`) constraint; a machine-checkable pass is a single surviving pattern
  that no packing can realize, a machine-checkable fail is one validated legal
  allocation. This is the n12 sibling of the H-226 one-spare inventory and reuses its
  `devtools/bentz2016` scaffolding.

## n17: New Features Against the Frozen Dual, But Retention Is Capped

Proved constraints: the exp-222 mass floor bounds any re-pricing on the frozen support
at fixed `(L, A)` to `+0.0034` in the bound (X-042); the triples are load-bearing
(H-235, least point-only charge `0.741585` vs `0.861183`); and the parent-centre
restriction is load-bearing (exact row-6512 witness).
So the only live headroom is **new columns**, not re-weighting.

- **Angle:** synthesize five-site and weighted threshold features and price their
  reduced cost (X-043 eq.
  4\) against the retained exp-222 dual; a negative reduced cost names a violated valid
  budget. Discriminator (finite, overnight-suitable, X-043 B3): LP primal on a frozen
  common-row set below the matched ordinary-point control dual, both rational.
  Machine-checkable exit: the rational primal/dual gap.
  Falsifier: the old optimal dual survives every synthesized column (X-027’s whole-face
  test), or the realized incidence pattern is geometrically unrealizable.
- **Hard limit that caps the payoff tonight:** the retention gate refuses any input
  above `MAX_INTERVAL_ATOMS = 4096` (`interval.py:145`), and the external n17 measure
  expands to `6744` point atoms (X-042). So even a successful richer-feature certificate
  can only be a **finite LP gain replayable as bytes**, not a gate-retained rung, until
  the boxes-by-atoms mask is chunked.
  X-043’s own token-group spike already found zero budget saving from regrouping the
  existing tokens, so only genuinely new supported features have a chance.

## n18–n19: Microscopic Additive Headroom; ParentClip For More

Additive crossings sit `~0.01` above the current bounds, and the frozen-`B` `L/B`
ceilings (X-044) are `4.6898` (n18) and `4.8111` (n19). A `+0.01` additive rung is
owner-disfavoured as microscopic.
To reach `4.70` (n18) or `4.82` (n19) the core must shrink below `B`: the frozen-weight
transfer is **arithmetically dead** — at the net’s half-step the core reaches
`B*(cos + sin) = 0.99885` past centre, exceeding the shrunk parents
`A = 4679/4700 = 0.99553` (n18) and `240/241 = 0.99585` (n19), so the core pokes out of
the parent and containment fails (recomputed in `attic/x047/checks.py`). The **live**
form is a re-priced clipped LP — the ParentClip instrument below.
n18 is the cleanest producer-calibration case because its verified upper
`(7+sqrt7)/2 = 4.8229` is far away and its recent T-027→T-030 ladder shows the seed
continuation works. Discriminator: a re-priced clipped LP at side `4.70` converting to a
parent-core certificate that `verify_parent_core_rows` accepts.
Exit: `accepted = True` on a complete row inventory with `budget < n * minimum_charge`.
Falsifier: an exact undercharged pose (`exact_parent_charge` rejects the interval
refutation), or incomplete coverage.

## n20–n21: The Real Additive Headroom, and the Exact-Five Question

- **n21, pure additive (top low-n lane).** The estimated crossing is `~4.886`, so a
  window-enriched point certificate could reach roughly `+0.03` on the **stock**
  instrument, no new geometry.
  X-042’s redesigned A3 already diagnoses n20/21 as *site-limited, not
  endpoint-limited*: the `4.855`/`4.86` searches stalled with violated rows because the
  site set missed the near-grid overlap windows, not because the endpoint binds.
  Discriminator: `run_fractional_colgen` at n21, side `4.88`, `B = 9977/10000`,
  window-enriched sites; freeze and run `decide_certificate`. Exit: `RETAINABLE` on a
  freeze of mass below 21. Falsifier: converged value `>= 21` on two site sets, or the
  search returns the grid.
- **n21, ParentClip (larger reach).** Above the crossing, the `5.483%` charge slack is
  the largest on the board.
  At fixed `L = 97/20` the target `S = 4.9` needs `A = 97/98`, and a smaller
  row-dependent core; the clipped re-priced LP is the vehicle.
  This is the ParentClip’s first consumer.
- **Exact five is not tonight-sized but not dead.** n21 is one count below Bentz 2016’s
  n22. The one-spare wall-charge lemma (H-226) was **rejected as stated**: exp-216’s
  inventory leaves `3,461` D2-orbits with at most four charges on every wall line and no
  confined partial box, which the paper’s toolkit cannot close, plus `22,603` orbits
  that need an unproved claim `Q(i, j)`. The creative move is to attack the 3,461 kill
  orbits with a resource the paper does not use — a threshold charge on the finishing
  segment, or a parent-compatibility no-good from the ParentClip’s two-body geometry —
  since those orbits are exactly where “too few charges” survives.
  High payoff (`s(21) = 5`), high risk, days of casework; a bounded first probe is to
  take the largest surviving pattern (`(2,2),(2,3)`, 16,468 raw pairs) and ask whether
  one parent-disjointness inequality removes it.
  n20 is `5^2 - 5`, a strictly worse two-deficit case; treat it as n21’s companion, not
  a separate lane.

## n26–n29: External Density Bounds Are High; Only a Cheap Probe Tonight

The lower bounds here jumped to Tokoharu’s density values `5.508` (n26–28) and `5.71`
(n29). A first-party point or threshold certificate would have to beat those from
Nagamochi’s grid floor — a large jump — and the density-plus-floor hybrid that could do
it (X-043 Direction C, eq.
6\) is an unbuilt instrument.
Upper bounds leave room (`5.62`, `5.71`, `6`, `5.93`), but the room is above bounds
nobody here can currently reproduce first-party.
**These were never tried with the parent-centre restriction or with thresholds**
(brief), so the one cheap, honest tonight-probe is: add the ParentClip to a small n26
point/density family at a side just under `5.508` and measure whether the restriction
buys any charge at all — a calibration of whether the lever does anything at this scale,
not a bound attempt.
Expected value low; include only if a slot is idle.

## The Shared Instrument: ParentClip + Freeze-to-Parent-Core (W7)

Several lanes above need the same two pieces.
The frozen-weight transfer is dead; the covering LP must be **re-priced on the
parent-centre-restricted domain**, then converted to a certificate the n-general
parent-core validators decide.

**ParentClip (a domain predicate, sibling of `CornerClip`).** A frozen dataclass that,
per net direction, insets the centre domain to the axis-aligned square
`[r_k, L - r_k]^2`, with

```
r_k = A * min_{u in row}( cos(u) + sin(u) ) / 2
```

which is exactly `parent_core.ParentCoreRow.centre_margin(A)` (identity checked:
`cos + sin = (1 + 2u - u^2)/(1 + u^2)`). It implements the same interface `CornerClip`
exposes, so it drops in behind the existing `clip` parameter already threaded through
`colgen.py` at `square_excluded` (`:286`), `dual_support` (`:691`–`:718`),
`check_ceiling` (`:975`, `:993`), `solve_rows` (`:498`, `:585`) and `generate_adaptive`
(`:1227`, `:1309`, `:1334`), and through `sweep.centre_domain`. Required methods:
`excludes(x, y, cos, sin)`, `excludes_square(axes, centre, half)`, and
`half_planes`/`clip_polygon` for the sweep.
Its cuts are four **axis-aligned** half-planes (`x >= r_k`, `x <= L - r_k`, and the two
in `y`), simpler than `CornerClip`’s rotated corner cuts, and the domain stays a convex
rational polygon.

**Boundary convention, on purpose.** Copy `CornerClip`’s two-sided discipline: the
`excludes` side (consumed by `dual_support`/`check_ceiling`, which *drop* what is
excluded) keeps the open interior, so dropping only weakens a ceiling; the
`half_planes`/`clip_polygon` side (consumed by the sweep, which *quantifies* Condition
5\) keeps the **closed** inset, retaining the measure-zero boundary band as extra rows
and a strictly harder Condition 5 — the safe direction for a covering program.
A core exactly on the parent boundary is the closed case, and it must be decided, not
tidied away.

**Converter `freeze_to_parent_core`.** Take a colgen freeze (point + threshold atoms)
and the row inventory (contiguous half-tangent intervals, per-row core sides) and
assemble a `ParentCoreCertificate` (`parent_core.py:73`, constructed at `:319`).
Decision is then the existing `validate_parent_core` (`:155`) for the exact premises and
`parent_core_interval.verify_parent_core_rows` (`:154`) for the universal
centre-coverage, which already re-checks every refutation with an exact
`exact_parent_charge` witness.

**Controls (soundness, non-negotiable).**

1. **Regression:** T-017 at side `99/25` must still be accepted after the ParentClip and
   converter are in the path (the clip at that geometry must not spuriously refuse a
   known-good family, and the converter round-trip must preserve its decision).
2. **Refutation:** a *planted* undercharged pose — an atom-poor legal parent whose core
   charge is below `minimum_charge` — must be refuted, with `verify_parent_core_rows`
   returning an exact admissible witness.
   A run that accepts it is a broken instrument.
3. **Closed-boundary:** a core whose centre sits exactly at `r_k` (parent boundary) must
   be decided on the conservative side per consumer, pinned by a test in the shape of
   `test_the_two_kept_sets_differ_exactly_on_the_boundary_band`.

**First runs and consumers.** Order by cost and slack: **n21 at `4.9` first** (largest
slack, `A = 97/98`), then **n12 at `3.97` with the check_ceiling kill run in parallel**
— the kill decides whether additive is dead there while the clipped run tests whether
the restricted domain escapes the grid obstruction (the clip removes wall-adjacent
placements, which can drop the grid ceiling below `n`); then n18 at `4.70` and n19 at
`4.82` as the mid-slack consumers.
Downstream consumers: the n18/n19/n20 producer-calibration lanes and, via its two-body
parent-disjointness output, the n21 exact-five kill-orbit probe.

## Adversarial: What Is Likely Dead on Arrival

- **Frozen-weight transfer at the old nets (rows 216, 219 “as stated”):** dead, proved
  arithmetically. The core exceeds the shrunk parent at the half-step in every case
  checked. Only re-priced live LPs survive.
- **Net-refinement + `dilation_corollary` rungs on T-017/T-030/T-020/T-021:** alive but
  microscopic (`+0.007`–`0.0085`), and for n12 capped by `L/B = 3.9691` below the `3.97`
  target. Owner-disfavoured; keep only as free idle-slot controls, never as a lane.
- **n12 additive above `~3.961`:** dead (grid ceiling proved above `3.9908`; kill-switch
  would sharpen to `~3.961`). Any n12 point/density retry above there is wasted.
- **n17 gate-retained rung tonight:** dead on the `4096`-atom cap; only a finite LP gain
  is reachable. Re-pricing beyond `+0.0034` is dead on the exp-222 floor.
- **n26–n29 first-party bound above the external density values:** effectively dead
  tonight — no instrument reaches it; only a calibration probe is honest.
- **n21 exact-five via the paper’s toolkit unchanged:** dead (H-226 rejected, 3,461
  unclosable orbits). Only a new resource on those orbits is live, and it is not
  tonight-sized.
- **Grid-escape upper-bound annealing at n12/20/21:** measured null and total (X-042);
  not a lower-bound lane and not worth re-running.

## Ranked Top-3 Low-n Lanes for the W6/W7 Loop

n11 lanes take priority; these fill the remaining `<= ~3` concurrent slots.
Ranked by expected information per hour against instruments that exist.

| Rank | Lane | Question | Entry | Discriminator | Machine-checkable exit | Falsifier | Budget | Owned files |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | **n21 pure-additive at 4.88** (W6) | Does a window-enriched point certificate reach mass `< 21` at side `4.88`, above the grid floor and below the estimated crossing? | `run_fractional_colgen --n 21 --side 22/5 --shrink 9977/10000` with window-enriched grids; freeze; `decide_certificate` | `decide_certificate` verdict on the freeze | `RETAINABLE` on mass `< 21` (`+~0.03`) | Converged value `>= 21` on two site sets, or grid returned | 1–2 runs `<= 3600 s` + gate | `attic/x047-n21/`, a candidate JSON under `cases/n21_fractional_certificate/` (coordinator registers) |
| 2 | **n12 additive kill-switch** (W6) | Is the additive route dead at n12 above `~3.961`? | `run_fractional_cutting --n 12 --side 39609/10000 --shrink 9977/10000 --seed-certificate cases/n12_fractional_certificate/certificate.json` | `colgen.check_ceiling` (`colgen.py:969`) | `CeilingResult.proved` with `feasible_total >= 12` | Converged `< 12` after the loop settles | one cutting run + log | `attic/x047-n12/`, run log/state |
| 3 | **ParentClip + converter, first consumer n21 at 4.9** (W7) | Can a re-priced clipped LP convert to a parent-core certificate accepted below `21*Gamma`? | Build `ParentClip` behind colgen’s `clip`; `freeze_to_parent_core`; run clipped colgen at `L=97/20`, `A=97/98` | `parent_core_interval.verify_parent_core_rows` on the frozen certificate | `verify_parent_core_rows(...).accepted == True` on a complete row inventory | A planted or found exact undercharged pose refutes; coverage incomplete; regression control T-017 refuses | instrument build (hours) + first run | new `sqpack/fractional/parent_clip.py`, `devtools/freeze_to_parent_core.py`, their tests, `attic/x047-parentclip/` |

Lanes 1 and 2 have disjoint deliverables (different `n`, different drivers, separate
attic subdirs) and run concurrently on stock instruments; Lane 3 is the enabling W7
build whose first run supersedes Lane 1’s reach if it lands, and whose two-body output
later feeds the n21 exact-five probe.
The n17 richer-feature LP and the n26 calibration probe are held below the cut: n17 for
its retention cap, n26 for absent instrument.

## Candidate Hypotheses (Unnumbered, for Codification)

Each needs the coordinator to freeze target, family and instrument before execution.

- **The n21 additive crossing.** A window-enriched point certificate at side `4.88`,
  `B = 9977/10000`, retains mass `< 21`. *Positive:* `decide_certificate` RETAINABLE.
  *Negative:* value `>= 21` converged on two site sets refutes the site sets, not the
  target.
- **The n12 additive kill.** `check_ceiling` at `3.9609` certifies
  `total/maxdepth >= 12`. *Positive:* closes n12 additive above `~3.961` for good.
  *Negative:* value `< 12` leaves additive headroom and reopens a window-enriched point
  run.
- **The ParentClip escape at n21.** A clipped, re-priced LP at `L=97/20`, `A=97/98`
  converts to a parent-core certificate `verify_parent_core_rows` accepts.
  *Positive:* `s(21) > 4.9` structurally.
  *Negative:* an exact undercharged pose refutes those bytes.
- **The n18 producer rung.** The same clipped LP at side `4.70`, `A = 4679/4700`,
  accepted. *Negative:* an exact defeating pose seeds new columns rather than another
  grid sweep.
- **The n12 excess-4 allocation cut.** Some excess-4 occupancy pattern of the 16-point
  set is refuted by an exact parent-footprint / box-diagonal constraint.
  *Positive:* a single unrealizable survivor is a new cut toward `s(12) = 4`.
  *Negative:* one validated legal allocation refutes that pattern only.
- **The n21 kill-orbit resource.** One parent-disjointness no-good or finishing-segment
  threshold charge removes a largest surviving H-226 kill pattern (e.g. `(2,2),(2,3)`).
  *Negative:* a validated realizable structure leaves the orbit unclosable.

## Expected Information and Limits

**Proved and relied on here:** the grid obstruction (`s(n)` additive dead above `kB`);
the frozen-weight transfer deadness at all three targets (core `> A` at the half-step);
n11’s `L* = 38200/9977` one-body ceiling (X-042, for the additive-vs-structural
dichotomy); X-044’s per-target charge slacks; that the `clip` parameter is already
threaded through colgen and the sweep.
**Conjecture, labelled as such:** every additive-crossing side in the map above (linear
estimate from retained masses and X-042’s two measured points); that window-enriched
sites reach the crossing; that the ParentClip escapes the grid obstruction on the
restricted domain; that new n17 features beat the matched control; that a new resource
closes the n21 kill orbits.

**Limits.** No lane here was run: the kill-switch, the crossing retains, and the
ParentClip build are discriminators, not results.
The crossing sides are estimates and must be frozen before any retain.
The n17 payoff is capped at a finite LP gain by the gate’s `4096`-atom wall until
chunking lands. The n26–29 band has no tonight-sized route.
And a `+0.01` additive rung at n18/19/20 is real but microscopic and owner-disfavoured —
the material low-n moves tonight are n21 (additive then ParentClip) and, as a decisive
negative, the n12 kill.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
