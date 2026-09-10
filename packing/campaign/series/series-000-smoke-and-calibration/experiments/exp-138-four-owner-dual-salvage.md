---
title: "exp-138 \u2014 shared-screen four-owner obstruction verdict"
softschema:
  contract: packing.squares:Experiment/v2
  schema: ../../../schemas/experiment.schema.yaml
  envelope: experiment
  status: enforced
experiment:
  id: exp-138
  series: series-000
  title: Four-owner verdict from the shared exact footprint screen
  date: '2026-09-09'
  hypotheses:
  - H-138
  tier: exploratory
  known_defects:
  - D-489
  subject:
    label: Exact translated BC232 depth-one family and full-net guaranteed owner footprints
    engine: devtools.screen_corner_dual_salvage and devtools.owner_footprints; published launch-head receipt
      binds source
    assurance: verified
    method: exact-algebraic
    host_system: Darwin arm64; project Python3.14.7; one process
    selftest_passed: true
    engine_commit: 223c969d
  instance:
    axis: n
    point: 11
    role: target
  method:
    control: Source768 family has exact pointwise depth1 and mass21342289572/2055263195; point and triangle
      filters are nested geometric controls.
    candidate: Translate all original poses by(+1/100,+1/100), scale1; retain only full canonical direction
      members strictly separated from each endpoint footprint. Enumerate16one-corner and65536four-corner
      combinations for each of point,triangle,endpoint.
    runs_per_condition: 1
    interleaved: false
    operator: GPT-6 Astra, max; session113 coordinator
    entry_point: packing/devtools/screen_corner_dual_salvage.py
    budget: This record consumes the single shared exp137 producer receipt; it authorizes no second target
      process. All producer wall time is charged once to exp137. Complete65536endpoint classes required,
      with point/triangle nested controls.
    record: packing/campaign/series/series-000-smoke-and-calibration/results/agenda-032/exp-137-corner-dual-salvage.json.gz
    command: cd packing && /opt/homebrew/bin/timeout --signal=TERM --kill-after=2s 5m .venv/bin/python3
      -m devtools.screen_corner_dual_salvage campaign/series/series-000-smoke-and-calibration/results/agenda-025/bc-232-leg-01-family.json
      --footprint-kinds point,triangle,endpoint --corner-counts 1,4 --target-side 96/25 --expect-source-blob
      8a0bf1a264a1361649bc0acd0f70907ba8125f2f --out campaign/series/series-000-smoke-and-calibration/results/agenda-032/exp-137-corner-dual-salvage.json.gz
    commit: 223c969d
  results:
  - shape: determination
    role: outcome
    question: The minimum endpoint survivor mass over all65536four-owner combinations is at least7.
    outcome: criterion_missed
    checked_by: Exact source-bound producer summaries and complete class records; independently replayed
      by exp141 at published source44bf815f.
  verdict:
    decision: rejected
    primary_criterion: The minimum endpoint survivor mass over all65536four-owner combinations is at least7.
    reason: Complete exact producer screen found0of65536endpoint combinations with massatleast7; maximum13394344077/2055263195
      and minimum1642317587/2055263195. Sharedproducerchargedtoexp137; no secondprocess. Independent retained-receipt
      audit exp141 confirmed all exact checks.
    needs_review: false
  effort:
    timebox: One shared five-minute producer ownedbyexp137; no duplicateprocessfor138
    wall_seconds: 0
    stopped_by: criterion
---
# Exp138: Four-Owner Verdict from the Shared Screen

**Source-scope annotation, September 10, 2026 ([D-489](../../../../../defects.md)).**
The declared source has mass `21342289572/2055263195`, about `10.3842`, below eleven.
The screen’s source predicate accepts that particular deficient receipt but refuses
valid mass-eleven source receipts.
Fix the predicate before using the instrument for that broader input class (tracked as
`think-rm5c`). This does not invalidate this experiment’s exact negative on its named
source; exp141 independently confirmed the arithmetic and complete retained enumeration.
It supplies no negative verdict on other fractional families or on the conditional cover
method. The later mass-eleven X1 screen is a different source comparison.

Complete exact producer screen found0of65536endpoint combinations with massatleast7;
maximum13394344077/2055263195 and minimum1642317587/2055263195.
Sharedproducerchargedtoexp137; no secondprocess.
Exp141 independently confirmed the complete retained receipt, so this verdict no longer
needs review.

This separate prospective verdict applies H138 to the four-owner portion of exp137’s
single producer receipt.
It authorizes no second process and charges no duplicate producer wall time.
The source, geometry, direction membership, exact SAT, complete class enumeration,
timeout and provenance obligations are exactly those declared in
[exp137](exp-137-corner-dual-salvage.md).

Accept H138 only if all65536endpoint-footprint combinations retain exact mass at least
seven. A lower mass rejects this specific retained-family claim; it does not prove that
the affected residual covering problem has a useful solution.
Incomplete data or a guard failure is unresolved.
This record was created before any target filtering, so a result on H137 cannot silently
dictate H138’s verdict.

## Limitation attached 2026-09-10: D-489, the source filter

`devtools/screen_corner_dual_salvage.py:_source_receipt` required the source family’s
own `verify_ceiling` receipt to carry `failures == ["K3 total weight at least n"]`
exactly, which is the failure a family records when its total weight is **below** `n`.
The predicate therefore admitted only a source short of mass `n` and refused every
proved ceiling family, and this round was run under it.
The defect is [`D-489`](../../../../../defects.md).

**What still stands.** Every exact verdict here remains valid **for the source family it
names**, `agenda-025/bc-232-leg-01-family.json` of total weight
`21342289572/2055263195 = 10.384212`. The arithmetic was never in question: `exp-141`
independently re-audited this round with 147,456 exact SAT checks and agreed.

**What must not be inferred.** The negative reading does not transfer to conditioning in
general, because the source is `1265605573/2055263195 = 0.6158` short of eleven and
every shortfall reported here is smaller than that deficit.
Re-run on the mass-eleven ceiling family, the same `screen_footprint` reads survivor
weight exactly 10 at four of the sixteen one-corner classes and exactly 7 at the
corresponding four-corner combination.
That measurement is
[lane X1](../results/agenda-034/lane-x1-corner-conditioning-is-mass-neutral.md), and its
scope is the ladder in
[X-026](../../../explorations/X-026-what-conditioning-does-and-does-not-buy.md).

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
