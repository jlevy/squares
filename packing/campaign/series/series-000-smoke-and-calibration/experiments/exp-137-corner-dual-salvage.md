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

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
