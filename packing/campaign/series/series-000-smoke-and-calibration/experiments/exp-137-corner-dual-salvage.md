---
title: "exp-137 \u2014 exact owner-footprint fractional-family deletion screen"
softschema:
  contract: packing.squares:Experiment/v2
  schema: ../../../schemas/experiment.schema.yaml
  envelope: experiment
  status: enforced
experiment:
  id: exp-137
  series: series-000
  title: Exact owner-footprint fractional-family deletion screen
  date: '2026-09-09'
  hypotheses:
  - H-137
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
    command: cd packing && /opt/homebrew/bin/timeout --signal=TERM --kill-after=2s 5m .venv/bin/python3
      -m devtools.screen_corner_dual_salvage campaign/series/series-000-smoke-and-calibration/results/agenda-025/bc-232-leg-01-family.json
      --footprint-kinds point,triangle,endpoint --corner-counts 1,4 --target-side 96/25 --expect-source-blob
      8a0bf1a264a1361649bc0acd0f70907ba8125f2f --out campaign/series/series-000-smoke-and-calibration/results/agenda-032/exp-137-corner-dual-salvage.json.gz
    budget: One exact target process, five-minute external timeout plus two-second TERM grace. At most3kinds
      times64component screens times768sourceposes;3times65536joint masks. No LP, target retries, alternative
      family, or repeated full arrangement verification. Retain compressed raw class receipts and process/exit
      evidence.
    record: packing/campaign/series/series-000-smoke-and-calibration/results/agenda-032/exp-137-corner-dual-salvage.json.gz
    commit: 223c969d
  results:
  - shape: determination
    role: outcome
    question: The maximum endpoint one-corner survivor mass is at least10. H138 has its own prospective
      verdict record exp138 over the same producer receipt.
    outcome: criterion_missed
    checked_by: Exact source-bound producer summaries and complete class records; independently replayed
      by exp141 at published source44bf815f.
  verdict:
    decision: rejected
    primary_criterion: The maximum endpoint one-corner survivor mass is at least10. H138 has its own prospective
      verdict record exp138 over the same producer receipt.
    reason: Complete exact producer screen found0of16endpoint classes with massatleast10; maximum77421212793/8221052780.
      This particular retained-family obstruction conjecture fails; the conditionalcover method remains
      open. Exp141 independently confirmed the source identities, directions, transports, positiveSAT gaps,
      masks, cardinalities, exact masses and summaries.
    needs_review: false
  effort:
    timebox: One shared five-minute producer ownedbyexp137; no duplicateprocessfor138
    wall_seconds: 53.38
    stopped_by: criterion
---
# Exp137: Exact Fractional-Family Obstruction Screen

Complete exact producer screen found0of16endpoint classes with massatleast10;
maximum77421212793/8221052780. This particular retained-family obstruction conjecture
fails; the conditionalcover method remains open.
Exp141 independently confirmed the retained receipt, so this verdict no longer needs
review.

This protocol is recorded before target filtering.
The unchanged source family has Git blob `8a0bf1a264a1361649bc0acd0f70907ba8125f2f` and
a retained exact depth-one receipt.
The published instrument must bind those bytes, all source poses and the
full361-direction manifest.
Quarter-turn canonicalization changes square naming, never the actual pose.
Translation changes no weight or angle.

Every survivor has an exact positive separating gap from the closed footprint.
Touching poses are removed.
Nonnegative deletion inherits the all-point depth bound; no new depth arrangement needs
to be computed for each class.
The resulting lower bound applies to covering measures on arbitrary supports, including
banked objectives. It is a consequence of the retained exact source receipt, not a fresh
independent reverification of that original arrangement.

H137 asks whether at least one single-owner endpoint class obstructs massbelow10. Exp138
separately tests H138: every four-owner endpoint combination obstructs massbelow7.
Report the two verdicts separately: neither is inferred from a sample of classes.
Point and triangle runs are nested controls and useful scope comparisons.
A mass below the threshold fails this particular witness test only; it cannot establish
that a useful cover exists.
A timeout, provenance failure or incomplete enumeration is unresolved, with no silent
retry.

The target is admitted only after the geometry/SAT/source-binding controls pass, and its
protocol and instrument are committed and pushed.
Retain actual source HEAD, UTC launch, exit and wall time.
Compressed JSON preserves every raw class and its component witness; the screen does not
change the global packing bracket.

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
