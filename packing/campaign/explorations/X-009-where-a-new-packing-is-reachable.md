---
title: X-009 — where a new packing is actually reachable, and what runs first
softschema:
  contract: packing.squares:Exploration/v1
  schema: ../schemas/exploration.schema.yaml
  envelope: exploration
  status: enforced
exploration:
  id: X-009
  title: Where a new packing is actually reachable, and what runs first
  date: '2026-08-31'
  author: Claude (agent), under BC-088 in agenda-009, run as phase 3 of session-049
  campaign: packing.squares
  brief: >-
    BC-088 asked where a new packing is reachable given machinery the research queue
    predates, and in what order the attempts should run. Four read-only investigations
    (three returned in time to be used) plus one first-hand exact verification answer it.
    The order is recognition first, the narrowed grid question second, search third and
    gated, generative enumeration folded into the search instrument. The reasons are
    measurements: 14 of the 15 trailing published-exact-side cases verify exactly at
    their published side -- one of them re-verified first-hand here, 82 squares in side
    6 + (5/2)sqrt(2) decided by exact_sign with a firing negative control -- while the
    stock annealer's one mechanism-matched calibration (exp-011, n = 17) returned the
    grid on five of five seeds, and the grid family's only defensible entry reduces to
    one finite primitive question at n = 90. Sub-agent findings are marked as report
    evidence pending in-repo replay; nothing is promoted by this document.
  sources:
  - packing/campaign/agendas/agenda-009-pipeline-hygiene-and-the-search-reassessment.md
  - packing/campaign/series/series-000-smoke-and-calibration/experiments/exp-011-h-020-n17.md
  - packing/campaign/series/series-000-smoke-and-calibration/experiments/exp-001-baseline-sweep.md
  - packing/campaign/series/series-000-smoke-and-calibration/experiments/exp-005-basin-entry-n11.md
  - packing/resources/papers/friedman-ds7-packing-unit-squares-in-squares.md
  - packing/resources/papers/arslanov-improved-packings-n-n-1.md
  - packing/resources/web/kingbird-squares-in-squares.md
  - packing/resources/web/kingbird-squares-in-squares-compared.md
  - packing/witnesses/prospective/n-110.yaml
  - packing/cases/gobel_family/packing.py
  - docs/project/research/research-2026-08-23-search-philosophy-and-landscape-cartography.md
  proposes: [H-049, H-050]
---
# X-009 — Where a New Packing Is Actually Reachable, and What Runs First

**Date:** 2026-08-31

**Status:** W3 synthesis under `BC-088`, phase 3 of `session-049`. It sequences the four
candidate blocks of `agenda-009` and registers two hypotheses.
It promotes nothing and adjudicates nothing.

**Owns:** the sequencing argument.
The measurements it rests on are owned by the artifacts in `sources`; the sub-agent
reports it cites are session-049 delegation evidence under `OR-2` — evidence, not
verdicts — and every claim taken from one is marked below.

## The Answer

Run the blocks in this order:

1. **`BC-089` (recognition) first**, immediately, as the session’s own next slice — and
   paired with the rational-promotion sweep the machinery inventory surfaced, which
   moves the same frontier for under a minute of compute.
2. **`BC-091` narrowed to one construction question at `n = 90`** — not a 31-case survey
   — plus two record repairs it surfaced.
3. **`BC-090` (search) third, and gated**: no search runs until an instrument beats the
   already-measured calibration failure at `n = 17`.
4. **`BC-092` (generative contacts) folded into `BC-090`’s instrument design** rather
   than run as its own block.

## Why Recognition Is First

`BC-089` was listed first on a hit rate of two (`D-389`, `D-398`). The investigation
raises that to a measured claim about the whole block: **14 of the 15 open cases with a
published exact side admit an exactly verified feasible packing at that side today**
(sub-agent report; per-case table in the session-049 delegation record).
Eight follow from a published construction rule alone — Göbel’s diagonal strip at
`n = 27, 38, 52, 67, 84`, one L on the already-built family pose at `n = 82`, Friedman’s
off-centre rule at `n = 26, 85` — and six more lift from the retained witness into the
field the published side names (`n = 18, 19, 50, 54, 66, 86`). `n = 53` alone refuses:
two of its four tilt classes yield no stable algebraic relation at 49 retained digits,
so it moves to `BC-090`’s pool, exactly as `BC-089`’s exit anticipated.

One of the fourteen is **verified first-hand, in this repository, this session**:
`cases.gobel_family.build(4, 5)` plus a seventeen-square L packs 82 unit squares into
side `6 + (5/2)·sqrt(2)`, decided by `verify_packing` under `exact_sign` over
`Q(sqrt 2)` with zero failures, and an eighteenth L square is refused — the same
mechanism, replayed against the tree, with its negative control firing.
That is why the report’s remaining thirteen are treated as probably right and still
individually replayed before any record moves.

A recognition hit is not a new packing.
It is a published result made exact and verified here, and its record entry carries that
novelty basis.
What it moves is the *verified* frontier: each hit replaces a grid ceiling
with an exact ceiling at the published side, about `0.3` to `0.5` per case, roughly
`3.9` in total across the fourteen.
It also retires the cheapest explanations for the gap between reported and verified,
which is what makes the later search blocks honest: after `BC-089`, a case that still
trails is trailing for a real reason.

The report also corrects a framing error in `BC-089`’s own entry, worth keeping: `D-402`
refused contact-structure extraction from padded decimals, and `BC-049` measured
`reach_degree = 0` for unknown-degree minimal-polynomial recovery.
Neither forecloses lifting coordinates into a **known** field — the operation the six
witness-lift cases need — because feasibility at a stated side is provenance-free once
an exact verifier accepts it.

## Why the Grid Block Shrinks to One Question

The grid investigation (sub-agent report, session-049 delegation record) reduces
`BC-091` from 31 cases to one attempt, one parked proof target, and two record repairs.

Re-indexed by `k = m² − n`, the 31 open grid cases are exactly the staircase `3 ≤ k ≤ m`
for `m = 4..10` minus Bentz’s four proved `k = 3` cases, and over the whole retained
catalogue to `n = 324` **nobody has ever beaten a grid at `k ≤ m − 2`**. The frontier of
the `s(m² − m) = m` conjecture, though, has been moving: bounded to `m < 17` (Cleemann),
`m < 16` (Hajba 2015), `m < 12` (Arslanov 2019), and — retained in the Kingbird archive
but recorded nowhere in this repository’s frontier — **`m < 11` (Cantrell, February
2025)**, whose `n = 110` pose this repository already holds as a numerically checked
prospective witness.

So the one defensible attempt is **`n = 90`** (`m = 10`, `k = m`), and Arslanov’s
rectangle-decomposition mechanism turns it into a finite question: his scheme fails
below `m = 12` only because his smallest squeezable primitive is `δ((4,8), 26)`; a
`10 × 10` decomposition needs a squeezable packing of **20 unit squares in a `4 × 6`
rectangle**, and nothing else.
That is `H-049`, registered by this document.
The 29 other cases are absorbed as hard-open on the staircase measurement, and `n = 61`
stays parked as the proof-lane target `H-033` already names.

The two record repairs, filed as beads rather than fixed here because both touch claims
outside a W3 phase’s authority to adjudicate: the `n < 17` boundary quoted in
`SYNOPSIS.md` and `frontier/n-012.md` is stale by three improvements, and Friedman DS7’s
Table 2 carries lower bounds above the frontier’s at 23 open cases — a reconstructed
table, so adopting any of it needs a `W2` read of the primary first.

## Why Search Is Third, and Gated

The one mechanism-matched calibration of the stock annealer has already run and failed:
`exp-011` at `n = 17`, the smallest oblique record, returned exactly `5.0` — the grid —
on five of five seeds, a gap of `+0.324` against Bidwell’s `4.67553`. `exp-005` showed
the refiner cannot hold a known record basin it is handed (0 of 40 returns from `1e-3`
off Trump’s pose), and `exp-001` fell `+3.7e-2` short at `n = 11`. **A search that
cannot leave the grid basin where a much better packing is known cannot be argued to
beat an incumbent where none is.** So `BC-090` opens with a calibration kill, not a
target: the instrument must reach `s(17)` within `1e-4` on at least one of five seeds at
declared budget, or the block closes as a measured negative for the price of one run.

If the gate passes, the target is **`n = 71`**, on the only external evidence of its
kind in the ten annealed cases (sub-agent report, from the Kingbird compared pages):
Schadt’s from-randomness run plateaus at `8.95539101419843` while the record,
`8.94407155757031`, descends from a constructed seed — cold search is *recorded* failing
there, which is precisely the condition under which a differently informed search has
room.
The incumbent also splits sixteen squares across two angle classes `0.0358°` apart;
whether that split is load-bearing is `H-050`, decidable by a bracketed fixed-angle LP
sweep above the measured `1e-11` solver floor (`D-021`), with any apparent gain below
`1e-8` read as failure.

`n = 29` stays the certification target rather than a beat target, and `n = 28` — the
tightest structure in the set, with zero movable squares — is recorded as the shape of
the expected negative.

## Why Generative Enumeration Is Folded In

`BC-092` asked whether the contact grammar can generate candidates rather than describe
retained ones.
The enumeration price is already measured at the wrong order of magnitude:
`9.3e9` raw orbit work at `n = 5` (contact-enumeration pricing), against target sizes
ten times larger. What the structural corpus is good for at `n = 71` is *proposal
information* — which contact shapes recur, which angle-class structures carry records —
and that is an input to `BC-090`’s instrument, not a separate enumeration block.
The review answers the agenda’s closing question — one block or two — with: one, and
`BC-090` owns it.

## What Would Have to Be True, and How the Attempt Knows It Failed

For **`n = 90`** (the specific case `BC-088`’s exit requires): a new packing exists if
20 unit squares pack in a `4 × 6` rectangle with positive squeeze (`H-049`), because
Arslanov’s decomposition then assembles `36 + 8 + 26 + 20` squares into side strictly
under `10`. The attempt knows it failed when the primitive’s candidate structures are
exhausted with no positive squeeze — a refusal by lemma, closing the decomposition route
at `m = 10` outright, not a budget running out.
For **`n = 71`**: the four kill conditions in the session-049 delegation record, in
ascending cost — the `s(17)` calibration gate, basin retention on the retained witness,
the `H-050` angle sweep, and a pre-declared budget in LP solves rather than wall-clock
(`D-126`).

## What the Machinery Inventory Adds

The fourth delegation returned while this was being written, and three of its measured
findings sharpen the sequencing without changing the order.

**Certification is seconds; search is the whole bottleneck.** Its own cold run of the
annealer returned the trivial grid at `n = 29`, `41` and `51`, while
`packing-witness promote --strategy robust-rational` took a quench pose at `n = 11` to
an independently verified exact rational upper bound in about eleven seconds.
That confirms `BC-090`’s gate from the other side: the proposer, not the pipeline, is
what does not exist.

**A sweep the queue never named.** 34 of the 36 decimal known-best witnesses promote to
exact rational certificates in 33 seconds of compute (report measurement), each within
`~1e-9` to `~1e-30` of its reported side, while nine of the ten annealed sizes still
carry the trivial grid as their verified ceiling.
Running that sweep and retaining the certificates is the largest available movement of
the verified frontier per unit work anywhere in the queue, and it belongs inside
`BC-089`’s slice: the recognition builds then replace relaxed rational ceilings with
exact ones at the published sides where a rule exists.
Recording is not promotion — each `verified_upper_bound` move remains a reviewed change
under the evidence contract.

**A calibration question under `D-402`.** The report measured that inside declared
precision, with the retained tolerance sign, contact extraction reproduces both known
structures exactly (`n = 11`: 14/20; `n = 29`: 52/37), and that the pricing tool’s
`reproduced: false` came from reading the finest deciding floor — the padding window its
own docstring warns about — with an exact-zero sign the retained extraction never used.
`D-402`’s substantive finding stands (a floor below declared digits reads padding, and
the guard comparing floor to declared digits is still missing), but the derived claim
that decimals cannot yield structure needs that calibration re-run before anything is
sequenced on it. Filed as a bead rather than adjudicated here.

## Corrections (2026-08-31)

Two figures above did not survive first-hand re-measurement; both are recorded as
defects, and X-010 carries the corrected sequencing input.

- The entry measurement repeated from `BC-088` — a best-known-to-proved gap of “about
  0.5 for every open case” that therefore “ranks nothing” — is unmeasured and wrong by a
  factor of ten: the spread is 0.056 to 0.536, structured by `k = m² − n` (D-404).
  `devtools/gap_ranking.py` now carries the measurement.
- The enumeration price quoted against `BC-092` ("9.3e9 raw orbit work at `n = 5`")
  traces to no artifact; the recorded size-five atlas gives 1,533,696 coloring
  candidates collapsing to 11,013 orbits, a 139× quotient the price never applied, and
  the realizability prefilter is unpriced (D-405). The fold of `BC-092` into `BC-090` is
  therefore unproved in both directions; X-010’s Lane B reprices it.

## What This Document Does Not Establish

The thirteen recognition cases not replayed here remain report evidence until each is
rebuilt and verified in-repo; the machinery report’s sweep and calibration measurements
are likewise report evidence until replayed; the Table 2 lower-bound question is opened,
not answered; and no statement here bears on optimality anywhere — every reachable move
above is an upper-bound move.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
