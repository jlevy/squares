---
title: "exp-252 — Session 182 lane A: the per-state price of excluding n17 residue states"
softschema:
  contract: packing.squares:Experiment/v2
  schema: ../../../schemas/experiment.schema.yaml
  envelope: experiment
  status: enforced
experiment:
  id: exp-252
  series: series-000
  title: H-264's seed-182 draw of residue states run through the 17-owner kernel at 32 bins, each closure
    admitted on the standing verifier's full pass
  date: '2026-10-05'
  hypotheses:
  - H-264
  tier: confirmatory
  subject:
    label: The 12 residue orbits survey_n17_residue draws from its arity8 frame with --sample 12 --seed 182
      (2 at distance 2, 7 at 4, 3 at 6 from the endpoint's state; 10 counted), each run as a whole 17-cell
      pattern on the unique-state 24-cell cover at U = 1169/250.
    engine: devtools.check_n17_subpattern (producer and checker) and devtools.verify_n17_kernel_certificate in
      full mode under the kernel-streamed listing, both from the clean run worktree at the session-182
      registration commit; devtools.survey_n17_residue as the float pre-screen
    assurance: verified
    method: exact-algebraic
    host_system: Linux x86_64 remote session container, project Python 3.14.7, one worker per job at nice 10
    selftest_passed: true
    engine_commit: cebb5d15aaa17d0cc13aa302ecbd750a54bfc57d
  instance:
    axis: n
    point: 17
    role: target
  method:
    control: The float pre-screen placed the endpoint's own state (its positive control) and no other draw
      (receipts/A/survey-seed182.json). The kernel on the endpoint's own state, which is feasible at U, at a
      2,700 s ceiling must not close; it returned PASS_CERTIFIED_STALL in 333 s (receipts/A/kernel-control-endpoint.json).
    candidate: Each draw's seed and node, re-proved in full by the standing kernel verifier on a closure.
    runs_per_condition: 1
    interleaved: false
    operator: Claude Session 182; the run operator's lane A queue ran the survey, the control and the draws two
      at a time in the survey's own seeded random order, verified each closure and admitted it in the session
      checkout
    entry_point: packing/devtools/check_n17_subpattern.py
    command: 'From packing/ of the run worktree: nice -n 10 timeout -k 120 7600 .venv/bin/python3 -m
      devtools.check_n17_subpattern --cells CELLS17 --bins 32 --max-rounds 24 --hull-limit 16 --max-seconds
      7000 --save-objects DIR --output FILE; on a closure, nice -n 10 timeout -k 120 4000 .venv/bin/python3 -m
      devtools.verify_n17_kernel_certificate --progress --output CERT/verification.json CERT; then
      devtools.census_n17_certified in the session checkout.'
    budget: 7,000 s wall per state and 4,000 s per verification on one worker; lane A at most 26 CPU-hours
    record: packing/campaign/series/series-000-smoke-and-calibration/results/exp-252-n17-overnight-per-state-price
    dirty: false
    commit: cebb5d15aaa17d0cc13aa302ecbd750a54bfc57d
  results:
  - shape: determination
    role: outcome
    question: Is the draw at index 2 (mask 5683195, distance 4) infeasible at U, by a certificate the kernel's
      checker accepts and the standing verifier re-proves in full?
    outcome: criterion_met
    checked_by: The run (receipts/A/kernel-m5683195.json) returns PASS_CERTIFIED_CLOSED in 2,147 s of wall and
      869 s of process CPU (producer 1,366 s, checker 780 s, under contention from other agents' test runs)
      on 135 steps and 4,320 rows in 8 rounds, closure all_parent_poses_forbidden for interior-N at step 134.
      The standing verifier at cebb5d15a passes it in full mode in 676 s, checking all 4,247 live rows in full
      and 13,198 collision regions by 23,720,272 exact facet checks. It excludes its own 8 states, one orbit.
  - shape: determination
    role: outcome
    question: Is the draw at index 4 (mask 2817021, distance 4) excluded within the 7,000 s ceiling?
    outcome: criterion_missed
    checked_by: The run (receipts/A/kernel-m2817021.json) returns PASS_CERTIFIED_STALL in 2,072 s of wall and
      827 s of process CPU, the producer at a fixed point after 11 rounds (187 steps, 5,984 rows), well inside
      its ceiling, so the registered re-run does not apply. A non-closure.
  - shape: determination
    role: outcome
    question: Is the draw at index 1 (mask 3063677, distance 4) excluded within the 7,000 s ceiling?
    outcome: criterion_missed
    checked_by: The run (receipts/A/kernel-m3063677.json) returns PASS_CERTIFIED_STALL in 1,129 s of wall
      and 634 s of process CPU, the producer at a fixed point after 6 rounds (102 steps, 3,264
      rows), inside its ceiling, so the registered re-run does not apply. A non-closure.
  - shape: determination
    role: outcome
    question: Is the draw at index 5 (mask 1964767, distance 2, the declared secondary stratum, not
      counted) excluded within the 7,000 s ceiling?
    outcome: criterion_missed
    checked_by: The run (receipts/A/kernel-m1964767.json) returns PASS_CERTIFIED_STALL in 989 s of wall
      and 623 s of process CPU, the producer at a fixed point after 8 rounds (136 steps, 4,352
      rows), inside its ceiling, so the registered re-run does not apply. A non-closure,
      reported separately.
  - shape: determination
    role: outcome
    question: Is the draw at index 8 (mask 2878207, distance 6) excluded within the 7,000 s ceiling?
    outcome: criterion_missed
    checked_by: The run (receipts/A/kernel-m2878207.json) returns PASS_CERTIFIED_STALL in 1,940 s of wall
      and 925 s of process CPU, the producer at a fixed point after 11 rounds (187 steps, 5,984
      rows), inside its ceiling, so the registered re-run does not apply. A non-closure.
  - shape: determination
    role: outcome
    question: Is the draw at index 10 (mask 2784767, distance 4) excluded within the 7,000 s ceiling?
    outcome: criterion_missed
    checked_by: The run (receipts/A/kernel-m2784767.json) returns PASS_CERTIFIED_STALL in 1,997 s of wall
      and 828 s of process CPU, the producer at a fixed point after 13 rounds (221 steps, 7,072
      rows), inside its ceiling, so the registered re-run does not apply. A non-closure.
  - shape: determination
    role: outcome
    question: Is the draw at index 3 (mask 5500414, distance 6) infeasible at U, by a certificate the
      kernel's checker accepts and the standing verifier re-proves in full?
    outcome: criterion_met
    checked_by: The run (receipts/A/kernel-m5500414.json) returns PASS_CERTIFIED_CLOSED in 1,109 s of wall
      and 594 s of process CPU (producer 712 s, checker 396 s) on 129 steps and 4,128 rows in 8
      rounds, closure all_parent_poses_forbidden for side-E1 at step 128. The standing verifier
      at cebb5d15a passes it in full mode in 328 s, checking all 3,536 live rows in full and
      9,948 collision regions by 15,599,756 exact facet checks. It excludes its own 8 states,
      one orbit.
  - shape: determination
    role: outcome
    question: Is the draw at index 12 (mask 7844815, distance 6) infeasible at U, by a certificate the
      kernel's checker accepts and the standing verifier re-proves in full?
    outcome: criterion_met
    checked_by: The run (receipts/A/kernel-m7844815.json) returns PASS_CERTIFIED_CLOSED in 646 s of wall
      and 395 s of process CPU (producer 264 s, checker 377 s) on 82 steps and 2,624 rows in 5
      rounds, closure all_parent_poses_forbidden for interior-W at step 81. The standing
      verifier at cebb5d15a passes it in full mode in 184 s, checking all 2,337 live rows in
      full and 6,828 collision regions by 11,554,568 exact facet checks. It excludes its own 8
      states, one orbit.
  - shape: determination
    role: outcome
    question: Is the draw at index 11 (mask 4028335, distance 4) infeasible at U, by a certificate the
      kernel's checker accepts and the standing verifier re-proves in full?
    outcome: criterion_met
    checked_by: The run (receipts/A/kernel-m4028335.json) returns PASS_CERTIFIED_CLOSED in 857 s of wall
      and 545 s of process CPU (producer 461 s, checker 394 s) on 82 steps and 2,624 rows in 5
      rounds, closure all_parent_poses_forbidden for interior-W at step 81. The standing
      verifier at cebb5d15a passes it in full mode in 252 s, checking all 2,579 live rows in
      full and 8,326 collision regions by 15,726,176 exact facet checks. It excludes its own 8
      states, one orbit.
  - shape: determination
    role: outcome
    question: Is the draw at index 7 (mask 2601983, distance 4) infeasible at U, by a certificate the
      kernel's checker accepts and the standing verifier re-proves in full?
    outcome: criterion_met
    checked_by: The run (receipts/A/kernel-m2601983.json) returns PASS_CERTIFIED_CLOSED in 489 s of wall
      and 352 s of process CPU (producer 283 s, checker 205 s) on 79 steps and 2,528 rows in 5
      rounds, closure all_parent_poses_forbidden for side-S2 at step 78. The standing verifier
      at cebb5d15a passes it in full mode in 151 s, checking all 2,485 live rows in full and
      7,051 collision regions by 12,940,716 exact facet checks. It excludes its own 8 states,
      one orbit.
  - shape: determination
    role: outcome
    question: Is the draw at index 6 (mask 1949551, distance 4) excluded within the 7,000 s ceiling?
    outcome: criterion_missed
    checked_by: The run (receipts/A/kernel-m1949551.json) returns PASS_CERTIFIED_STALL in 1,613 s of wall
      and 1,297 s of process CPU, the producer at a fixed point after 13 rounds (221 steps,
      7,072 rows), inside its ceiling, so the registered re-run does not apply. A non-closure.
  - shape: determination
    role: outcome
    question: Is the draw at index 9 (mask 851903, distance 2, the declared secondary stratum, not
      counted) excluded within the 7,000 s ceiling?
    outcome: criterion_missed
    checked_by: The run (receipts/A/kernel-m851903.json) returns PASS_CERTIFIED_STALL in 88 s of wall and
      77 s of process CPU, the producer at a fixed point after 2 rounds (34 steps, 1,088 rows),
      inside its ceiling, so the registered re-run does not apply. A non-closure, reported
      separately.
  verdict:
    decision: accepted
    primary_criterion: At least half of the counted draws excluded within two CPU-hours each, with N1's 7,000 s
      wall ceiling standing in for that limit; falsified by six non-closures of the ten counted.
    reason: >-
      Five of the ten counted draws closed within the 7,000 s ceiling, each re-proved in full
      by the standing kernel verifier, which meets the criterion of at least half; every
      closure cost under 900 s of process CPU and every verification under 700 s, far inside
      two CPU-hours. The other five counted draws reached producer fixed points inside the
      ceiling, as did both distance-2 draws. The W2 factual review
      (docs/project/reviews/review-2026-10-05-exp-252-h264.md) confirmed the verdict with
      corrections to bookkeeping and attribution, which this record carries.
    needs_review: false
    commit: dfd38187c
  effort:
    timebox: 7,000 s per state and 4,000 s per verification, one worker per job
    wall_seconds: 12041
    stopped_by: criterion
---
# exp-252: Session 182 Lane A, the Per-State Price

[H-264](../../../hypotheses/H-264-n17-geometric-exclusion-cost-per-leaf.md), as
rewritten in Session 182’s registration, asks what fraction of a seeded draw of residue
orbits the 17-owner kernel excludes by a certificate the standing verifier re-proves,
and at what cost per state.
This round is lane A of the
[n17 overnight plan](../../../../../docs/project/specs/done/plan-2026-10-05-n17-overnight.md)
(BC-419). All twelve draws have run.

## Verdict

The criterion is met: five of the ten counted draws closed within N1’s 7,000 s ceiling,
and the standing verifier re-proved each in full, so the falsifier (fewer than half) did
not fire.
A closed state cost 352 to 869 s of process CPU and its verification 151 to 676
s; the five counted states that did not close each reached a producer fixed point in 634
to 1,297 s, well inside the ceiling, so more time would not have closed them under this
recipe (H-274 asks whether adaptive rows close the first four; index 6 stalled after it
was registered). The wall of 12,041 s runs from the survey’s start at 08:46 UTC to the
last draw’s receipt at 12:07 UTC, through a container restart at 10:32 UTC; the verdict
was fixed at the fifth verification, at 12:02 UTC. The
[W2 factual review](../../../../../docs/project/reviews/review-2026-10-05-exp-252-h264.md)
the plan requires before X-048 or the frontier states the verdict confirmed it, with
corrections to bookkeeping and attribution (its F1 to F4, applied here) and one gap, the
extrapolation over the drawn strata (its F5, below).
All twelve draws have run: the last counted draw (index 6) and the distance-2 draw at
index 9 reached producer fixed points too.

## Extrapolation Over the Drawn Strata

H-264 asks what the closures extrapolate to over the frame’s drawn strata, and requires
the strata the draw does not reach to be reported as unsampled.
The survey’s strata cross corners, interior cells and distance to the endpoint’s orbit;
its receipt (receipts/A/survey-seed182.json) gives each stratum’s size.
The ten counted draws come from 8 strata holding 1,354 of the frame’s 2,255 non-endpoint
orbits:

| Stratum | Orbits | Counted draws | Closed | Process CPU per state, mean |
| --- | ---: | ---: | ---: | ---: |
| c3/i4/d4 | 182 | 2 | 1 | 752 s |
| c3/i<=3/d4 | 64 | 1 | 0 | 828 s |
| c4/i4/d4 | 258 | 2 | 1 | 824 s |
| c4/i<=3/d4 | 135 | 1 | 0 | 828 s |
| c4/i>=5/d4 | 86 | 1 | 1 | 545 s |
| c3/i4/d6 | 253 | 1 | 1 | 594 s |
| c4/i4/d6 | 249 | 1 | 0 | 925 s |
| c4/i>=5/d6 | 127 | 1 | 1 | 396 s |

Weighting each stratum’s closed share by its size gives a point estimate of about 686 of
those 1,354 orbits closing under this recipe, about half, and a size-weighted mean of
about 730 s of process CPU per state run.
The statement is bounded, and holds per stratum.
Six of the eight strata rest on a single draw, so each of their shares is 0 or 1, and
the other two rest on two draws.
The estimate is a description of these draws scaled to the strata they came from, not a
measured closure rate for any stratum.
The draw is weighted toward distances 2 and 4 (Sainte-Laguë weights 4 and 2), so the raw
5 of 10 is not a frame-wide rate either; the verdict does not depend on that rate, since
the criterion counts draws.

The two distance-2 draws, reported apart, come from 2 strata holding 74 orbits (c4/i4/d2
and c4/i<=3/d2); neither closed.

**Unsampled:** 21 strata holding 827 orbits, reported as unsampled and not extrapolated:
430 orbits in the 9 strata at distance 8 or more, and 397 in 12 strata at distances 2 to
6 (c3/i4/d2 13, c3/i<=3/d2 8, c3/i>=5/d4 46, c3/i>=5/d6 52, c3/i<=3/d6 70, c4/i<=3/d6
82, and the six strata with at most two corners, 126 between them).
H-264’s regime gave the unsampled set as “every distance-8-or-more stratum, 430 of 2,256
orbits”, which holds only if strata are read as distance bands; under the survey’s own
strata it understates the unsampled set by 397 orbits.
No price for the residue tail is claimed: the tail includes the unsampled 827 orbits,
and the drawn strata carry too few draws each to price it.

## Per-State Table

| Index | Mask | Distance | Stratum | Outcome | Wall | Process CPU | Verifier |
| --- | --- | --- | --- | --- | ---: | ---: | --- |
| control | 3439615 (the endpoint’s state, orbit 1900015) | 0 | endpoint | stalled, as it must | 333 s | 321 s | — |
| 2 | 5683195 | 4 | c3/i4/d4 | closed, 8 rounds, admitted | 2,147 s | 869 s | full pass, 676 s |
| 4 | 2817021 | 4 | c3/i<=3/d4 | producer fixed point after 11 rounds | 2,072 s | 827 s | — |
| 1 | 3063677 | 4 | c3/i4/d4 | producer fixed point after 6 rounds | 1,129 s | 634 s | — |
| 5 | 1964767 | 2 | c4/i4/d2 | producer fixed point after 8 rounds (not counted) | 989 s | 623 s | — |
| 8 | 2878207 | 6 | c4/i4/d6 | producer fixed point after 11 rounds | 1,940 s | 925 s | — |
| 10 | 2784767 | 4 | c4/i<=3/d4 | producer fixed point after 13 rounds | 1,997 s | 828 s | — |
| 3 | 5500414 | 6 | c3/i4/d6 | closed, 8 rounds, admitted | 1,109 s | 594 s | full pass, 328 s |
| 12 | 7844815 | 6 | c4/i>=5/d6 | closed, 5 rounds, admitted | 646 s | 395 s | full pass, 184 s |
| 11 | 4028335 | 4 | c4/i>=5/d4 | closed, 5 rounds, admitted | 857 s | 545 s | full pass, 252 s |
| 7 | 2601983 | 4 | c4/i4/d4 | closed, 5 rounds, admitted | 489 s | 352 s | full pass, 151 s |
| 6 | 1949551 | 4 | c4/i4/d4 | producer fixed point after 13 rounds | 1,613 s | 1,297 s | — |
| 9 | 851903 | 2 | c4/i<=3/d2 | producer fixed point after 2 rounds (not counted) | 88 s | 77 s | — |

State 5500414’s orbit was already excluded by SW9’s certificate (flag 3, arity 9,
admitted in exp-250), so its admission leaves the count unchanged, while states 7844815,
4028335 and 2601983 each remove their own orbit.
With all five closures admitted, the certified census counts 72,272 states in 9,165
orbits, the endpoint surviving
([census](../results/exp-252-n17-overnight-per-state-price/census.json)).

The draws run in the survey’s own seeded random order (indices 2, 4, 1, 5, 8, 10, 3, 12,
11, 6, 7, 9). The receipt’s `index` field is the stratified draw position, not that
order. Wall exceeds process CPU by up to about 2.5 times here (1.9 times over the 13
kernel runs) because other agents’ test runs held the host at a load near 10; the
per-state price is read from process CPU.

The receipts are under
[receipts/A](../../../explorations/X048-session-182-overnight/receipts/A/), the admitted
certificate’s small files under the X048 certificates folder, and its objects in the
[hosted-data manifest](../../../../hosted/n17-x048-session-168-certificates.yaml).

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
