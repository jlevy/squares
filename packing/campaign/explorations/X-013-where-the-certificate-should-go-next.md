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
    The owner asked, after a day in which one instrument moved seven registered cases
    through eight result transitions, for a deep mathematical strategy session on what
    to do next, given where movement
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

**Owns:** the reading of the day’s seven cases and eight transitions, the
attainment-ratio argument and its qualifications, and the cost accounting against the
reach table’s top prizes.
The certificates themselves, the reach table, and the ceiling and independence results
are owned by the records this document cites, not by it.

## The Shape of Seven Cases and Eight Transitions

One instrument — `sqpack.fractional`’s weighted fractional unavoidable-set certificate,
decided by an exact event-cell sweep and a method-distinct interval branch-and-bound
that must agree on the value before anything is retained — moved seven registered cases
through eight immediate result transitions in one day.
`n = 11` rose to `381/100` (1121 atoms, `T-018`), `n = 12` to `99/25` (2097 atoms,
`T-017`), `n = 17` and `n = 18` to `459/100` (1184 atoms, `T-019`, which also reached
`n = 19` before a second certificate superseded it there), and `n = 19`, `20`, `21` to
`24/5` (2260 atoms, `T-020`). Every atom count above is read directly from the retained
`certificate.json` files, not from prose.
There are eight transitions because `n = 19` first moved with `T-019` and then moved
again with `T-020`.

The movements are unequal, and ranked they run: `n = 11` at `+0.021146` (narrowest),
`n = 21` at `+0.058343`, `n = 17`/`18`/`19` via `T-019` at `+0.0842`, `n = 12` at
`+0.171146`, `n = 20` at `+0.194449`, and `n = 19` via `T-020` at `+0.21`. These are
movements from the verified register immediately before each result.
They do not make `+0.21` the register-wide record: `T-001` moved `n = 17` by about
`0.263935`. The raw ordering invites the idea that less search time produced larger
movements, but the evidence does not sustain that causal reading.
At `n = 11`, one of the oldest baselines in this register — Stromquist’s bound stood
since 2003, this branch ran two separate attempts at `381/100` before one converged, and
an earlier improving rung (`19/5`) and a calibration rung (`189/50`) were retained below
it — and it shows the smallest movement.
`T-020` was generated specifically for `n = 20`; its mass below 19 moved `n = 19`
directly, while `n = 21` was the untargeted byproduct.
Friedman’s 2000 DS7 survey had already listed `6√2 − 4` for the grouped `n = 19`–`20`
row and about `4.7438` for `n = 21`; those older reports were not independently replayed
here.

But the ranking does not hold as a strict “least time, largest movement” ordering, and
the exception is instructive rather than an inconvenience.
`n = 21`’s movement (`+0.058343`) is the *second-smallest* in the table, despite zero
dedicated attention ever paid to it — smaller than `n = 12`’s, which received a full
eight-rung ladder built that day (`19/5` through `99/25`) and still moved more than
three times as far. What separates them is not effort spent but how loose each case’s
*prior* bound already was relative to the side the day actually reached.
The verified register at `n = 20` and `n = 21` had carried Nagamochi’s 2005 closed form,
`min(⌈√N⌉, √(N − 2⌊√N⌋ + 1) + 1)`, whose value climbs toward the next perfect square
from below: `4.6055` at `N = 20` and `4.7416` at `N = 21`. At `n = 21`, DS7’s stronger
reported value of about `4.7438` was also already close to `24/5 = 4.80`. The formula
itself tightens as `N` approaches `25`, so this case’s improvement was small by
construction, not by neglect.
`n = 12`’s prior, by contrast, was a monotonicity inheritance from `n = 11`
(`2 + 4/√5 = 3.788854`) that was not specific to twelve squares; once a dedicated ladder
was pointed at it, it closed a gap for which the retained record had no dedicated lower
bound. The narrow `n = 11` movement and the comparatively small `n = 17` movement
displaced stronger case-specific priors: this repository’s repaired certificate for
Stromquist’s stated value at `n = 11`, and Massaccesi’s fractional certificate, newly
adopted here at `n = 17`. Those priors already sat close to what this implementation
proved nearby.

The mechanism that makes this possible at all is the second structural fact below: only
one of the five certifying conditions mentions `n`, so a single atom set proves a bound
for *every* integer above its own mass.
That is why a run aimed at `n = 20` moved `n = 19` directly and gave `n = 21` the same
bound without another search.
The small sample is consistent with a useful hypothesis: prior-bound looseness explains
the movement sizes better than dedicated search time does.
The instrument’s independence from `n` is what lets one search test that hypothesis
across several cases.

## Two Structural Facts That Changed What a Run Buys

**(a) The fixed-net ceiling.** `sqpack.fractional.certificate.ceiling_side_for_net`
proves that no certificate on one fixed finite direction net can exist above
`⌈√n⌉ / (1 + D)`, where `D` is the largest half-gap tangent that net admits.
The argument is four cheap steps: over that side, a lattice of `⌈√n⌉²` pairwise-disjoint
axis-parallel `B`-squares fits inside the container with room to spare; **Condition 5**
forces each of them to carry mass at least 1 (direction `0` is always in the net); the
total is then at least `⌈√n⌉² ≥ n`; and **Condition 2** forbids a total mass that large.
`s(n) ≤ ⌈√n⌉` holds trivially by grid packing, and every finite-net ceiling sits
*strictly below* `⌈√n⌉`. A single finite certificate therefore cannot attain the grid
endpoint. This does not rule out a proved family on successively finer nets whose sides
tend to the endpoint, followed by a separate limit argument.
For the current 181-direction net at `n = 12`, the ceiling is `3.9908`, below the
conjectured and grid-verified `4`; this net cannot supply a single endpoint certificate,
but the whole method is not thereby foreclosed.

**(b) Independence of `n`.** Of the five conditions, only **Condition 2** — the total
mass falls strictly below `n` — mentions `n` at all; **Conditions 1 and 3–5** say
nothing about it, and the covering linear program the search actually solves (minimise
total mass subject to every admissible `B`-square carrying mass at least 1) does not
contain `n` either. It is a question about `L`, `B`, and the net alone.
So one atom set proves `s(n) ≥ L` for every integer `n` above its own mass, not only the
one its record happens to name.
As `n` increases, **Condition 2** becomes strictly weaker; the other feasibility
conditions remain unchanged.
This is the exact mechanism behind the `n = 20`-targeted run’s direct reach to `n = 19`
and its untargeted carry to `n = 21`, and it is why `T-019`’s 1184 atoms reached
`n = 17`, `18` and `19` without a monotonicity step.

Together these separate the mathematical payoff from the computational bill.
At fixed `L`, `B`, net, and site universe, the covering program does not depend on `n`;
the cases above the achieved mass determine the payoff.
Cost is not a function of side alone: it also depends on the net and site grids, the
atoms produced, rationalisation, implementation, machine, and load.
Side is one scale variable among those inputs, and the measurements below are too sparse
to isolate its effect.

## The Attainment Ratio: What It Supports and What It Doesn’t

Restrict attention to the three retained certificates whose binding constraint is the
best known *packing* rather than the method’s own ceiling.
Using each case’s recorded best-packing value:

| `n` | certified side | recorded best packing | ratio |
| ---: | ---: | --- | ---: |
| 11 | `381/100 = 3.81` | `3.87708359002281417730789706010096` (Trump 1979, degree 8) | `0.982697` |
| 17 | `459/100 = 4.59` | `4.6755300936045509516…` (Bidwell 1998, degree 18) | `0.981707` |
| 19 | `24/5 = 4.80` | `4.88561808316412673173558496561293` (Wainwright 1979) | `0.982475` |

All three ratios were recomputed here directly from the certified fraction and the
recorded best-packing value, not copied from a rendered table.
They land inside a band **`[0.98171, 0.98270]`, width `0.00099`, mean `0.98229`** — a
spread narrower than one part in a thousand across three distinct certificates whose
sides were each decided exactly.
They share the same theorem, representation, generator, and premises; only the exact and
interval decision routes are method-distinct.

Three registered cases are deliberately excluded, for two reasons.
`n = 12`’s own ratio (`0.99228`) is measured against the method’s *ceiling* (`3.9908`),
not the packing (`4.0000`), because the ceiling sits below the packing there — a
different quantity entirely, and mixing it into the same band would compare a structural
limit against a construction record.
`n = 20` and `n = 21` share `n = 19`’s certificate, so they add no new certificate
observation; their denominator is also the trivial grid (`5.0000`), unlike the
case-specific packings used above.
Their common ratio would be `4.8/5 = 0.96`, a different number that answers a different
question.

**What this does and does not support.** It does not support a claimed bound anywhere:
no value of `s(n)` beyond what is already certified is asserted by this section.
What it does supply is a testable prior for where a run is worth starting: three
distinct retained artifacts produce ratios agreeing to within `0.001`. That is a
regularity worth testing, not an independently replicated rate.

**The stopped-on-cost qualification, stated as precisely as the record supports it.**
For `T-018` (`n = 11`, `381/100`), the result narrative reports that one finite-site
row-generation loop ended after three row rounds and `25,318` rows, with final oracle
least covered mass exactly `1` at every direction.
No raw run or checkpoint survives.
The `n = 20`-targeted build behind `T-020` (`n = 19`–`21`, `24/5`) carries an operator
report in the other direction: column generation stopped at round 9 with a reported
restricted optimum of `18.916941`, because four further rounds were projected to cost
about `3.75 h`. No raw run or checkpoint is retained for that statement.
The frozen certificate’s feasible mass, `18.922620`, is replayable; the stop reason,
restricted optimum, and projection are not.
`T-019` (`n = 17`, `459/100`) is the one case where the record does not narrate its own
build’s stopping condition the way it does for the other two; what *is* explicit is that
the very next side attempted for the same case family — `4.68`, targeting `n = 18` — was
abandoned after `7056` s and `157` row-generation rounds; the row set grew from 15,888
to 27,516 while the restricted optimum remained `18.000000`. The record states that the
run was stopped for its cost rather than for its answer.
An earlier generated paragraph read this pattern as two cost stops and one converged
run. The sources support a narrower statement: one `n = 11` finite-site row loop is
reported as converged, the `n = 20`-targeted build has a qualified operator report of a
cost stop, and `n = 17` has no recorded stop reason for the measured build.
`D-481` records and corrects that drift.
A ratio built partly from where a search may have stopped, rather than entirely from
what a better search may reach, is not a rate to spend a rung’s confidence on.

**What observation would separate the two readings.** Run column generation at a side
outside the current `3.8`–`4.8` band on prospectively fixed, increasingly dense
atom-site sets.
Carry each row loop to its own stopping condition — no violated placement
remaining, not a wall-clock budget — and retain the raw runs.
If the resulting feasible ratios remain near `[0.98171, 0.98270]` as the site sets are
refined, the evidence for a geometric regularity strengthens.
If they land well below, the existing band was at least partly an artifact of search
choices or stopping.
Even a converged finite-site run measures only that restricted program; a method-wide
limit would require a valid dual bound over all atom positions or a separate theorem.

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

Every predicted gain (`0.34`–`0.40`) is larger than the register’s largest prior
single-case movement (`T-001` at about `+0.263935`), by roughly `1.3×` to `1.5×`. These
remain extrapolated prizes, not achieved movements.

**The cost objection, stated as far as the evidence permits.** A simple area heuristic
predicts more atoms at larger sides, but the four retained certificates already range
from `56.2` to `133.7` atoms per unit area — a `2.4×` spread inside the narrow
`3.81`–`4.80` band. The heuristic can rank rough scale; it cannot price a run.

The historical exact sweep has three unretained operator reports: `1473 s` at 1184
atoms, `4866 s` at 2097, and `5378 s` at 2260. Their least-squares log-log exponent is
`2.04`; `2.00` is only the endpoint slope.
The gate has since been rewritten with exact integer arithmetic, span geometry, and a
bounded process pool.
Pre-integration operator reports gave `21.8 s` at 1184 atoms and `38.7 s` or `29.4 s` at
2260, but those runs lack raw timing and environment records and predate the integrated
worker-memory cap. They do not justify dividing projected costs by a fixed speedup, and
the current implementation has no retained benchmark.

Search cost is less settled still.
Operator reports put row generation at `79%`–`94%` of measured rounds, but no retained
end-to-end comparison establishes what now dominates or how cost changes with side.
One site-grid choice at side `4.80` reportedly ran for over `3300 s` without finishing
round 0, while another finished in `376 s`; that single `8.8×` contrast is a warning
about tuning, not a cost law.

**What has to be true before a run at the top of the reach table is worth starting.**
Two things, and both are already registered rather than newly proposed here.
First, `BC-190` must compare the current integer sweep with the interval route inside
the generator; old interval-to-Fraction ratios do not answer that question.
Retention must continue to require both method-distinct decisions, regardless of which
route is used in the search loop.
Second, `BC-191`’s site-density-as-a-function-of-container-side rule has to exist and be
applied, because the one clean lesson available — the `8.8×` cost of an untuned grid at
`n = 20`’s own side — makes untuned extrapolation unsafe.
Both measurements already gate `BC-194` by name in agenda-019.

## Three Proposals, Each With a Falsifier

**1. Re-run `BC-190` against the current baseline.** The interval route decides *more*
(`361` doubled-net directions against the exact sweep’s `181`) with *fewer* hypotheses
(it never needs **Condition 1**, since deciding on the doubled net never invokes the
`D4` reflection). The three largest historical operator-reported pairs give speed ratios
of `22.7×`, `44.2×`, and `31.1×` against the former Fraction sweep at 1184, 2097, and
2260 atoms; they are nonmonotone and lack raw timing or load records.
A three-point log-log fit gives exponents near `2.04` for the exact route and `1.29` for
the interval route; the earlier `0.92` interval figure was only the 1184-to-2097
two-point slope. None is an asymptotic law.
They do not compare the interval route with the current integer sweep.
The correctness argument is unchanged: nothing is retained unless both method-distinct
routes agree on the value.
**Falsifier:** if reproduced, controlled end-to-end runs show that using the interval
decision in the inner loop does not reduce elapsed search time, the operational case for
the change fails regardless of these sparse fits.
A second, harder falsifier is already built into the design: any single disagreement
between the two routes during equivalence-guard testing kills the change outright,
independent of speed.

**2. Point the next search at `n = 26`, side `5.5218` — not `n = 51` despite its higher
raw prize.** `n = 26`’s predicted gain (`+0.3987`) differs numerically by only `0.0013`
from `n = 51`’s (`+0.4000`) and by `0.0001` from `n = 39`’s (`+0.3986`) — a near-tie in
the top of the full predicted-gain table.
Its predicted side, `5.5218`, is the smallest among those near-tied candidates, so the
area heuristic makes it the least ambitious first test.
No retained cost model establishes its atom count, gate time, or full-run cost; `BC-190`
and `BC-191` must do that before the run starts.
`n = 26` is also already on this agenda’s own candidate list — both `BC-192` and
`BC-194` name it first among their instances — so this is a sharpening of the existing
plan by its own numbers, not a new direction.
**Falsifier:** if prospectively fixed, increasingly dense site universes at `5.52`
converge to restricted optima above `26`, or the best retained feasible certificate
lands well below a `0.90` attainment ratio, that is evidence that this search
architecture does not carry the `0.982` observation outside its narrow band.
A finite-site optimum above `26` refutes only that site universe, not the existence of a
certificate on other sites; the operational response would be to stop climbing until a
better site model exists.

**3. Measure restricted-program growth in the side — the measurement that would most
change the picture.** Seven side-level program values survive in repository narrative,
but their evidential status differs.
The reports are `11.0000` at `3.82`, `11.9706` at `3.95`, `11.9936` at `3.96`, `16.9628`
at `4.58`, `16.9303` at `4.59`, `18.0000` at `4.68`, and `18.916941` at `4.80`. No raw
run is retained for these objective values.
Frozen certificates at `3.95` and `4.80` recompute feasible masses of `11.97059` and
`18.922620`, not optima; frozen candidates at `3.96`, `4.58`, and `4.59` corroborate
scale with different feasible masses.
The result narratives report convergence at `3.82`, `3.96`, and `4.58`, a plateau
without convergence at `4.68`, and a cost stop at `4.80`; the `4.59` stop reason is
unrecorded. None of those execution histories is independently replayable.
All seven cluster in a side-band of width `0.98` (`3.82` to `4.80`), while every
predicted target among the seven top-prize cases sits between `6.59` and `9.65` —
outside that band by a margin wider than the band itself.
A genuinely converged eighth restricted-program point anywhere past `~5.5` (which
proposal 2’s run would supply) would be the first retained raw measurement outside this
narrow cluster. It would test, but not settle, whether the chosen finite-site programs
exhibit any coherent trend outside the current band.
No curve is fit here past what seven clustered and incompletely retained reports can
support; the generated reach table presents that limitation directly.

## If This Argument Is Wrong

The strongest case against going large is that the `0.982` ratio is local to the present
sides and site universes.
The heterogeneous program reports support no growth law for the unrestricted covering
value. If the ratio is a coincidence of the narrow `3.8`–`4.8` band, it may collapse
before the sides occupied by the reach table’s top prizes.

Where this would show up, roughly in order of how early it would be visible:

First, in the seven existing reports — but only as a warning about what is not yet
measurable.
From `3.82` to `3.96` the reported value rises at roughly `7.1` mass per unit
side, and from `3.96` to `4.58` at roughly `8.0`; it then decreases from `16.9628` at
`4.58` to `16.9303` at `4.59`, across different, unretained site-universe runs.
A hybrid slope from the reported `4.58` objective to the `4.80` certificate’s feasible
mass is roughly `8.9`, but it is not a bound.
These heterogeneous values do not justify a growth trend.
A retained eighth point over prospectively declared site-set refinements would provide a
first controlled comparison outside the existing side band.

Second, and most directly, in proposal 2’s own outcome.
A restricted optimum at `5.52` above `26` — unlike the operator-reported converged
`n = 11` site-set run at `11.000000`, with room under `12` — would show that the
prospectively fixed site universe cannot clear the mass bar at the predicted side.
It would be an operational failure of that search, not a proof that another site
universe or certificate family cannot clear the bar.

Third, structurally, in whether the fixed net and site machinery even generalise.
The shrink margin `B(1+D) < 1` is set by the net alone and does not change with the
side, but the row-generation search has only ever explored inside the narrow band, and
`BC-191`’s own finding — that a fixed site *count* thins out relative to the growing
`B`-square as the side grows, costing `8.8×` on one already-observed step near `4.80` —
is itself a small instance of exactly this worry, measured on the search’s efficiency
rather than on the true covering value.
If the same thinning affects not just how long the search takes but whether it can find
a small enough covering at all, a search that is merely too slow to finish and a chosen
site universe that is too weak become difficult to distinguish from the outside.
That is why proposal 2 needs both completed row loops and prospectively declared
site-set refinement; neither alone measures the unrestricted covering value.

## What This Document Does Not Establish

No new lower bound is proved, proposed for adoption, or estimated as anything more than
a clearly labelled extrapolation.
No hypothesis is registered and no agenda item is amended: the three proposals argue for
and against candidates already on record, and enacting any of them is a decision for
whoever runs the next block.
The `0.982` ratio rests on three points: one `n = 11` site-set row loop is reported as
converged, `n = 19` has an unretained operator report of a cost stop, and `n = 17` has
no recorded stop reason for this build.
Nothing here treats it as more than a place to look, and the predicted-gain table built
from it, and every cost estimate built on top of that, inherits the same qualification
at every row.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
