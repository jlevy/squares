---
title: "session-069 — BC-117 n = 68 refusal localization"
softschema:
  contract: packing.squares:AgentSession/v2
  schema: ../schemas/agent-session.schema.yaml
  envelope: session
  status: enforced
session:
  id: session-069
  primary_bead: think-t7v1
  status: stopped
  title: "BC-117 n = 68 refusal localization"
  date: '2026-09-01'
  started_at: '2026-09-01T12:16:55Z'
  deadline_at: '2026-09-01T14:56:55Z'
  branch: codex/w3-nine-hour-autonomous-run
  goal: >-
    Localize BC-109's target-blind interval-enclosure refusal to one reproducible
    instrument, source, transform, serialization or pose-compatibility boundary without
    opening the child, running surgery or disposing H-053.
  workflow_phases:
  - workflow: insight-iteration
    recording: contemporaneous
    clock_role: work
    focus: correctness
    objective: >-
      Freeze the localization-only claim, baseline, fixtures, proof instrument, runner,
      retention boundary, controls, mutations, seven cells and refusal exits without
      retrieving a parent, reading a child or fitting target geometry.
    commitment: BC-117
    bead: think-t7v1
    status: completed
    entered_by: session_start
    switch_reason: null
    budget_minutes: 15
    started_at: '2026-09-01T12:16:55Z'
    deadline_at: '2026-09-01T12:31:55Z'
    expected_output: >-
      A complete target-blind BC-117 contract that the coordinator can preregister
      serially before any W7 implementation or target access.
    validation_command: >-
      uv run --frozen softschema validate
      campaign/agent-sessions/session-069-bc117-n68-refusal-localization.md
    kill_condition: >-
      Stop if any parent or child bytes are opened or retrieved, target geometry is fit,
      an experiment id is allocated, or the frozen baseline depends on target evidence.
    fallback: >-
      Retain the first missing contract field as a typed W3 stop and leave W7
      unauthorized.
    outcome: >-
      Artifact: this session now freezes the localization-only BC-117 contract. Result:
      the target-blind interval-enclosure baseline, one-parent selector, rational proof
      design, independent verifier, injected runner, retention boundary, controls,
      mutations, future path templates, exclusive scope and seven cells are fixed.
      Guard: no parent or child bytes were retrieved or opened, no target geometry was
      parsed or fit, and no experiment or result id was allocated. Next: stop before W7
      and return this contract for serial experiment allocation and authorization.
    evidence:
    - packing/campaign/agent-sessions/session-066-bc109-n68-n69-precision.md
    - packing/campaign/series/series-000-smoke-and-calibration/experiments/exp-047-h-053-unitsquare-rigid-pose-serialization.md
    - packing/campaign/hypotheses/H-053-unitsquare-rigid-pose-serialization.md
    - packing/campaign/agendas/agenda-012-weighted-proof-precision-bridge-and-cross-scale-controls.md
    - packing/campaign/agendas/agenda-013-nine-hour-autonomous-run.md
    - packing/resources/web/known-best-packings/README.md
    - packing/resources/web/unitsquare-release1-2026/results.json
    - packing/src/sqpack/research/unitsquare_precision.py
    - packing/tests/test_unitsquare_precision.py
    - packing/cases/unitsquare_precision/readiness-controls.json
    stop_reason: The 15-minute W3 contract is complete without target access.
    next_action: >-
      Wait for the coordinator to allocate the next experiment and result paths and
      append an explicitly authorized W7 phase; do not begin implementation meanwhile.
  - workflow: research-loop
    recording: contemporaneous
    clock_role: work
    focus: correctness
    objective: >-
      Build the target-blind exact rational witness and complete-cover data model with
      known-answer single-square, transform and wall-sign controls from exp-051.
    commitment: BC-117
    bead: think-t7v1
    status: completed
    entered_by: planned_checkpoint
    switch_reason: W3 contract and exp-051 preregistration are complete.
    budget_minutes: 25
    started_at: '2026-09-01T12:31:55Z'
    deadline_at: '2026-09-01T12:56:55Z'
    expected_output: >-
      Import-safe rational proof types and synthetic known-answer tests that establish
      exact half-angle witnesses, transform order, gap-free cover representation and
      exact wall-sign intervals without target access.
    validation_command: >-
      uv run --frozen pytest -q tests/test_unitsquare_precision.py -k refusal
    kill_condition: >-
      Stop on any parent, child or network access; target geometry parse or fit; binary64
      proof arithmetic; incomplete cover representation; or a known-answer mismatch.
    fallback: >-
      Retain the smallest failing synthetic fixture and exact proof or representation
      residue; do not enter the next W7 cell.
    outcome: >-
      Artifact: run.py now defines exact rational intervals, half-angle poses and
      witnesses, affine composition, locally gap-free binary cover nodes, canonical
      proof serialization and exact point-pose wall signs; four refusal-prefixed tests
      retain the known answers and a partition mutation. Result: all four new controls
      and all 17 precision tests pass under the project interpreter, with Ruff and
      BasedPyright clean. Guard: the code used only synthetic rational fixtures and made
      no parent, child or network access; no target geometry was parsed or fit. Next:
      stop at this cell boundary. A separately authored verifier still needs outward
      interval corner images, complete-tree replay, sign-width decisions and proof
      mutation coverage before the next W7 cell can pass.
    evidence:
    - packing/campaign/series/series-000-smoke-and-calibration/experiments/exp-051-h-053-n68-refusal-localization.md
    - packing/cases/unitsquare_precision/refusal/run.py
    - packing/tests/test_unitsquare_precision.py
    stop_reason: The first 25-minute W7 proof-format and known-answer cell is complete.
    next_action: >-
      Wait for serial authorization of the 2026-09-01T12:56:55Z W7 cell; do not begin
      interval image or independent-verifier work before that authorization.
  - workflow: research-loop
    recording: contemporaneous
    clock_role: work
    focus: correctness
    objective: >-
      Bind exact witnesses and cover receipts to synthetic source facts, compute outward
      rational corner and wall intervals, and independently replay every proof boundary
      and named mutation without target access.
    commitment: BC-117
    bead: think-t7v1
    status: completed
    entered_by: planned_checkpoint
    switch_reason: >-
      The coordinator admitted the second W7 cell after cross-auditing the first cell's
      representation and witness controls.
    budget_minutes: 25
    started_at: '2026-09-01T12:56:55Z'
    deadline_at: '2026-09-01T13:21:55Z'
    expected_output: >-
      Source-bound exact witness and complete-cover receipts with outward interval
      images, strict independent verification, normal and optimized selftests, and the
      queued witness, tree and sign mutations.
    validation_command: >-
      uv run --frozen pytest -q tests/test_unitsquare_precision.py -k refusal && uv run
      --frozen python -m cases.unitsquare_precision.refusal.run --selftest
    kill_condition: >-
      Stop on target access, verifier reuse of fitter geometry decisions, a nonexact
      proof operation, incomplete root coverage, unbound source facts, assertion-only
      correctness or nonidentical normal and optimized selftests.
    fallback: >-
      Retain the smallest failing synthetic receipt and exact verifier residue; do not
      enter the runner cell or W6.
    outcome: >-
      Artifact: run.py now emits source-bound exact proof receipts and verify.py
      independently replays them without importing producer geometry helpers. Result:
      the verifier binds the model, source and polygon digests, source-cell digest,
      transform and container; admits only eight dihedral correspondences; enforces the
      quotient and source-derived root; recomputes rational half-angle identities,
      outward images, rejection leaves, retained-leaf wall signs, recursive splits,
      separated, possible-contact and overlapping pair signs, canonical digest and all
      named mutations. Normal and optimized selftests are byte-identical; 31 precision
      tests pass with Ruff and BasedPyright clean. Guard:
      all evidence is synthetic and no parent, child, network or target geometry was
      opened, parsed or fit. Next: stop at this boundary. The authorized runner,
      ephemeral retrieval, cleanup and atomic publication remain the final W7 residue;
      W6 stays closed.
    evidence:
    - packing/cases/unitsquare_precision/refusal/run.py
    - packing/cases/unitsquare_precision/refusal/verify.py
    - packing/tests/test_unitsquare_precision.py
    stop_reason: The second 25-minute W7 proof and independent-verifier cell is complete.
    next_action: >-
      Wait for serial authorization of the runner cell at 2026-09-01T13:21:55Z; do not
      build retrieval, cleanup or atomic-publication paths before that authorization.
  - workflow: research-loop
    recording: contemporaneous
    clock_role: work
    focus: correctness
    objective: >-
      Build and mutation-test the fully injected authorized runner around the frozen
      proof producer and independent verifier without opening any target channel.
    commitment: BC-117
    bead: think-t7v1
    status: completed
    entered_by: planned_checkpoint
    switch_reason: >-
      The coordinator admitted the third W7 cell after the exact proof and independent
      verifier passed every target-blind guard in the preceding cell.
    budget_minutes: 25
    started_at: '2026-09-01T13:21:55Z'
    deadline_at: '2026-09-01T13:46:55Z'
    expected_output: >-
      An injected authorized runner that binds the exp-051 authorization and result
      path, verifies the parent digest before structural parsing, isolates all three
      models, excludes child and gain channels, verifies before publication, cleans up
      every resource and publishes one canonical receipt atomically.
    validation_command: >-
      uv run --frozen pytest -q tests/test_unitsquare_precision.py -k refusal && uv run
      --frozen python -m cases.unitsquare_precision.refusal.run --runner-selftest
    kill_condition: >-
      Stop on network or target access, child or gain channel availability, parsing
      before digest verification, retained raw or operational data, model-state reuse,
      publication before independent verification, an unclean exit or nondeterministic
      normal and optimized selftest output.
    fallback: >-
      Retain the smallest injected runner failure as the unmet W6 admission guard; do
      not access a target or create the declared result.
    outcome: >-
      Artifact: run.py now exposes an exp-051-bound injected runner with an exact
      session-phase authorization, digest-before-scan parent handling, complete
      structural selection, isolated model evaluation, independent proof verification,
      sanitized canonical receipts and atomic no-overwrite publication. Result: all 38
      precision tests pass; normal and optimized runner selftests are byte-identical;
      response, buffer and temporary cleanup pass success, refusal, exception and
      interrupted-publication controls. Guard: every stream and model result was
      synthetic, no network or target source was opened, no child or gain channel
      exists, and the declared result remains absent. Next: stop at this boundary. W6
      may supply its target parser and model evaluators only through the frozen injected
      interfaces after coordinator readmission; the runner itself has no unmet guard.
    evidence:
    - packing/campaign/series/series-000-smoke-and-calibration/experiments/exp-051-h-053-n68-refusal-localization.md
    - packing/cases/unitsquare_precision/refusal/run.py
    - packing/cases/unitsquare_precision/refusal/verify.py
    - packing/tests/test_unitsquare_precision.py
    stop_reason: >-
      The third 25-minute W7 injected-runner and atomic-publication cell is complete.
    next_action: >-
      Wait for serial coordinator readmission of the 2026-09-01T13:46:55Z W6 cell; do
      not open a parent or instantiate a target parser or model evaluator before then.
  - workflow: factual-review
    recording: contemporaneous
    clock_role: work
    focus: correctness
    objective: >-
      Independently replay the completed W7 runner gates from the frozen lane return and
      decide whether the one-parent W6 cell may open at its exact boundary without
      changing the runner or reading target data.
    commitment: BC-117
    bead: think-t7v1
    status: completed
    entered_by: evidence_checkpoint
    switch_reason: >-
      The third W7 cell returned early with a frozen runner revision and the declared
      result still absent, leaving time for the required independent readmission.
    budget_minutes: 13
    started_at: '2026-09-01T13:34:26Z'
    deadline_at: '2026-09-01T13:46:55Z'
    expected_output: >-
      A read-only determination over the authorization and result binding,
      digest-before-scan order, structural selector, model isolation, independent proof
      verification, sanitized retention, cleanup, deterministic selftests and atomic
      no-overwrite publication.
    validation_command: >-
      uv run --frozen pytest -q tests/test_unitsquare_precision.py && uv run --frozen
      ruff check cases/unitsquare_precision/refusal tests/test_unitsquare_precision.py &&
      uv run --frozen basedpyright cases/unitsquare_precision/refusal
      tests/test_unitsquare_precision.py
    kill_condition: >-
      Keep W6 closed if any result exists, a target channel was opened, a normal and
      optimized selftest differs, or any authorization, source, selector, independence,
      cleanup, retention or publication guard cannot be reproduced.
    fallback: >-
      Retain the first unreproduced guard as a typed premeasurement stop and do not open
      the parent inside this agenda wall.
    outcome: >-
      Artifact: the coordinator independently read the frozen runner and mutation tests
      and replayed the full 38-test file, Ruff, BasedPyright, both enforced records and
      normal versus optimized runner selftests, then invoked the exact preregistered
      command against its still-absent result path. Result: the generic injected-runner
      controls passed and the selftest bytes matched at SHA-256
      18664b24b43044cee119cc72fc6cb9801753a1df82b4f5d9282dcf5e0363c954,
      but the preregistered `--record` command exited 2 because the frozen CLI exposes
      only `--selftest` and `--runner-selftest`. The declared result remained absent.
      Guard: this review made no code change and opened no network, parent, child, gain
      or target parser. Next: keep W6 closed and terminalize the lane as a
      premeasurement executable-runner stop; do not repair or rerun the instrument in
      this registered round.
    evidence:
    - packing/cases/unitsquare_precision/refusal/run.py
    - packing/cases/unitsquare_precision/refusal/verify.py
    - packing/tests/test_unitsquare_precision.py
    - packing/campaign/series/series-000-smoke-and-calibration/experiments/exp-051-h-053-n68-refusal-localization.md
    stop_reason: >-
      Independent W2 reproduced the generic runner controls but rejected W6 admission
      because the exact preregistered target command is not executable.
    next_action: >-
      Keep target access closed, retain the useful generic runner residue and record the
      missing production entry point as the smallest premeasurement stop.
  - workflow: insight-iteration
    recording: contemporaneous
    clock_role: work
    focus: insight
    objective: >-
      Terminalize the independent W2 executable-runner refusal with its mechanism,
      scientific limits and reusable handoff, without repairing the instrument or
      opening W6.
    commitment: BC-117
    bead: think-t7v1
    status: stopped
    entered_by: evidence_checkpoint
    switch_reason: >-
      Independent W2 found the first failed W6 admission guard at the exact 13:46:55Z
      boundary, so the two planned W6 cells were canceled before target access.
    budget_minutes: 20
    started_at: '2026-09-01T13:46:55Z'
    deadline_at: '2026-09-01T14:06:55Z'
    expected_output: >-
      A terminal typed premeasurement record that preserves the generic proof,
      verifier and injected runner while refusing any n = 68 source or geometry claim.
    validation_command: >-
      uv run --frozen softschema repair --check
      campaign/agent-sessions/session-069-bc117-n68-refusal-localization.md && uv run
      --frozen softschema validate
      campaign/agent-sessions/session-069-bc117-n68-refusal-localization.md
    kill_condition: >-
      Stop without further action if terminalization would require a runner repair,
      target command, network request, parent or child access, gain inspection or result
      creation.
    fallback: >-
      Preserve the independent W2 phase as the terminal evidence and report any schema
      defect without changing scientific content.
    outcome: >-
      Artifact: session-069 and exp-051 now retain the exact executable-runner refusal,
      the useful generic proof/verifier/runner residue and its frozen hashes. Result:
      `--record` exit 2 is the first failed W6 admission guard; exp-051 is blocked on an
      invalid instrument before measurement, and H-053 remains unresolved. Guard: no
      target, network, parent, child or gain channel opened, no target parser or model
      evaluator ran, and no result file exists. Next: repair and independently test a
      production CLI adapter in W7, then register a new experiment before any target
      access; exp-051 must not be repaired or rerun.
    evidence:
    - packing/campaign/agent-sessions/session-069-bc117-n68-refusal-localization.md
    - packing/campaign/series/series-000-smoke-and-calibration/experiments/exp-051-h-053-n68-refusal-localization.md
    - packing/cases/unitsquare_precision/refusal/run.py
    - packing/cases/unitsquare_precision/refusal/verify.py
    - packing/tests/test_unitsquare_precision.py
    stop_reason: >-
      The exact preregistered `--record` command exited 2 before target access because
      no production dependency-injection or adapter entry point exists.
    next_action: >-
      Return this terminal stop to the coordinator; do not enter W6 or alter the frozen
      exp-051 instrument.
  budget:
    wall_minutes: 160
    max_cycles: 7
    checkpoint_minutes: 25
    slice_minutes: 25
    finalization_minutes: 20
  stop_conditions:
  - Any target access occurs before the W7 instrument and runner pass every readiness guard.
  - Raw Kingbird bytes, XML, source excerpts, palettes or temporary paths would be retained.
  - A source, transform, interval, independence, determinism, mutation or atomicity guard fails.
  - The exact 2026-09-01T14:56:55Z session deadline arrives.
  progress:
    metric: smallest reproducible n = 68 parent refusal localized without child access
    before: >-
      Exp-047 retains a numerical prototype, but its interval-enclosure and executable
      runner readiness guards failed before target access.
    after: >-
      The target-blind proof, independent verifier and generic injected runner pass
      their exact source, cover, sign, authorization, retention, cleanup, determinism
      and atomic-publication controls, but the exact preregistered `--record` entry point
      is absent. W6 stays closed and no target source was opened.
  delegations: []
  resource_rollups:
  - packing/campaign/resource-usage/codex-task-tree-session-069.yaml
  outputs:
  - packing/campaign/agent-sessions/session-069-bc117-n68-refusal-localization.md
  - packing/campaign/resource-usage/codex-task-tree-session-069.yaml
  - packing/campaign/series/series-000-smoke-and-calibration/experiments/exp-051-h-053-n68-refusal-localization.md
  - packing/cases/unitsquare_precision/refusal/run.py
  - packing/cases/unitsquare_precision/refusal/verify.py
  - packing/tests/test_unitsquare_precision.py
  checks:
  - >-
    uv run --frozen softschema repair --check
    campaign/agent-sessions/session-069-bc117-n68-refusal-localization.md — valid,
    no repairs
  - >-
    uv run --frozen softschema validate
    campaign/agent-sessions/session-069-bc117-n68-refusal-localization.md — valid
  - >-
    uvx --from flowmark-rs==0.3.2 flowmark --auto
    packing/campaign/agent-sessions/session-069-bc117-n68-refusal-localization.md —
    completed
  - >-
    uv run --frozen pytest -q tests/test_unitsquare_precision.py — 17 passed
  - >-
    uv run --frozen ruff check cases/unitsquare_precision/refusal/run.py
    tests/test_unitsquare_precision.py — passed
  - >-
    uv run --frozen basedpyright cases/unitsquare_precision/refusal/run.py
    tests/test_unitsquare_precision.py — 0 errors, 0 warnings, 0 notes
  - >-
    uv run --frozen softschema repair --check and validate on session-069 and exp-051 —
    both valid, no repairs or warnings
  - >-
    uvx --from flowmark-rs==0.3.2 flowmark --auto --check --no-cache on session-069 and
    exp-051 — clean
  - >-
    uv run --frozen pytest -q tests/test_unitsquare_precision.py — 31 passed
  - >-
    uv run --frozen ruff check and basedpyright on run.py, verify.py and
    test_unitsquare_precision.py — passed; 0 errors, 0 warnings, 0 notes
  - >-
    uv run --frozen python -m cases.unitsquare_precision.refusal.run --selftest and the
    same command under python -O — exit 0 with byte-identical output
  - >-
    uv run --frozen pytest -q tests/test_unitsquare_precision.py — 38 passed
  - >-
    uv run --frozen ruff check and basedpyright on run.py, verify.py and
    test_unitsquare_precision.py — passed; 0 errors, 0 warnings, 0 notes
  - >-
    uv run --frozen python -m cases.unitsquare_precision.refusal.run
    --runner-selftest and the same command under python -O — exit 0 with byte-identical
    output
  - >-
    Independent W2 ran the exact preregistered `--record` command — exit 2 before any
    network or target access; the declared result remained absent
  stop_reason: >-
    Typed premeasurement `executable-runner` stop: independent W2 found that the exact
    preregistered `--record` command has no CLI production entry point, so W6 remained
    closed and exp-051 produced no scientific result.
  next_action: >-
    Repair and independently test the production CLI adapter in a new W7 round, then
    preregister a new experiment before any parent or target access; do not repair or
    rerun exp-051.
---
# Session 069 — BC-117 `n = 68` Refusal Localization

## W3 Checkpoint

**Artifact:** This session contains the complete BC-117 contract.

**Result:** The round localizes one target-blind instrument or source boundary.
It does not repeat BC-109’s full two-pair H-053 determination.

**Guard:** This phase read retained metadata, the terminal records, the prototype and
its synthetic tests.
It did not retrieve a Kingbird parent, open either retained child, parse or fit target
geometry, allocate an experiment, create a result file, or inspect H-051 gain
information.

**Next:** The coordinator assigns the next free experiment id and matching result path,
then appends W7 with an exact clock and exclusive scope.
No W7 code or target command may run before that append.

## Localization Claim and Outcomes

The frozen question is:

> Can one target-blind, proof-carrying single-square instrument distinguish exp-047’s
> interval-enclosure defect from the first provenance, affine-transform, serialization
> or pose-compatibility refusal on one deterministically selected `n = 68` parent
> polygon?

The baseline outcome is `interval-enclosure / instrument-defect`. On a synthetic rotated
unit square, the retained prototype may emit a binary64 midpoint pose and pass its
numerical replay, but neither the fitter nor the verifier proves these three facts:

- an exact rigid pose exists inside all four closed source cells;
- the emitted rational boxes cover every compatible pose in the declared quotient; and
- wall and pair signs are outwardly decided at the widths the receipt reports.

The existing `2e-12` fit tolerance, `2e-15` transform pad, quantized point pose and
heuristic center and angle radii are prototype behavior.
They never count as an existence, outer-cover or sign certificate.

The localization determination has these terminal values:

| outcome | meaning |
| --- | --- |
| `instrument-defect-reproduced` | The target-blind proof or independent-verifier guard fails on the smallest synthetic fixture. |
| `instrument-ready-source-unmeasured` | The proof and runner guards pass, but W6 is not authorized or reaches no target source fact. |
| `provenance-refusal` | The one allowed parent retrieval or digest gate fails before parsing. |
| `affine-transform-refusal` | The source uses a transform or container mapping that the sound parser cannot resolve. |
| `serialization-refusal` | The cited side or coordinate tokens do not justify one frozen source-cell model. |
| `pose-compatibility-refusal` | A sound and complete single-square certificate exhausts the three models for the selected polygon without a compatible pose. |
| `localized-compatible` | At least one model has an exact witness and checked outer cover for the selected polygon. This is a repair seam, not a parent-arm or H-053 result. |
| `unresolved` | The declared wall expires with the first incomplete proof node or undecided sign retained. |

This one-parent, one-polygon round cannot accept or reject H-053, select an H-051 arm,
route BC-113 during this wave, infer contacts, or run surgery.
H-053 remains `instrument_ready: false` unless a later full two-pair instrument
separately meets its registered criterion.

## Frozen Evidence and Selector

Exp-047 is the immutable negative baseline at commit `d7c94590`:

| retained artifact | SHA-256 |
| --- | --- |
| `packing/src/sqpack/research/unitsquare_precision.py` | `92e7b6e43b8785c0b618f2a48c3a26c09afb1b5cd9009a69189dfab0f606b22c` |
| `packing/tests/test_unitsquare_precision.py` | `9aeaf96d45fd94ba38af00a713a76297077a1aa7c55efc6783d6c94561c2038f` |
| `packing/cases/unitsquare_precision/readiness-controls.json` | `fe3a17fc3f4573c80ca0d9b00987b831d483ac4ba9ac13f288bad34e0e2cec4f` |

The retained release record has SHA-256
`dd7c1c62050b004c86959e59621c51d097f70d51cb142be9c19b15a16693d8b3`. The only W6 parent
allowed by this round is `https://kingbird.myphotos.cc/packing/square-68.svg`, expected
SHA-256 `558fbdddfeb0b2f8752b88e172d2776544beb4d2a7122189ef77c1e1c5ebdc6d`. Its cited
side token is `8.80345993651653`. The token is metadata, not an assertion that the value
is exact; an absent point or directional-bound declaration causes a
`serialization-refusal`.

The retained child path `packing/resources/web/known-best-packings/unitsquare/n068.svg`,
its digest, offered side, reduction, pose and every child-derived summary are embargoed
inputs. BC-117 never opens them.

After digest verification and a complete duplicate-id and four-vertex scan, the selector
chooses the lexicographically smallest UTF-8 stable square id.
A missing or duplicate id, an ambiguous container, or a polygon count other than four
vertices is a typed refusal.
The selected fixture may retain closed normalized source cells and a derived proof
receipt. It may not retain an XML element, original source excerpt, palette, raw byte
range or temporary path.

## Transform and Serialization Contract

The fixed model order is:

1. `declared:svg-literal`
2. `nearest-6`
3. `truncate-6`

Models never share cells, witnesses, covers or search state.
Using homogeneous column vectors, a transform list is consumed left to right with
`M_current <- M_current * M_operation`; a descendant receives
`M_global = M_parent * M_local`. The parser applies `M_global` to each vertex,
identifies one unambiguous positive-width container `(x0, y0, W, H)`, and maps a global
point `(X, Y)` to `(L*(X-x0)/W, L*(y0+H-Y)/H)`. The mathematical container is `[0,L]^2`;
every fitted square has side exactly `1`.

Exact decimal matrix, translation and scale operations use rational interval arithmetic.
A decimal-angle `rotate(...)` requires an outward trigonometric interval with a checked
error bound. The fixed binary64 `sin` or `cos` plus `2e-15` pad is not admissible.
Unsupported, singular or ambiguous transforms stop the round rather than falling back to
the prototype.

## Proof-Carrying Single-Square Instrument

The proof parameter is `t = tan(theta/2)` in the canonical orientation quotient.
Freeze the root interval to `[-1/2, 1/2]` and enumerate cyclic and reversed corner
correspondences explicitly.
For rational `t`, define

```text
c = (1 - t^2) / (1 + t^2)
s = 2t / (1 + t^2)
x = cx + c*u - s*v
y = cy + s*u + c*v
```

where `(u,v)` ranges over `(±1/2,±1/2)`. The denominator is positive throughout the root
interval. All certificate endpoints and arithmetic are rational; the proof path does not
call binary64 trigonometry.

An **existence certificate** contains one rational `(cx, cy, t)`, one corner
correspondence and exact corner images inside the four closed source cells.
An outer cover does not substitute for this witness.

An **outer-cover certificate** is a complete rational bisection tree over `(cx, cy, t)`.
Every leaf is either rejected by a checked source-cell inequality or retained with
outward rational corner images.
The tree records the split coordinate and midpoint so an independent verifier can prove
that the leaves cover the root without gaps.
The retained boxes enclose every compatible pose in the enumerated quotient.

A **sign certificate** evaluates inward wall clearance over every retained box.
Synthetic two-square controls also evaluate separating-axis gaps over the Cartesian
product of the two covers.
A sign qualifies only when the whole rational interval is nonnegative.
An interval containing zero is `possible-contact` and cannot be relabeled from a
point-pose value.

## Independent Verifier and Runner Boundary

The verifier consumes only the proof receipt and source-cell facts.
It independently checks rational parsing, model identity and order, the exact witness,
bisection-tree coverage, interval corner images, wall signs, synthetic pair signs,
canonical ordering and receipt digest.
It must not import or call the fitter’s branch selection, corner image, rejection or
sign functions. Fitter-verifier disagreement is an instrument stop.

The complete runner is tested with injected byte streams before network access.
Its authorized path is fixed:

1. Require the coordinator-assigned result path and an explicit W6 authorization bound
   to this session phase.
2. Retrieve through an injected opener, hash all bytes before parsing, and reject a
   mismatch without calling the parser.
3. Parse the parent, select the frozen square id, evaluate the three models
   independently and verify the proof receipt.
4. Serialize only sanitized provenance, normalized cells, certificates, typed outcome
   and exact hashes.
5. Write a temporary file beside the result, flush it, and atomically replace the final
   path only after verification.
   Refuse an existing final result unless the frozen experiment contract explicitly
   permits an identical replay.
6. Close the response and remove raw buffers and temporary files on success, refusal,
   exception and interrupted write.

Injected tests must prove that child data has no input channel and that parent selection
cannot inspect child or gain information.
The runner retains no partial scientific result when atomic publication fails; it
retains a bounded public error in the experiment record instead.

## Retention and Blindness

Kingbird bytes may exist only in memory or a private temporary file during one
hash-verified parse.
The repository may retain the URL, expected and observed digest, retrieval time, parser
and policy versions, sanitized normalized numerical facts and derived receipts.
It must not retain parent bytes, XML, source excerpts, palettes, response headers
containing private data, or temporary paths.
Cleanup runs on every exit.

No process in this session may open the child SVG, offered side, reduction, released
gain, child pose or child-derived summary.
A child read before terminal publication contaminates the round.
A compatible localized parent polygon cannot rescue BC-113 or create an H-051 result
during this second-wave block.

## Controls and Mutations

W7 must pass all controls before W6:

- exact axis-aligned and rational-half-angle rotated squares with known witnesses and
  covers;
- exact rational matrix, translation, scale and nested-transform scenes, plus a
  decimal-angle rotation that is either outwardly certified or refused;
- point, positive and negative `nearest-6`, and positive and negative `truncate-6`
  boundary cells;
- interior, wall-tangent and wall-crossing squares;
- separated, tangent and overlapping synthetic pairs;
- cyclic and reversed corners with byte-identical canonical receipts;
- injected retrieval, cleanup and atomic-write success and failure paths.

Each mutation must fire its named guard:

- change one source byte before digest verification;
- reverse two noncommuting transforms;
- move one corner outside its closed source cell;
- duplicate a square id or reorder the model inventory;
- forge `c^2+s^2 = 1`, remove one bisection leaf or create overlapping cover leaves;
- perturb a wall interval across zero or move a separated synthetic pair into overlap;
- expose a child channel before parent publication;
- return raw bytes from the parent consumer, fail cleanup, leave a temporary file or
  attempt to overwrite an existing result.

A control or mutation without its predeclared result stops before target access.

## Seven Cells and Admission

The wall is exactly `2026-09-01T12:16:55Z` through `2026-09-01T14:56:55Z`:

| elapsed | workflow | required exit |
| --- | --- | --- |
| 0–15 | W3 | This frozen contract, with no experiment id or target access. |
| 15–40 | W7 | Exact rational witness format and target-blind single-square known-answer controls. |
| 40–65 | W7 | Complete rational outer-cover and independent sign verifier, or the smallest proof-node stop. |
| 65–90 | W7 | Fully injected authorized runner, cleanup, deterministic serialization and atomicity guards. |
| 90–115 | W6 | One hash-verified ephemeral `n = 68` parent parse and deterministic polygon selection. |
| 115–140 | W6 | Three separate model certificates, implicated mutations and the first typed localization. |
| 140–160 | W3 | Localization-only determination, limits, validation and handoff. |

Cells 5 and 6 remain unauthorized unless all three W7 cells pass.
No cell borrows from the final 20 minutes.
A cell without a durable proof receipt or typed stop closes the lane before the next
cell.

## Future Paths and Exclusive Scope

The coordinator assigns the next free `exp-NNN` serially.
The frozen path templates are:

- `packing/campaign/series/series-000-smoke-and-calibration/experiments/exp-NNN-h-053-n68-refusal-localization.md`
- `packing/campaign/series/series-000-smoke-and-calibration/results/exp-NNN-h-053-n68-refusal-localization.json`

This W3 phase does not allocate `NNN` and does not create either file.

After allocation, the lane’s exclusive write scope is limited to:

- this session;
- the coordinator-assigned experiment and future result paths;
- `packing/cases/unitsquare_precision/refusal/`;
- the implicated tests in `packing/tests/test_unitsquare_precision.py`; and
- H-053’s instrument description, hashes and readiness fields only when the evidence
  supports the exact edit.
  This localization-only instrument cannot set full H-053 readiness true.

The existing prototype is read-only negative-control evidence.
Shared agendas, generated views, ledgers, frontier records, witnesses, retained source
files, H-051 artifacts, receipts, tbd, Git and GitHub remain outside the lane scope.

## Refusal Conditions

Stop before W6 on missing experiment allocation, changed baseline hashes, failed
provenance or retention controls, unsupported transforms, source-side ambiguity,
incomplete correspondence enumeration, absent exact witness, incomplete outer cover,
verifier disagreement, nondeterministic serialization, undecided required control signs,
failed cleanup or atomicity, or any child/gain access.
During W6, retain the first exact failing boundary without changing the model inventory,
selector, proof policy or criterion.

## Terminal W3 Mechanism and Handoff

**Artifact:** The exact rational proof producer, independent verifier and generic
injected runner remain reusable at these SHA-256 revisions:

- `run.py`: `3d91046ad9d4ea7b3a7e2f3e7f1ca02aec7cd7118d2291a50f622e8541020029`
- `verify.py`: `1533210f9d8e17cbdfa822da59187d280fc4ab063816644825c50d7b8b24552f`
- `test_unitsquare_precision.py`:
  `7cc3a7f59d74e78648966af0ecf88443abfe99432213d30bcb33dee568f3f3c8`

**Result:** Independent W2 invoked the exact preregistered command against the absent
exp-051 result path.
Argument parsing returned exit 2 because `_main` exposes `--selftest` and
`--runner-selftest`, but not `--record` or any production adapter that can supply the
injected opener, structural scan and model factory.
This executable-runner guard failed before W6.

**Guard:** The failure is premeasurement evidence about the instrument only.
No network request, parent or child read, gain inspection, target parse or fit, proof
evaluation on target cells, or result publication occurred.
It therefore establishes no provenance, serialization, pose-compatibility, contact or
H-053 outcome for `n = 68`.

**Next:** A successor must add and independently mutation-test a production CLI adapter
around the retained generic runner, including the exact authorization and result-path
binding. That repair belongs to W7 and requires a new experiment registration before
target access. Exp-051 remains stopped and must not be repaired or rerun.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
