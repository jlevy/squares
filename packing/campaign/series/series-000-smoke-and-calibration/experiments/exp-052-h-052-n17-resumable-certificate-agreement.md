---
title: exp-052 — H-052 n = 17 resumable certificate agreement
softschema:
  contract: packing.squares:Experiment/v2
  schema: ../../../schemas/experiment.schema.yaml
  envelope: experiment
  status: enforced
experiment:
  id: exp-052
  series: series-000
  title: Resume exact n = 17 certificate agreement without changing the kernels
  date: '2026-09-01'
  hypotheses:
  - H-052
  tier: confirmatory
  subject:
    label: exact all-direction agreement for the retained n = 17 weighted certificate
    engine: sqpack n17 resumable certificate driver 0.1.0-preregistered
    engine_commit: e21598f6
    assurance: verified
    method: exact-algebraic
    host_system: macOS arm64, Apple M1 Pro
    selftest_passed: true
  instance:
    axis: n
    point: 17
    role: target
  method:
    control: >-
      Byte-identical synthetic receipts from the frozen uninterrupted assembler, a new
      external uninterrupted driver, and interrupted-plus-resumed runs; interruptions
      before row zero, between the two accumulators, after a paired row, and before
      assembly; changed-input, gap, duplicate, reorder, chain, payload, truncation,
      path-binding and malformed-rational mutations; normal and optimized Python.
    candidate: >-
      An external direction-sliced driver that calls both unchanged exact accumulators
      for each of the retained 181 directions and atomically preserves only complete
      paired rows in a hash-chained checkpoint before assembling the existing canonical
      H-052 result semantics.
    runs_per_condition: 1
    interleaved: false
    operator: openai-codex
    commit: e21598f6
    dirty: true
    entry_point: cases/n17_weighted_certificate_resume/run.py
    command: >-
      uv run --frozen python -m cases.n17_weighted_certificate_resume.run --record
      campaign/series/series-000-smoke-and-calibration/results/exp-052-h-052-n17-resumable-certificate-agreement.json
      --checkpoint
      campaign/series/series-000-smoke-and-calibration/results/exp-052-h-052-n17-resumable-certificate-agreement.checkpoint.json
      --progress
      campaign/series/series-000-smoke-and-calibration/results/exp-052-h-052-n17-resumable-certificate-agreement.progress.json
    budget: >-
      The fixed BC-116 wall ends at 2026-09-01T14:56:55Z. Two 20-minute target-blind
      W7 cells and one 15-minute independent W2 readmission precede one uninterrupted
      75-minute W6 process. The final 15 minutes are reserved for W3. At the hard stop,
      retain the last valid paired-row prefix and interrupt once; never rerun.
    record: campaign/series/series-000-smoke-and-calibration/results/exp-052-h-052-n17-resumable-certificate-agreement.json
  effort:
    timebox: >-
      One fixed 75-minute W6 interval, declared before launch as
      2026-09-01T13:26:55Z--14:41:55Z; the process started at 13:27:39Z and retained the
      original hard stop.
    wall_seconds: 4456
    agent_minutes: 74.26666666666667
    stopped_by: timebox
  results:
  - shape: determination
    question: >-
      Did the sole preregistered process finish all 181 paired directions inside the
      declared W6 wall while preserving a replayable terminal artifact?
    role: cost
    outcome: criterion_missed
    checked_by: >-
      Frozen-driver replay validated 33 contiguous agreeing rows, ordinals 0--32, and
      the chained ordinal-33 independent-start marker after the one authorized interrupt;
      the canonical result path remained absent.
  verdict:
    decision: unresolved
    needs_review: false
    primary_criterion: >-
      Accept H-052 only if all 181 paired rows agree exactly and every frozen fixture,
      precondition, mutation, provenance and independence guard passes. A valid prefix
      at the deadline is an unresolved process outcome; a row disagreement may reject
      only after every instrument guard passes.
    reason: >-
      The declared timebox ended before all 181 paired rows and the frozen precondition
      and mutation checks completed. The preserved 33-row prefix is valid process
      evidence and every retained pair agrees, but it is not a completed sample under
      H-052's all-direction criterion. No canonical result exists, so H-052 remains
      neither accepted nor rejected.
    commit: e21598f6+sha256-3e5284fd56fd33f7
    resume_from: >-
      Canonical checkpoint SHA-256
      db5c156959b6de4e6f2c9be283454d01dd5f3a436e6489f5e6bb60c38559fdb8
      contains the validated contiguous prefix through ordinal 32, whose last row hash
      is 9badcc57c05e328344b0ec7ae4fbf9815e8eae027a79bec1bf1a35b9871fade6.
      Canonical progress SHA-256
      08e301b01c7ac6eef4b03c3a4daa5f72c5f1bdbe217dbbb061b57f5c94d947af
      records ordinal 33 at `independent_started`, chained to that row. Any continuation
      requires a newly preregistered round that first replays the frozen binding and
      resumes at ordinal 33; exp-052 itself must not be rerun.
---
# Exp-052 — H-052 `n = 17` Resumable Certificate Agreement

Exp-049 established that the independent exact calculation could consume the whole
first-wave budget without publishing even one canonical row.
This round changes only the process boundary: it places atomic, hash-chained checkpoints
around the two frozen scientific accumulators.
It is not a speed claim and does not change H-052’s agreement criterion.

## Frozen Boundary

Session-068 is authoritative for the source hashes, package-manifest digest, exact
fixture constants, ordered directions, checkpoint schema, interruption semantics,
controls, cell clocks and typed outcomes.
The new package may live only at `packing/cases/n17_weighted_certificate_resume/`; every
file under `packing/cases/n17_weighted_certificate/` remains byte-for-byte frozen.

The experiment, result, checkpoint and progress paths share the `exp-052` slug.
At preregistration the three output paths were absent.
A checkpoint is process evidence, not an experiment result, and a progress marker cannot
contain or stand in for a completed paired row.

## Admission and Outcome Boundary

W6 remains closed until target-blind equivalence and corruption controls pass at a
frozen revision and an independent W2 reviewer confirms that the driver imports rather
than translates both accumulators.
Resume must reverify every input, binding, ordinal, direction and hash-chain link before
continuing at the first incomplete direction.

A deadline with a valid prefix records the prefix length, active stage, elapsed cost and
restart ordinal as `needs_review: true`; it does not decide H-052. A complete exact
agreement or guarded disagreement also remains review-pending for BC-120 and BC-121 and
does not adopt the retained certificate as a frontier result.

## W2 Readmission

Independent W2 replay admitted driver
`3e5284fd56fd33f7b767954164128e9d43f5efad09eae4666035c3ef32c63f54` and focused test
`4226ab0cb5f9e46256b5fc47d5bc493dfbb6ef77354e9e7a61d624ba4db76a53`. Six focused tests
and twenty-seven named selftest guards passed with zero skips.
Normal and optimized Python emitted byte-identical receipt SHA-256
`beaf5b2b9bcaa0b95ff053c8f6e0aa955d075d21d877460c52b779a68d60ca60`; the frozen
scientific-package manifest remained
`309ec24158f73dd2e9b837c773b1e5c1642f357de5bdf73311b73232abdb6d54`. The result,
checkpoint and progress paths were absent at admission.
W6 remains limited to the one preregistered process and fixed wall.

## W6 Timebox Stop

Artifact: The sole registered command ran once from `2026-09-01T13:27:39Z` until the
fixed `2026-09-01T14:41:55Z` hard stop.
One PTY interrupt returned exit 130 with a `KeyboardInterrupt` inside the unchanged
independent accumulator.
Both process IDs were absent afterward.

Result: Read-only replay through the frozen driver validated 33 contiguous paired rows,
ordinals 0--32, all with exact source/independent agreement.
The last row hash is `9badcc57c05e328344b0ec7ae4fbf9815e8eae027a79bec1bf1a35b9871fade6`.
The canonical progress marker records ordinal 33 at `independent_started` and chains to
that hash. The checkpoint and progress artifacts hash to
`db5c156959b6de4e6f2c9be283454d01dd5f3a436e6489f5e6bb60c38559fdb8` and
`08e301b01c7ac6eef4b03c3a4daa5f72c5f1bdbe217dbbb061b57f5c94d947af`. The result path is
absent.

Guard: The replay validated the exp-052 binding, canonical serialization, frozen input
digests, direction order, manifest direction and event hashes, row hashes, previous-row
chain, agreement flags, and nonfuture progress marker.
No rerun, repair, target-informed edit, empty result, H-052 disposition, or frontier
adoption occurred.

Next: Keep exp-052 `needs_review: true` and H-052 scientifically unresolved.
Prefix agreement is not a sample-based H-052 decision because 148 paired directions plus
the frozen precondition and mutation decisions remain unevaluated.
A continuation must use a newly preregistered resume round from ordinal 33.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
