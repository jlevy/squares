---
title: exp-051 — H-053 n = 68 refusal localization
softschema:
  contract: packing.squares:Experiment/v2
  schema: ../../../schemas/experiment.schema.yaml
  envelope: experiment
  status: enforced
experiment:
  id: exp-051
  series: series-000
  title: Localize the n = 68 parent precision refusal on one polygon
  date: '2026-09-01'
  hypotheses:
  - H-053
  tier: exploratory
  subject:
    label: proof-carrying compatible-pose localization for one deterministic n = 68 parent polygon
    engine: sqpack UnitSquare rational pose enclosure 0.1.0-preregistered
    engine_commit: e21598f6
    assurance: verified
    method: interval-certified
    host_system: macOS arm64, Apple M1 Pro
    selftest_passed: false
  instance:
    axis: n
    point: 68
    role: target
  method:
    control: >-
      Exact axis-aligned and rational-half-angle rotated squares; exact affine and nested
      transforms; outward-certified or refused decimal rotation; wall interior, tangent
      and crossing cases; separated, tangent and overlapping pairs; cyclic and reversed
      corners; source-cell, digest, transform-order, cover-completeness, sign,
      child-channel, cleanup and atomic-write mutations.
    candidate: >-
      A rational half-angle existence witness plus complete rational outer-cover and
      outward sign certificate for the lexicographically first stable-id polygon from
      one hash-verified ephemeral n = 68 parent, evaluated separately under
      declared:svg-literal, nearest-6 and truncate-6 by an independently authored
      verifier and injection-tested runner.
    runs_per_condition: 1
    interleaved: false
    operator: openai-codex
    commit: e21598f6
    dirty: true
    entry_point: cases/unitsquare_precision/refusal/run.py
    command: >-
      uv run --frozen python -m cases.unitsquare_precision.refusal.run --record
      campaign/series/series-000-smoke-and-calibration/results/exp-051-h-053-n68-refusal-localization.json
    budget: >-
      The fixed BC-117 wall ends at 2026-09-01T14:56:55Z. Three 25-minute W7 cells must
      establish the exact witness, complete outer cover, independent verifier, injected
      runner, cleanup and atomicity before two 25-minute W6 cells may retrieve one parent
      and localize one polygon. The final 20 minutes are reserved for W3. No child access
      or full H-053 determination is permitted.
    record: campaign/series/series-000-smoke-and-calibration/results/exp-051-h-053-n68-refusal-localization.json
  effort:
    timebox: 75m target-blind W7 instrument wall
    wall_seconds: 4500
    agent_minutes: 75
    stopped_by: guard
  results:
  - shape: determination
    question: >-
      Did the exact preregistered `--record` command expose the complete authorized
      runner required before n = 68 target access?
    role: guard
    outcome: invalid
    checked_by: >-
      Independent W2 invoked the exact command against the absent result path; argument
      parsing exited 2 because `_main` exposes only `--selftest` and
      `--runner-selftest`, with no production dependency-injection or adapter entry.
  verdict:
    decision: blocked
    needs_review: true
    primary_criterion: >-
      Retain the first reproducible localization among instrument defect, provenance,
      affine transform, serialization, pose compatibility, compatible localized pose or
      unresolved proof node, after every target-blind proof and runner guard passes. This
      one-parent, one-polygon result cannot accept or reject H-053.
    reason: >-
      Typed premeasurement stop `executable-runner`: the proof, verifier and generic
      injected-runner controls pass, but the exact preregistered `--record` command exits
      2 before target access because no production CLI adapter exists; no scientific
      H-053 disposition follows.
    commit: e21598f6+sha256-3d91046ad9d4ea7b
---
# Exp-051 — H-053 `n = 68` Refusal Localization

This round reduces exp-047’s target-blind precision refusal to one proof-carrying
single-square decision.
It does not repeat H-053’s full n = 68/69 paired determination, select an H-051 arm,
inspect a child, infer contacts or run surgery.

## Frozen Baseline and Parent

The immutable numerical-prototype baseline is commit `d7c94590`:

- `unitsquare_precision.py`:
  `92e7b6e43b8785c0b618f2a48c3a26c09afb1b5cd9009a69189dfab0f606b22c`
- `test_unitsquare_precision.py`:
  `9aeaf96d45fd94ba38af00a713a76297077a1aa7c55efc6783d6c94561c2038f`
- `readiness-controls.json`:
  `fe3a17fc3f4573c80ca0d9b00987b831d483ac4ba9ac13f288bad34e0e2cec4f`

The only target source is the ephemeral parent at
`https://kingbird.myphotos.cc/packing/square-68.svg`, expected SHA-256
`558fbdddfeb0b2f8752b88e172d2776544beb4d2a7122189ef77c1e1c5ebdc6d`. The cited side token
`8.80345993651653` carries no implicit exactness or one-sided-bound semantics.
After digest and structural checks, the runner selects the lexicographically smallest
stable square id. Raw bytes, XML, source excerpts, palettes and temporary paths may not
be retained.

Every retained child byte, pose, side, reduction, gain and derived child summary is
embargoed. Child access before terminal publication contaminates the round.

## Proof and Model Contract

The fixed independent model order is `declared:svg-literal`, `nearest-6`, then
`truncate-6`. Models never share cells, witnesses, covers or state.
Transform lists use homogeneous column vectors with
`M_current <- M_current * M_operation`; descendants use `M_global = M_parent * M_local`.
Unsupported, singular, ambiguous or uncertified decimal-angle transforms refuse rather
than receiving a binary64 pad.

The proof uses `t = tan(theta/2)` on the frozen quotient interval `[-1/2,1/2]`. It must
provide:

1. one exact rational `(cx,cy,t)` witness whose four derived corners lie in their closed
   source cells;
2. a gap-free rational bisection tree whose rejected and retained leaves cover the whole
   root and whose retained boxes enclose every compatible pose; and
3. rational outward wall signs, plus separating-axis signs on synthetic pair controls.

An independently authored verifier consumes only the receipt and source-cell facts.
It must not import fitter branch, corner-image, rejection or sign functions.
A zero-straddling interval remains undecided.

## Runner and Retention Admission

Before network access, injected streams must prove digest-before-parse, child-channel
absence, deterministic selector and model order, canonical serialization, cleanup on
every exit, atomic create/replace and refusal to overwrite an existing result.
Only a fully verified sanitized receipt may reach the declared result path.

The result path was absent at preregistration.
The runner retains no partial scientific record on verification or atomic-publication
failure.

## Outcome Boundary

Session-069 owns the complete controls, mutations, cell clocks and typed outcomes.
W6 remains closed until every W7 proof and runner guard passes at a frozen revision and
an independent W2 readmission confirms it.
A compatible localized polygon is only a repair seam.
H-053 remains `instrument_ready: false` because this round does not cover both
parent-child pairs or pairwise geometry.

Every terminal decision remains `needs_review: true` for BC-120 and BC-121.

## W7 Cell 1 Checkpoint

**Artifact:** `cases/unitsquare_precision/refusal/run.py` defines exact rational
intervals, half-angle poses and witnesses, affine composition, locally gap-free binary
cover nodes, canonical proof serialization and exact point-pose wall signs.
Four `refusal` tests retain the rational `t = 1/2` rotated-square answers, noncommuting
transform order, a complete split and gap mutation, and interior, tangent and crossing
wall signs.

**Result:** The four new controls pass, the full precision file reports 17 passing
tests, and Ruff and BasedPyright report no findings.
At this first-cell boundary, `subject.selftest_passed` remained false because two W7
admission cells were still incomplete.

**Guard:** The cell used synthetic rational fixtures only.
It made no network request, opened no parent or child, and parsed or fit no target
geometry.

**Next:** The proof model still lacks outward rational corner images for pose boxes,
complete-tree replay by independently authored code, interval wall-sign decisions and
the named proof mutations.
The runner, cleanup and atomicity cell also remains unbuilt.
W6 stays closed.

## W7 Cell 2 Checkpoint

**Artifact:** `run.py` emits `UnitSquarePoseProof/v1`; `verify.py` independently parses
and replays it without importing producer corner, rejection or sign functions.

**Result:** The receipt binds its source model, source and polygon digests,
independently supplied source-cell digest, exact transform and container normalization.
The verifier admits the eight dihedral correspondences, enforces `t in [-1/2,1/2]` and
the exact root quotient, checks the source-derived center bound, recomputes `c^2+s^2=1`,
outward corner intervals, retained and rejected leaves, retained-leaf wall signs,
recursive partitions and the canonical proof digest.
Both children include their split point; this shared zero-width boundary is required.
A gap or positive-width overlap fails partition replay.

The synthetic cells were declared before their compatible witness and have positive
width. The test suite rejects changed source binding, a moved witness, a nondihedral
permutation, noncanonical rational text, a forged rotation, changed source-cell digest,
a missing child, overlapping children, a changed outward image and a changed sign.
The same receipt carries exact separating-axis intervals for distinct separated, tangent
`possible-contact` and overlapping synthetic pairs; the independent verifier recomputes
all four axes and rejects a forged pair sign.
All 31 precision tests pass; Ruff and BasedPyright are clean.
Normal and `python -O` selftests exit zero with byte-identical proof bytes.

**Guard:** This cell used synthetic values only and made no network, parent, child or
target-geometry access.
The numerical prototype remains read-only.

**Next:** The proof instrument has no authorized target runner yet.
Injected retrieval, digest-before-parse, deterministic selection/model order, cleanup on
every exit and atomic publication remain for the third W7 cell.
W6 stays closed.

## W7 Cell 3 Checkpoint

**Correction:** Independent W2 later invalidated this checkpoint’s W6-admission claim;
the terminal premeasurement section below is authoritative.

**Artifact:** `run.py` now exposes `run_exp051_runner`, bound to the exact exp-051
result path and `session-069` W6 clock, on top of the reusable `run_authorized_runner`
injected boundary.

**Result:** The runner hashes and wipes the parent buffer before and after its only
structural-parser channel, requires unique stable ids and four vertices, selects the
lexicographically first UTF-8 id, and creates a distinct evaluator in the fixed
`declared:svg-literal`, `nearest-6`, `truncate-6` order.
Only independently verified, source-bound proofs or typed refusal codes enter the
canonical receipt. The receipt rejects raw bytes, source markup and operational or
child-derived keys. Publication flushes a sibling temporary file and uses atomic
no-overwrite creation; existing results refuse before retrieval.

Injected tests cover digest failure before scanning, duplicate ids, the non-four-vertex
mutation, model reordering, forbidden child state, independent-verifier failure before
publication, existing-result refusal, response and buffer cleanup, and temporary cleanup
after ordinary and interrupted publication failures.
All 38 precision tests pass; Ruff and BasedPyright are clean.
Normal and optimized `--runner-selftest` executions are byte-identical.

**Guard:** The cell used injected synthetic byte streams and synthetic proof receipts
only. It made no network request, opened no parent or child, parsed or fit no target
geometry, and did not create the declared result path.

**Next:** No W7 runner guard remains.
W6 must instantiate its target structural parser and three model evaluators only through
the frozen injected interfaces after the coordinator appends the exact W6 phase.
Until then the parent, result path and all target adapters remain unopened.

## Terminal Premeasurement Stop

Independent W2 invalidated the preceding cell’s W6-admission claim without changing the
retained implementation.
The exact preregistered command was:

```text
uv run --frozen python -m cases.unitsquare_precision.refusal.run --record campaign/series/series-000-smoke-and-calibration/results/exp-051-h-053-n68-refusal-localization.json
```

It exited 2 in argument parsing because `_main` has no `--record` mode and no production
adapter that supplies `run_exp051_runner` with its injected opener, structural scanner
and model factory. The generic callable runner is useful residue, but its synthetic
runner selftest cannot substitute for the registered command’s execution gate.

The retained residue is bound to these SHA-256 values:

- `run.py`: `3d91046ad9d4ea7b3a7e2f3e7f1ca02aec7cd7118d2291a50f622e8541020029`
- `verify.py`: `1533210f9d8e17cbdfa822da59187d280fc4ab063816644825c50d7b8b24552f`
- `test_unitsquare_precision.py`:
  `7cc3a7f59d74e78648966af0ecf88443abfe99432213d30bcb33dee568f3f3c8`

No network request, parent or child read, gain inspection, target parse or fit, target
proof evaluation, or result publication occurred.
The result path remains absent.
This is an invalid-instrument guard result, not a rejection of H-053 or evidence about
the n = 68 source geometry.

Reopening requires a production CLI adapter that passes the frozen authorization,
digest-before-parse, selector, model-isolation, verification, retention, cleanup and
atomic-publication mutations.
That repair must be independently reviewed and registered as a new experiment before
target access; exp-051 is not repairable in place.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
