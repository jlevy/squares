---
title: exp-133 — the corner-skeleton measure at 96/25, and the corner-pair theorem
softschema:
  contract: packing.squares:Experiment/v2
  schema: ../../../schemas/experiment.schema.yaml
  envelope: experiment
  status: enforced
experiment:
  id: exp-133
  series: series-000
  title: >-
    Decide whether a valid D4-symmetric measure at 96/25 carries T-018's four corner atoms
    at weight at least 3/20 with mass below 11 + 3/20, and register what the free measure
    proves instead
  date: '2026-09-08'
  hypotheses: [H-128]
  tier: confirmatory
  subject:
    label: >-
      bounded column generation for a valid D4-symmetric measure at side 96/25, shrink
      B = 9977/10000, on the retained 181-direction net, over T-018's 1121 atoms scaled by
      384/381 unioned with the library's density-matched grids 25, 34 and 42 at inset 1/2 —
      four phases on one site set and one row set (free, corner-bounded, corner-and-centre
      bounded, and the corner orbit priced), each final measure decided by the exact
      eighth-turn sweep
    engine: >-
      sqpack 0.2.0 fractional — colgen.generate_adaptive's column loop and
      certificate.verify as the exact decider, driven by the lane's bounded_colgen.py, which
      re-implements solve_rows line for line with a bounded linprog call because the library
      fixes every variable at (0, ∞), and bounded_ceiling.py, which decides the dual's
      symmetrised depth exactly at the arrangement vertices; both are listed verbatim in
      lane C's appendix of scripts and outputs as run, and sqpack itself was not edited
    engine_commit: '22884081'
    assurance: verified
    method: exact-algebraic
    host_system: >-
      linux x86_64, four cores shared with five other agents at load average 3 to 8, one
      process with PACK_JOBS=1, OMP_NUM_THREADS=1 and one BLAS thread, project Python 3.14
    selftest_passed: true
  instance: {axis: n, point: 11, role: target}
  method:
    control: >-
      Run 1, the seed alone with no grids, is the site control: its free value
      48415397/4000000 = 12.10384925 sits a unit above the geometry's and shows why the
      density-matched grids are needed, so a run "seeded with T-018" that skips them is
      reading a site artefact. Run 4 replays run 2 with the duals saved and reproduced its
      LP objectives to the last printed digit. Every final measure of runs 1, 2, 4, 5 and 6
      was decided by certificate.verify(workers=1): Conditions 1, 3, 4 and 5 hold for each,
      Condition 2 failing exactly as the reported mass says. The ownership premise was
      decided in Fraction arithmetic before any run, the driver refusing to start otherwise:
      the corner atoms' least squared pairwise distance 4633032392704/1385114794281 ≈
      1.82890² exceeds 2B² = 99540529/50000000 ≈ 1.41096², so no core holds two of them.
    candidate: >-
      the four-bound program, the corner orbit at w ≥ 3/20 (orbit 122 of the scaled seed,
      four members, so the orbit variable is the per-atom weight), read against H-128's
      11.15 criterion; beside it the five-bound program with the centre orbit at w ≥ 1/8,
      the free program on the same site set and rows, and the priced program whose objective
      is M − w_c, which asks whether any lower bound at that position could work. Run 6
      re-ran the four-bound phase alone with 45 column rounds of six candidate orbits and a
      settle threshold of 0.005 to buy a dual worth taking a floor from.
    runs_per_condition: 1
    interleaved: false
    operator: >-
      the BC-293 lane agent of agenda-030, bead think-1136, session-101; the record was
      written by a separate record lane from the frozen result section
    commit: '22884081'
    dirty: false
    entry_point: >-
      packing/src/sqpack/fractional/colgen.py and certificate.py, reached through the lane's
      bounded_colgen.py and bounded_ceiling.py, whose full text is in lane C's "Appendix:
      scripts and outputs as run"
    command: >-
      from packing/, PACK_JOBS=1 OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 uv run --frozen
      --all-extras --group dev python bounded_colgen.py --seed-certificate
      cases/n11_fractional_certificate/certificate.json --grid-counts auto --out run2
      --column-rounds 10 --deadline-b 1500 --deadline-a 1200 --deadline-c 600 for the
      decision, the same with --out run6 --phases B --column-rounds 60 --columns-per-round 6
      --settle 0.005 --support-cap 200 --deadline-b 2100 for the settling attempt, and
      python bounded_ceiling.py --dual run6/dual-B-four.json --support-cap 200 --decide 3000
      for the floor; the scripts live in the session scratchpad and are reproduced verbatim
      in the result section's appendix, so the appendix is the artifact to re-run from, not a
      repository console script
    budget: >-
      the research phase of session-101 — 110 minutes of a 150-minute lane clock on one
      process — with per-phase deadlines of 1500 s (four-bound), 1200 s (free) and 600 s
      (each other phase), none of which was reached, and at most ten column rounds per phase
      outside run 6
    record: packing/campaign/series/series-000-smoke-and-calibration/results/agenda-030/lane-c-n10-transfer.md
  effort:
    timebox: 110m, the research phase of session-101 inside its 150-minute lane clock
    wall_seconds: 3813
    stopped_by: criterion
  results:
  - shape: determination
    role: outcome
    question: >-
      Is there a valid D4-symmetric measure at side 96/25 on the retained shrink and net
      whose four corner atoms each carry weight at least 3/20 and whose total mass is below
      11 + 3/20?
    outcome: criterion_missed
    checked_by: >-
      Not on the retained shrink and net. On the density-matched site set (637 orbits and
      4777 sites after ten column rounds, 8517 rows) the least four-bound measure column
      generation reaches has exact rationalised mass 23596423/2000000 = 11.7982115 over 401
      atoms — against H-128's threshold of 11.15 — with corner weight 600001/4000000 ≥ 3/20,
      and it is valid: certificate.verify(workers=1) accepts Conditions 1, 3, 4 and 5 with
      least cell 400001/400000 at direction 0, so the reading is of a real measure and not
      of an infeasible program. The five-bound measure sweeps at 47276821/4000000 =
      11.81920525 over 369 atoms. The free measure on the same site set and rows sweeps at
      22524199/2000000 = 11.2620995 over 377 atoms, carrying nothing on the corner orbit, so
      the price of the forced skeleton is M(forced) − M(free) = 33507/62500 = 0.536112
      exactly: four atoms at 3/20 add 3/5 of mass and the free optimum recovers 0.064 of it
      elsewhere. Pricing rather than bounding the corner orbit does not help: the priced
      program M − w_c equals the free value 11.262035287 on the 637-orbit set, and after nine
      more column rounds (646 orbits, 9934 rows) reaches 44758451/4000000 = 11.18961275 with
      the corner orbit still at weight zero, the fall being the free mass moving with the
      columns rather than the corner site earning weight. So no lower bound at that position,
      of any size, yields the theorem on these site sets: the position and not the 3/20 is
      what fails.
  - shape: determination
    role: mechanism
    question: >-
      What does a single exactly verified free measure prove at 96/25 about the corners,
      without any bound, column settlement or floor?
    outcome: criterion_met
    checked_by: >-
      The corner-pair containment theorem, proved from the phase-D free measure and Lemma C'
      applied to sets. With M = 11 + ε the mass outside the eleven pairwise disjoint B-cores
      of any packing is at most ε, so any atom set of total weight above ε has an atom inside
      some core. That measure is exactly verified valid with mass 22524199/2000000, hence
      ε = 524199/2000000 = 0.2620995, and it carries 106251/800000 on each of the eight atoms
      (3152/3175, 2336/3175), (2336/3175, 3152/3175) and their images — T-018's (197/200,
      73/100) orbit scaled by 128/127, and the free measure's heaviest orbit, not the corner
      point. Per corner that pair has mass 106251/400000 = 0.2656275, above ε by
      441/125000 = 0.003528; the two marks of one corner are √(1331712/10080625) ≈ 0.3635
      apart, so one core can hold both, which is why the pair and not either mark is the
      anchor; and the least squared distance between marks of different corners is
      34668544/10080625 ≈ 1.8545², above 2B² = 99540529/50000000, so no core meets two
      corners' pairs. Hence, proved: every packing of eleven unit squares in [0, 96/25]² has
      four distinct squares, one per corner, each containing in its interior at least one of
      its corner's two marks. The margin is 0.0035 of mass and belongs to this measure: the
      lighter phase-F measure (ε = 0.1896) spreads its corner mass differently and does not
      reproduce it.
  - shape: determination
    role: guard
    question: >-
      Did the exact sweep accept every final measure, did the replay reproduce the decision,
      and was the ownership premise decided before it was used?
    outcome: criterion_met
    checked_by: >-
      Yes on all three. certificate.verify(workers=1) decided every final measure of runs 1,
      2, 4, 5 and 6: Conditions 1, 3, 4 and 5 hold for each and Condition 2 fails exactly as
      each reported mass says, so validity is never inferred from an LP objective. Run 4
      reproduced run 2's LP objectives to the last printed digit with the duals saved. The
      corner premise 4633032392704/1385114794281 > 99540529/50000000 and the pair premises
      were decided in Fraction arithmetic before any run, the driver refusing to start
      otherwise. The seed-only control (run 1, no grids) returned a free value of
      48415397/4000000 = 12.10384925, a unit above the geometry's, which is the guard that
      says the density-matched grids are load-bearing.
  - shape: determination
    role: mechanism
    question: >-
      How much of the obstruction is a theorem for the net rather than a reading on this
      site set — does the bounded dual force every valid D4 measure with the corner bound to
      mass 11.15 or above?
    outcome: criterion_missed
    checked_by: >-
      It does not, and that is what scopes the verdict. Run 6 (four-bound alone, 45 column
      rounds of six candidates, settle threshold 0.005) reached LP objective 11.730827068 on
      883 orbits and 10364 rows without settling — the last candidate orbit's averaged depth
      was nan — and its rationalised measure, mass 2932721/250000 = 11.730884 with least cell
      250001/250000, is valid. From that dual, decided exactly: 70 of 70 rows kept, weight
      11.130827 of 11.130827, symmetrised to 560 squares, 1487212 arrangement vertices, 3076
      decided exactly above the threshold T = 1.058083, exact maximum symmetrised depth
      153/140 = 1.092857 taken as D, depth exactly 0 at each of the four corner atoms, and
      correction Σ(1 − depth/D)·3/20 = 0.600000, giving the floor Σy/D + correction =
      10.185071 + 0.600000 = 10.785071. Every valid D4 measure on this (96/25, 9977/10000,
      net) with the corner bound has mass at least that — but 10.785071 is below 11.15, so
      the obstruction is a reading on the retained site sets and not yet a theorem for the
      net. A settled dual would put the floor within half a per cent of the LP value, and
      that is the measurement this round did not buy.
  verdict:
    decision: unresolved
    primary_criterion: >-
      the exactly verified total mass of the column-generation measure at 96/25 with the four
      corner atoms bounded below by 3/20, against the threshold 11.15
    reason: >-
      Handoff correction, 2026-09-08: the original rejected verdict applied a stopping
      criterion for a finite-support attempt to H-128's broader existence claim. The
      valid four-bound measure has exact mass 23596423/2000000 = 11.798, above 11.15;
      that attempt did not obtain the target. The bounded dual's floor over the net is
      only 10.785, below 11.15, so H-128 remains inconclusive on its declared domain.
      The independent corner-pair theorem remains proved.
    commit: '22884081'
---
# exp-133 — The Corner Skeleton Is a Pair, Not a Point

[H-128](../../../hypotheses/H-128-corner-skeleton-ownership.md) asked for one measure: a
valid `D4`-symmetric measure at side `96/25` carrying T-018’s four corner atoms at
weight at least `3/20` with total mass below `11 + 3/20`. Such a measure would make
X-021’s Corollary C.2 free and hand the closing route four pinned points.
Lane BC-293 of
[agenda 030](../../../agendas/agenda-030-parallel-structural-lanes-at-n11.md), bead
`think-1136`, spent
[session-101](../../../agent-sessions/session-101-corner-skeleton-ownership.md) building
the bounded program and running it.
The attempt did not produce that measure, and it proved a corner-pair theorem.
This record registers both.
Every figure below is read from
[lane C’s session-101 section](../results/agenda-030/lane-c-n10-transfer.md#session-101--corner-skeleton-ownership-at-9625-2026-09-08),
which holds the derivation, every run’s inputs and exact verdicts, and the scripts.

## What was tested, and what would have refuted it

The ownership step is Lemma C′. In any packing of eleven unit squares in `[0, L]²` each
square strictly contains a closed `B`-square at a net direction (Condition 4); those
eleven cores are pairwise disjoint and each carries mass at least one (Condition 5), so
with `M = 11 + ε` every core has mass at most `1 + ε` and the mass outside them is at
most `ε`. An atom heavier than `ε` therefore lies in exactly one core.
Corner atoms too far apart to share a core are then owned by *distinct* squares, and the
structural theorem follows from the LP alone.

The falsifiers were fixed before each run.
**A bounded run that converges with rationalised mass at or above `11 + 3/20 = 11.15`; a
final measure the exact eighth-turn sweep refuses on Condition 1, 3, 4 or 5; or a
bounded LP that does not converge inside its wall.** The first occurred, on a measure
the sweep accepts. Only the exact sweep decides validity here; every LP objective quoted
below is context.

## Inputs, fixed for every run

Side `L = 96/25`, shrink `B = 9977/10000`, the retained net of 181 directions
`t_k = k · 207107/500000 / 180`, `k = 0..180`, with `D = 207107/90000000` and
`B(1 + D) = 899996306539/900000000000 < 1`. Seed: T-018’s 1121 atoms from
`cases/n11_fractional_certificate/certificate.json` with every coordinate scaled by
`384/381 = 128/127`, 149 `D4` orbits, weights not read.
Site set: that seed unioned with the library’s density-matched grids —
`site_counts_for_side(96/25, 9977/10000)` gives counts `25, 34, 42` at inset `1/2` — 619
orbits and 4645 sites at the start, 637 orbits and 4777 sites after the column rounds,
every added orbit coming from the dual’s arrangement vertices.
Corner orbit: `(29586032/29422725, 29586032/29422725)` and its three images, orbit 122
of the scaled seed, size 4. Centre orbit: `(48/25, 48/25)`, size 1. Column generation
with `rows_per_direction 3`, `max_rounds 60`, `support_cap 32` for pricing, one
candidate orbit per column round and at most ten column rounds per phase, rows carried
across every phase; rationalisation by `rationalise_sites` at scale `4 000 000` with the
`1000001/1000000` bump, which rounds up only, so a lower bound survives it.
One process, `PACK_JOBS=1`, one BLAS thread, four cores shared with five other agents at
load average 3 to 8.

Because the LP column for a `D4` orbit is one variable whose rationalised weight is
given to every member, the corner constraint is the single bound `w ≥ 3/20` on that
orbit. The library fixes every variable at `(0, ∞)`, so the lane’s driver re-implements
`solve_rows` with a bounded `linprog` call and drives the column loop itself; `sqpack`
is not edited.

## The tested support did not produce the H-128 measure

| Phase, on the final 637-orbit site set and 8517 rows | LP objective | Rationalised mass, exact | Atoms | Corner weight | Valid |
| --- | --- | --- | --- | --- | --- |
| four-bound (E) | `11.798148881` | `23596423/2000000 = 11.7982115` | 401 | `600001/4000000 ≥ 3/20` | yes |
| five-bound (C) | `11.819153276` | `47276821/4000000 = 11.81920525` | 369 | `600001/4000000` | yes |
| free (D) | `11.262035287` | `22524199/2000000 = 11.2620995` | 377 | none; the orbit carries `0` | yes |
| priced `M − w_c` (F), after nine more column rounds | `11.189559666` | `44758451/4000000 = 11.18961275` | 373 | none | yes |

The four-bound phase spent its ten column rounds — its first converged LP, on the
619-orbit set before the rounds, read `11.849054622` — so its value is an upper reading
on this site set, bounded from underneath by the floor of the last section.
The four-bound mass is `11.798` against a threshold of `11.15`, and the sweep accepts
the measure, so this is a real measure read exactly and not an infeasible program.
The price of the forced skeleton is exact:
`M(forced) − M(free) = 23596423/2000000 − 22524199/2000000 = 33507/62500 = 0.536112` on
one site set and one row set.
Four atoms at `3/20` add `3/5` of mass and the free optimum recovers `0.064` of it
elsewhere.

**The bound is not the obstacle; the position is.** Phase F prices the corner orbit
instead of bounding it, so its optimum is `min_t (M(t) − t)` over every bound `t ≥ 0`,
and the theorem needs that below eleven.
On the 637-orbit set it equals the free value exactly: the LP leaves T-018’s scaled
corner site at weight zero even when a unit of its weight is free, because that site’s
orbit-averaged depth under the free dual is `0.559`, below `3/4`. Nine further column
rounds lowered the objective to `11.189559666` with the corner orbit **still at zero** —
the fall is the free mass moving with the columns, not the corner site earning weight.
So H-128’s `3/20` is not a tunable that was set too high.
Where the mass actually goes is the next section.

## What the free measure does prove

Lemma C′ applies to sets exactly as it does to atoms: with `M = 11 + ε` the mass outside
the eleven cores is at most `ε`, so any atom set of total weight above `ε` has at least
one atom inside some core.

The phase-D free measure is valid and exactly verified, with mass `22524199/2000000` and
therefore `ε = 524199/2000000 = 0.2620995`. Its heaviest orbit is not T-018’s corner
point but T-018’s `(197/200, 73/100)` orbit scaled — the eight atoms
`(3152/3175, 2336/3175)`, `(2336/3175, 3152/3175)` and their images, at `106251/800000`
each. Per corner that pair carries `106251/400000 = 0.2656275`, which exceeds `ε` by
`441/125000 = 0.003528`. The two marks of one corner are `√(1331712/10080625) ≈ 0.3635`
apart, so a single core can hold both — which is why the *pair*, and not either mark, is
the anchor — and the least squared distance between marks of different corners is
`34668544/10080625 ≈ 1.8545²`, above `2B² = 99540529/50000000`, so no core meets two
corners’ pairs.

> **Theorem (four-corner pair containment at `96/25`).** Every packing of eleven unit
> squares in `[0, 96/25]²` has four distinct squares, one per corner, each containing in
> its interior at least one of its corner’s two marks `(3152/3175, 2336/3175)` and
> `(2336/3175, 3152/3175)`, and their images under the container’s symmetries.

It is proved by that one measure and the exact sweep alone — no bound, no column
settlement, no floor — and it is not implied by insertion saturation’s blockers, which
need only meet an open corner box.
It is the two-point form of what H-128 asked for at one point.
The margin is `0.0035` of mass and belongs to *this* measure: the lighter phase-F
measure (`ε = 0.1896`) spreads its corner mass differently and does not reproduce it, so
the pair-priced program that would widen the margin (phase G, run 5) is the unfinished
part.

For BC-299 the anchor this hands over is a two-branch choice per corner — sixteen
patterns before symmetry, two up to `D4` per corner choice — each branch a pinned point
inside a named square, which is what the frame-conditioned certificate asked for in a
weaker but proved form.

## How far the rejection reaches

Run 6 re-ran the four-bound phase alone with 45 column rounds of six candidate orbits
and a settle threshold of `0.005`, reaching LP `11.730827068` on 883 orbits and 10 364
rows in 35 minutes.
It did **not** settle — the last candidate orbit’s averaged depth was
`nan` — and its rationalised measure (mass `2932721/250000 = 11.730884`, least cell
`250001/250000`) is valid.

From that dual the floor is decided exactly: 70 of 70 rows kept, symmetrised to 560
squares, `1 487 212` arrangement vertices, 3 076 of them decided exactly above the
threshold `T = 1.058083`, exact maximum symmetrised depth `153/140 = 1.092857` taken as
`D`. The depth at each of the four corner atoms is exactly `0` — no tight placement of
the final row set covers T-018’s corner site, so the bound’s price in the dual is the
full `4 · 3/20 = 3/5` with no substitution at all, which is what phase F said in the
primal. The floor is `Σy/D + Σ(1 − depth/D)·lb = 10.185071 + 0.600000 = 10.785071`, and
it holds for **every** valid `D4` measure on this `(L, B, net)` with the corner bound,
on any site set and any atom count.

`10.785 < 11.15`. So the obstruction is, in this block, a reading on the retained site
sets and not a theorem of nonexistence over the net.
H-128 remains unresolved on its declared shrink and net; the unsuccessful support cannot
justify the original broader rejection.
A settled dual would put the floor within half a per cent of the LP value, and that is
the first thing a successor should buy.

## Limits

- **Every free reading here is an upper reading.** Each phase’s last candidate orbit
  still had averaged depth `1.09` to `1.29` when its ten column rounds ran out, so the
  free values `11.19` to `11.26` are upper bounds on this site set, not the net’s value.
  They sit `0.19` to `0.26` above the certificate line, which is the number BC-297’s
  ladder and BC-294’s duality readings should be checked against.
- **The seed alone is a site artefact.** T-018’s 1121 atoms scaled to `96/25` with no
  grids give a free value of `12.10`; the density-matched grids bring it to `11.26`. Run
  1 is retained as the control that shows this, not as a reading of the geometry.
- **One measure, one theorem.** The corner-pair theorem is a property of the phase-D
  measure. A different valid measure at the same side need not prove it, and the margin
  beyond `441/125000` is unmeasured because run 5 crashed after its free phase hit its
  wall — the driver hands back the last converged solution while the shared row matrix
  still carries the unconverged round’s column, so the next phase’s warm solve fails on
  a dimension mismatch.
  The fix is one line and is left with the scripts.
- **Wall times are not comparable.** Four cores shared with five other agents at load
  average 3 to 8, one process.
  The declared `3813` seconds is the first-to-last span of the four runs this record
  rests on — run 1 at `148 s`, run 2 at `495 s`, run 4 at `1045 s` and run 6 at `2125 s`
  — and nothing else; run 5’s `609 s` and the Lemma C dry run’s sweeps are not counted
  in it.
- **Nothing about a packing bound.** The theorem constrains where four squares of a
  hypothetical packing of eleven must lie.
  It establishes no side, and no result is written to the frontier register.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
