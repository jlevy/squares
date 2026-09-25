# Plan: What R052 and Rung 0 Change at n = 11 and n = 17

**Date:** 2026-09-25 · **Workflow:** W10 review, planning and oversight · **Session:**
[159](../../../../packing/campaign/agent-sessions/session-159-n17-guzhou-r052-intake.md)
· **Agenda:**
[agenda-042](../../../../packing/campaign/agendas/agenda-042-overnight-n11-settlement-and-low-n-angles.md),
BC-385

The owner asked for an extra planning block after R052 was integrated, to decide what
else the new n = 11 and n = 17 results make possible.
Two Fable max assessments ran in parallel, one per case, each reading the record and
running at most ten minutes of probes.
This document keeps their evidence and the decisions the coordinator took from them.
Nothing in it moves a bound.

## Where Things Stand

- **n = 17.** Guzhou0806’s R052 is the verified lower bound, `s(17) > 231001/50000`, at
  `V4/C3` ([review](../../reviews/review-2026-09-25-n17-guzhou-r052.md)). Bidwell’s
  packing at `4.67553…` is about `0.0555` above it.
- **n = 11.** `31/8 < s(11) ≤ U`, with Kleddamag’s bound at `V4/C4`. Rung 0 of the
  settlement ladder is closed (T-035, T-036). Rung 1 is priced out with the present
  relaxation (exp-234), and BC-384 owns the stronger per-node bound it needs.

## What the Assessments Found

### n = 17: the certificate family is nearly converged

These are numerical readings of R052’s own ledger and certificate, from probes kept in
`attic/planning-159/n17/`.

- **Saturation.** 14,986 of R052’s 15,721 rows are within a relative `10^-3` of the
  binding charge `Γ`, and the largest slack anywhere is `1.4×10^-3`. Reweighting the
  same dictionary could buy at most about `+0.0014` in side.
  The row catalogue is also spent: cores sit within `7×10^-8` to `7×10^-5` of their
  parents.
- **The public ladder is flattening.** Its steps are `+5.6×10^-3` for adding thresholds
  and the parent core, then `+4.6×10^-5`, `+4.6×10^-5`, `+4.6×10^-6`, and `+1.3×10^-4`
  for about twice the dictionary.
  A first-party certificate that adds `10^-4` is not worth building.
- **A ceiling lemma, derived but not yet reviewed.** Every atom R052 and Kleddamag use
  has capacity one, and two cores that trigger a capacity-one atom share a site, so they
  overlap. Suppose `N` unit squares fit in `[0,S]²` at any angles and no three of them
  overlap pairwise. Then giving each square the dual weight ½ is feasible for every such
  certificate, and `N = 34` refutes every point or capacity-one certificate at side `S`.
  R052 itself proves no such family of 34 fits at `4.62002`. Two copies of Bidwell’s
  packing give one at `4.6755`, so the architecture’s ceiling lies in between.
  A search for 34 squares at `4.63` or `4.65` prices that ceiling exactly, and the same
  instrument prices n = 12 with 24 squares below side 4, and n = 18 and n = 21 as well.
- **Native `C4` is mechanical.** The native coverage engine refuses R052 at
  memory-policy constants (`interval.py` lines 141–149, `threshold_interval.py` lines
  127–134). Nine spread sizing rows and the four sizing rows in the packet all certified
  at or above `Γ`, at about 2.7 to 3.5 s a row.
  A full run is about 15 CPU-hours, about eight hours on the tool’s two workers.
  Zero slack means a seam refusal is possible at an unsampled row; a refusal is recorded
  as such, never as a negative.

### n = 11: the cost is the relaxation, not the box

Readings from the retained pilot trees and four extra box runs, kept in
`attic/planning-159/n11/`.

- **The separating-axis LP ignores every unbranched pair.** Leaves peak at depth 19 to
  21 of 55 pairs, 82% are Farkas certificates, and each branch node keeps about 1.7 of
  its 7 children. The best LP value at expanded nodes is within `10^-6` of the target at
  every tilt, and boxes at targets 3.90 and 3.95 behave the same as at `U`. So a
  per-node bound that helps must price all pairs at once, which is a counting bound.
  Tiling is a second multiplier, since a certificate found at one tilt already holds
  across a box `10^-2` wide.
- **R052’s lesson applies, but not as a bound campaign.** Agenda-042’s statement that
  Kleddamag’s n = 11 certificate has no side headroom is about its frozen bytes, not the
  mixed relaxation. Any lower-bound gain at n = 11 is below `0.0021`, so a campaign for
  one falls under the owner’s 2026-09-14 hold.
  The same producer, aimed at excluding angle sets away from Trump’s rather than at the
  side, is in scope.
- **A short probe of the existing class certificate** (X-014 Lemma 3, composition
  `(6,5)`, grid 39) refuted no one-degree tilt band from 6° to 44°, and its control band
  at Trump’s tilt correctly did not refute.
  That is inconclusive by construction, since exp-064 measured the shrink alone at
  `0.0089` of side, but it shows the tool path is short.

## Decisions

Each selected item becomes an agenda-042 BC with one bead.
The first night runs builds by day and two CPU jobs overnight, within about three
agents.

| BC | Case | Commitment | Kind | Routing and price | Stop or reconsider |
| --- | --- | --- | --- | --- | --- |
| BC-386 | 17 | Native decision of R052 for `C4`: lift the ceilings behind an explicit byte budget recorded in the receipt, add a contract test admitting R052’s dimensions, re-baseline the n11 native audit, then run all rows on a clean reviewed commit | tool validation | Opus xhigh about 2 h; about 15 CPU-h on 2 workers; Fable xhigh checks the transfer contract | A stalled or seam row is recorded as a refusal |
| BC-387 | 17, 12 | Price the architecture ceiling: review the capacity-one lemma first, then search for triangle-free overlap families of 34 squares at `463/100` and `465/100`, and 24 at `397/100` and `399/100`, with an exact checker | research | Fable xhigh lemma review about 1 h; Opus xhigh build 4–6 h; runs take minutes | The lemma fails review, or no family is found (inconclusive, not a negative) |
| BC-388 | 11 | The side profile `f(θ)` along the six-axis plus five-common-angle family: a frozen-angle census over 200 tilts with 100 jolted starts each | research | Opus high about 2 h; one night on 7 workers | None; it is a measurement that prices BC-389 and BC-384 |
| BC-389 | 11 | A two-class parent-core certificate that closes one rung-1 box outright, at 20° | research | Opus xhigh 1–2 days; Fable xhigh reviews the two-class lemma | Mass stays above 11 after site column generation with two-of-three and three-of-five atoms |
| BC-390 | 11 | Rung 0 widened to half-width `10^-4` with the unchanged instrument | research | Launcher only; about `1.7×10^8` nodes, one night on 9 workers | The enclosure reach meets the local-theorem radius |
| BC-391 | 21 | The additive certificate at 4.89 on stock column generation, without the parent clip | research | Opus high, runs under an hour each; idle-slot work | The value reaches 21 on two site sets, or fails on both |

**BC-384 narrows.** Its design note chooses between parametric-in-tilt certificates,
which certify a midpoint dual vector over a whole tilt interval by univariate polynomial
positivity so that rung 1 costs about one rung-0 tree instead of forty or more, and
per-square counting at each node.
It chooses after BC-388 and BC-389 report.
The second-order dual bound, the descent filter, symmetry reduction and LP warm starts
are retired as BC-384 candidates; node throughput is a separate efficiency item.

**Not selected.** A first-party n = 17 producer beyond `4.62002` waits for BC-387; it is
reconsidered only if the ceiling is at least `4.64`. The n = 12 parent-core transfer
waits for BC-387’s n = 12 price and BC-380’s parent clip.
Any n = 11 lower-bound increment stays under the owner’s hold.

## Order

1. **Day:** BC-387’s lemma review, and the builds for BC-386 and BC-388. BC-386’s cap
   lift lands as a reviewed commit before its run starts.
2. **First night:** BC-386’s full native run on 2 workers and BC-388’s census on 7.
   BC-387’s searches run in minutes and fit wherever a slot is free.
3. **Next:** BC-389’s build, then BC-390’s night.
   A Fable max reading of BC-388 and BC-389 selects BC-384’s design.

The Session 159 handoff selects BC-386 under `think-amx8` as the entry for this order.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
