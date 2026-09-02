---
title: "session-067 — BC-110 n = 50 exact rational control"
softschema:
  contract: packing.squares:AgentSession/v2
  schema: ../schemas/agent-session.schema.yaml
  envelope: session
  status: enforced
session:
  id: session-067
  primary_bead: think-uz6f
  status: stopped
  title: "BC-110 n = 50 exact rational control"
  date: '2026-09-01'
  started_at: '2026-09-01T09:01:55Z'
  deadline_at: '2026-09-01T11:01:55Z'
  branch: codex/w3-nine-hour-autonomous-run
  goal: >-
    Decide H-054 for the reported n = 50 side 53/7 through a target-blind W3 contract, a
    W7 rational certificate and compatibility instrument, W6 exact reconstruction or
    typed refusal, and a final W3 choice of the n = 54 or n = 39 next rung without
    editing the frontier.
  workflow_phases:
  - workflow: insight-iteration
    recording: contemporaneous
    clock_role: work
    focus: insight
    objective: >-
      Freeze H-054's source and witness fixture, hashes, square correspondence, symmetry
      and source-precision compatibility manifest, metric, threshold, budget, refusal
      conditions, controls, mutations and instrument design without reconstructing the
      target.
    bead: think-uz6f
    status: completed
    entered_by: session_start
    switch_reason: null
    budget_minutes: 20
    started_at: '2026-09-01T09:01:55Z'
    deadline_at: '2026-09-01T09:21:55Z'
    expected_output: A complete target-blind W6 contract returned to the coordinator for serial preregistration.
    validation_command: >-
      uv run --frozen --all-extras --group dev packing-validate --only "soft-schema"
    kill_condition: >-
      Stop before measurement if target reconstruction starts, the witness mapping or
      source-precision cells remain unfrozen, or a rational result could escape the
      retained witness-compatibility boundary.
    fallback: Retain the smallest source, representation or compatibility gap as a typed premeasurement stop.
    outcome: >-
      Froze the target-blind H-054 contract, including immutable fixture hashes, a
      deterministic correspondence and symmetry manifest, the source-cell refusal gate,
      metric, 53/7 threshold, controls, mutations, instrument boundary and all 120 minutes
      of lane cells. No target reconstruction or W7/W6 command ran.
    evidence:
    - packing/campaign/agent-sessions/session-067-bc110-n50-exact-control.md
    - packing/campaign/hypotheses/H-054-n50-exact-rational-reconstruction.md
    - packing/frontier/n-050.md
    - packing/witnesses/known-best/n-050.yaml
    - packing/resources/web/known-best-packings/sources.json
    stop_reason: The initial 20-minute W3 contract-freeze artifact is complete.
    next_action: >-
      Return this contract to the coordinator for serial H-054 experiment/result path
      assignment before any W7 instrument work.
  - workflow: pipeline-improvement
    recording: contemporaneous
    clock_role: work
    focus: correctness
    objective: >-
      Under exp-048, establish whether retained evidence supplies defensible source cells
      for every witness scalar; build and exercise the separated rational-certificate,
      exact-geometry and compatibility interfaces on the n = 18, n = 19, rational and
      source-refusal controls without reconstructing n = 50.
    bead: think-uz6f
    status: stopped
    entered_by: evidence_checkpoint
    switch_reason: >-
      The target-blind W3 contract is complete and the coordinator allocated exp-048 and
      its exact future result path without reconstructing the target.
    budget_minutes: 25
    started_at: '2026-09-01T09:13:09Z'
    deadline_at: '2026-09-01T09:38:09Z'
    expected_output: >-
      Source-justified cells plus separated instruments passing every readiness guard and
      H-054 instrument_ready true, or a typed E1/E4 premeasurement stop with no n = 50
      target output.
    validation_command: >-
      uv run --frozen --all-extras --group dev pytest -q tests/test_n050_exact.py && uv
      run --frozen --all-extras --group dev packing-validate --records
    kill_condition: >-
      Stop before target reconstruction if retained evidence cannot justify every source
      cell, a known-answer or mutation guard fails, or the independent interfaces
      disagree.
    fallback: >-
      Leave H-054 instrument_ready false, retain exp-048 as premeasurement refusal E1 or
      invalid-instrument E4, and create no n = 50 target result.
    outcome: >-
      Artifact: exp-048 now retains the frozen E1 source/provenance refusal. Result: the
      retained source inventory and numerical witness do not declare upstream
      serialization semantics from which every scalar's closed source cell can be
      justified. Guard: W7 stopped at its first admission decision; no n = 50
      reconstruction, solver, verifier, control execution, target sample or result file
      was created, and H-054 remains instrument_ready false. Next: return the lane, ready
      for terminalization, to the coordinator for receipt attachment and fallback
      routing; do not enter W6.
    evidence:
    - packing/campaign/series/series-000-smoke-and-calibration/experiments/exp-048-h-054-n50-exact-rational-reconstruction.md
    - packing/witnesses/known-best/n-050.yaml
    - packing/resources/web/known-best-packings/sources.json
    - packing/frontier/n-050.md
    stop_reason: >-
      E1 source/provenance fired before instrument construction: no retained declaration
      gives every upstream source scalar an exact, nearest-rounding, truncation or
      interval meaning.
    next_action: >-
      Return the lane to the coordinator, ready for terminalization; W6 is unauthorized,
      and only a new preregistered round with complete source semantics may revisit
      reconstruction.
  budget:
    wall_minutes: 120
    max_cycles: 4
    checkpoint_minutes: 20
    slice_minutes: 30
    finalization_minutes: 15
  stop_conditions:
  - Any target reconstruction runs before preregistration and instrument readiness.
  - A source, compatibility, known-answer, independent-verifier or mutation guard fails.
  - The 11:01:55Z lane deadline arrives.
  progress:
    metric: witness-compatible exact n = 50 reconstruction or typed refusal retained
    before: The frontier records only the grid as verified; no exact 50-pose certificate exists.
    after: >-
      Frozen refusal E1 establishes that retained evidence supplies no defensible
      upstream serialization cell for every n = 50 witness scalar. H-054 remains
      instrument-unready, no target reconstruction or result file exists, and the lane
      is preserved for BC-118 source/provenance localization.
  delegations: []
  outputs:
  - packing/campaign/agent-sessions/session-067-bc110-n50-exact-control.md
  - packing/campaign/series/series-000-smoke-and-calibration/experiments/exp-048-h-054-n50-exact-rational-reconstruction.md
  - packing/campaign/resource-usage/codex-task-tree-session-067.yaml
  checks:
  - uv run --frozen softschema validate campaign/agent-sessions/session-067-bc110-n50-exact-control.md (valid)
  - uv run --frozen softschema validate campaign/series/series-000-smoke-and-calibration/experiments/exp-048-h-054-n50-exact-rational-reconstruction.md (valid)
  - uvx --from flowmark-rs==0.3.2 flowmark --auto --check --no-cache campaign/agent-sessions/session-067-bc110-n50-exact-control.md (clean)
  - The frozen exp-048 result path is absent.
  - The disjoint session-067 Codex task-tree receipt passed semantic generation.
  - Independent closure audit retained a guard determination, corrected the dependency taxonomy, and aligned BC-118's E1--E5 mapping.
  resource_rollups:
  - packing/campaign/resource-usage/codex-task-tree-session-067.yaml
  stop_reason: >-
    Stopped before W6 at the frozen E1 source/provenance gate: retained metadata does not
    declare the upstream scalar serialization semantics required to construct complete
    source cells, so target reconstruction would exceed the registered evidence.
  next_action: >-
    Enter BC-122 under think-iv3e. After that checkpoint, follow only the coordinator's
    retained route for the n = 50 E1 refusal; do not reopen either stopped first-wave
    lane directly.
---
# Session 067 — BC-110 `n = 50` Exact Control

## Cell ledger

### 0--20 — Target-Blind W3 Contract Freeze

- **Artifact:** This session now contains the complete H-054 fixture, compatibility,
  measurement, refusal, control, mutation and instrument contract.
- **Result:** The contract is frozen at side `53/7`. The retained source metadata does
  not declare source serialization or rounding semantics, so W7 must either establish
  defensible per-scalar cells from retained evidence or stop before reconstruction.
- **Guard:** No reconstruction, solver, n = 50 verifier or target-output command ran.
  Only the declared agenda, H-054, retained frontier/witness metadata, source inventory,
  exact-control code and file digests were inspected.
- **Next:** Return this record to the coordinator.
  The coordinator allocates the exact experiment/result paths; only then may W7 build
  and validate the frozen instrument.

### 20--45 — W7 Source-Semantics Gate

- **Artifact:** `exp-048` retains typed premeasurement refusal E1 against the frozen
  `source-semantics-required-v1` model.
- **Result:** The retained source inventory supplies provenance and a retention policy,
  and the witness supplies numerical-replay precision metadata, but neither fixture
  declares upstream scalar serialization semantics.
  No defensible closed cells exist for all source scalars, so the readiness guard fails
  and H-054 remains `instrument_ready: false` without a scientific verdict.
- **Guard:** The first W7 admission gate fired immediately.
  No target reconstruction, solver, verifier, readiness-control execution, target sample
  or result JSON was created; the frozen fixture hashes and compatibility manifest were
  not changed.
- **Next:** Return the lane to the coordinator, ready for receipt attachment, session
  terminalization and fallback routing.
  W6 remains unauthorized.

## Frozen H-054 Contract

### Exact Claim

The retained n = 50 source facts admit exactly 50 rational center-direction poses at
container side `L = 53/7`. A passing result must establish all of the following at the
same frozen revision:

1. Every pose has `x,y,c,s` in `Q`, with `c^2 + s^2 = 1`; `(c,s)` is the unit direction
   of one square edge and is interpreted modulo a quarter turn.
2. An independently implemented exact checker accepts every wall predicate and all
   `50*49/2 = 1225` pair predicates.
3. One compatibility receipt maps the exact certificate bijectively to the 50 retained
   witness rows under the frozen D4, local-orientation and source-cell rules below.
4. The exact geometry and compatibility mutations are both rejected.

Acceptance would certify one feasible upper-bound construction compatible with the
retained witness. It would not establish optimality, rigidity, uniqueness or a frontier
change. A different packing at `53/7` cannot satisfy H-054.

### Immutable Fixtures

| Fixture | Frozen SHA-256 | Contract role |
| --- | --- | --- |
| `packing/campaign/hypotheses/H-054-n50-exact-rational-reconstruction.md` | `df451856a02b734ec9e36e1985522568c8d0fce4ccdd28725646d0e05e531926` | Claim, criterion and evidence boundary |
| `packing/campaign/agendas/agenda-012-weighted-proof-precision-bridge-and-cross-scale-controls.md` | `866f2610407942caf9a39023645a6be52fea573fbb9bff9589320fd3525b9d2a` | BC-110 launch and 120-minute lane contract |
| `packing/frontier/n-050.md` | `a5f9ead7cd94ee14bef77d4cdd3f37f64c9a803ff47f406a2dba9f8097f2c746` | Reported side, attribution and current evidence boundary |
| `packing/witnesses/known-best/n-050.yaml` | `8318cbc7ec4c4a8b3d15634531535b204f0106360361f81e71820a6e2308b21e` | Fifty retained center-angle rows and numerical-feasibility metadata |
| `packing/resources/web/known-best-packings/sources.json` | `4fa25fab27f69a9c2d8e28c6924a36b8d0bfc00ac9b066fb53fa796412b0d687` | Source URL, attribution and retention policy |

The frontier reports Thomas Schadt’s 2025 simulated-annealing construction at decimal
side `7.57142857142857`, exact form `7 + 4/7`, while the repository-verified upper bound
remains the grid value `8`. The witness stores 50 center-angle rows at decimal side
`7.571428571428571428571428571428571428571`; its retained numerical replay used 120
decimal digits and tolerance `1e-8`. Those are checker settings, not
source-serialization semantics.
The source inventory records the upstream n = 50 SVG URL, retrieval date 2026-08-26, and
policy `metadata-and-derived-numerical-facts-only`; raw source bytes are not retained.

### Correspondence and Compatibility Manifest

The certificate numbers its exact poses `1..50` only for stable serialization.
Those ids do not assume the same labels as the witness rows.

1. **Global D4 order:** test `identity`, rotations by 90, 180 and 270 degrees,
   reflection `(x,y)->(L-x,y)`, then that reflection composed with the same three
   rotations. Apply the same exact affine action to centers and direction vectors.
2. **Orientation periodicity:** a square-edge direction is equivalent under the four
   quarter turns `(c,s)`, `(-s,c)`, `(-c,-s)`, `(s,-c)`. A reflected source frame also
   records a local winding bit.
   Compatibility compares the induced square, not a decimal degree label as an exact
   angle.
3. **Bijection:** for each global action, build a bipartite graph from exact certificate
   ids to retained witness rows.
   An edge exists only when the transformed center and direction satisfy every frozen
   source cell for that row.
   Require a perfect matching.
4. **Tie-breaking:** among all passing receipts choose the lexicographically first tuple
   `(global-D4-index, witness-row vector ordered by certificate id, quarter-turn vector,
   winding-bit vector)`. Never select a symmetry or matching from geometric slack or a
   favorable H-054 outcome.
5. **Source cells:** each retained row requires closed cells for center `x`, center `y`
   and the stored orientation observation.
   A source-declared exact token yields a singleton; declared nearest rounding at `d`
   decimal places yields the corresponding half-ulp cell; declared truncation yields its
   directed one-ulp cell; a declared interval is used verbatim.
   Direction-component boxes are derived from an angle cell with outward-rounded
   interval trigonometry.
   No model may be inferred from the number of stored digits or the witness checker’s
   `rounding: nearest` field.

The current retained source metadata declares none of those serialization models.
Therefore the manifest freezes model id `source-semantics-required-v1` with no
admissible per-scalar cells yet.
W7 may set `instrument_ready: true` only if retained evidence—not the target
reconstruction—supplies one of the declared cell semantics for every scalar.
Otherwise BC-110 stops through refusal E1 below.

### Metric, Threshold, and Review State

- **Shape:** determination.
- **Threshold:** exact container side `53/7`.
- **Accept:** all four claim clauses pass exactly and both mutation classes are
  rejected.
- **Reject:** a sound exact contradiction proves the entire frozen, source-compatible
  reconstruction system inconsistent.
- **Unresolved:** any source, representation, compatibility, independence or budget gate
  prevents an exact determination.
- **Review:** any executed experiment decision is written with `needs_review: true`.
  Only BC-121 may clear it unchanged after BC-120 explicitly passes this exact decision.

### Lane Budget and Cells

The lane has 120 wall minutes, including its 15-minute final W3 reserve:

| Relative time | Workflow | Frozen work |
| --- | --- | --- |
| 0--20 | W3 | Freeze this contract without target reconstruction. |
| 20--45 | W7 | Build the rational certificate representation and two independent checkers; validate them on n = 18, n = 19 and source-refusal controls; run readiness guards. |
| 45--70 | W6 | Reconstruct the exact rational target or retain the first typed source gap. |
| 70--90 | W6 | Verify every exact wall, pair and compatibility predicate. |
| 90--105 | W6 | Fire the frozen geometry and compatibility mutations. |
| 105--120 | W3 | Interpret the mechanism, retain the result, select n = 54 versus n = 39 from the observed seam, validate and hand off. |

Coordinator experiment allocation and any wait for its returned paths count against the
lane clock. No cell or deadline moves after target evidence appears.

### Refusal Branches

- **E1 — source/provenance:** a fixture hash differs, the retained source cannot justify
  complete per-scalar cells, source rows are missing, or attribution cannot be bound to
  this witness.
- **E2 — representation:** a source-compatible pose requires a nonrational scalar, the
  rational certificate cannot express an orientation, or no complete 50-pose certificate
  can be formed without assuming a rounding rule.
- **E3 — compatibility:** no D4 action has a perfect row matching, a required pose lies
  outside its cell, or deterministic tie-breaking cannot select a unique receipt.
- **E4 — verifier/instrument:** the independent checkers disagree, a known-answer
  control fails, or either mutation is accepted.
  Record `invalid_instrument`; do not dispose H-054.
- **E5 — priced exhaustion:** the 120-minute wall expires without an exact contradiction
  or complete verified certificate.
  Retain the partial equations and first unresolved predicate without inferring
  rejection.

E1--E3 and E5 are unresolved H-054 outcomes unless an exact contradiction covers the
whole frozen compatibility system.
A guard firing before target measurement makes the agenda row `stopped`; an executed
negative or unresolved determination makes it `complete` while preserving the scientific
status.

### Controls

- **Positive exact-field control:**
  `uv run --frozen python -m cases.lifted_q7.verify_exact` must exactly verify n = 18
  over `Q(sqrt(7))` and reject its duplicated-square mutation.
- **Mechanism contrast:** `uv run --frozen python -m cases.lifted_q2.verify_exact` must
  exactly verify n = 19 over `Q(sqrt(2))` and reject its duplicated-square mutation.
- **Rational exact-LP control:** the rational grid cell exercised by
  `tests/test_promote_exact_phase1.py` must pass without a float dependency.
- **Source-refusal control:** a synthetic retained row set with identical decimal values
  but no declared serialization semantics must produce E1, and
  `tests/test_exact_construction_price.py` remains the known control that retained
  decimals alone do not establish exact structure.

These controls validate representation, exact predicates and refusal behavior.
They do not supply an n = 50 pose or authorize target measurement.

### Frozen Mutations

- **G1 geometry mutation:** after a candidate certificate is immutable, replace pose 50
  with an exact duplicate of pose 1. Both independent geometry checkers must reject the
  resulting coincident pair.
- **C1 compatibility mutation:** duplicate the first witness-row id in the frozen
  certificate-to-witness mapping while leaving the certificate and cell claims
  unchanged. The compatibility checker must reject the nonbijective receipt before
  geometry status is considered.
- **C2 source-cell parser control:** reverse the endpoints of the first declared
  center-x cell. The manifest parser must reject the empty interval before matching.

G1 and at least one of C1/C2 must fire in the experiment.
None may be chosen from a target-specific weak predicate.

### Proposed Exact Instrument

W7 may build, but not yet run on n = 50, the following separated components:

1. A manifest loader that verifies all frozen hashes, validates 50 source rows,
   materializes only source-declared closed cells and serializes the
   D4/matching/tie-break contract.
2. A rational certificate format for `L,x,y,c,s` using `Fraction`, with exact
   `c^2+s^2=1` checks and stable certificate ids.
3. A constructor allowed to use `fixed_cell_lp` and `solve_from_scratch` but forbidden
   to treat decimal witness values as exact or infer their rounding model.
4. An independent geometry checker that does not reuse the constructor’s LP rows.
   It constructs corners over `Q`, checks all walls, evaluates separating axes for all
   1225 pairs, and reports the first exact failing predicate.
5. A compatibility checker separate from geometry.
   It replays source cells, D4 actions, local orientation variants, perfect matching and
   deterministic tie-breaking, then emits a hash-bound receipt.

W7 readiness requires both exact-field controls, the rational control, source refusal,
G1 and C1/C2 to pass without reading n = 50 target output.
Only then may the lane update H-054’s instrument description, set
`instrument_ready: true`, record the readiness evidence in its coordinator-assigned
experiment, and enter W6.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
