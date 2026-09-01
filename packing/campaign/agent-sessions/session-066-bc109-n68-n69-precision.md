---
title: "session-066 — BC-109 n = 68/69 precision bridge"
softschema:
  contract: packing.squares:AgentSession/v2
  schema: ../schemas/agent-session.schema.yaml
  envelope: session
  status: enforced
session:
  id: session-066
  primary_bead: think-26b1
  status: stopped
  title: "BC-109 n = 68/69 precision bridge"
  date: '2026-09-01'
  started_at: '2026-09-01T09:01:55Z'
  deadline_at: '2026-09-01T11:11:55Z'
  branch: codex/w3-nine-hour-autonomous-run
  goal: >-
    Decide H-053 for the fixed UnitSquare n = 68/69 parent-child pairs through a
    target-blind W3 contract, a W7 provenance and rigid-pose instrument, W6 compatible-
    serialization measurement, and a final W3 mechanism interpretation without
    inferring exact contacts or running surgery.
  workflow_phases:
  - workflow: insight-iteration
    recording: contemporaneous
    clock_role: work
    focus: insight
    objective: >-
      Freeze H-053's child and parent fixtures and hashes, retention rule, transform,
      stable serialization models and order, metric, threshold, budget, refusal
      conditions, controls, mutations and instrument design without fitting target
      geometry.
    bead: think-26b1
    status: completed
    entered_by: session_start
    switch_reason: null
    budget_minutes: 15
    started_at: '2026-09-01T09:01:55Z'
    deadline_at: '2026-09-01T09:16:55Z'
    expected_output: A complete target-blind W6 contract returned to the coordinator for serial preregistration.
    validation_command: >-
      uv run --frozen --all-extras --group dev packing-validate --only "soft-schema"
    kill_condition: >-
      Stop before measurement if target geometry is fit, source semantics or model order
      remains unfrozen, or raw parent retention would violate policy.
    fallback: Retain the smallest provenance, transform or serialization ambiguity as a typed premeasurement stop.
    outcome: >-
      Artifact: this session's target-blind BC-109 contract. Result: the fixtures,
      digests, retention boundary, transform, three-model inventory and order,
      determination threshold, 130-minute cells, controls, mutations and refusal exits
      are frozen. Guard: neither target SVG geometry nor target pose output was read or
      fit, and parent-arm selection remains child-and-gain blind. Next: the coordinator
      may enter W7 against this contract without changing it after target evidence.
    evidence:
    - packing/campaign/agent-sessions/session-066-bc109-n68-n69-precision.md
    - packing/campaign/agendas/agenda-012-weighted-proof-precision-bridge-and-cross-scale-controls.md#bc-109--unitsquare-parentchild-precision-bridge
    - packing/campaign/hypotheses/H-053-unitsquare-rigid-pose-serialization.md
    - packing/resources/web/unitsquare-release1-2026/results.json
    - packing/resources/web/known-best-packings/README.md
    stop_reason: The 15-minute W3 contract-freeze cell produced its complete handoff.
    next_action: Enter W7 provenance and instrument work without reopening this contract.
  - workflow: pipeline-improvement
    recording: contemporaneous
    clock_role: work
    focus: correctness
    objective: >-
      Build the exp-047 ephemeral provenance adapter, transform and source-cell parser,
      rigid-pose enclosure fitter, canonical serializer and independent receipt verifier;
      pass every synthetic, determinism and mutation guard before parsing target geometry.
    bead: think-26b1
    status: stopped
    entered_by: evidence_checkpoint
    switch_reason: >-
      The target-blind W3 contract is complete and the coordinator allocated exp-047 and
      its exact future result path without retrieving parents or fitting target geometry.
    budget_minutes: 45
    started_at: '2026-09-01T09:13:09Z'
    deadline_at: '2026-09-01T09:58:09Z'
    expected_output: >-
      A reusable fitter and separately written verifier passing all readiness guards,
      with H-053 bound to the exact validated revision and instrument_ready true; or a
      typed premeasurement provenance, transform, enclosure or mutation stop.
    validation_command: >-
      uv run --frozen --all-extras --group dev pytest -q
      tests/test_unitsquare_precision.py tests/test_known_best_atlas.py && uv run --frozen
      --all-extras --group dev packing-validate --records
    kill_condition: >-
      Stop before target parsing if provenance, retention, transform, interval,
      determinism, independent-verifier or mutation guards fail, or parent bytes cannot
      remain ephemeral.
    fallback: >-
      Leave H-053 instrument_ready false, retain exp-047 as a typed premeasurement stop,
      and return the smallest failed readiness guard without a scientific verdict.
    outcome: >-
      Artifact: the reusable UnitSquare precision module, its 13-test synthetic suite,
      and its named-control inventory. Result: typed premeasurement stop
      `interval-enclosure`; numerical controls pass, but heuristic fit radii and fixed
      float tolerances do not establish the frozen outward interval claim, and the
      `--record` route has no complete authorized measurement orchestration. Guard: the
      exact preregistered command returns the W6 gate at exit 3 before any child read or
      parent retrieval; neither target geometry nor target pose output was parsed or
      fit. Next: replace the heuristic pose/sign checks with a sound outward verifier and
      complete the injected target runner before allocating a new target round.
    evidence:
    - packing/src/sqpack/research/unitsquare_precision.py
    - packing/tests/test_unitsquare_precision.py
    - packing/cases/unitsquare_precision/readiness-controls.json
    - packing/campaign/series/series-000-smoke-and-calibration/experiments/exp-047-h-053-unitsquare-rigid-pose-serialization.md
    stop_reason: >-
      The interval-enclosure and executable-runner admission guards failed before target
      access; exp-047 is blocked without a scientific verdict.
    next_action: >-
      Keep W6 closed; repair and independently test sound outward enclosure/sign
      semantics plus the complete target orchestration before registering a new round.
  budget:
    wall_minutes: 130
    max_cycles: 4
    checkpoint_minutes: 20
    slice_minutes: 30
    finalization_minutes: 15
  stop_conditions:
  - Any target fit runs before preregistration and instrument readiness.
  - A provenance, transform, known-answer, interval, independence or mutation guard fails.
  - The 11:11:55Z lane deadline arrives.
  progress:
    metric: fixed n = 68/69 source serializations evaluated with conservative rigid-pose enclosures
    before: No reusable rigid-pose regularizer or H-053 experiment record exists.
    after: >-
      A content-hash-bound numerical prototype and explicit interval-enclosure blocker
      are retained; zero of four target members were retrieved, parsed or fit.
  delegations: []
  outputs:
  - packing/campaign/agent-sessions/session-066-bc109-n68-n69-precision.md
  - packing/campaign/series/series-000-smoke-and-calibration/experiments/exp-047-h-053-unitsquare-rigid-pose-serialization.md
  - packing/campaign/hypotheses/H-053-unitsquare-rigid-pose-serialization.md
  - packing/src/sqpack/research/unitsquare_precision.py
  - packing/tests/test_unitsquare_precision.py
  - packing/cases/unitsquare_precision/readiness-controls.json
  - packing/campaign/resource-usage/codex-task-tree-session-066.yaml
  checks:
  - Session-066 and exp-047 pass their enforced soft schemas.
  - 31 focused and atlas tests pass; the 13 focused tests also pass under optimized Python.
  - Ruff, BasedPyright, optimized module self-test and scoped diff-check pass.
  resource_rollups:
  - packing/campaign/resource-usage/codex-task-tree-session-066.yaml
  stop_reason: >-
    W7 stopped before measurement on the interval-enclosure and complete-runner guards;
    H-053 remains instrument-unready and exp-047 is blocked without target samples.
  next_action: >-
    Keep W6 closed and wait for first-wave terminalization, BC-122 and BC-111. Only the
    coordinator may route this lane to BC-117; do not repair the verifier or allocate a
    new round directly from this terminal session.
---
# Session 066 — BC-109 `n = 68/69` Precision Bridge

## Cell ledger

### 0–15 minutes — W3 contract freeze

**Artifact.** The contract below freezes the BC-109 measurement before any target
geometry is parsed or fit.

**Result.** The two source pairs, transform, serialization models, ordering, metrics,
thresholds, lane cells and failure semantics are fixed.

**Guard.** This cell read the agenda, H-053, release metadata, source-retention policy
and file digests. It did not open either target SVG’s geometry, retrieve either parent,
inspect target pose output, or enter W7 or W6.

**Next.** Build the provenance and regularization instrument against synthetic controls,
then run the fixed cells in order.
Any required contract change after target inspection stops this round as contaminated
rather than amending the contract.

### 15–54 minutes — W7 premeasurement stop

**Artifact.** `packing/src/sqpack/research/unitsquare_precision.py`,
`packing/tests/test_unitsquare_precision.py`, and
`packing/cases/unitsquare_precision/readiness-controls.json`, bound respectively to
SHA-256 `92e7b6e43b8785c0b618f2a48c3a26c09afb1b5cd9009a69189dfab0f606b22c`,
`9aeaf96d45fd94ba38af00a713a76297077a1aa7c55efc6783d6c94561c2038f`, and
`fe3a17fc3f4573c80ca0d9b00987b831d483ac4ba9ac13f288bad34e0e2cec4f` at baseline commit
`d7c94590`.

**Result.** Thirteen synthetic tests passed normally and under optimized Python.
Ruff, BasedPyright and the optimized module self-test passed.
The test inventory covers the digest-before-parse adapter and cleanup,
identity/translation/scale/nested and rotated transforms, the three source-cell models,
cyclic/reversed canonicalization, wall- tangent/interior/crossing scenes,
separated/tangent/overlap pairs, deterministic replay, all named mutations, the frozen
target plan and the parent-only first-valid seal.
These are numerical behavior checks: the fitter’s fixed tolerance and heuristic radii do
not prove a nonempty outward pose enclosure, and the verifier does not outwardly decide
the retained wall and pair signs.
The `--record` entry point also stops at its gate rather than continuing through the
complete frozen measurement after authorization.

**Guard.** The preregistered `--record` command returned its typed W6 gate at exit 3. No
network request, parent retrieval, child read, target parse or target fit occurred.
The record validator’s soft-schema and substantive research checks passed; its terminal
failure was limited to concurrent coordinator-owned generated views, ledger state and
session-065 phase drift.

**Next.** Keep H-053 unready and W6 closed.
A successor W7 cell must supply a sound outward existence/sign argument and
injection-test the complete authorized retrieval, parse, parent-seal, child,
verification and atomic-write path before a new experiment is registered.

## Frozen claim and determination

For each fixed UnitSquare Release 1 pair at `n = 68` and `n = 69`, at least one model
from the inventory below must admit nonempty compatible rigid-unit-square pose
enclosures for both the parent and its corresponding child.
The source digest and transform guards must pass, and the independent verifier must
decide every container and pairwise-validity sign.

The outcome is `accepted` only if both pairs qualify.
It is `rejected` only if the instrument soundly and exhaustively evaluates all three
models for at least one pair and none qualifies.
A provenance, transform, enclosure, verifier or exhaustiveness failure is a typed
premeasurement or measurement refusal and leaves H-053 unresolved.

The primary metric is the determination tuple, per `n` and model:
`(parent_compatible, child_compatible, parent_valid, child_valid)`. A pair qualifies
only when all four values are proven true.
Search failure is not proof of an empty pose set.

Secondary mechanism metrics, recorded as outward-rounded intervals, are:

- maximum published-to-rigid corner displacement;
- maximum corresponding-corner ambiguity diameter;
- compatible-pose component count or the typed value `not-proven-finite`;
- conditioning diagnostics that do not enter the verdict;
- container-side width, signed wall-clearance intervals and signed pair-separation
  intervals.

Signed wall clearance is the minimum inward corner-to-wall distance.
Signed pair separation is the maximum separating-axis projection gap over the two
squares’ edge normals, positive for separation and negative for overlap.
A validity predicate is decided only when its interval proves the required nonnegative
sign. An interval that straddles zero is `possible-contact` and cannot qualify H-053; a
label never substitutes for a sign proof.

The separate, downstream `n = 68` surgery-grade screen does not decide H-053. Its frozen
width threshold is one quarter of `7.68618004216131e-5`, namely `1.9215450105403275e-5`
in unit-square-length coordinates.
Displacement, ambiguity, container-side width and every signed-predicate width must each
meet that bound before the selected arm may be offered to H-051.

## Frozen fixtures and provenance

The retained release metadata anchor is
`packing/resources/web/unitsquare-release1-2026/results.json`, SHA-256
`dd7c1c62050b004c86959e59621c51d097f70d51cb142be9c19b15a16693d8b3`.

| n | member | fixture | required SHA-256 |
| ---: | --- | --- | --- |
| 68 | child | `packing/resources/web/known-best-packings/unitsquare/n068.svg` | `d7385d6ce1b5a959d06893c94f3c0355f17175bd68608db6f012ca309854ed66` |
| 68 | parent | `https://kingbird.myphotos.cc/packing/square-68.svg` | `558fbdddfeb0b2f8752b88e172d2776544beb4d2a7122189ef77c1e1c5ebdc6d` |
| 69 | child | `packing/resources/web/known-best-packings/unitsquare/n069.svg` | `b32aa37d37b07248ac92e683bbfd9be7ca6eb6aafa35a35e46a2484467afee41` |
| 69 | parent | `https://kingbird.myphotos.cc/packing/square-69.svg` | `0333814c7b43ddc7db549a54771de117f8a6b7b3db0f89c12fe035115546fd08` |

The release records bind the `n = 68` and `n = 69` rows to record digests
`b44aac1accc9a4d5b92f96077aaaaecb88b99faaef24870b3dd7f4507070f9d8` and
`04af1825f36d4ec70c0372b3dabf0bb5871025e2ee37563fc6242c4ac2af253d`, respectively.
These source-supplied hashes are provenance fields, not mathematical verification.

Child SVG bytes remain retained archival fixtures and must match their hashes before
parsing. Parent SVG bytes may exist only in memory or a private temporary file for the
duration of a hash-verified parse.
The instrument may retain the URL, expected and observed digest, retrieval time, parser
version, normalized numerical facts and derived receipts.
It must not retain parent bytes, XML, source excerpts, palettes or temporary paths.
A parent digest mismatch is a refusal before parsing, and cleanup must run on success
and failure.

## Transform and serialization semantics

The parser composes every SVG transform in document order into one global-SVG mapping
before reading the container or square vertices.
It must identify one container rectangle `(x0, y0, W, H)` in that same frame, with
`W > 0` and `H > 0`. For candidate container side `L`, a global point `(X, Y)` maps to

`(L*(X-x0)/W, L*(y0+H-Y)/H)`.

The mathematical container is `[0,L] × [0,L]`; the second coordinate reverses the SVG
y-axis.
Every fitted object is a rigid square of side exactly `1`. Corner correspondences
are cyclic orderings of the four transformed source vertices, with orientation reversal
considered explicitly and a deterministic lexicographic tie break.
A model is compatible only when every matched rigid corner’s inverse image lies inside
its closed source cell.
Singular transforms, multiple plausible containers, unstable square IDs, fewer or more
than four usable vertices, or unresolved corner correspondence cause refusal.

The inventory and evaluation order are fixed:

1. `declared:svg-literal` — each SVG numeric token denotes its exact parsed decimal
   value; side fields retain their source-declared point or directional-bound semantics.
2. `nearest-6` — a published six-place coordinate `d` denotes the closed cell
   `[d-0.5e-6,d+0.5e-6]` in global-SVG coordinates.
3. `truncate-6` — for `d ≥ 0`, the cell is `[d,d+1e-6]`; for `d < 0`, it is
   `[d-1e-6,d]`.

The three models never share or merge cells or pose sets.
The serializer orders rows by
`(n, member, model-order, stable-square-id, canonical-corner-index)` and emits decimal
interval endpoints without binary-float round trips.
A byte-for-byte repeat on the same fixture is required before target measurement.

## Parent-only selection and blindness

H-053 evaluates all models, but the downstream H-051 arm is selected from the `n = 68`
parent alone.
A selector with no access to either child SVG, offered child side, released
reduction or child-derived summary evaluates parent models in the frozen order.
It selects the first compatible, independently valid model, hashes its canonical parent
receipt and seals the model ID before child evaluation.
The hash input contains only the parent URL and digest, `n`, model ID, transform and
interval-policy versions, canonical parent enclosures and independent validity result.

The corresponding child is then evaluated under that sealed model.
Child failure or a failed surgery-grade screen is a refusal for the downstream pilot;
selection never falls through to a later parent model.
H-053’s all-model determination remains separate from this selector.
Any process that reads child or gain information before sealing the parent receipt
contaminates the selection and stops the round.

## Controls, mutations and refusal exits

The reusable instrument must pass these fixtures before target parsing:

- exact axis-aligned and rotated unit squares under identity, translation, scale and
  nested transform stacks, with known recovered poses;
- a wall-tangent square, a strictly interior square and a wall-crossing square;
- a separated pair, an exact tangent pair and an overlapping pair with known signed
  separating-axis outcomes;
- positive and negative decimal values at nearest-cell and truncation-cell boundaries;
- cyclic and reversed corner enumerations that serialize to the same canonical pose.

Frozen mutations must make the named guard fail: change one source byte to trigger the
digest guard; reverse two noncommuting transforms; move one corner outside its decimal
cell; duplicate a square ID; perturb a wall corner outward; and move a separated pair
into overlap. The verifier is written independently of the fitter and consumes only the
canonical pose-enclosure receipt.
A control or mutation that does not produce its predeclared outcome stops target work.

Other refusal exits are retrieval failure, a policy-unsafe parent cache, unsupported or
singular transform syntax, ambiguous container selection, unbounded decimal or side
semantics, unavailable outward rounding, nondeterministic serialization, fitter/verifier
disagreement, undecided validity signs, incomplete model enumeration, or any change to
this contract after target evidence is visible.

## Proposed reusable instrument and lane cells

Build `packing/src/sqpack/research/unitsquare_precision.py` around typed source
fixtures, serialization models, transform-normalized decimal cells, rigid-pose
enclosures and canonical predicate receipts.
Its public boundary accepts bytes plus an expected digest; parent retrieval is a thin
ephemeral adapter. The fitter and independent receipt verifier expose separate entry
points. Deterministic YAML or JSON case receipts belong under
`packing/cases/unitsquare_precision/`; raw parent material does not.

The 130-minute lane budget is fixed:

| elapsed | workflow | required exit |
| --- | --- | --- |
| 0–15 | W3 | this frozen contract, with target fitting unrun |
| 15–35 | W7 | hash-verified ephemeral parent adapter and transform normalization |
| 35–60 | W7 | reusable regularizer, independent verifier and all synthetic controls green |
| 60–80 | W6 | parent fits, mechanism metrics and sealed parent-only arm receipt |
| 80–95 | W6 | children fit under the unchanged model inventory and sealed arm |
| 95–115 | W6 | wall/pair predicates and every frozen mutation |
| 115–130 | W3 | typed verdict, limits, permitted artifacts, validation and handoff |

No cell may borrow from the final 15 minutes.
A cell that has no durable instrument, guard receipt or typed result at its boundary
stops the lane before the next cell.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
