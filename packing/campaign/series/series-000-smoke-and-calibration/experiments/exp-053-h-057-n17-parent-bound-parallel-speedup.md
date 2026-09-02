---
title: exp-053 — H-057 n = 17 parent-bound parallel speedup
softschema:
  contract: packing.squares:Experiment/v2
  schema: ../../../schemas/experiment.schema.yaml
  envelope: experiment
  status: enforced
experiment:
  id: exp-053
  series: series-000
  title: Profile parent-bound parallel execution on three fixed n = 17 directions
  date: '2026-09-01'
  hypotheses: [H-057]
  tier: exploratory
  subject:
    label: fixed-input parent-bound process speed and exact byte equivalence
    engine: sqpack n17 parent-bound parallel profiler 0.1.0-preregistered
    engine_commit: 909efafa0773fbea23b24de072ef59a03a01317a
    assurance: verified
    method: exact-algebraic
    host_system: macOS arm64, Apple M1 Pro
    selftest_passed: true
  instance:
    axis: n
    point: 17
    role: calibration
  method:
    control: >-
      The unchanged exp-052 serial kernels on ordinals 33, 107 and 180, with the frozen
      checkpoint and progress inputs read-only.
    candidate: >-
      Three parent-bound worker processes writing disjoint fragments followed by one
      deterministic merger that validates and emits canonical rows.
    runs_per_condition: 3
    trials: 3
    interleaved: true
    operator: openai-codex
    commit: 909efafa0773fbea23b24de072ef59a03a01317a
    dirty: true
    entry_point: benchmarks/n17_weighted_certificate_parallel.py
    command: >-
      From packing/, execute the four exact pair and assemble invocations in the Frozen
      Commands section once, in order; each pair has its own exclusive output root.
    budget: >-
      BC-123 receives 150 minutes through 2026-09-02T02:45:00Z. Measurement begins only
      after target-blind corruption controls and independent W2 admission pass.
    record: campaign/series/series-000-smoke-and-calibration/results/exp-053-h-057-n17-parent-bound-parallel-speedup.json
  effort:
    timebox: >-
      One fixed BC-123 build, admission and measurement wall through
      2026-09-02T02:45:00Z; the contamination guard ended measurement before Pair 1
      could complete.
    wall_seconds: 738
    agent_minutes: 107.83333333333333
    stopped_by: guard
  results:
  - shape: determination
    question: >-
      Did the complete three-pair AB/BA/AB speed profile remain admissible under the
      preregistered quiet-host timing regime?
    role: guard
    outcome: invalid
    checked_by: >-
      The coordinator observed sustained unrelated CPU-heavy work begin only during
      Pair 1's parallel arm, after its serial arm was durable, and invoked the
      contamination kill guard. Cleanup retained arm A, removed the partial arm B and
      left no profiler child; the Pair 1 receipt and sample, arm B, Pairs 2--3 and the
      canonical result are absent.
  - shape: determination
    question: >-
      Did the durable serial arm produce exact source-faithful and target-independent
      agreement for fixed ordinals 33, 107 and 180 in a valid child chain from the
      frozen exp-052 parent hash?
    role: guard
    outcome: criterion_met
    checked_by: >-
      Exact arm replay independently reparsed all three canonical fragments, recomputed
      their event hashes, confirmed source-faithful equals target-independent at each
      ordinal, rebuilt the ordered child chain from parent row hash
      9badcc57c05e328344b0ec7ae4fbf9815e8eae027a79bec1bf1a35b9871fade6 and matched
      merged SHA-256 bd383747cfcfaf2c13c800c1b09fa4e430ef3d2f5f04106d7d9f37482dce33ba.
      This is not serial-versus-parallel equivalence, a paired timing sample or an H-052
      decision.
  verdict:
    decision: unresolved
    needs_review: true
    primary_criterion: >-
      Median paired speedup is at least 2.8x, every candidate row and merged chain is
      byte-identical to serial, no pair is at or below 1x, and every corruption and
      interruption mutation rejects.
    reason: >-
      Asymmetric external CPU load contaminated Pair 1's parallel arm after the serial
      control completed, so no paired timing is admissible and H-057 remains neither
      accepted nor rejected. The durable serial arm records 524.743164166 seconds of
      process cost, not a speedup sample; the interrupted parallel arm, Pair 1 receipt,
      Pairs 2--3 and canonical result do not exist. The 738-second effort is a
      conservative observed command wall, bounded from the 01:49:22Z process start
      through the 02:01:40Z cleanup observation, not a nanosecond timing receipt.
    commit: 909efafa+sha256-e31abda6ce13df47
    resume_from: >-
      A future separately preregistered round may bind the immutable durable arm A at
      campaign/series/series-000-smoke-and-calibration/results/exp-053-h-057-n17-parent-bound-parallel-speedup.raw/pair-01-ab/arm-A,
      receipt SHA-256
      30c40271a8e8fc71dac8c3f8ee9750b09338ca1d3e8375cfb79cf0daba0f6b93, only as
      historical process-cost evidence. A valid timing round must allocate fresh paired
      roots and fresh conditions under its own preregistered quiet regime; it cannot
      pair this stale control with a later candidate. Exp-053 itself must not resume.
---
# Exp-053 — H-057 `n = 17` Parent-Bound Parallel Speedup

This preregistration allocates the experiment and output paths before any writer or
profile starts. Exp-052 and its checkpoint and progress files remain read-only.

The three fixed ordinals are an admission discriminator.
They do not establish the cost of the remaining 148 directions or decide H-052.

## Frozen Commands

Run once from `packing/`, after W2 admission and with no competing CPU-heavy command:

```bash
uv run --frozen --all-extras --group dev python -m benchmarks.n17_weighted_certificate_parallel pair --experiment exp-053 --session session-073 --parent-checkpoint campaign/series/series-000-smoke-and-calibration/results/exp-052-h-052-n17-resumable-certificate-agreement.checkpoint.json --parent-progress campaign/series/series-000-smoke-and-calibration/results/exp-052-h-052-n17-resumable-certificate-agreement.progress.json --ordinals 33 107 180 --workers 3 --start-method spawn --pair-index 1 --order AB --output-root campaign/series/series-000-smoke-and-calibration/results/exp-053-h-057-n17-parent-bound-parallel-speedup.raw/pair-01-ab
uv run --frozen --all-extras --group dev python -m benchmarks.n17_weighted_certificate_parallel pair --experiment exp-053 --session session-073 --parent-checkpoint campaign/series/series-000-smoke-and-calibration/results/exp-052-h-052-n17-resumable-certificate-agreement.checkpoint.json --parent-progress campaign/series/series-000-smoke-and-calibration/results/exp-052-h-052-n17-resumable-certificate-agreement.progress.json --ordinals 33 107 180 --workers 3 --start-method spawn --pair-index 2 --order BA --output-root campaign/series/series-000-smoke-and-calibration/results/exp-053-h-057-n17-parent-bound-parallel-speedup.raw/pair-02-ba
uv run --frozen --all-extras --group dev python -m benchmarks.n17_weighted_certificate_parallel pair --experiment exp-053 --session session-073 --parent-checkpoint campaign/series/series-000-smoke-and-calibration/results/exp-052-h-052-n17-resumable-certificate-agreement.checkpoint.json --parent-progress campaign/series/series-000-smoke-and-calibration/results/exp-052-h-052-n17-resumable-certificate-agreement.progress.json --ordinals 33 107 180 --workers 3 --start-method spawn --pair-index 3 --order AB --output-root campaign/series/series-000-smoke-and-calibration/results/exp-053-h-057-n17-parent-bound-parallel-speedup.raw/pair-03-ab
uv run --frozen --all-extras --group dev python -m benchmarks.n17_weighted_certificate_parallel assemble --experiment exp-053 --session session-073 --raw-root campaign/series/series-000-smoke-and-calibration/results/exp-053-h-057-n17-parent-bound-parallel-speedup.raw --record campaign/series/series-000-smoke-and-calibration/results/exp-053-h-057-n17-parent-bound-parallel-speedup.json
```

The scored paired change is the median of `(parallel - serial) / serial`, not the ratio
of medians. The `2.8x` threshold is `change_pct <= -64.285714%`; every paired speedup
must also exceed `1x`.

## Frozen Input Boundary

The launch revision is `909efafa0773fbea23b24de072ef59a03a01317a`. The read-only exp-052
checkpoint and progress SHA-256 digests are
`db5c156959b6de4e6f2c9be283454d01dd5f3a436e6489f5e6bb60c38559fdb8` and
`08e301b01c7ac6eef4b03c3a4daa5f72c5f1bdbe217dbbb061b57f5c94d947af`. The checkpoint
contains ordinals `0` through `32`; the first profile row chains from row hash
`9badcc57c05e328344b0ec7ae4fbf9815e8eae027a79bec1bf1a35b9871fade6`. The progress marker
remains at ordinal `33`, stage `independent_started`, with binding hash
`2446fa39e154800410b9b5cc19f19aed7cc0c797d116f7ece1c97a2c7c0b4d1a`.

The retained fixture, ordered directions and frozen scientific package remain bound to
`112fc6313def2fb05edd550e2948a1ed51bd262c581c55e52785973d31827a06`,
`cc789e1a16d190064a0eda2fe5e4bf0399d939362c85fb448f1162ef5cac4e79` and
`309ec24158f73dd2e9b837c773b1e5c1642f357de5bdf73311b73232abdb6d54`. Neither workers nor
the merger may write an exp-052 path.

Independent W2 admitted the 30-guard target-blind instrument before measurement.
The instrument-ready H-057 record is bound at SHA-256
`77c82bd2c82886933a82cbe9c175183dcdac3d037ea8d5b8e648cd66a7f7bbbd`.

## Fragment and Timing Contract

Each worker receives one preassigned ordinal and one fresh path under its arm’s private
working directory. It imports both unchanged accumulators, writes one canonical exact
fragment and cannot write the parent checkpoint.
The single parent process validates the binding, ordinal, direction, event hashes,
manifest equality and complete selected set before sorting rows as `33`, `107`, `180`
and deriving the profile-only hash chain.
The serial and parallel arms must produce identical merged bytes.

Arm wall time starts before serial dispatch or cold process-pool creation and stops
after fragment validation and deterministic merge.
A complete arm is renamed into its durable location atomically.
Interrupted partial directories are removed without touching a completed arm, so a
resumed pair never reruns completed evidence.

## Terminal Contamination Stop

Pair 1’s serial arm completed before unrelated sustained CPU-heavy processes appeared.
The coordinator stopped the parallel arm under the preregistered quiet-host guard.
Cleanup left no arm B, partial directory or child process; Pair 1 never became a paired
sample, and Pairs 2 and 3 never opened.

The retained serial receipt has SHA-256
`30c40271a8e8fc71dac8c3f8ee9750b09338ca1d3e8375cfb79cf0daba0f6b93`, elapsed time
`524743164166` nanoseconds and merged SHA-256
`bd383747cfcfaf2c13c800c1b09fa4e430ef3d2f5f04106d7d9f37482dce33ba`. These bytes price
the serial workload but cannot support any paired speed or H-057 claim.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
