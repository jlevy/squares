---
title: exp-119 — exact near-45 A3 forcing on a moving triangle
softschema:
  contract: packing.squares:Experiment/v2
  schema: ../../../schemas/experiment.schema.yaml
  envelope: experiment
  status: enforced
experiment:
  id: exp-119
  series: series-000
  title: Test the complete canonical near-45 A3 forcing clause
  date: '2026-09-07'
  hypotheses: [H-108]
  tier: confirmatory
  subject:
    label: Fixed q=1939/500 and A3 formulas throughout both closed near-45 angle signs
    engine: Exact formal-vertex producer and independent polarized-Bernstein reader
    engine_commit: bdc687841467599231b59447b38f9037625deb43
    assurance: verified
    method: exact-algebraic
    host_system: macOS arm64, Python 3.14.7; GNU coreutils timeout 9.9
    selftest_passed: true
  instance: {axis: n, point: 11, role: target}
  method:
    control: >-
      Thirteen source-free producer controls and seventeen source-free reader
      controls passed separate mathematical reviews. They cover direct polynomial
      identities, positive denominators, a nonvacuous unrelated toy cover,
      empty/singleton/full triangles, negatives, exact packet identity and refusal.
      No target or original-source geometry was evaluated during readiness.
    candidate: >-
      Side 1939/500, unchanged A3=(3/2,13/10), canonical region [1,q/2]x[0,1],
      and both closed half-angle slabs [-110880/50803079,0] and
      [0,110880/50803079] around pi/4. Check E,F,G and all four signed margins:
      24 unsplit Bernstein obligations, including duplicates.
    runs_per_condition: 1
    interleaved: false
    operator: Codex coordinator, max mathematical reasoning, Session 090 BC-255
    commit: bdc687841467599231b59447b38f9037625deb43
    dirty: false
    entry_point: packing/devtools/angle_near45_triangle_control.py
    command: >-
      /usr/bin/time -p /opt/homebrew/bin/timeout --signal=KILL 10s
      env PYTHONPATH=src OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1
      /Users/levy/wrk/github/squares/packing/.venv/bin/python3
      -m devtools.angle_near45_triangle_control --target-a3
      --output /Users/levy/wrk/github/squares/packing/campaign/series/series-000-smoke-and-calibration/results/exp-119-h-108-near45-a3-forcing/packet.json
      --log /Users/levy/wrk/github/squares/packing/campaign/series/series-000-smoke-and-calibration/results/exp-119-h-108-near45-a3-forcing/worker.log
    budget: >-
      One ten-second external producer cap, in addition to its existing child and
      worker caps. Only complete positive output with actual exit zero earns one
      independent file replay with a separate ten-second external and internal cap.
      No retries, subdivision, point changes, side changes or angle narrowing.
    record: packing/campaign/series/series-000-smoke-and-calibration/results/exp-119-h-108-near45-a3-forcing/packet.json
  effort:
    timebox: One ten-second producer and one ten-second independent reader, each invoked once
    wall_seconds: 0.67
    stopped_by: criterion
  results:
  - shape: determination
    role: outcome
    question: Does every declared canonical near-45 P10 avoider contain A3?
    outcome: criterion_met
    checked_by: >-
      Producer completed all 24 formal-vertex inequalities with actual exit zero.
      The source-distinct reader returned actual exit zero, decision proved,
      six vertex-slab checks, 24 independent inequalities and no unresolved entries.
      The generic two-point implication and outward-angle premise were reviewed
      separately; no localization or global packing conclusion follows.
  verdict:
    decision: accepted
    primary_criterion: Complete independently verified A3 forcing in the declared canonical near-45 domain.
    reason: The complete canonical A3 forcing implication passed the independent exact reader on both closed angle signs.
    commit: 97cf8dde
---
# exp-119 — Near-45 A3 Forcing

H-108 is accepted. The sole producer ran after the observed 03:34:05 UTC preflight and
before 03:34:32 UTC, returning actual exit zero, all 24 inequalities and no unresolved
entries. The independent reader ran once at the observed 03:35:51 UTC boundary and
returned actual exit zero, six vertex-slab checks, all 24 independent inequalities and
the exact side, point and slab identity.
Its operator interval was 03:35:28–03:36:41 UTC. Both commands used clean immutable
`bdc68784`.

The prospective protocol was committed at `97cf8dde`; all 31 record checks passed in
29.92 seconds before dispatch.
Producer process cost was 0.57 seconds wall and 0.23 CPU seconds; the independent reader
used 0.10 seconds wall and 0.09 CPU seconds.
Total process costs were 0.67 seconds wall and 0.32 CPU seconds, distinct from author,
review and operator time.
Neither ten-second allowance was repeated or extended.
The result directory retains both streams, the packet, worker log and independent
replay.

This proves only the canonical A3 clause.

## Retained Prospective Protocol

This tests [H-108](../../../hypotheses/H-108-near45-canonical-a3-forcing.md), one
auxiliary clause of H-036. The hand-derived reduction proves that a canonical contained
square avoiding just L and M lies in the closed triangle used by the instrument.
Avoiding P10 implies that weaker two-point antecedent, so the proved implication is
stronger than the registered P10 claim.
The reader independently derives its own margins and degree-four polarized Bernstein
coefficients; it does not trust the producer’s coefficients or counters as a proof.

The producer review under `think-vnwo` accepted the complete triangle argument and its
positive denominator clearing.
Its thirteen controls independently passed in 0.38 seconds wall and 0.32 CPU. The
separate reader review under `think-1bxf` completed at 03:27:57 UTC: seventeen
source-free controls passed in 0.95 seconds wall and 0.75 CPU, with clean Ruff,
formatting and BasedPyright checks.
Neither review evaluated the target.
The earlier full-P10 source result is not asserted as a known-positive control of the
stronger two-point implication.

Commit this protocol and pass record checks before dispatch.
Both commands run from a clean detached `bdc68784` checkout’s `packing/` directory, with
`PYTHONPATH=src` selecting that source and the existing Python 3.14 environment
supplying dependencies.
The result directory and every output path must be fresh.
Atomic publication does not prevent overwrite, so freshness is checked by the
coordinator before the sole launch.

Retain producer stdout as `stdout.log`, external stderr/timing as `run.log`, and the
producer’s own `worker.log` and `packet.json`. An actual exit zero, `status=proved`, all
24 inequalities and an empty unresolved inventory permit one independent reader:

```bash
/usr/bin/time -p /opt/homebrew/bin/timeout --signal=KILL 10s env PYTHONPATH=src /Users/levy/wrk/github/squares/packing/.venv/bin/python3 -m devtools.check_angle_near45_triangle_control ABSOLUTE_PACKET_PATH --target-a3
```

Retain its stdout as `replay.json` and stderr/timing as `replay.log`. Accept only actual
exit zero, `decision=proved`, exactly six vertex-slab checks, all 24 independent
inequalities, fixed side/point/slabs and no unresolved inventory.
The internal alarm does not cover imports or final serialization; external exits remain
mandatory.
If the producer is incomplete, externally killed or nonpositive, do not invoke
the reader; retain an explicit non-invocation note rather than an invented receipt.

Producer and reader share exact `NumberField` arithmetic.
The reader also shares the bounded JSON loader.
The analytic angle bound and generic avoidance-to-triangle proof are explicit
mathematical premises, not facts inferred from counters.

A failed formal vertex, negative Bernstein coefficient, timeout or missing output is
unresolved, not a counterexample.
The instrument deliberately checks an enlarged center and angle domain, including formal
vertices when the triangle is empty.
This profile has no rejection path and no automatic repair.
Success does not establish localization, A1/A2 forcing, twelve-point coverage, H-036 or
a global packing bound.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
