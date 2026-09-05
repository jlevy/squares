---
title: "X-015 — the map and the three programs: where significant progress is likeliest next"
softschema:
  contract: packing.squares:Exploration/v1
  schema: ../schemas/exploration.schema.yaml
  envelope: exploration
  status: enforced
exploration:
  id: X-015
  title: "The map and the three programs: where significant progress is likeliest next"
  date: '2026-09-05'
  author: Claude (agent), at the owner's request, on the branch of PR #81 after merging PR #82
  campaign: packing.squares
  brief: >-
    After one instrument moved four cases in a day, the owner asked for a holistic
    review: which of the campaign's explorations and ideas led to concrete results and
    which did not; which agendas are the most ambitious that are still likely to show
    progress; whether further improvements exist at n = 11 specifically; and whether
    constructive, computer-assisted proofs of exact values at larger n are stepping
    stones toward closing n = 11. A fifth question was folded in as a W7 block: which
    research structures the record does not track. This report compiles a map of every
    recorded direction (114 rows, six programs), joins the twenty results to the
    instruments that produced them, ranks three programs by expected significance per
    agent-hour, prices the grid-frontier stepping stones by reading Bentz's proofs in
    X-014's terms, records the eight untracked structures and what was built for them,
    and lays out the next twelve hours as agendas 021 and 022 with four hypotheses
    registered and four doubling-down rules fixed in advance. It adjudicates nothing
    and promotes nothing.
  sources:
  - packing/frontier/results.yaml
  - packing/frontier/results.schema.yaml
  - packing/frontier/CERTIFICATE-REACH.md
  - packing/frontier/covering-values.yaml
  - packing/frontier/proof-strategies.yaml
  - packing/frontier/n-011.md
  - packing/frontier/n-012.md
  - packing/frontier/n-013.md
  - packing/frontier/n-019.md
  - packing/frontier/n-020.md
  - packing/frontier/n-021.md
  - packing/frontier/n-026.md
  - packing/frontier/n-061.md
  - packing/resources/papers/bentz-2010-optimal-packings-13-and-46.md
  - packing/resources/papers/bentz-2016-optimal-packings-22-and-33.md
  - packing/campaign/ideas.md
  - packing/campaign/ledger.md
  - packing/campaign/agenda-map.md
  - packing/campaign/explorations/X-010-two-lanes-two-ladders.md
  - packing/campaign/explorations/X-013-where-the-certificate-should-go-next.md
  - packing/campaign/explorations/X-014-closing-from-both-ends.md
  - packing/campaign/hypotheses/H-022-trump-local-geometry.md
  - packing/campaign/hypotheses/H-033-m2-minus-3-at-n61.md
  - packing/campaign/hypotheses/H-039-s12-proof-frontier.md
  - packing/campaign/hypotheses/H-061-n12-first-party-fractional-certificate.md
  - packing/campaign/agendas/agenda-017-six-hour-generator-rigidity-ceilings-and-w9-block.md
  - packing/campaign/agendas/agenda-018-ten-hour-continuation-ladders-theorems-and-wave-two.md
  - packing/campaign/agendas/agenda-019-efficiency-first-retarget-and-deep-strategy.md
  - packing/campaign/agendas/agenda-020-efficiency-block-the-exact-sweep.md
  - packing/src/sqpack/fractional/certificate.py
  - packing/src/sqpack/fractional/interval.py
  - packing/devtools/render_certificate_reach.py
  - packing/devtools/decide_certificate.py
  - packing/devtools/check_bead_tree.py
  - packing/cases/bentz46/verify_cover.py
  - packing/cases/bentz13/verify_cover.py
  - docs/project/handoff-2026-09-04-block-close.md
  - SYNOPSIS.md
  - operating-rules.md
  proposes: []
---
# X-015 — The Map and the Three Programs

## The Question

After the week in which one instrument moved four cases at once — `s(11) >= 3.81`,
`s(12) >= 3.96`, `s(17), s(18) >= 4.59`, `s(19..21) >= 4.80` — the owner asked four
things at once, and this report answers them in order.
Holistically, which of the campaign’s explorations and ideas led to concrete results,
and which did not? Given that much progress, which agendas are the most ambitious that
are still likely to show progress?
Are there further improvements to be had at `n = 11` specifically?
And are there constructive, computer-assisted proofs of exact values at larger `n` that
would serve as stepping stones toward closing `n = 11`?

A fifth question was folded in during the same block, because answering the first four
exposed it: which research structures does the record not track, so that a result, a
cost, or a proposal can exist without a place to be written down?
That part ran as a W7 pipeline-improvement block alongside this W3 report, and the
section
[The Structures the Record Did Not Track](#the-structures-the-record-did-not-track) says
what was found, what was built in the same block, and what was deferred.

This report adjudicates nothing and promotes nothing.
Its deliverables are a map — one row per direction anyone has recorded, with its
provenance, its status, its yield and the program it belongs to — and three programs
ranked by expected significance per agent-hour, each with the first measurement that
would advance it and the outcome that would retire it.
Where a figure is quoted it was recomputed from the repository in this block; where it
is an estimate it says so and gives its basis.

## What Produced Results, and What Did Not

The register holds twenty results.
Joined to the instrument that produced each, they sort as follows; the join was
recomputed from `results.yaml`, the experiment records and the commit history in this
block, and the `produced_by` field the block added now carries it for the seven most
recent.

| Instrument | Results | Ids |
| --- | ---: | --- |
| First-party fractional certificate generator (`sqpack/fractional/`) | 4 | T-017, T-018, T-019, T-020 |
| The same architecture through the retained source verifier (Massaccesi’s certificate adopted) | 2 | T-015, T-016 |
| Integral unavoidable-set certifier and falsifier (`sqpack/cover.py`, `falsify.py`; the Green, Bentz and Stromquist cases) | 7 | T-001 to T-005, T-008, T-010 |
| Rigidity (`local_rigidity/`, the `n = 5` and `n = 40` assessments) | 3 | T-012, T-013, T-014 |
| Exact witness verification (`cases/trump11`) | 1 | T-011 |
| Interval witness certification (`cases/kingbird29`) | 1 | T-009 |
| Literature only | 2 | T-006, T-007 |
| Search, quench, atlas, chunk enumeration, proposers | 0 | — |

Every result that moved a frontier lower bound past a published value came from the
fractional instrument, and the significance distribution says the same thing from the
other side: the one `S5` and three of the four `S4` results are its; the rest of the
register is `S3` twelve times and `S2` three times.
The instrument’s first commit was followed by its first retained certificate after nine
minutes and by `T-017`’s registration after twenty-three; the idea it descends from
(`H-006`, “LP duals as unavoidable-set generators”) had sat on the board for eleven
days.

Three traits separate the directions that produced theorems from the ones that produced
sessions.

- **The object was `n`-independent and the instrument was exact.** The fractional
  certificate is one LP shape parameterised by the side; a run at side `L` with
  restricted optimum `M` certifies every `n > M`, which is why one run at `4.80` moved
  three cases. Verification is a finite sweep in integer arithmetic on the weights’
  common scale, and a second route decides the same object independently.
  Nothing in the search lane had that shape: an annealer’s output is a pose, and a pose
  is evidence about one basin.
- **The gap between “instrument runs” and “theorem registered” was minutes.** The
  fixed-side rigidity result at `n = 5` (`T-014`) had the same property: an exact
  linear-algebra object with a certificate a reviewer can recompute.
- **The cost was measured by the same tool that produced the result.** Every rung
  carries its atom count and its gate time, which is why X-013 could rank the next case
  by predicted gain per hour and why this report can.

What did not produce results is as instructive, and the hypothesis census says how much
of the record it is.
Of sixty-one registered hypotheses (fifty-four claims, seven open questions), twenty-one
have at least one recorded round and forty have none; of the forty, twenty-six belong to
the search-and-cartography program, six to `n = 11`, three to the grid frontier, and the
remaining five to infrastructure and other.
The agendas from 012 to 015 carry thirty-nine commitments, nineteen of them complete,
and produced no result; agendas 016 and 017 produced seven between them.
In detail:

- The annealing search (`H-016`, refuted) and the grid return (`H-020`, refuted: the
  annealer found the grid on five of five seeds at `n = 17`) measured the landscape and
  found the record’s basin rare, which was the campaign’s original question answered in
  the negative for the search lane — a result, but a bounded one.
- The basin atlas and identity program spent fourteen rounds on `H-021` and twelve on
  `H-023` without a terminal decision on what a basin is; it produced no claim about
  `s(n)`.
- The chunk-enumeration pricing (X-003, `BC-095`) came back at `4.4 × 10²⁰` raw
  configurations at `K ≤ 6`, and no chunk instrument was built.
- The `n = 29` exact solve and the `n = 90` primitive stalled on exactness and on an
  unbuilt instrument rather than on ideas.

One blind spot in the record itself was found and closed in this block: `H-061`, the
hypothesis under which the four strongest results were produced, had no experiment
record and read in the ledger as `open, 0 rounds`, so the campaign’s own effort total
excluded every minute that produced them.
The `produced_by` field now joins the results to the hypothesis, and the ledger shows
`result registered` beside it.
`T-019` and `T-020` still name no hypothesis, because none was registered for them; that
is a fact about how the block ran, not a field left blank.

## The Directions Map

The appendix lists every direction the record contains — one row per distinct direction,
with duplicates across the idea board, the registry, the strategy catalogues and the
agendas merged — with its provenance, its status, its yield, the program it belongs to,
its next measurable step and the outcome that would retire it.
It was compiled read-only over the whole campaign record in this block and it is
exhaustive over what the record holds; a direction that lives only in a session
transcript is not in it.

| Program | Rows | Produced a result | Ran without a result | Never run | Shaped only |
| --- | ---: | ---: | ---: | ---: | ---: |
| A — grid-frontier exact values | 13 | 3 | 3 | 6 | 1 |
| B — `n = 11` specifically | 23 | 6 | 2 | 10 | 5 |
| C — reach-table ladder | 12 | 4 | 1 | 7 | 0 |
| D — search and cartography | 38 | 0 | 9 | 23 | 5 |
| E — instrument and record infrastructure | 22 | 10 | 8 | 3 | 1 |
| F — other | 6 | 2 | 1 | 3 | 0 |
| Total | 114 | 25 | 24 | 52 | 12 |

The one dead row (the idea board’s four dead ends, merged) sits in D.

Two things the table says are worth stating plainly.
A third of the map is the search-and-cartography program, which holds twenty-six of the
forty never-run hypotheses and produced no result; nothing in this report proposes
spending the next twelve hours there, and nothing here kills it either, since a
direction never run is not a direction refuted.
And the three programs this report ranks account for forty-eight rows between them, of
which thirteen produced a result; those are the rows the plan below draws from.

The map also found fifteen directions that exist in the record only implicitly.
Five of them matter for what follows: the `B = 1` route past the ceiling had no row and
no hypothesis (it has a row now); X-014’s measurements had rows but no falsifiable claim
(four are registered now); the proof-assistant port is named by seven results’
`next_rung` and scheduled by no commitment; the semidefinite, sum-of-squares, Delsarte
and discharging entries of the proof catalogue have never been aimed at `s(n)` by anyone
here, while the LP side of the same catalogue produced every recent bound; and the
`n = 18` and `n = 20, 21` continuations existed only inside result prose (the second is
`BC-197` now).

## The Three Programs

Three programs account for the rows of the map that produced results and for every cell
of the next twelve hours.
They are ranked here by expected significance per agent-hour on the last week’s yield,
which is one week: A first because its first measurement is cheapest and its theorem
would be the first exact value in a decade, B second because its measurements are the
ones X-014’s verdict named and its theorem is the campaign’s, C third because its
results are the most certain and the least significant.

### Program A — exact values on the grid frontier

The most ambitious program that is still likely to show progress, and the one whose
first measurement costs the least.
The claim it aims at is a theorem of the form `s(m² − k) = m` for an open `n`:
`s(12) = 4`, `s(20) = s(21) = 5`, or a member of the `m² − 3` family at `m ≥ 8`. Nobody
has proved such a value since Bentz’s `s(22) = 5` and `s(33) = 6` in 2016, and every one
of them is a grid value, so the packing side is free and the whole difficulty is the
lower bound.

**What the classical proofs do, in this record’s terms.** This block read Bentz’s two
papers against X-014’s lemmas, and the reading changes the plan.
`s(46) = 7` is one unconditional integral certificate at the grid side: forty-five
points on an equilateral lattice, closed unit squares covered, disjoint open boxes
counted, the container side exactly seven, and the nonavoidance lemmas direction-free —
no case split, no orientation split, no limit argument.
The repository has already audited it exactly (`T-004`, ninety-two cells over
`Q(√2, √3)`). `s(13) = 4` is the other shape: a sixteen-point set with thirteen boxes is
Lemma 1 used integrally (a mass gap of three forces two boxes to be tight, the
“corner-restricted” ones), the forced hulls of Lemmas 10 and 11 are Corollary 1a, and
the rest is a Lemma 2 tree — six leaves of fifteen to twenty-one points, with up to
sixteen alternative point choices in one of them, a sliding point and
intersection-length thresholds.
No step in either paper is a class certificate; the only orientation-conditioned
argument in the literature is Stromquist’s Theorem 3.

**Where the walls are, and the finding that reorders the block.** The covering value
`τ*(L)` has been measured at seven sides, all inside `[3.82, 4.80]`, and every measured
value is an upper bound on it (a restricted optimum on one site set).
Extrapolating linearly from the top measured point, with the local slopes between
reported values as the spread, gives lower estimates of the side where `τ*` reaches `n`:

| Case | Estimated wall | Sliver to the grid value | What pins it |
| --- | --- | --- | --- |
| `n = 12` | `3.961`–`3.963` | about `0.037` to `4` (about `0.03` once the shrink is dropped) | a converged run at `793/200` |
| `n = 13` | above the ceiling: `τ*(3.9908) ≈ 12.06`–`12.24 < 13` | `0.0092`, the shrink tax only | one run at `399/100` (`BC-211`) |
| `n = 20` | `4.915`–`4.935` | `0.065`–`0.085` to `5` | the bisection of `BC-197` |
| `n = 21` | above the ceiling: `τ*(4.9885) ≈ 20.4`–`20.7 < 21` | `0.0115`, the shrink tax only | one run at `4.985` (`BC-197`’s first rung) |
| `n = 61` | unmeasured; the ceiling is `7.9816`, `0.053` above Nagamochi | — | one run at `7.95` |

The `n = 12` ladder is at its wall: `T-017`’s retained rung at `3.96` has `0.001` of
margin and no further rung of the present kind is worth a run.
The two rows that change the plan are `n = 13` and `n = 21`. At both, the covering value
extrapolates to *below* `n` at the ceiling, which means the ladder is expected to run
all the way to the method’s structural limit and stop only for the shrink — and then the
endgame is not a tree at all but one certificate at shrink `B = 1` at the integer side,
which is exactly the shape of Bentz’s `s(46) = 7`. These are extrapolations over `0.03`
and `0.19` of side from two and three points, labelled as such, and the cheapest
measurements in the whole plan are the two runs that test them.

**What the `B = 1` route needs.** The ceiling is a theorem about finite nets: on any net
with largest half-gap tangent `D`, Condition 4 forces `B < 1/(1 + D)`, and a
quarter-turn net alone buys nothing, since boxes of side `1 + η` on a net with half-gap
`D` still prove only sides at most `m/(1 + D)`. A certificate at `B = 1` must satisfy
the covering condition at every angle, so the instrument that escapes the ceiling
decides over the direction continuum: an angle-interval branch and bound on top of the
interval route, which today branches over centre boxes at fixed doubled-net directions.
That is `BC-212`, contingent on `BC-211`’s run confirming that one certificate is enough
at `n = 13`. The `n = 12` endgame is different: its wall sits below the ceiling, so
after the shrink is dropped a sliver of about `0.03` remains, the mass gap at side four
is about `0.06`–`0.24`, and Lemma 1 bites — every square of a hypothetical packing sits
on a core of mass at most about `1.2`. Class certificates first (at side `s < 4` at most
nine squares tilt by less than `θ₀(s)`, which is `0.58°` at `3.96` and `0.14°` at
`3.99`, so only compositions with three or more tilted squares survive), then
conditional certificates on the tilted squares’ angle bins and centre boxes.
The generic count for one boxed square runs from about `2 × 10³` LPs at quarter-unit
boxes and `5°` bins to about `7 × 10⁴` at tenth-unit boxes and `1°` bins; two boxed
squares are out of reach.
Whether a Bentz-like forced structure cuts that to tens is what the tight-core census
(`BC-201`, `H-065`) is for.

**The `m² − 3` family is not a stepping stone.** Bentz’s lattice spans the container
only for `m ≤ 7.18`: the spanning inequality has slack `+0.025` at `m = 7` and deficits
of `0.109`, `0.243` and `0.377` at `m = 8, 9, 10`, so `H-033`’s instrument ("substitute
`m = 8`") fails at its first forcing step, and any proof there is a weighted LP-found
set whose covering value near side `7.93`–`7.98` is unmeasured.
The reach table’s ratio heuristic predicts `7.858` for `n = 61`, below Nagamochi’s
`7.928`; the honest prize is at most `0.053` of side for about `2.7` times `T-020`’s
atoms. It stays on the reach ladder and nowhere else.

**First measurement and kill.** `BC-211` (`n = 13` at `399/100`, zero build, about
seventy minutes) and `BC-197`’s first rung (`n = 21` at `4.985`). A converged optimum at
or above `n` on two independent site sets at either side retires the one-certificate
reading for that case and returns the endgame to the tree; a converged optimum below `n`
is a certificate within `0.01` of the grid value and opens the `B = 1` build.

### Program B — `n = 11` beyond `3.81`

`s(11)` sits in `[3.81, 3.877084]`. Three facts, all from the record, fix what the next
move can and cannot be.

- **The ladder alone cannot reach Trump.** The retained net and shrink carry a
  packing-side cap: scaling Trump’s packing into a container of side `L` places eleven
  `B`-squares at net directions as soon as `L/U >= B (cos δ + sin δ)`, where `δ` is the
  distance from the tilted squares’ `40.181937°` to the nearest net direction, and
  Condition 5 then forces mass at least eleven.
  X-014 computed the cap at `3.868983` for the retained `B = 9977/10000`; this block put
  the same computation into the reach table so every case with an angle inventory
  carries it — the net-level cap, over every admissible shrink, is `3.868999`, and
  `n = 11` is now ranked on a prize of `+0.0590` rather than `+0.0671`
  ([The Structures the Record Did Not Track](#the-structures-the-record-did-not-track)).
  Every certificate on this net therefore proves a lower bound strictly below `U`, and
  equality — `s(11) = U` — needs an argument of a different shape above the cap.
- **The wall at `3.82` is measured, not decided.** Two independent site sets stop at a
  covering value of exactly eleven, and the rejection route’s exact maximum pointwise
  depth is `1925/1152`, capping its feasible total at `1152/175` against the eleven a
  ceiling needs. The record calls that a measurement; whether `τ*(3.82) = 11` (a genuine
  wall, the covering LP’s own limit) or the site sets were short (a search artefact, as
  at `n = 18`’s `4.68`) is the single cheapest unknown in the program.
- **The pose is first-order rigid and the radius is unquantified.** Exp-013 found every
  one of the 128 branchwise linearized fixed-side cones zero with a strictly positive
  stress; `BC-176` (agenda-018, `H-022`) is the costed, blocked cell that turns that
  into an exact rational isolation radius, with its claim boundary already written
  (fixed side, labeled pose, side-stability by embedding; no optimality, no uniqueness).

The program, in the order the dependencies run:

1. **Decide the wall (X-014’s measurement 1).** Run the covering LP at `3.82` on a
   third, deliberately different site set (certificate-seeded rather than grid-built) to
   convergence, and one rung at `3.815`. Outcome that advances: the value stays at
   eleven on both — the wall is real and the ladder is finished at `3.81`, so the
   program moves to steps 2–4. Outcome that advances differently: the value drops below
   eleven — the `3.82` stop was the site set, the ladder continues, and every step below
   is deferred until it stops again.
2. **Read the exact cover at the wall (Corollary 1a).** At mass exactly eleven the
   tight-core lemma says every packing at `3.82` covers the heavy atoms exactly once;
   the retained `3.81` certificate’s 649 atoms above `1/200` carry `9.97` of its
   `10.86`. The measurement is the cell census (Corollary 1b): which event cells are
   tight, and whether their union is a small number of coarse placement classes.
   Advances if the census names fewer than a few hundred classes; retires if the tight
   set is dense over the container.
3. **The radius as a theorem (`BC-176`).** Independent of steps 1–2 and already costed
   at 195 minutes. It is a stepping stone for the perturbation half of any closing
   argument, and it is the one piece of Program B with a known answer to calibrate on
   (`T-014` at `n = 5`).
4. **Class theorems below Trump — “Gardner with margin”.** Stromquist proved the
   `0°/45°` class is bounded below by `3.885618 > U`; a class certificate (X-014, Lemma
   3\) is the instrument that would extend that to “no packing whose tilts all lie
   within `±α` of `{0°, 45°}` beats Trump”, and the nine-point fact (at most nine
   squares tilted less than `θ₀(s)`, `1.85°` at `U`) gives “at least two squares are
   genuinely tilted” for free.
   These are theorems about `n = 11` that do not need the wall decided; they need the
   class-certificate variant built (a partition of net cells into classes with two
   thresholds, and a solver that takes it).
5. **The run above `U`.** Equality and uniqueness need a certificate — conditional, with
   open cores, at a rational `L₁ > U` — in every branch of the tree that steps 2 and 4
   leave. This is the expensive end and it is not priced here; X-014’s verdict table says
   which three numbers price it (tight-cell count, class count, branch count).

What Program B does not contain is a search for a better packing: fifty years of search,
a purpose-built inflation algorithm and the campaign’s own annealer (`H-016`, refuted)
found nothing, and a further failed search certifies nothing.

Priced honestly, the chance of a theorem at `n = 11` inside one block is about zero.
The block-sized results here are the four measurements, and that is why Program B runs
as a lane in every block rather than as the block.

### Program C — the reach-table ladder

This is the program the queue already holds, and the one with the highest certainty of a
registered result per block.
The instrument is built, the retention gate decides `68×` to `183×` faster than it did
two days ago (agenda-020), and X-013 has ranked the cases by predicted gain: `n = 26` at
side `5.5218` first (`+0.3987`, statistically tied with `n = 51` and `n = 39` but at a
third of `n = 51`’s estimated gate time), then the `37`–`39`, `51`, `66`–`68` and
`83`–`86` clusters. Each rung is `S3`–`S4`: it displaces Nagamochi’s closed form at a
case nobody has proved anything specific about, which is what `T-020` did at
`n = 19..21`.

Two things make it a program rather than a chore.

- **It is the only source of covering-value data outside the `3.82`–`4.80` band.** Six
  restricted optima have been measured, all inside a side band of width `0.98`, two of
  them unconverged; every top-prize target sits between `6.59` and `9.65`. A converged
  point past `5.5` is the first evidence about how `τ*(L)` grows with the side, which is
  the quantity that decides whether Program A’s walls are near or far from the grid
  values.
- **`BC-191` prices the side.** Row generation is `79`–`94%` of every round and site
  density was never set as a function of the side; until it is, every cost estimate
  above `n = 21` is an extrapolation.
  `BC-191` is the selected next entry of the standing queue and nothing in this report
  displaces it.

The kill outcome is X-013’s own: a column-generation run at `5.52` carried to genuine
convergence that needs mass above `26`, or lands its attained ratio below `0.90` of the
best packing, is direct evidence the `0.982` band does not survive outside the band it
was measured in, and the right response is to stop climbing and spend the hours on
Programs A and B.

## Larger `n` as Stepping Stones

The owner’s fourth question was whether constructive proofs at larger `n` are a road to
`n = 11` rather than a detour from it.
They are, for one reason that is easy to state: every exact value on the grid frontier
is proved by the same moves that a closing argument at `n = 11` needs, and at the grid
frontier those moves can be calibrated on cases whose answer is known.
The moves are X-014’s lemmas read as instruments: a certificate ladder to the wall
(built); a certificate at `B = 1` over the direction continuum for the last sliver
(`BC-212`, not built); class certificates (Lemma 3, a threshold change, `BC-198`);
conditional certificates on boxed squares (Lemma 2, a domain generalisation, `BC-204`);
and the tight-core census that says whether an exact cover is a check or a search
(Corollary 1a, `BC-201`).

Ranked by machinery reuse toward `n = 11` and `n = 12` and by the chance of a theorem
inside one block, with the chances as this block’s own estimates:

| Stone | What it proves | Why this position | First measurement | Kill | Chance in one block |
| --- | --- | --- | --- | --- | --- |
| `n = 13` | `s(13) ≥ 3.99` by the present instrument, then `s(13) = 4` by one `B = 1` certificate: a machine reproof of Bentz without his case analysis | The answer is known, so every failure is the instrument’s; the covering value extrapolates to `12.06`–`12.24` at the ceiling | `BC-211`: the generator at `399/100`, zero build | mass `≥ 13` converged on two site sets, or `≥ 13` at side `4` under `B = 1` (then Bentz’s six-leaf tree via Lemma 2) | about `0.4`–`0.5` for the calibration |
| `n = 21` (`n = 20` as byproduct) | `s(21) ≥ 4.985` by the ladder; possibly `s(21) = 5` by one `B = 1` certificate at side `5`; `s(20)` to about `4.92` | The first proved member of `n = 12`’s own `k = 4` family; no packing record in the way | `BC-197`’s rung at `4.985` on the `n = 21` reading | a converged optimum `≥ 21` at `4.985`: `n = 21` has an `n = 12`-shaped sliver | about `0.7` for a rung above `4.90`; about `0.1` for `s(21) = 5` |
| `n = 12` | `s(12) = 4` | The target; its wall is measured and its sliver is a tree | the census on the `99/25` certificate; thirteen class LPs at `3.97`–`3.99` | a fat tight set at `ε = 0.05`; compositions with three or more tilted squares not closing near `3.99` | below `0.1` for the theorem; the census and the class LPs are the block-sized results |
| `n = 11` | `s(11) = U` | Last: needs the perturbation half as well, and `U` is not a grid value; its ladder is at the `3.82` wall and its cap is `3.869` | `ν*(3.82)` by cutting planes; `ρ₀` from the 128 branches (`BC-200`, `BC-199`) | `ρ₀ < 10⁻⁶`; `τ*(3.82) = 11` exactly | about `0` for a theorem; measurements only |
| `n = 61` family | past Nagamochi by at most `0.053` | Bentz’s lattice does not span the container at `m ≥ 8`; the ratio heuristic predicts a gain of zero | one converged run at `7.95` | a restricted optimum `≥ 61` | about `0`; stays on the reach ladder |

Two cautions. Every wall in the table is an extrapolation from two or three measured
points, and the sliver’s width is what sets the endgame’s size; the two runs that test
the `n = 13` and `n = 21` rows are the cheapest things in this report and the ones most
likely to change it.
And the `n = 12` endgame is not a smaller copy of the `n = 20` one: the wall at `m = 4`
sits below the ceiling where `n = 13`’s does not, `m = 4` leaves less room, and Bentz’s
`n = 13` proof is a six-leaf tree where his `n = 46` proof is a single certificate.
Which of those the mechanised route inherits at `n = 12` is what the census decides.

## The Structures the Record Did Not Track

The audit ran as a W7 block with named consumers, over the working tree at the merge of
PR #82’s head, and it measured rather than listed: each item below is a structure that a
result, a cost, or a proposal needs and the record had no field for, with the consumer
that reads it and the failure its absence has already caused or would cause.
Eight were found. Five were built in the same block, one as a refusal only, and two were
deferred with the reason.

| # | Structure | Consumer | Failure prevented | This block |
| --- | --- | --- | --- | --- |
| a | A covering-values register, one row per `(n, side, site set)` with a `converged` flag | The reach renderer, already gated in the records tier | An unconverged value read as an optimum; four of seven reported values were not recomputable from anything retained | Built: `frontier/covering-values.yaml`, ten rows, four of them converged, validated in the soft-schema step; the renderer reads it and the hardcoded tuple is gone |
| b | `produced_by` on the result object (hypothesis, agenda cell, session, experiment) | `check_results` and the ledger’s hypothesis table | The ledger reported `H-061` as `open, 0 rounds` while it owned four of the register’s strongest results | Built: schema field, dangling-id check, a `results` column and a `result registered` status in the ledger; filled for `T-014` to `T-020` from the record’s own words |
| c | Registration state for an exploration report’s proposals | The ledger’s ideas-board integrity check | Nine costed, falsifiable measurements aging out of context with no row | Rows 71 to 82 on the idea board; four of them registered as `H-062` to `H-065`; no schema change |
| d | `program` on agenda cells, for commitments that span agendas | The agenda map’s “By program” section; W10 closeouts | A program half-done across four agendas reads as two agendas finished | Built: schema field and renderer section; agendas 021 and 022 carry the three slugs |
| e | A results-to-session cost join | The results view; W10 replanning | Planning cost from memory, the documented instance being an agenda that quoted a figure nobody measured, wrong by a factor of three | Deferred: falls out of (b) once every result names its session |
| f | The packing-side cap per case | The reach table’s prize ranking | `n = 11` ranked on a prize `0.12` above what the method can reach | Built: `n = 11` now reads cap `3.8690`, prize `+0.0590`; `n = 5` and `n = 10` move to foreclosed by the cap; grid cases reproduce the ceiling exactly; sixteen tests |
| g | A `variant` field on the retained certificate (`unconditional`, `class`, `conditional`) | The retention gate, before Condition 1 is applied | A conditional certificate on a doubled net passing a gate that checks a D4 invariance it does not have | Refusal built: the gate refuses any variant but `unconditional` by name |
| h | Bead state against agenda state | `check_bead_tree` and `tbd ready` | The queue offering finished work as takeable; `BC-097`’s whole question | Report built, never failing: twelve in-progress beads named only by terminal cells, sixteen named by no cell |

Two of the eight are what this report’s programs need before their first measurement.
Program A’s class, conditional and `B = 1` certificates cannot be retained without (g),
and cannot be planned without (a) telling the truth about which walls are measured and
which are plateaus of a short site set.
The rest are hygiene of a specific kind: the audit’s own reading of the last three days
of history found four recurrences of one shape — a number stated in prose drifting from
the artifact that owns it — and every item above is a place where that shape can recur.

## The Next Twelve Hours

The owner asked for at least twelve hours of planned work in blocks of four to eight, so
that progress is visible at each boundary and the following block can double down on
what moved. The plan is two blocks — seven and a half hours and six — as agendas
[021](../agendas/agenda-021-three-numbers-and-a-wall.md) and
[022](../agendas/agenda-022-the-conditional-route.md), with a third block’s shapes named
but not written as cells.
Three lanes run in each block, one per program, because the programs need different
instruments and a lane waiting on a solver is a lane whose hours are lost (`OR-3`); the
closeout of block one (`BC-203`) evaluates four doubling-down rules written now and
names which leads of block two open.

**Block one, agenda 021, 450 minutes.** The cheapest measurement in each program, and
the four numbers X-014’s verdict said nobody had measured.

- *Lane A, grid frontier.* `BC-197`: one rung at `4.985` on the `n = 21` reading, then a
  pre-registered bisection of `[4.80, 4.9885]` for the `n = 20` wall (`H-062`);
  `BC-198`: the class-certificate program with its two controls, the nine-point bound
  and Stromquist’s `{0°, 45°}` class (`H-063`); `BC-211`: the generator unchanged at
  `n = 13`, side `399/100`.
- *Lane B, `n = 11`.* `BC-199`: the isolation radius `ρ₀` and the stress constant from
  the 128 branch certificates (`H-022`); `BC-200`: the covering value from below at
  `3.82` and `3.85` by an exact-depth fractional packing (`H-064`); `BC-201`: the
  near-tight cell census on the retained `381/100` certificate (`H-065`).
- *Lane C, the ladder.* `BC-191` from agenda 019, as selected, then `BC-202`: the
  `n = 26` run at `138/25` if the pricing allows it, carried to convergence rather than
  a clock.

**The doubling-down rules, fixed before block one runs** (`BC-203`). If the `m = 5` wall
lands within `0.02` of five, the ladder has nothing left there and block two opens the
endgame. If the `n = 11` covering value is below eleven at `3.85`, the ladder is not
blocked where X-014 assumed and block two climbs `n = 11` rungs instead of opening the
exact cover. If `ρ₀` comes out below `10⁻⁶`, no conditional lead opens against Trump’s
pose and the radius goes to agenda 018 as a theorem.
If the `n = 13` run converges below thirteen, block two builds the `B = 1` route
(`BC-212`) before the conditional route.
Two rules can fire at once; the third overrides the endgame half of the first; the
fourth reorders a lane without closing any lead.

**Block two, agenda 022, 360 minutes, every cell contingent on `BC-203`.** Lane A is
either the conditional route — the admissible-domain generalisation in all four
consumers (`BC-204`) and the `n = 13` calibration on it (`BC-205`) — or, under rule
four, the `B = 1` route over the direction continuum (`BC-212`) with the same
calibration at side exactly four.
Lane B is the two class theorems at `n = 11`, Gardner with the class widened to two
cells and the composition count (`BC-208`), then the exact cover at whichever wall block
one found (`BC-207`). Lane C is the `n = 12` ladder to the ceiling with the `n = 21`
continuation as its second leg (`BC-206`), then the reach-table rungs `BC-191` priced or
`n = 11` rungs under rule two (`BC-209`).

**Block three, four to eight hours, not written as cells.** Its shape is whichever of
three block two leaves open: the `n = 21` certificate at side five and the `n = 20`
sliver if the `B = 1` route calibrated; the `n = 11` handshake (X-014’s measurement 5)
if the radius and the census both came in enumerable; or the conditional route if rule
four fired and deferred it.
The closeout of block two (`BC-210`) selects it, and this report does not.

Every research cell in both agendas carries one of the three program slugs, so the
closeouts report per program rather than per agenda.
The four hypotheses registered for the blocks are `H-062` (the `m = 5` wall sits below
the ceiling and four rungs bracket it to `0.02`), `H-063` (a two-cell `{0°, 45°}` class
certificate certifies above Trump’s side, and compositions with at most one tilted
square are closed), `H-064` (an exact-depth fractional packing puts the `n = 11`
covering value at eleven by `3.85`), and `H-065` (the near-tight set on the `381/100`
certificate is under a fifth of the reachable cells).
Each carries a falsifier and an instrument that exists or is the cell’s first task; two
are blocked on their instrument and read so in the ledger.

## If This Argument Is Wrong

- **The yield analysis may over-credit the instrument.** Four results in a day is one
  data point about one instrument on the cases it was built for; the attainment band is
  three points wide. If `n = 26` comes back below the band, Program C’s certainty is gone
  and Program A’s wall estimates, which lean on the same growth picture, go with it.
- **The walls may be far from the grid values.** Program A’s premise is that a
  certificate ladder reaches within a small sliver of `m` at `n = 20, 21` or `n = 12`.
  The two-point trend at `n = 12` says the wall is near `3.963`; if the true wall is
  `3.9` the endgame is not a sliver, it is the whole problem, and Bentz’s hand proof
  becomes the only route.
- **Class and conditional certificates may not solve at useful sizes.** Lemma 3’s
  homogeneous LP has as many variables as an ordinary certificate and more constraints;
  nothing has been solved in that shape yet.
  If the first class LP at `n = 13` does not converge in a block, Program A’s endgame is
  unpriced again.
- **The ranking may be wrong about what is significant.** The rubric scores movement on
  `n = 11` at `S5` and a new grid-value theorem at `S4`–`S5` depending on the case; if
  the owner weights a first exact value for an open `n` above a further rung at
  `n = 11`, Program A moves ahead of B in every block.
- **The record hygiene items may be smaller than they look.** The audit measured what is
  not tracked; it did not measure what that has cost.
  If no planning error traces to the untracked structures beyond the two already
  documented, the deferred items should stay deferred.

## What This Document Does Not Establish

No bound moves here and no claim is promoted.
The wall estimates are linear extrapolations from two or three measured points, labelled
as such, and the endgame branch counts are ranges computed from the net’s geometry under
stated assumptions, not from a run.
The directions map is exhaustive over what the record contains as of this branch’s head,
and it is a reading of the record, not the record: a direction that exists only in a
session transcript is not in it.
The three programs are ranked by expected significance per agent-hour on the yield of
the last week, which is one week.
The next-twelve-hours plan is written into agendas `021` and `022` as commitments with
budgets and stop rules; it is a plan, and the closeout of block one is what decides
whether block two runs as drafted.

## Appendix — The Directions Map

Compiled read-only in this block over the record at the merge of PR #82’s head
(`25c5f502`), with this block’s own additions — the idea-board rows, the `produced_by`
fields, the ledger’s `results` column, the reach table’s `cap` column — cited as “this
block” where a row relies on them.
One row per distinct direction; duplicates across the idea board, the registry, the
strategy catalogues and the agendas are merged, with every provenance pointer kept.
Columns: direction; provenance; status; yield; program; next measurable step; kill
outcome.

## Program A — grid-frontier exact values

| # | direction | provenance | status | yield | program | next measurable step | kill outcome |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | Fractional-certificate ladder at `n = 12` toward the ceiling `4B = 3.9908` | ideas row 70; H-061 (registered 2026-09-04, `packing/campaign/hypotheses/H-061-…md`); BC-160, BC-161, BC-162 (agenda-017, all complete); BC-171 (agenda-018, blocked); `results.yaml` T-017 `produced_by` H-061/BC-161/session-085 (this block) | produced result | T-017 (rungs 19/5, 77/20, 97/25, 39/10, 393/100, 197/50, 79/20, 99/25; `results.yaml` T-017 rationale) | A | BC-171: one rung above 99/25 inside the 0.0308 runway (`CERTIFICATE-REACH.md` n = 12 row) | a converged covering value ≥ 12 at every side above 99/25; the ceiling already proves no single certificate reaches 4 (T-017 `next_rung`) |
| 2 | `s(12) = 4` by integral or forcing resources (Stromquist-style CEGIS: certifier + escaping-pose falsifier + LP-dual candidates) | ideas row 42; H-039 (open question, 0 rounds); X-010 Lane A rung A3; BC-102 (agenda-010, complete via its diagnostic branch: `devtools/pierce_pilot.py` τ* pilot, session-059); agenda-016 ranked table rank 5 `think-0z9b` “deferred, cost in agent-days”; agenda-017 rank 10 “the generator supersedes the integral-set framing” | ran, no result (diagnostic only) | none | A | none scheduled; superseded by rows 1 and 3 | already retired de facto: no integral set above 99/25 was ever exhibited, and the ceiling theorem bounds every shrink-net certificate below 4 |
| 3 | Escape the ceiling: `B = 1` open-placement certificates decided over the continuum of directions, or a proved family of certificates with sides tending to 4 plus a limit argument | BC-193 (agenda-019, blocked, “what would a method that escapes the ceiling have to change”); T-017 `next_rung` (family-with-limit reading, PR 78 review F14); X-014 §"`n = 12` Is a Different Proof" (drop the shrink, decide Condition 5 by interval branch-and-bound in three parameters) | never run | none | A | BC-193 written argument, then a prototype interval decision of Condition 5 at `B = 1` on the retained `n = 12` bytes | a proof that the covering value at `4 − δ` is ≥ 12 for all small δ, or that the shrink is essential to a finite decision |
| 4 | Class-certificate composition ladder at `n = 12` (`n₁ = 0` capped at `4B`; every other composition conditioned on how many squares tilt) | X-014 §"`n = 12` Is a Different Proof", Lemma 3; the `n = 11` instance is ideas row 77 (this block) | shaped only | none | A | run after row 21 succeeds at `n = 11`; a threshold change to the covering program, no new geometry | the `n₁ = 0` class fails to certify above U at `n = 11` (row 21’s kill) |
| 5 | `n = 13` calibration: Bentz’s corner-restricted configuration at side 399/100 as a conditional certificate with two boxed squares | X-014 measurement 6; ideas row 79 (this block); BC-173 (agenda-018, blocked) first half “reproduce Bentz’s `s(13) = 4` fractionally or meet a certified ceiling” | never run | none | A | multi-box Lemma 2 after the admissibility-domain generalisation in `sweep`, `generate`, `interval`, `colgen` | the boxed case still returns mass ≥ 13 (conditioning cannot close a case the classical method closes by hand) |
| 6 | Bentz 2010 Theorem 9 (`s(13) = 4`) full machine audit, Sections 3.1–3.2 | T-006 `next_rung`; BC-099 (agenda-010, still `ready`, bead `think-1o1f`); agenda-017 rank 6 “park: 12–18 agent-hours”; T-005 came from the Lemma 10 half (BC-099, commit 27028c4d 2026-08-31) | ran, no result for the remainder (Figure 2 and Lemma 10 audited) | T-005; T-006 stays at V3/C1 | A | encode the staged sets of Sections 3.1–3.2 in `sqpack/cover.py`; T-006 to C3 | none — either a full audit or a repaired printed gap is a result; retire when complete |
| 7 | Bentz 2010 Theorem 8 (`s(46) = 7`) audit and the equality | BC-099 (agenda-010, session-053, commit e804097f 2026-08-31); BC-106 (agenda-011) determination; proof strategy 2/7 | produced result | T-004, T-008 | A | C4 by a pose-space interval audit generalised to `Q(√2, √3)` sides; V5 by a proof-assistant port (T-004 `next_rung`) | retired at C4 |
| 8 | Bentz 2016 continuously-varying families (`s(22) = 5`, `s(33) = 6`) machine audit | proof strategy 7 (status `used`, refs Bentz 2016); H-033’s prerequisite “machine-readable Bentz m = 7 certificate” covers only `m = 7` = `s(46)`; no ideas row, no hypothesis, no agenda commitment | never run | none | A | encode the parametrised family for `s(22)` in the general certifier (row 88) | none — an audit outcome either way; this is a gap (see `gaps.md`) |
| 9 | `s(61) = 8`, the `m = 8` case of `s(m² − 3) = m` | ideas row 38; H-033 (open question, 0 rounds); X-010 Lane A rung A4; BC-103 (agenda-010, complete, session-058: “the m = 7 pattern’s ceiling at m = 8 is `7√3/2 + 2√2 − 1`, exactly below side 8 — parked”); `CERTIFICATE-REACH.md` n = 61: lower 7.9282, ceiling 7.9816, prize +0.0534 | ran, no result (sizing slice; parked) | none | A | a resource system beyond the `m = 7` pattern, or a fractional rung inside the 0.0534 runway | a sub-grid packing at `n = 61`, or a proof that the `m = 7` pattern’s ceiling is the method’s |
| 10 | Nagamochi 2005 Lemma 1 “λ may be taken as 1” audit — the step under 58 verified lower bounds | BC-181 (agenda-018, blocked, two-hour spike); T-007 `next_rung` (C3 = machine-check Theorem 1); agenda-017 rank 7 | never run | none | A | prove the unargued sentence exactly, or exhibit the gap | none — a found gap is itself a result (and a defect across the register) |
| 11 | `s(20) = s(21) = 5`: close the last 0.1885 from 24/5 to the ceiling `5B = 4.9885`, then the 0.0115 the ceiling forbids | T-020 (`results.yaml`, produced_by BC-161/session-085 this block); `CERTIFICATE-REACH.md` n = 20, 21 prize +0.1885, predicted +0.1115; T-020 `next_rung` “a run between 4.80 and 4.9885 moves 20 and 21 and stops at 19” | produced result | T-020 | A | one converged run at a side in (4.80, 4.9885), e.g. the predicted 4.9115 | covering value ≥ 20 at side ≤ 4.9885; the final 0.0115 needs row 3 |
| 12 | The grid-bound open cases as a class: “is the grid optimal or merely unbeaten” | BC-091 (agenda-009, ready; X-009 narrowed it to `n = 90` = row 83); `CERTIFICATE-REACH.md`: ceiling-limited open cases 30, 31, 32, 42–45, 56–61, 72–78, 90–97 with prizes up to +0.4330 (n = 90), +0.4295 (72), +0.4242 (56), +0.4162 (42), +0.4036 (30) | never run as a survey | none | A | fractional rungs at the largest ceiling-limited prizes, each certifiable to within `1/(1+D)` of the grid | case by case: covering value at the ceiling side ≥ n, or a sub-grid packing (row 83’s route) |
| 13 | Machine audits of the other published small-case proofs: Kearney–Shiu (`s(6) = s(7) = 3`, dual lattice counting), Friedman’s forcing (`n = 7, 14`), Göbel 1979 | proof strategies 5, 6, 2 (`used`); X-010 Lane A rationale ("four recorded defects in El Moumni’s route to `s(7)`"); BC-031 (agenda-003, complete: one missing primary recovered); no ideas row, hypothesis, or commitment | never run | none | A | encode Kearney–Shiu’s dual counting in the general certifier | none — audit either way; a gap (see `gaps.md`) |

### Program B — `n = 11` specifically

| # | direction | provenance | status | yield | program | next measurable step | kill outcome |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 14 | Fractional-certificate ladder at `n = 11` | BC-172 (agenda-018, blocked; done inside agenda-017’s continuation, session-085); T-018 `produced_by` H-061/BC-161 (this block); rungs 189/50, 19/5, 381/100 (`results.yaml` T-018) | produced result | T-018 | B | row 15 decides whether any rung above 3.81 exists | both routes fail by an infinitesimal at exactly 11 at side 3.82 (T-018 `next_rung`) |
| 15 | The 3.82 plateau: `τ*(L)` on a third site set to convergence and at 3.815; the packing dual `ν*(L)` at 3.82, 3.85, 3.87 by cutting planes on the 3.82 dual | T-018 `next_rung` (two site sets at exactly 11.000000; `sqpack.fractional.ceiling` max depth 1925/1152, feasible total 1152/175 = 6.5829); X-014 measurement 1; ideas row 74 (this block); agenda-019 “State at handoff”; handoff-2026-09-04 §"Where the next rungs are" | ran, no result (stopped on cost) | none | B | run row 74 as written | nothing kills it — either outcome fixes the ladder’s top and the tree’s working side |
| 16 | Fractional-piercing ceiling of the pure ten-point method at Trump’s side: is `τ*(U_s) > 10`? | ideas row 30; H-034 (blocked, 0 rounds; prereqs continuous pose falsifier, certified discretisation bounds); BC-102 hypotheses list | never run | none | B | two-sided discretisation certificate of `τ*(U_s)` | `τ* ≤ 10` with an integral ten-set (a Stromquist-shape proof could then reach U) or `τ* > 10` (retires pure-point routes at U) |
| 17 | Trump’s pose is first-order rigid at fixed side (all 128 branch cones zero) | ideas row 31; H-026 (confirmed, exp-013); `packing/frontier/n-011.md` rigidity `locally-rigid / verified`; evidence `E-n011-trump-local-rigidity` | produced result (frontier rigidity field; no T-id) | none | B | row 18 | retired — confirmed |
| 18 | Explicit isolation radius `ρ₀` and side-perturbation stability at Trump’s pose (`κ_b` on 128 branches, curvature `K`, stress constant `C`) | H-022 (open question, 0 rounds); ideas open question “what quantitative local geometry remains after exp-013”; BC-176, BC-177 (agenda-018, blocked); X-014 measurement 2; ideas row 75 (this block); agenda-018 §"Why These Lanes Are Next" ("reachable at V4, no curve selection") | never run | none | B | 66 LPs per branch on `cases.trump11.tangent_cones` matrices, exact confirmation; `ρ₀ = min_b 2κ_b/K` | `ρ₀ < 10⁻⁶` in the chart — no tree reaches a box that small |
| 19 | Incidence-minimal rigidity cores in every Trump derivative branch | ideas row 45; H-043 (blocked, 0 rounds; prereq exp-013 replay) | never run | none | B | exact grouped-row minimal subsets for all 128 branches | some branch has no proper subset that still forces `{0}` |
| 20 | Tight-core census: event cells with mass ≤ `1 + ε` on the 381/100 certificate and the 3.82 atom set | X-014 measurement 3 (Corollary 1a/1b); ideas row 76 (this block) | shaped only | none | B | per-cell readout of `sweep.minimum_covered_mass` at `ε ∈ {0, 0.01, 0.05, 0.1}` | the tight set at `ε = 0.05` covers most of the centre domain |
| 21 | Class certificates by composition `n₁` (Lemma 3): twelve LPs at a rational side just above U, near-axis class = first nineteen half-gap cells | X-014 measurement 4; ideas row 77 (this block); Stromquist Theorem 3 as the precedent (proof strategy 9) | shaped only | none | B | a threshold change to the covering program; decide the sign of each LP’s optimum | the `n₁ = 0` class fails to certify above U |
| 22 | Conditional (boxed) certificate handshake at `U − 0.01` with all eleven squares boxed at radius 0.05 (Lemma 2, multi-box) | X-014 measurement 5; ideas row 78 (this block); X-014 codebase inventory: no admissibility hook in `sweep.centre_domain`, `generate.py`, `interval.DirectionSearch`, `colgen` | shaped only | none | B | generalise the admissible domain to non-convex sets and a quarter-turn net; time one node with a coarse net | the conditional value stays ≥ 11 (the middle tier is not empty) |
| 23 | A full branch-and-bound optimality tree for Trump’s packing (coarse class/conditional certificates, fixed-angle cell LP with interval propagation, modulus lemma at the leaves) | X-014 §"Assembling a Proof"; proof strategy 15 (Montanher `n = 3`, Markót circles); the `n = 11` report’s calibration “do not target `s(11)` with a rigorous solver” | shaped only | none | B | only after rows 15, 18, 20 set the three unmeasured numbers | the band between the tools is non-empty: `ρ₀ ≈ 10⁻⁵` while conditioning stops at `10⁻¹`, forcing 34-variable interval propagation |
| 24 | Other near-optimal arrangements inside the band the certificate cannot see | X-014 §"Other near-optimal arrangements" (H-016’s 3.9144 on every seed; Gensane–Ryckelynck re-finds; SCIP 2026 at 3.87709); ideas open question “what does the searcher actually find at `n = 11`” | never run as a measurement | none | B | a restart histogram of local optima below 3.9 with tilt counts (also row 35) | a second local minimum inside the band — it needs its own box and lemma |
| 25 | Stromquist 2003 Theorem 3 (`0°/45°` packings need side ≥ `2 + (4/3)√2`) audited as printed | BC-164 (agenda-017, never opened); BC-185 (agenda-018, blocked); agenda-017 rank 3; proof strategy 9 | never run | none | B | encode Lemmas 7–8 and the twelve points in `sqpack/cover.py`; certify or exhibit the escape | none — either is a determination |
| 26 | Robust restricted-orientation theorem: all angles within 0.25° of `{0°, 45°}` forces side ≥ 3.878 | ideas row 39; H-036 (blocked, 0 rounds; prereqs Stromquist control, interval PoseBox) | never run | none | B | after row 25, interval-certify the angle neighbourhood | a packing with every angle within 0.25° of `{0, 45}` and side < 3.878 |
| 27 | Restricted-class chunk optimality: “no packing of ≤ K chunks with ≤ 2 tilt classes beats Trump”, certified per stratum | ideas row 50 (raw); BC-022 (agenda-002, blocked); BC-105 (agenda-010, tentative); X-010 Lane B rung B5; BC-096 (agenda-010, complete: exact LP at the full `n = 11` cell ≈ 1.4 s per pivot, float-seeded exact certification ≈ 2.6 s per stratum) | never run | none | B | sweep in float, certify winners exactly per stratum at `K ≤ 3` under the measured wall seatings | a stratum whose exact optimum beats Trump (a new record), or whole-class exact certification priced out (BC-096 says it is) |
| 28 | Stromquist’s Figure 14 falsified and repaired: `s(11) ≥ 2 + 4/√5` by a source-distinct point set | ideas rows 24, 44; H-010 (refuted, exp-016); H-041 (confirmed, exp-017); session-008 | produced result | T-010 | B | C4 by the pose-space interval audit at `2 + 4/√5` over the repaired twelve points (T-010 `next_rung`) | retired |
| 29 | Trump’s packing exactly valid at the degree-8 side | `cases/trump11/verify_exact.py`; evidence `E-n011-trump-upper`; H-038’s `n = 11` instance | produced result | T-011 | B | C4 by a second independent exact verification; V5 | retired |
| 30 | Publication rungs for T-018: C5, third-party package, proof card, external review, archival release | `results.yaml` T-018 `next_rung` and `review_artifact` (PR 78 adversarial review ported 2026-09-05, commit d83d8864); `cases/n11_fractional_certificate/thirdparty/` (c68c1616), `PROOF-CARD.md`, `t-018-proof.md` (b9587996, 9de1309a) | produced result (record) | T-018 at C5 | B | an outside mathematical review and an archival release | none |
| 31 | The angle optimum at the Trump cell is a kink (one-sided slopes 0.175 / 0.384) | ideas row 4a; H-019 (confirmed, exp-010) | produced result (no T-id) | none | B | none | retired — confirmed |
| 32 | Reference-cell two-angle value sheets `Φ_C(a₁, a₂)` at `n = 11`, then `n = 17` | ideas row 29; H-028 (blocked, 0 rounds) | never run | none | B | adaptive refinement on 2° class-angle boxes in the imported Trump cell | refinement fails to recover the published angles as the sole minimiser |
| 33 | Positive first-order growth in every independent class-angle direction at record cells | ideas row 26; H-027 (blocked, 0 rounds) | never run | none | B | minimum one-sided directional derivative at `n = 11` and `n = 17` | derivative below `10⁻⁴` side units per radian |
| 34 | `n = 11` at inflated δ as a continuous progress metric | ideas row 21 (shaped); H-013 is the search cousin | shaped only | none | B | define the fixed-side projection family; minimum inflation for a preregistered target-component hit rate | no hit at any inflation within budget |
| 35 | What the searcher finds at `n = 11`: histogram of local optima and tilt counts; two-tilt configurations unprompted | ideas “Open questions” bullets 2–3 | never run | none | B | a restart histogram at the baseline budget | either answer retires the question |
| 36 | Trump’s attraction mass and basin width | ideas row 7 and open question “How wide is Trump’s basin”; H-018 (refuted as stated, exp-005); H-012 at `n = 11` via BC-014 (agenda-001, blocked) | ran, no result | none | B | needs row 51’s terminal-component relation first | measured attraction probability above H-012’s threshold — the cartography premise fails and scaling the proposer is right |

### Program C — reach-table ladder

| # | direction | provenance | status | yield | program | next measurable step | kill outcome |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 37 | The generator instrument: covering LP by row generation, dual-driven column generation, exact event-cell sweep, interval decision, ceiling object | ideas row 23 / H-006 (registered ancestor, 0 rounds); X-010 rungs A0, A3; BC-160 (agenda-017, complete); `packing/src/sqpack/fractional/` (first commit 6e08a691 2026-09-04T03:28:18Z; `colgen.py` 0f5b80bc; `ceiling.py` c876ab12; `interval.py` 02f35ce7) | produced result | T-017, T-018, T-019, T-020 | C | rows 38–39 | none |
| 38 | Row-generation cost against the container side; site density as a function of side; the rationalisation scale | BC-191 (agenda-019, ready; “79–94 % of every round”, untuned grid 8.8× at `n = 20`’s side); SYNOPSIS “Current Handoff” selected next entry `think-ji0r`; X-013 §"The cost objection" | never run | none | C | BC-191 as written | none — a measurement |
| 39 | Move the generator’s accept-or-reject decision to the interval route (baseline now the integer sweep) | BC-190 (agenda-019, ready); X-013 proposal 1; ideas row 71 (this block); agenda-019 table: 22.7×, 44.2×, 31× | never run | none | C | re-fit both exponents at two further atom counts under an equivalence guard | the interval exponent drifts toward quadratic, or any single disagreement between the two routes |
| 40 | The exact sweep decides in integers, in parallel | BC-196 (agenda-020, complete: 68× at `n = 17`, 139× at `n = 20`, same least covered mass) | produced result (instrument; no bound moved) | none | C | none | retired |
| 41 | Retarget to `n = 26` at side ≈ 5.5218 | X-013 proposal 2; ideas row 72 (this block); BC-192, BC-194 (agenda-019, blocked on BC-190/191); `CERTIFICATE-REACH.md` n = 26: prize +0.4982, predicted gain +0.3987 | never run | none | C | BC-192 prices it, BC-194 runs it to convergence rather than a wall clock | a converged restricted optimum at 5.52 needing mass ≥ 26, or an attained ratio below 0.90 |
| 42 | The top-prize cases just above a perfect square: `n = 51, 68, 84, 39, 86, 66, 38, 83, 37, 53` | `CERTIFICATE-REACH.md` “Ranked by prize” (+0.5364 … +0.4983); X-013 cost table (`n = 51` ≈ 2.48× atoms; predicted gains +0.34 to +0.40) | never run | none | C | after row 43 supplies the seventh covering-value point | covering value growing faster than side² (row 43), or BC-191’s cost law prohibitive |
| 43 | Measure the covering value’s growth in the side: one genuinely converged restricted optimum past 5.5 | X-013 proposal 3; ideas row 73 (this block); `CERTIFICATE-REACH.md` reported-value table (seven reports in a 0.98-wide band, two unconverged) | never run | none | C | row 41 run to convergence; read the rate against ≈ 9–10 mass per unit side | none — acceleration retires the ratio extrapolation |
| 44 | The `n = 17` ladder: integral sixteen-point set, Massaccesi adoption, first-party 459/100 | T-001–T-003 (BC-101 agenda-010, BC-106 agenda-011; `cases/green17`); ideas row 56, 61; H-052 (confirmed, exp-049/052/056/059; BC-108, 116, 129, 137, 148–151); T-015/T-016 `produced_by` BC-150/session-083 (this block); T-019 (BC-161); `CERTIFICATE-REACH.md` n = 17 prize +0.0855 (HEAD), cap 4.6710 / +0.0810 (this block) | produced result | T-001, T-002, T-003, T-015, T-016, T-019 | C | a rung inside the retained margin 0.066920 (T-019 `next_rung`) | covering value ≥ 17 above 4.59; the packing-side cap 4.6710 (this block) bounds every rung |
| 45 | `n = 18` at 117/25 = 4.68 (and any bespoke `n = 18` rung) | T-019 `next_rung` (three site sets at exactly 18.000000, 157 rounds, 7056 s); agenda-019 “State at handoff”; T-016 `next_rung`; `CERTIFICATE-REACH.md` n = 18 prize +0.2329 (HEAD), cap 4.8216 / +0.2316 (this block) | ran, no result (stopped on cost) | none | C | separate “covering value ≥ 18” from “degenerate vertex” with the cheaper decision path of row 39 | a proved covering value ≥ 18 at 4.68 |
| 46 | `n = 19` beyond 24/5 | T-020 (`produced_by` BC-161 this block); `CERTIFICATE-REACH.md` n = 19 runway 0.0856 to the packing 4.8856; T-020 `next_rung` (a success above 4.885618 would contradict the retained packing) | produced result | T-020 (also T-016, T-019 earlier) | C | none beyond row 11’s run | capped by the best known packing |
| 47 | Green17 exact ceiling in `Q(√2)` (turn T-003’s bracket into an equality) | bead `think-iye2`; T-003 `next_rung`; agenda-016 rank 4; agenda-017 rank 10 “the generator supersedes the integral-set framing” | never run | none | C | none | retired de facto — dominated numerically by T-019 |
| 48 | Generic weighted-point certifier and sound LP candidate pipeline from the fixed-certificate code | BC-115 (agenda-012, blocked on a reviewed adoption and a named second consumer) | never run (superseded) | none | C | re-scope onto `sqpack/fractional` or close | superseded by row 37 |

### Program D — search and cartography

| # | direction | provenance | status | yield | program | next measurable step | kill outcome |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 49 | LP-in-cell quench with bracketed angle search (the polisher every proposer runs on) | ideas rows 1, 4b; H-002 (refuted as a universal claim, confirmed per cell: exp-006–009, exp-031); BC-008 (agenda-001) | ran, no result (instrument works as a polisher, 1.1–1.3× on annealer output) | none | D | none — instrument | retired as a rescue; kept as the spine |
| 50 | Terminal-component identity relation and endpoint identifiability ("what is a basin") | ideas row 2 (shaped); H-021 (blocked after 14 rounds, exp-018–032); H-009 (0 rounds); BC-009, BC-011 (agenda-001); BC-046/080/082/083 (agendas 005–008); X-005 (contact + closure the sole survivor), X-006 (candidate `n = 5` control); D-034 | ran, no result | none | D | BC-010: the final bounded `n = 5` discriminator with a matched `n = 10` transfer (X-011) | no relation separates the labelled controls, or no transfer to `n = 10` — X-011 parks the lane |
| 51 | `n = 5` terminal connectivity: are the equal-side endpoints one family | H-023 (open question, 12 rounds exp-033–045: exact face, angle-and-slide sheet, first-order cones, −W obstruction); BC-010 (agenda-001, ready); BC-029/036/037 (agendas 003–004); ideas row 37 | ran, no result (no terminal decision) | none | D | BC-010 as written | X-011: another open-ended local-geometry series is not defensible; park without transfer |
| 52 | Exact quotient topology of the optimal sets at `n = 3 … 6` | H-032 (open question; exp-014/015 solved `n = 3, 4` in 1.28 s); ideas row 37; BC-001/002/009 | ran, no result (`n = 3, 4` solved exactly in exp-014/015; `n = 5, 6` open) | none | D | the `n = 5` quotient after row 51 | none |
| 53 | Basin atlas as a soft-schema artifact | ideas row 3 (shaped); SYNOPSIS “The map layer — built, not admissible” | shaped only (built, not admissible) | none | D | needs row 50 | the relation stays undefined |
| 54 | Census the `n ≤ 10` landscape to saturation | ideas row 5; H-011 (blocked, 0 rounds; prereqs H-002, H-021, H-023); BC-012, BC-013 (agenda-001, blocked) | never run | none | D | after row 50 | the coverage model is unstable on the proved ladder |
| 55 | Record basins are rare in quench measure — the cartography premise | ideas row 6; H-012 (blocked, 0 rounds); BC-014 (agenda-001, blocked); SYNOPSIS “The cartography premise is still untested” | never run | none | D | measured attraction probability of the `n = 10` optimum, then Trump’s component | probability not below the threshold — scaling the proposer is right after all |
| 56 | Saturation curves as a coverage estimator | ideas row 8; H-007 (blocked, 0 rounds); BC-012 | never run | none | D | after row 50 | no held-out-stable coverage model |
| 57 | False-basin rate `r(n)` | ideas row 9; H-008 (blocked, 0 rounds) | never run | none | D | retained witnesses through an independent stronger verifier | none — zero is a legitimate result |
| 58 | Contact count predicts attraction frequency | ideas row 10a; H-003 (blocked, 0 rounds) | never run | none | D | held-out predictor test on the proved ladder | no monotone relation |
| 59 | Adaptive multilevel splitting for rare target events | ideas row 32; H-029 (blocked, 0 rounds); BC-014 | never run | none | D | exact synthetic controls, then one `n = 10` target event | fails the synthetic controls or under 4× efficiency |
| 60 | Calibrated extreme-value sensitivity analysis on a fixed-budget endpoint sample | ideas row 28 (raw) | shaped only (raw) | none | D | none | the archive is too small (ideas row 28) |
| 61 | Angle-class two-level search | ideas row 11; H-001 (blocked, 0 rounds; prereq H-002) | never run | none | D | paired comparison on `n = 5, 10, 17, 11` | no fewer pair-tests to the target component |
| 62 | Record angle-class count and effective orientation compression | ideas rows 11a, 11b, 33; H-024 (unresolved, exp-012); H-042 (refuted, exp-037: six classes at `n = 29`); H-025 (blocked, 0 rounds) | ran, no result | none | D | H-025 refit on the imported corpus | under 80 % of records retain quality with three fitted classes |
| 63 | δ-continuation from an inflated container | ideas row 12; H-013 (blocked, 0 rounds); BC-014; BC-033 (agenda-003, blocked proposer interface) | never run | none | D | after BC-033’s interface | no more target-component arrivals than multistart at equal work |
| 64 | MAP-Elites over mechanism descriptors | ideas row 13; H-015 (blocked, 0 rounds); BC-033 | never run | none | D | after BC-033 | under 1.5× distinct components per pair-test |
| 65 | Neighbour-transfer seeding from `n ± 1` records | ideas row 14; H-004 (blocked, 0 rounds); BC-014 | never run | none | D | equal-budget `n = 11` comparison | median side not ≥ 0.01 lower than cold starts |
| 66 | Superdisk continuation from circles | ideas row 15; H-014 (blocked, 0 rounds) | never run | none | D | last in line (needs new geometry) | no components unreachable by a direct proposer |
| 67 | Stock annealer at the baseline budget | ideas row 16; H-016 (refuted, exp-001–004); BC-015 | ran, no result (refuted; the series baseline) | none | D | none | retired |
| 68 | Same annealer at 100× budget | ideas row 17; H-017 (open, 0 rounds); X-011 “routes to avoid: the registered 100-times annealer” | never run (parked) | none | D | only behind a short budget-response ladder | parked by X-011 |
| 69 | Billiard / inflation proposer | ideas row 18 (raw); search strategy 11 | shaped only (raw) | none | D | none | none |
| 70 | LLM-proposed constructor DSL evaluated by LP + exact check | ideas row 19 (raw) | shaped only (raw) | none | D | sequenced behind a verified atlas | none |
| 71 | `s(17)` as the mechanism-matched search calibration; the annealing race at the ten annealed sizes | ideas row 20; H-020 (refuted, exp-011: grid on five of five seeds); BC-090 (agenda-009, tentative, gated); X-009, X-010 “parked” | ran, no result (refuted; race gated) | none | D | an instrument that reaches `s(17)` within `10⁻⁴` on one seed of five (the BC-090 gate) | the gate itself |
| 72 | Load-guided block moves from the LP dual | ideas row 25; H-031 (blocked, 0 rounds) | never run | none | D | paired kernel test at `n = 10, 17` | under 2× to the target scores |
| 73 | Active-cell neighbour walk instead of resampling | ideas row 43; H-040 (blocked, 0 rounds) | never run | none | D | known-answer `n = 5` control, then `n = 10` | under 2× new cells per LP solve |
| 74 | One proposer interface at equal counted work; pair-tests / counted LP solves as the budget currency | ideas row 4 (shaped); BC-033 (agenda-003, blocked); BC-017 (agenda-002, ready); D-126 | shaped only | none | D | BC-017: price a stratum in counted LP solves | none |
| 75 | Stratified chunk enumeration pipeline (stage-1 enumerator, glued rows, class-angle sweep) | ideas row 46 (shaped); X-003; BC-016, BC-018 (agenda-002, blocked); BC-095 (agenda-010, complete: raw 4.357e20 at `K ≤ 6`, orbit floor 2.763e18, a `K ≤ 3` slice tractable); BC-104 (agenda-010, tentative); BC-092 (agenda-009, stopped); X-010 Lane B rungs B0–B4; D-406 | ran, no result (priced only) | none | D | BC-104 at `K ≤ 3` under the measured wall seatings | the proved controls are not reproduced from enumeration alone (BC-018) |
| 76 | Chunk-grammar rediscovery ladder (`n = 5, 10`, then one shot at `n = 11`, `n = 16` guard, `n = 17` differentiator) | ideas row 47; H-045 (blocked, 0 rounds); BC-018, BC-021 | never run | none | D | after row 75 | the frozen grammar does not rank the standing best first at `n = 11`, or fails the `n = 16` guard |
| 77 | Trump predecessor continuation from `0°` to `40.18°` | ideas row 48; H-046 (blocked, 0 rounds); BC-020 | never run | none | D | 0.01° sweep on the built quench | an infinite LP value at some step (chunk fission needed) |
| 78 | Chunk expressibility of the record corpus at `K ≤ 6` | ideas row 49; H-044 (unresolved, exp-046: 23/30 = 0.7667 or 3/10 = 0.30 against 80 %); BC-019, BC-100; X-008 (the residue is 109 axis-aligned components) | ran, no result (criterion missed) | none | D | a grammar move for axis-aligned polyominoes, then re-measure | already missed as registered |
| 79 | Chunk-regular predecessors as a coordinate system (round trip) | ideas row 51; H-047 (blocked, 0 rounds); BC-025 (blocked, manual condition) | never run | none | D | round trips on records and ordinary endpoints | under 70 % return |
| 80 | Glued-chunk screen fidelity | ideas row 52; H-048 (blocked, 0 rounds); BC-026 | never run | none | D | screen on the proved `n = 5, 10` cells | the soft-mode winner leaves the top decile |
| 81 | `n = 71` angle merge: is the 0.0358° two-class split load-bearing | ideas row 55; H-050 (blocked, 0 rounds; gated on BC-090); X-009 kill conditions | never run | none | D | bracketed single-angle LP sweep of the sixteen-square block | a merged-angle configuration below 8.94407 refutes it (a record lead); otherwise confirmed and priced |
| 82 | `n = 90` primitive: twenty squares squeezable in `4 × 6` (also `s(30) < 6`) | ideas row 54; H-049 (blocked, 0 rounds); BC-091 (agenda-009, narrowed by X-009); BC-178 (agenda-018, blocked); agenda-017 rank 8 | never run | none | D | build the rectangle-squeeze instrument with Arslanov’s two-sided calibration; decide the declared structure class | refusal by lemma over the declared class — closes the decomposition route at `m = 10` |
| 83 | Cleemann-style 3-4-5 construction at `n = 97` (`n = 78` diagnostic) | ideas row 22; H-005 (blocked, 0 rounds) | never run | none | D | one exact construction check | side not strictly below 10 |
| 84 | Finite transfer of the 2025–26 asymptotic primitives at `100 ≤ n ≤ 324` | ideas row 36; H-035 (blocked, 0 rounds) | never run | none | D | one preregistered parent | no parent improved |
| 85 | Public-parent surgery reproducing UnitSquare children; blinded `n = 68` pilot | ideas rows 34, 60; H-030 (blocked, 0 rounds); H-051 (blocked, 0 rounds); BC-113 (agenda-012, stopped); BC-050 (agenda-005, blocked: no surgery-grade witness) | never run | none | D | after row 97 supplies a surgery-grade pose | fewer than two of six children reproduced (H-030); the pilot’s own hit rule (H-051) |
| 86 | Dead ends: the `14 + 20 = 34` isostatic count; GPU population search; fixed-side shrink-and-re-anneal; squared overlap penalty | ideas “Dead ends” (four bullets, lines 259 ff.) | dead | none | D | none (GPU only at large `n`) | killed without a round |

### Program E — instrument and record infrastructure

| # | direction | provenance | status | yield | program | next measurable step | kill outcome |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 87 | General unavoidable-set certifier and escaping-pose falsifier (`sqpack/cover.py`, `sqpack/falsify.py`) | BC-093, BC-094 (agenda-010, complete, session-054); X-010 rung A0 and weak points 1, 2, 5; bead `think-yrvm` | produced result (instrument) | T-001, T-002, T-004, T-005 through it | E | consume the shared `sqpack.field` layer (X-010 weak point 5) | none |
| 88 | Pose-space interval audit (exhaustive branch-and-bound over `(x, y, θ)`) | `cases/green17/interval_audit.py` (BC-106, commit 5af3a486); T-001 C4, T-003 | produced result | T-001 (C4), T-003 | E | generalise to `Q(√2, √3)` for T-004 and run at `2 + 4/√5` for T-010 | none |
| 89 | The fractional-certificate decision path: exact sweep, interval route, retention gate `devtools.decide_certificate`, detectors `check_rung_figures`, `check_case_prose`, `check_nagamochi_bounds` | agenda-017 Lane A; `docs/project/handoff-2026-09-04-block-close.md` §"The instrument"; D-434, D-439–D-443 | produced result | C4 on T-017–T-020 | E | rows 38–39 | none |
| 90 | Third-party validation package, proof card, and proof document for T-018 | `cases/n11_fractional_certificate/thirdparty/` (c68c1616), `PROOF-CARD.md`, `t-018-proof.md`; commits 2026-09-05 | produced result (record) | T-018 at C5 | E | none | retired |
| 91 | Interval certification bridge (Krawczyk operator, witness contract) and the `n = 29` interval certificate | BC-052, BC-053, BC-057 (agenda-006, complete); `cases/kingbird29/certify_interval.py` (24a7dd04); D-431 outstanding | produced result | T-009 | E | C4 by exact-algebraic confirmation of the same witness (T-009 `next_rung`) | none |
| 92 | Exact algebraic characterisation of the `n = 29` record | X-004 (four unregistered candidates); BC-042–048, BC-054, BC-059–061, BC-065–067, BC-070–073 (agendas 005–006: Bézout 1,039,500; BKK 15,744; integer-relation refusal at the supported degree); H-038 | ran, no result (exact solve not reached) | none | E | X-004 candidates 1–2: elimination or integer relation at a declared degree bound | the refusal at the supported degree stands (BC-073) |
| 93 | Exact LP over certified rational or algebraic coefficients (the D-021 fix) | BC-048, BC-061 (complete); `sqpack/exact_lp.py`; BC-096 cost measurement | produced result (instrument) | none | E | consumed by row 27 | none |
| 94 | Rational or exact promotion of the ten open cases whose verified upper bound sits at the grid, and T-009 to C4; recognition of the 13 trailing published-exact-side cases | BC-165, BC-166 (agenda-017, never opened); BC-089 (agenda-009, ready: X-009’s sweep found 14 of 15 verify exactly); bead `think-d0j1` | ran, no result (swept, never retained) | none | E | BC-165 as written | none |
| 95 | Generic interval certifier end to end: reproduce T-009 generically, then `n = 37`, `n = 39` | BC-184 (agenda-018, tentative); H-056 (blocked, 0 rounds); bead `think-mvrq` (square-subsystem selector, X-010 weak point 4) | never run | none | E | wire the generic path and replay `n = 29` | fails to reproduce T-009 through the generic path |
| 96 | Cross-scale exact/interval construction ladder `18 → 50 → 54 → 39 → 55` | ideas rows 57, 63, 64, 65, 68; H-054 (unresolved, exp-048/050: typed E1 source-semantics refusal); H-059 (confirmed, exp-055); H-055 (blocked; BC-126, BC-131, BC-141); H-056; BC-110, BC-114, BC-118 (agendas 012–013) | ran, no result (typed refusals) | none | E | the `n = 50` source-semantics seam BC-118 named | the refusal stands at source availability |
| 97 | UnitSquare `n = 68/69` parent-child rigid-pose serialization bridge | ideas rows 58, 62, 67; H-053 (blocked, exp-047/051); H-058 (unresolved, exp-054/057); BC-109, BC-117, BC-124, BC-130, BC-138, BC-139 (agendas 012–015); BC-050 | ran, no result (typed refusals) | none | E | provenance for the six-decimal coordinate rule (BC-138’s refusal) | the provenance never appears — the typed refusal is terminal |
| 98 | Independent accumulation of the fixed Massaccesi certificate | ideas row 61; H-052 (confirmed, exp-049/052/056/059); BC-108, BC-116, BC-129, BC-137, BC-148, BC-149 | produced result | T-015, T-016 (adoption via BC-150/151) | E | none | retired |
| 99 | Parent-bound three-process runner for the H-052 residue | ideas row 66; H-057 (unresolved, exp-053: contaminated timing); BC-123 (agenda-014, stopped) | ran, no result | none | E | none — exp-059 completed serially | retired |
| 100 | Generalised local-rigidity instrument (multi-branch contacts, 120 variables, degree-8 field) | `packing/src/sqpack/local_rigidity/` (ddeddb33); BC-175 (agenda-018, blocked) | never run | none | E | BC-175 as written | the chart does not build in minutes at 120 variables |
| 101 | Results register, epistemics rubric, evidence and defect registers | BC-107 (agenda-011, complete; `results.yaml` created d976e9f3 2026-08-31); `devtools/check_results.py`; this block adds `produced_by` for T-014–T-020 only | produced result (record) | every T-id’s rungs | E | `produced_by` for T-001–T-013; a hypothesis on T-015/016/019/020 | none |
| 102 | Agenda map, discharge edges, queue hygiene | BC-081 (agenda-008); BC-097 (agenda-010, ready: 25 stale `in_progress` beads, gap ranking on a durable surface); `devtools/gap_ranking.py` | ran, no result (partial) | none | E | BC-097 | none |
| 103 | Validation gate tiers and the unattended runner’s trust boundary (W9: D-044, D-046) | BC-075/079/084/086; BC-154 (agenda-016, stopped-achieved), BC-167 (agenda-017, never opened), BC-179 (agenda-018, blocked); BC-168 snapshot cap fixed; BC-180 slowest step; BC-142 test selection; BC-169 (push tier’s 900 s timeout) | ran, no result (mixed) | none | E | BC-179 wave two | none |
| 104 | Record-geometry corpus import for every `n ≤ 100` | ideas row 53 (shaped); BC-023 (agenda-002, complete) | produced result (record) | none | E | none | retired |
| 105 | Dated record-event and reproducibility corpus | ideas row 59 (shaped) | shaped only | none | E | none scheduled | none |
| 106 | Primary-source recovery and literature audits (Green 2000 private communication; Plakhta, D-139; `s(11)` literature audit) | BC-031 (agenda-003); X-010 rung A2 rationale; commit f68bad68 2026-09-05 | ran, no result (partial) | none | E | none scheduled | none |
| 107 | Proof-assistant port (V5) of any retained result | proof strategy 18 (`not_applied`); X-001 source `research-2026-08-22-lean-for-packing-proofs-and-validation.md`; `next_rung` of T-001, T-004, T-010, T-011, T-012, T-014, T-015 | never run (never scheduled) | none | E | port one rational-data result (T-010 or T-017) | none — a gap (see `gaps.md`) |
| 108 | Reach-table renderer and the ceiling instrument (`ceiling_side`; this block adds the packing-side `cap`) | `CERTIFICATE-REACH.md` (ee29501f 2026-09-04); `devtools/render_certificate_reach.py`; `sqpack.fractional.certificate.ceiling_side` | produced result (targeting instrument) | none | E | import tilt inventories for the cases whose `cap` shows `—` (this block) | none |

### Program F — other

| # | direction | provenance | status | yield | program | next measurable step | kill outcome |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 109 | `n = 5` second-order and fixed-side local rigidity of Göbel’s optimum | ideas row 69; BC-049 (agenda-005, still `ready`), BC-063 (agenda-006); X-007; H-060 (confirmed, exp-058); BC-152, BC-153 (agenda-016); X-012; T-014 `produced_by` H-060/BC-152/session-083/exp-058 (this block) | produced result | T-012, T-014 | F | V4 by mechanising the closing steps or V5; reach the printed BCR page (T-014 `next_rung`) | retired |
| 110 | `n = 40` infinitesimal flexibility and the admissible cone past dimension 45 | T-013; D-391; BC-183 (agenda-018, tentative); agenda-018 “priced at three hours with a coin-flip chance” | produced result | T-013 | F | characterise the cone on the disjunctive system | too few functionals pinned — only a conditional theorem |
| 111 | General fixed-side local-rigidity theorem from X-012’s method | BC-163 (agenda-017, never opened); BC-175 instrument | never run | none | F | the write-up BC-163 asks for | none |
| 112 | `n = 28` rigidity (the catalogue’s fourth “Rigid.” annotation) | BC-049 remainder ("`n = 28` is untouched and its optimum is not in Goebel’s family", ledger sessions 045–047) | never run | none | F | assess through row 100 | none |
| 113 | Close the asymptotic waste exponent gap `1/2` versus `3/5` | ideas row 40; H-037 (open question, 0 rounds); BC-034 (agenda-003, complete: Bui §3.1 index proof and Lemmas 3–5 packet); X-010 “parked” | ran, no result (parked) | none | F | audit Bui §4.2 Lemma 6’s recurrence (BC-034 `next_evidence`) | parked by X-010 — nothing here contributes differentially |
| 114 | Classify the number fields, elimination systems, and mechanism associations of verified record witnesses | ideas row 41; H-038 (open question, 0 rounds); X-004 | never run | none | F | after row 92 | none — a failed degree law is retained |

### Row counts

A 13 (rows 1–13) · B 23 (14–36) · C 12 (37–48) · D 38 (49–86) · E 22 (87–108) · F 6
(109–114) · **total 114** (counted from this file’s table rows; numbering is contiguous
and every row’s program column matches its section).

By the status column’s leading phrase: produced result 25, ran no result 24, never run
52, shaped only 12, dead 1 (row 86 merges the ideas board’s four dead ends).
Of the 25 “produced result” rows, 18 name a T-id in the yield cell (rows 1, 7, 11, 14,
28, 29, 30, 37, 44, 46, 87, 88, 89, 90, 91, 98, 109, 110 — five of them instruments
credited “through” them: 87, 88, 89, 90, 98) and 7 are instruments, records, or frontier
fields with no T-id (rows 17, 31, 40, 93, 101, 104, 108).

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
