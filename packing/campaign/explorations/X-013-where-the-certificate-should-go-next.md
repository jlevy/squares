---
title: "X-013 — where the certificate should go next"
softschema:
  contract: packing.squares:Exploration/v1
  schema: ../schemas/exploration.schema.yaml
  envelope: exploration
  status: enforced
exploration:
  id: X-013
  title: Where the certificate should go next
  date: '2026-09-04'
  author: Claude (agent), at the owner's request during the agenda-017 continuation
  campaign: packing.squares
  brief: >-
    The owner asked, after a day in which one instrument moved seven registered cases,
    for a deep mathematical strategy session on what to do next, given where movement
    actually happened: what the movements' wildly unequal sizes say about the method,
    what two structural results (a reach ceiling and an independence of n) changed about
    targeting, whether the near-constant fraction of the packing record that three
    certificates land on supports a claim about where to look next, and what it costs to
    test that at the reach table's top-prize cases. This document argues each point,
    states what would falsify it, and proposes three concrete next actions without
    enacting any of them. It adjudicates nothing and promotes nothing.
  sources:
  - packing/campaign/explorations/X-010-two-lanes-two-ladders.md
  - packing/campaign/explorations/X-012-one-chart-four-hundred-inequalities-and-an-order-2m-contradiction.md
  - packing/campaign/schemas/exploration.schema.yaml
  - packing/frontier/CERTIFICATE-REACH.md
  - packing/frontier/results.yaml
  - packing/frontier/RESULTS.md
  - packing/frontier/n-011.md
  - packing/frontier/n-012.md
  - packing/frontier/n-017.md
  - packing/frontier/n-018.md
  - packing/frontier/n-019.md
  - packing/frontier/n-020.md
  - packing/frontier/n-021.md
  - packing/frontier/n-026.md
  - packing/frontier/n-051.md
  - packing/frontier/evidence.yaml
  - packing/campaign/agendas/agenda-017-six-hour-generator-rigidity-ceilings-and-w9-block.md
  - packing/campaign/agendas/agenda-018-ten-hour-continuation-ladders-theorems-and-wave-two.md
  - packing/campaign/agendas/agenda-019-efficiency-first-retarget-and-deep-strategy.md
  - packing/campaign/ledger.md
  - docs/project/handoff-2026-09-04-block-close.md
  - packing/src/sqpack/fractional/certificate.py
  - packing/devtools/render_certificate_reach.py
  - packing/cases/n11_fractional_certificate/certificate.json
  - packing/cases/n12_fractional_certificate/certificate.json
  - packing/cases/n17_fractional_certificate/certificate.json
  - packing/cases/n20_fractional_certificate/certificate.json
  proposes: []
---
# X-013 — Where the Certificate Should Go Next

**Date:** 2026-09-04

**Status:** Strategy session at the owner’s request, following agenda-017’s block.
It adjudicates nothing and promotes nothing: no lower bound is proposed for adoption, no
hypothesis is registered, and no agenda item is amended.
The three proposals at the end argue for or against candidates already on record (BC-190
in agenda-019, and a target choice within BC-192/BC-194’s own instance lists); enacting
any of them is a decision for whoever runs the next block.

**Owns:** the reading of the day’s seven movements, the attainment-ratio argument and
its qualifications, and the cost accounting against the reach table’s top prizes.
The certificates themselves, the reach table, and the ceiling and independence results
are owned by the records this document cites, not by it.

## The Shape of a Day’s Seven Movements

One instrument — `sqpack.fractional`’s weighted fractional unavoidable-set certificate,
decided by an exact event-cell sweep and an independent interval branch-and-bound that
must agree on the value before anything is retained — moved seven registered cases in
one day. `n = 11` rose to `381/100` (1121 atoms, `T-018`), `n = 12` to `99/25` (2097
atoms, `T-017`), `n = 17` and `n = 18` to `459/100` (1184 atoms, `T-019`, which also
reached `n = 19` before a second certificate superseded it there), and `n = 19`, `20`,
`21` to `24/5` (2260 atoms, `T-020`). Every atom count above is read directly from the
retained `certificate.json` files, not from prose.

The movements are wildly unequal, and ranked they run: `n = 11` at `+0.021146`
(narrowest), `n = 21` at `+0.058343`, `n = 17`/`18`/`19` via `T-019` at `+0.0842`,
`n = 12` at `+0.171146`, `n = 20` at `+0.194449`, and `n = 19` via `T-020` at `+0.21` —
“the largest single-case movement in the register,” by `T-020`’s own scoring rationale.
The natural first reading is that the largest movements came from the cases the day
spent the least time on, and the two ends of the ranking support that: `n = 11` is the
case with the longest history in this project’s own record — Stromquist’s bound stood
since 2003, this branch ran two separate attempts at `381/100` before one converged, and
two calibration rungs (`19/5`, `189/50`) were retained below it — and it shows the
smallest movement. `n = 20` and `n = 21` had never had a bound specific to either size
proved by anyone before that day and picked up the second- and third-largest movements
without a single dedicated search round of their own.

But the ranking does not hold as a strict “least time, largest movement” ordering, and
the exception is instructive rather than an inconvenience.
`n = 21`’s movement (`+0.058343`) is the *second-smallest* in the table, despite zero
dedicated attention ever paid to it — smaller than `n = 12`’s, which received a full
seven-rung ladder built that day (`19/5` through `99/25`) and still moved more than
three times as far. What separates them is not effort spent but how loose each case’s
*prior* bound already was relative to the side the day actually reached.
`n = 20` and `n = 21` had carried only Nagamochi’s 2005 closed form,
`min(⌈√N⌉, √(N − 2⌊√N⌋ + 1) + 1)`, whose value climbs toward the next perfect square
from below: `4.4641` at `N = 19`, `4.6055` at `N = 20`, `4.7416` at `N = 21`. `n = 21`’s
prior already sat close to `24/5 = 4.80` for reasons that have nothing to do with this
project — the formula itself tightens as `N` approaches `25` — so its share of the day’s
free ride was small by construction, not by neglect.
`n = 12`’s prior, by contrast, was a monotonicity inheritance from `n = 11`
(`2 + 4/√5 = 3.788854`) that had never been specific to twelve squares at all; once a
dedicated ladder was pointed at it, the gap it closed was the gap nobody had ever tried
to close. And `n = 11` and `n = 17` show the smallest movements of all because what they
displaced was not a generic formula or a borrowed inheritance but *another certificate*
— Stromquist’s own carefully derived bound at `n = 11`, and Massaccesi’s own fractional
certificate, itself only a day old, at `n = 17` — priors that already sat close to what
this method can prove nearby.

The mechanism that makes this possible at all is the second structural fact below: only
one of the five certifying conditions mentions `n`, so a single atom set proves a bound
for *every* integer above its own mass, and `n = 20` and `n = 21` collected their
movements as a pure byproduct of a search that was never aimed at them.
The fact to carry forward is not “the day was fastest where it was laziest” but the
sharper and more useful one: **movement size is set by how stale or how borrowed the
prior bound was, not by how much fresh search time a case received that day** — and the
instrument’s own independence from `n` is what lets a borrowed prior get displaced for
free.

## Two Structural Facts That Changed What a Run Buys

**(a) The ceiling.** `sqpack.fractional.certificate.ceiling_side_for_net` proves that no
certificate of this shape can exist above `⌈√n⌉ / (1 + D)`, where `D` is the largest
half-gap tangent the direction net admits.
The argument is four cheap steps: over that side, a lattice of `⌈√n⌉²` pairwise-disjoint
axis-parallel `B`-squares fits inside the container with room to spare; `Condition 5`
forces each of them to carry mass at least 1 (direction `0` is always in the net); the
total is then at least `⌈√n⌉² ≥ n`; and `Condition 2` forbids a total mass that large.
`s(n) ≤ ⌈√n⌉` holds trivially by grid packing, and this ceiling sits *strictly below*
`⌈√n⌉` — so the method can approach the grid bound and never reach it, and can never
close a case whose true value equals the grid bound.
`n = 12` is exactly such a case: the ceiling there is `3.9908`, strictly below the
conjectured and grid-verified `4`, so no certificate of this shape will ever prove
`s(12) = 4`, however fine the net or the site set.

**(b) Independence of `n`.** Of the five conditions (`Condition 1` through
`Condition 5`), only `Condition 2` — the total mass falls strictly below `n` — mentions
`n` at all; `Condition 1`, `Condition 3`, `Condition 4` and `Condition 5` say nothing
about it, and the covering linear program the search actually solves (minimise total
mass subject to every admissible `B`-square carrying mass at least 1) does not contain
`n` either. It is a question about `L`, `B`, and the net alone.
So one atom set proves `s(n) ≥ L` for every integer `n` above its own mass, not only the
one its record happens to name, and a larger `n` is strictly easier to certify at the
same side. This is the exact mechanism behind `n = 20` and `n = 21`’s free ride above,
and it is why `T-019`’s 1184 atoms reached `n = 17`, `18` and `19` without a
monotonicity step.

Together these say the program’s *cost* is a function of the side alone — more atoms,
more row-generation rounds, a quadratic-time exact sweep as the certificate grows — and
its *payoff* is a function of which registered cases happen to sit above the achieved
mass at that side.
Those two choices are almost independent, which is exactly why a day’s
movements can look as uneven as they do: the side chosen sets the cost, and the roster
of cases it happens to clear sets the payoff, and neither one was optimised against the
other before this day.

## The Attainment Ratio: What It Supports and What It Doesn’t

Restrict attention to the three retained certificates whose binding constraint is the
best known *packing* rather than the method’s own ceiling.
Using each case’s exact algebraic upper bound:

| `n` | certified side | best known packing (exact) | ratio |
| ---: | ---: | --- | ---: |
| 11 | `381/100 = 3.81` | `3.87708359002281417730789706010096` (Trump 1979, degree 8) | `0.982697` |
| 17 | `459/100 = 4.59` | `4.6755300936045509516…` (Bidwell 1998, degree 18) | `0.981707` |
| 19 | `24/5 = 4.80` | `4.88561808316412673173558496561293` (Wainwright 1979) | `0.982475` |

All three ratios were recomputed here directly from the certified fraction and the
recorded exact upper bound, not copied from a rendered table.
They land inside a band **`[0.98171, 0.98270]`, width `0.00099`, mean `0.98229`** — a
spread narrower than one part in a thousand across three independent, exactly-decided
certificates at three different sizes.

Two cases are deliberately excluded, and the record states why.
`n = 12`’s own ratio (`0.99228`) is measured against the method’s *ceiling* (`3.9908`),
not the packing (`4.0000`), because the ceiling sits below the packing there — a
different quantity entirely, and mixing it into the same band would compare a structural
limit against a construction record.
`n = 20` and `n = 21` share `n = 19`’s exact certificate rather than being independently
searched, and their nominal “best packing” is the trivial grid (`5.0000`), not a genuine
record; a ratio against it would restate `n = 19`’s ratio under a different name rather
than add information.

**What this does and does not support.** It does not support a claimed bound anywhere:
no value of `s(n)` beyond what is already certified is asserted by this section.
What it does supply is a testable prior for where a run is worth starting — three
independently derived, exactly decided numbers agreeing to within `0.001` is a real
regularity, even though a sample of three cannot be called a rate.

**The stopped-on-cost qualification, stated as precisely as the record supports it.**
`T-018` (`n = 11`, `381/100`) ran its row-generation loop to its own natural end: three
row rounds, `25,318` rows, final oracle least covered mass exactly `1`, accepted at
every direction. That is an explicit, unambiguous convergence, recorded in
`results.yaml`’s own account of the two attempts made at that side.
`T-020` (`n = 19`, `21`, `24/5`) is just as explicit in the other direction: its own
`next_rung` field states plainly that the column generation “was halted at round 9 with
a restricted optimum of 18.916941, because four more rounds would have cost about 3.75 h
to buy margin nothing needed.”
That is a certificate whose search was stopped for its cost, not for its answer.
`T-019` (`n = 17`, `459/100`) is the one case where the record does not narrate its own
build’s stopping condition the way it does for the other two; what *is* explicit is that
the very next side attempted for the same case family — `4.68`, targeting `n = 18` — was
abandoned after `7056` s and `157` rows of a round that never moved the restricted
optimum off `18.000000`, with the record stating outright that “the run was stopped for
its cost rather than for its answer.”
`CERTIFICATE-REACH.md`’s own generated text reads this pattern as two of the three
retained runs halted on projected cost and one run to a converged optimum; that reading
is fully supported for `T-020`, directly contradicted for `T-018`, and supported for
`T-019` only indirectly — by the abandoned probe one side above it, and by the fact that
`T-019`’s own margin (`0.066920` below seventeen) sits an order of magnitude looser than
`n = 12`’s fully-converged `0.001040`, and much closer to `T-020`’s admittedly
unconverged `0.077380`. The more cautious statement, and the one adopted here, is: **at
least one of the three runs behind the `0.982` band is confirmed to have stopped on cost
rather than on convergence, at most one is confirmed to have converged, and the third’s
status is inferred rather than narrated.** A ratio built even partly from where searches
were stopped, rather than entirely from where they could go, is not a rate to spend a
rung’s confidence on.

**What observation would separate the two readings.** Run a column-generation search at
a side outside the current `3.8`–`4.8` band and carry it to its own natural stopping
condition — no violated placement remaining, not a wall-clock budget — rather than
halting it once a target margin is cleared.
If that fully converged ratio still lands in or near `[0.98171, 0.98270]`, the band is a
property of the covering geometry and not of this project’s patience.
If it lands well below, the band above was inflated by early stopping, and the
observation was measuring where the project stops, not where the method reaches.

## Where the Ratio Points

Applying the mean ratio (`0.98229`) to the reach table’s seven top-prize cases —
`n = 51, 68, 84, 39, 86, 66, 38`, ranked by prize in that order — and capping each at
its own ceiling, `CERTIFICATE-REACH.md`’s own generated “Ranked by predicted gain” table
gives:

| `n` | lower (Nagamochi) | best packing | ceiling | predicted side | predicted gain |
| ---: | ---: | ---: | ---: | ---: | ---: |
| 51 | 7.1644 | 7.7008 | 7.9816 | 7.5644 | +0.4000 |
| 39 | 6.2915 | 6.8107 | 6.9839 | 6.6901 | +0.3986 |
| 38 | 6.1962 | 6.7071 | 6.9839 | 6.5883 | +0.3922 |
| 68 | 8.2801 | 8.8034 | 8.9793 | 8.6475 | +0.3674 |
| 66 | 8.1414 | 8.6569 | 8.9793 | 8.5036 | +0.3621 |
| 84 | 9.1854 | 9.7071 | 9.9770 | 9.5352 | +0.3499 |
| 86 | 9.3066 | 9.8229 | 9.9770 | 9.6489 | +0.3423 |

Every predicted gain (`0.34`–`0.40`) is bigger than the largest movement seen so far
(`+0.21`, `n = 19`), by roughly `1.6×` to `1.9×` — an attractive number, and one this
section now prices.

**The cost objection, stated quantitatively.** Atom counts grow with the container’s
area, at least as a first approximation: the four existing certificates give
`atoms / side²` of `77.2` (`n = 11`), `133.7` (`n = 12`), `56.2` (`n = 17`) and `98.1`
(`n = 20`) — already a `2.4×` spread inside the tiny `3.81`–`4.80` band, which is the
first caveat on everything that follows.
Using it anyway as an order-of-magnitude heuristic: a run at the predicted side for
`n = 51` (`7.5644`) against `n = 20`’s `4.80` baseline is `(7.5644 / 4.80)² ≈ 2.48`
times the atoms — matching the `≈2.4` a side of `~7.5` gives by the same reasoning.
The retention gate’s own exact sweep is measured, from three paired runs on frozen
bytes, at `atoms^2.00` over the range `1184` to `2260` atoms (`1473 s`, `4866 s`,
`5378 s`); combined with an area-scaling atom count, that implies a *time* cost scaling
as roughly `side⁴`. Carried across all seven cases:

| `n` | predicted side | side ÷ 4.80 | atoms × | est. atoms | gate time × | gate time (h) |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 38 | 6.5883 | 1.373 | 1.88 | ~4,260 | 3.55 | 5.3 |
| 39 | 6.6901 | 1.394 | 1.94 | ~4,390 | 3.77 | 5.6 |
| 66 | 8.5036 | 1.772 | 3.14 | ~7,090 | 9.85 | 14.7 |
| 68 | 8.6475 | 1.802 | 3.25 | ~7,340 | 10.53 | 15.7 |
| 51 | 7.5644 | 1.576 | 2.48 | ~5,610 | 6.17 | 9.2 |
| 84 | 9.5352 | 1.986 | 3.95 | ~8,920 | 15.57 | 23.3 |
| 86 | 9.6489 | 2.010 | 4.04 | ~9,130 | 16.33 | 24.4 |

This is only the *one-time* retention-gate cost of deciding a single frozen candidate —
and given the `2.4×` variance already observed in `atoms / side²` inside the existing
band, the honest range for `n = 51` is closer to “four to twenty-some hours of gate time
alone” than a single point estimate.
It is also not the dominant cost of a whole run: row generation, not the exact sweep, is
`79%`–`94%` of every measured round (agenda-019’s own `BC-191` baseline), and it has
never been measured as a function of side at all.
The one existing case study of what an untuned parameter does at a larger side is not
reassuring: at `n = 20`’s own `4.80`, one site-grid choice cost over `3300 s` without
finishing round `0`, where a better-tuned grid finished the same round in `376 s` — an
`8.8×` factor from a single constant, found by accident.

*Note, later the same day.* The gate-time column above was computed from the `Fraction`
sweep, and that sweep has since been replaced at the gate by an integer one that returns
the same verdicts at `68×` and `139×` on the two largest certificates (`21.8 s` and
`38.7 s` against `1473 s` and `5378 s`). Divide the column by roughly a hundred.
The argument of this section does not change, because its second half never rested on
the gate: row generation and the untuned-grid `8.8×` are untouched, and `BC-191` is
still what has to land first.

**What has to be true before a run at the top of the reach table is worth starting.**
Two things, and both are already registered rather than newly proposed here.
First, `BC-190`’s move — decide accept/reject inside the search with the linear-scaling
interval route, keep the quadratic exact sweep only at the final retention gate — has to
be adopted and verified equivalence-safe; today the exact sweep sits inside the
generator’s own loop, so every *rejected* trial along the way pays the same tax the
final retained candidate does, at a side where that tax alone is measured in hours.
Second, `BC-191`’s site-density-as-a-function-of-container-side rule has to exist and be
applied, because the one clean lesson available — the `8.8×` cost of an untuned grid at
`n = 20`’s own side — already dwarfs anything the `atoms^2.00` fit predicts on its own.
Neither is optional, and both already gate `BC-194` by name in agenda-019.

## Three Proposals, Each With a Falsifier

**1. Adopt `BC-190` — argued on the numbers, not restated.** The interval route decides
*more* (`361` doubled-net directions against the exact sweep’s `181`) with *fewer*
hypotheses (it never needs `Condition 1`, since deciding on the doubled net never
invokes the `D4` reflection), and it is already `22.7×`–`44.2×` faster on the two atom
counts paired so far — a gap that *widens* as certificates grow (`atoms^2.00` against
`atoms^0.92`), which is exactly the direction the top-prize cases push the search.
The correctness argument is untouched: nothing is retained unless both routes agree on
the value, so the change moves what pays the quadratic tax on every rejected trial, not
what is finally trusted.
**Falsifier:** if the block that re-fits both exponents at two further atom counts finds
the interval route’s own exponent drifting toward quadratic rather than holding near
`0.92`, the entire argument — that the two routes scale differently — weakens in
proportion, and the case for moving the decision out of the exact sweep goes with it.
A second, harder falsifier is already built into the design: any single disagreement
between the two routes during equivalence-guard testing kills the change outright,
independent of speed.

**2. Point the next search at `n = 26`, side `5.5218` — not `n = 51` despite its higher
raw prize.** `n = 26`’s predicted gain (`+0.3987`) is statistically indistinguishable
from `n = 51`’s (`+0.4000`) and `n = 39`’s (`+0.3986`) — all three sit in a near-tie at
the top of the seven-case ranking — yet `n = 26` costs an estimated `1.32×` the atoms
and roughly `1.75×` the retention-gate exact-sweep time of `n = 20`’s already-run `4.80`
baseline (about `2.6 h`), against `n = 51`’s estimated `2.48×` atoms and `6.17×` gate
time (`~9.2 h`, plausibly `4`–`22 h` given the observed variance).
`n = 26` is also already on this agenda’s own candidate list — both `BC-192` and
`BC-194` name it first among their instances — so this is a sharpening of the existing
plan by its own numbers, not a new direction.
**Falsifier:** if a column-generation run at `5.52`, carried to genuine convergence
rather than halted on a wall-clock budget, reaches a restricted optimum requiring mass
above `26` (no certificate possible at that side at all) or lands its achieved ratio
well below the `0.98` band — say below `0.90` — that is direct evidence the `0.982`
ratio does not survive outside the narrow band it was measured in, and the correct
response is to abandon reach-table climbing in favour of further rungs on the cases
already proven to respond (`n = 11`, `n = 12`, `n = 17`).

**3. Measure the covering value’s growth in the side — the one measurement that would
most change the picture.** Six restricted optima have been measured, and each is
confirmed here against its source: `11.0000` at `3.82` (a grid-built site set converged
fully; a certificate-seeded set stood at the same value through 24 rounds without
exhausting its row loop); `11.9706` at `3.95` (the retained `79/20` certificate’s own
mass, `1197059/100000`); `11.9936` at `3.96` (the value the `99/25` search converged
toward before rationalisation lifted it to the certificate’s `149987/12500 = 11.998960`,
a difference consistent with the documented rounding-up rule); `16.9628` at `4.58`
(converged, `n = 17`); `18.0000` at `4.68` (three site sets in succession, all
plateauing at the same value, with the search explicitly stopped before separating
“covering value at or above eighteen” from “site set still short of it”); and
`18.916941` at `4.80` (the `T-020` build, explicitly halted at round 9 rather than
converged). Two of the six are therefore *not* converged and stand as upper bounds only.
All six cluster in a side-band of width `0.98` (`3.82` to `4.80`), while every predicted
target among the seven top-prize cases sits between `6.59` and `9.65` — outside that
band by a margin wider than the band itself.
A genuinely converged seventh point anywhere past `~5.5` (which proposal 2’s run would
supply) would be the first data this project has ever had about the covering value’s
behaviour outside a narrow cluster, and it would settle what the six cannot: whether
growth stays consistent with the loosely quadratic shape the four converged points
suggest, or departs from it before reaching the sides the top prizes need.
No curve is fit here past what six clustered points — two of them unconverged — can
support; that fit was already offered once, in this repository’s own generated table,
with its caveat attached, and nothing here tightens it.

## If This Argument Is Wrong

The strongest case against going large is that the covering value’s true growth rate in
the side is faster than the container’s area — faster than the roughly quadratic shape
the four converged points are loosely consistent with.
If so, the `0.982` ratio observed in the narrow `3.8`–`4.8` band is a coincidence of
that band rather than a stable fraction of the packing, and it would collapse well
before reaching the sides the reach table’s top prizes occupy.

Where this would show up, roughly in order of how early it would be visible:

First, in the finite-difference rate already implicit in the six existing points.
From `3.82` to `3.96` the converged covering value rises at roughly `7.1` mass per unit
side; from `3.96` to `4.58`, roughly `8.0`; the interval to `4.80` — using the
unconverged `18.92`, itself an overestimate since further rounds could only lower it —
is at most `8.9`. That sequence is not falling.
A genuinely converged run at `n = 26`’s side (the seventh point proposal 3 asks for)
landing on a rate meaningfully above roughly `9`–`10` mass per unit side would be the
first quantitative sign of acceleration rather than a flat or slowing one.

Second, and most directly, in the sign of proposal 2’s own outcome.
A restricted optimum at `5.52` that comes in *above* `26` — rather than safely below it,
the way `n = 11`’s converged run landed exactly at its wall, `11.000000`, with room
under `12` left unused — is the clearest possible signature, because it says the method
cannot clear the mass bar at the side the current ratio predicts, independent of how
much further budget a later round might need.

Third, structurally, in whether the fixed net and site machinery even generalise.
The shrink margin `B(1+D) < 1` is set by the net alone and does not change with the
side, but the row-generation search has only ever explored inside the narrow band, and
`BC-191`’s own finding — that a fixed site *count* thins out relative to the growing
`B`-square as the side grows, costing `8.8×` on one already-observed step near `4.80` —
is itself a small instance of exactly this worry, measured on the search’s efficiency
rather than on the true covering value.
If the same thinning affects not just how long the search takes but whether it can find
a small enough covering at all, a search that is merely too slow to finish and a
covering value that has genuinely grown past reach become difficult to distinguish from
the outside. That is precisely why proposal 2’s run needs to be pushed to its own
convergence rather than stopped on a clock, the way two of today’s three were.

## What This Document Does Not Establish

No new lower bound is proved, proposed for adoption, or estimated as anything more than
a clearly labelled extrapolation.
No hypothesis is registered and no agenda item is amended: the three proposals argue for
and against candidates already on record, and enacting any of them is a decision for
whoever runs the next block.
The `0.982` ratio rests on three points, one of them (`n = 11`) confirmed run to its own
convergence and at least one other (`n = 19`, via `T-020`) confirmed stopped on
projected cost; nothing here treats it as more than a place to look, and the
predicted-gain table built from it, and every cost estimate built on top of that,
inherits the same qualification at every row.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
