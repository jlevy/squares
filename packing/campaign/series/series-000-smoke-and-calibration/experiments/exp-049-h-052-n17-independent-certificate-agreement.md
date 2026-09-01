---
title: exp-049 — H-052 n = 17 independent certificate agreement
softschema:
  contract: packing.squares:Experiment/v2
  schema: ../../../schemas/experiment.schema.yaml
  envelope: experiment
  status: enforced
experiment:
  id: exp-049
  series: series-000
  title: Compare independent exact accumulation with the fixed n = 17 certificate
  date: '2026-09-01'
  hypotheses:
  - H-052
  tier: confirmatory
  subject:
    label: independent exact accumulation agreement for the fixed Massaccesi n = 17 certificate
    engine: sqpack n = 17 independent certificate checker 0.1.0-w7-ready
    engine_commit: d7c94590
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
      Hand-computable exact synthetic atom fixtures with interior and event-boundary
      cases; a separately built source-faithful adapter; frozen atom, weight,
      direction-cell, event-boundary and scaling mutations; the 28-interval versus /29
      grid and inclusive-range source-defect controls; AST independence checks; stable
      serialization; and optimized-Python replay.
    candidate: >-
      A clean-room Fraction-based Cartesian event-cell enumerator that consumes only a
      statically extracted certificate-data manifest and emits the same canonical exact
      per-direction and aggregate invariant manifest as the separately built
      source-faithful adapter, without importing, calling or translating the retained
      two-dimensional difference-array sweep.
    runs_per_condition: 1
    interleaved: false
    operator: openai-codex
    commit: d7c94590
    dirty: true
    entry_point: cases/n17_weighted_certificate/run.py
    command: >-
      uv run --frozen python -m cases.n17_weighted_certificate.run --record
      campaign/series/series-000-smoke-and-calibration/results/exp-049-h-052-n17-independent-certificate-agreement.json
    budget: >-
      115 minutes remain after the target-blind W3 contract cell, ending no later than
      2026-09-01T11:11:55Z. W7 has 40 minutes to build and hash-freeze the independent
      interface before building the source-faithful adapter, pass synthetic,
      provenance, independence and mutation guards, and bind the exact validated
      revision. Any failed readiness guard stops before target execution.
    record: campaign/series/series-000-smoke-and-calibration/results/exp-049-h-052-n17-independent-certificate-agreement.json
  effort:
    timebox: >-
      65 minutes 20 seconds, declared before launch as the fixed
      2026-09-01T09:51:35Z--10:56:55Z W6 interval
    wall_seconds: 3920
    agent_minutes: 65.33333333333333
    stopped_by: timebox
  results:
  - shape: determination
    question: >-
      Did the single preregistered exact target command finish and emit its canonical
      agreement record within the declared W6 timebox?
    role: cost
    outcome: no_progress
    checked_by: >-
      The command was launched exactly once at 2026-09-01T09:51:35Z. At the declared
      2026-09-01T10:56:55Z hard stop, one interrupt ended it with exit 130 while the
      independent Cartesian accumulator was still running. Post-interrupt process-table
      checks found neither the uv parent nor Python child command, and a presence-only
      check found no result JSON.
  verdict:
    decision: unresolved
    needs_review: false
    primary_criterion: >-
      Accept only if both exact paths agree on all 181 canonical direction manifests,
      all 168 atoms, the 29 by 29 grid, total mass 9744/576, global minimum 576/576,
      every event-cell reduction and every declared geometric precondition, and reject
      all five frozen mutations. Reject only for a reproducible exact disagreement after
      both instruments and fixtures pass; otherwise retain an unresolved provenance,
      independence or invalid-instrument refusal.
    reason: >-
      The declared 3920-second W6 timebox expired while the independently accumulated
      target manifest was still running; the single interrupt produced no canonical
      JSON, complete comparison, or checkpoint, so H-052 remains unmeasured and is
      neither accepted nor rejected.
    commit: d7c94590+sha256-309ec24158f73dd2
    resume_from: >-
      Frozen package-manifest SHA-256
      309ec24158f73dd2e9b837c773b1e5c1642f357de5bdf73311b73232abdb6d54
      and clean-room SHA-256
      55d36239f1f7e860f059030d87f655d2ac0c82685d788b599a7dd23d33d18de0;
      no checkpoint, partial canonical record, or result JSON exists, so any resumed
      round must restart the exact command under a newly declared timebox.
---
# Exp-049 — H-052 `n = 17` Independent Certificate Agreement

This record was allocated only after session-065 returned its complete target-blind W3
contract. It binds the future result path above and does not reserve an empty result
file.

## Frozen fixture and independence boundary

The opaque retained verifier digest is
`04531a54da9a654f2318401aff43222daf721bd99e948b2491f91c05bd0b5d3f`. The retained
result-post, LP-post and README digests are
`7dffb6e6e6cbff0ac2e887ca445b45f46c95055718219f7229d1c8cb06f84514`,
`cdd27897f4f6c3b83835d59a317b3248b4f94b888f8568b740c778524a11f177` and
`b48c0c31cf62366d44cd12f02cf321dd38b5a23391caec95f04445938e0b3d75`. The fixed side is
the exact rational `22529/5000`.

The two paths intentionally share the fixture, atom and direction data, geometric
definitions, event-cell reduction, angle-cover lemma, shrink lemma, scaling argument,
canonical manifest and exact-rational type.
They may not share the difference-array control flow.
The clean-room scalar implementation must pass synthetic guards and have its file hash
frozen before the source-faithful adapter is authored or the target verifier is opened.

## W7 admission

Target execution remains closed until the nonexecuting static extractor, canonical
manifest and both accumulation interfaces pass the synthetic known answers, all five
mutations, the provenance and AST independence checks, deterministic serialization and
optimized-Python replay.
Any target-informed edit to the clean-room accumulation logic contaminates this round
and requires a new registration.

## W7 readiness receipt

The direct Cartesian accumulator passed its synthetic known answer, deterministic
serialization, atom, weight, direction-cell, event-boundary and scaling mutations before
its file hash was frozen as
`55d36239f1f7e860f059030d87f655d2ac0c82685d788b599a7dd23d33d18de0`. Only then was the
retained source opened to build the separate difference-array adapter.
The static extractor and source-faithful adapter hashes are
`db176a8eff7235991c63c8e7f098e2e2979edf64905d8f76427e0cd218b011e2` and
`aaccd145c61fb20bc2b83a8ded83dfdd3f2d4b6d6c730ff46df31e1f1d8ae305`. The canonical runner
is `177e8545400799b6a701f258b685f2712f2529132803d78bf984575b897d027c`. The SHA-256 of
the sorted `sha256sum` manifest for every Python file in the instrument package is
`309ec24158f73dd2e9b837c773b1e5c1642f357de5bdf73311b73232abdb6d54`; this also binds the
fixture, shared geometry, canonical model and target adapter.
The post-W7 H-052 readiness revision is bound separately at
`156c0bbfaf8637e0a28077db541da2e8b2e34311fd3745b41292d899485f00b2`. This digest records
the readiness document after W7; it is not one of the four retained source hashes and
carries no unchanged-fixture claim.

Ruff, BasedPyright and eleven focused tests pass.
The production command
`uv run --frozen python -m cases.n17_weighted_certificate.run --selftest` and its
`python -O` form use explicit conditions and exceptions rather than assertions.
Both emit receipt hash
`9c43160ad7b9f7407c5c1f7057838a925a13b4553b4edcde580f8abc58d9ec00`, and both complete
canonical stdout lines hash to
`459af1bd0345bee04e5a3af0d1c7a93cec635920774b3d647be13bed9d617579`. The named receipts
include the actual `/28`-versus-`/29` synthetic grid and the
`KMAX + 1`-versus-omitted-final-endpoint direction control through both accumulation
paths and canonical manifests.
The preregistered result file does not exist.
W6 began only after the coordinator appended and authorized its measurement phase.

## W6 timebox stop

Artifact: The single registered command ran from `2026-09-01T09:51:35Z` through the
declared hard stop at `2026-09-01T10:56:55Z`. One interrupt ended it with exit 130. The
interrupt traceback located execution inside the independent direct Cartesian
accumulator; it exposed no canonical direction row or scientific invariant.

Result: The 3920-second run emitted no canonical JSON, complete
source-versus-independent comparison, mutation result, or checkpoint.
The result path remains absent.
This is a process determination of `no_progress`, not evidence for or against the
agreement criterion.

Guard: The exact command ran once.
After the interrupt, process-table checks found neither command process and the
result-path presence check returned absent.
No rerun, target-informed repair, package change, empty result file, hypothesis
disposition, or frontier adoption occurred.

Next: Keep H-052 readiness true but its scientific disposition unresolved and
review-pending. Route the frozen no-checkpoint timebox outcome to BC-116; any new run
requires a newly declared budget and starts from the same frozen package revision.

Agreement establishes implementation agreement for this one fixed certificate only.
It is not proof-method independence, frontier adoption, an LP-generator audit, or
transfer to `n = 18` or `n = 19`.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
