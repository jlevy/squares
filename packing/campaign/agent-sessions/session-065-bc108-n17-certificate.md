---
title: "session-065 — BC-108 n = 17 independent certificate agreement"
softschema:
  contract: packing.squares:AgentSession/v2
  schema: ../schemas/agent-session.schema.yaml
  envelope: session
  status: enforced
session:
  id: session-065
  primary_bead: think-swtr
  status: completed
  title: "BC-108 n = 17 independent certificate agreement"
  date: '2026-09-01'
  started_at: '2026-09-01T09:01:55Z'
  deadline_at: '2026-09-01T11:11:55Z'
  branch: codex/w3-nine-hour-autonomous-run
  goal: >-
    Decide H-052 on the fixed n = 17 certificate through a target-blind W3 contract, a
    W7 source-faithful and independently authored exact instrument, W6 invariant and
    mutation measurement, and a final W3 mechanism interpretation, without adopting or
    transferring the bound.
  workflow_phases:
  - workflow: insight-iteration
    recording: contemporaneous
    clock_role: work
    focus: insight
    objective: >-
      Freeze H-052's claim, certificate fixture and hashes, exact invariants, threshold,
      budget, refusal conditions, shared assumptions, independence boundary, controls,
      mutations and instrument design without executing or reading target output.
    commitment: BC-108
    bead: think-swtr
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
      Stop before measurement if target certificate output is read, an invariant or
      mutation remains unfrozen, or implementation independence cannot be stated
      audibly.
    fallback: Retain the missing field or independence ambiguity as a typed premeasurement stop.
    outcome: >-
      Froze the exact H-052 claim, retained fixture hashes, invariant manifest, equality
      threshold, seven-cell 130-minute lane plan, typed refusal rules, five named
      mutations, source-defect controls, shared-assumption boundary and clean-room scalar
      instrument design. The retained target verifier was hashed but neither opened nor
      executed, and no target output was read.
    evidence:
    - packing/campaign/hypotheses/H-052-n17-independent-certificate-agreement.md
    - packing/resources/web/n17-lower-bounds-2026/README.md
    - packing/campaign/agent-sessions/session-065-bc108-n17-certificate.md#frozen-w6-contract
    stop_reason: The target-blind contract is complete at the planned W3 checkpoint.
    next_action: >-
      Return this contract to the coordinator. The coordinator must create the exact
      H-052 experiment/result preregistration before appending and dispatching W7.
  - workflow: pipeline-improvement
    recording: contemporaneous
    clock_role: work
    focus: correctness
    objective: >-
      Build the nonexecuting extractor, canonical manifest, clean-room Cartesian
      accumulator and separate source-faithful adapter under exp-049, pass the synthetic,
      provenance, independence, mutation and optimized-Python guards, and bind the exact
      ready revision before any target execution.
    commitment: BC-108
    bead: think-swtr
    status: completed
    entered_by: evidence_checkpoint
    switch_reason: >-
      The target-blind W3 contract is complete and the coordinator allocated exp-049 and
      its exact future result path without opening target output.
    budget_minutes: 40
    started_at: '2026-09-01T09:13:09Z'
    deadline_at: '2026-09-01T09:53:09Z'
    expected_output: >-
      A reusable target-blind exact instrument with a frozen clean-room file hash,
      passing readiness guards, H-052 bound to its validated revision and
      instrument_ready true; or a typed premeasurement stop with no target sample.
    validation_command: >-
      uv run --frozen --all-extras --group dev pytest -q
      tests/test_n17_weighted_certificate.py && uv run --frozen --all-extras --group dev
      packing-validate --records
    kill_condition: >-
      Stop before target execution if any fixture, extraction, known-answer,
      independence, mutation, serialization or optimized-Python guard fails, or if the
      clean-room accumulator changes after its target-blind hash freezes.
    fallback: >-
      Leave H-052 instrument_ready false, retain exp-049 as a typed premeasurement stop,
      and return the smallest failed readiness guard without a scientific verdict.
    outcome: >-
      Built the nonexecuting hash-verified extractor, exact canonical model, clean-room
      direct Cartesian accumulator, shared event-cell geometry, separate source-faithful
      adapter, preregistered CLI and explicit-condition production self-test. Eleven
      focused tests pass; the production self-test emits byte-identical receipts under
      normal and optimized Python. Its named controls exercise `/28` versus `/29` grid
      spacing and `KMAX + 1` versus an omitted final endpoint through both accumulation
      paths and canonical manifests. Ruff and BasedPyright are clean. H-052 is bound to
      the repaired hashes and marked instrument_ready true. No target replay or result
      was produced.
    evidence:
    - packing/cases/n17_weighted_certificate/independent.py
    - packing/cases/n17_weighted_certificate/source_faithful.py
    - packing/cases/n17_weighted_certificate/selftest.py
    - packing/cases/n17_weighted_certificate/run.py
    - packing/tests/test_n17_weighted_certificate.py
    - packing/campaign/hypotheses/H-052-n17-independent-certificate-agreement.md
    - packing/campaign/series/series-000-smoke-and-calibration/experiments/exp-049-h-052-n17-independent-certificate-agreement.md
    stop_reason: All preregistered W7 readiness guards passed before the target boundary.
    next_action: >-
      Return the readiness receipt to the coordinator. Do not execute exp-049 until the
      coordinator appends and authorizes the W6 measurement phase.
  - workflow: research-loop
    recording: contemporaneous
    clock_role: work
    focus: correctness
    objective: >-
      Execute the one preregistered exp-049 target command against the hash-bound fixed
      n = 17 certificate, preserve its canonical result without target-informed repair,
      run the five frozen mutations and both source-defect controls, and return the
      immutable evidence for final W3 interpretation.
    commitment: BC-108
    bead: think-swtr
    status: stopped
    entered_by: evidence_checkpoint
    switch_reason: >-
      Coordinator replay and an independent readmission audit passed the repaired W7
      gate: the frozen clean-room hash is unchanged, the production self-test passes
      normally and under optimized Python with byte-identical output, source-defect
      controls use both implementations, retained-source hashes match, and the target
      result path is absent.
    budget_minutes: 65.34
    started_at: '2026-09-01T09:51:35Z'
    deadline_at: '2026-09-01T10:56:55Z'
    expected_output: >-
      The exact exp-049 result JSON and a terminal scientific determination or typed
      invalid-instrument result, with the first disagreement retained verbatim, every
      frozen mutation and source-defect receipt recorded, and no frontier adoption.
    validation_command: >-
      uv run --frozen python -m cases.n17_weighted_certificate.run --record
      campaign/series/series-000-smoke-and-calibration/results/exp-049-h-052-n17-independent-certificate-agreement.json
    kill_condition: >-
      Stop without repair if a retained source or clean-room hash changes, the exact
      command fails to emit one canonical record, a readiness or mutation guard becomes
      false, or the 10:56:55Z W6 deadline arrives. Preserve a reproducible mathematical
      disagreement as the result rather than treating it as a process failure.
    fallback: >-
      Retain the immutable partial or invalid-instrument record, leave H-052
      review-pending, and hand the first exact failed guard or unequal manifest row to
      final W3 and BC-116 without rerunning altered code.
    outcome: >-
      Launched the exact exp-049 target command once at 09:51:35Z. It remained live and
      silent through the declared 10:56:55Z hard stop. One interrupt ended it with exit
      130 while the independent direct Cartesian accumulator was running. Both command
      processes then disappeared and the result path remained absent. No canonical row,
      complete comparison, mutation result or checkpoint was emitted, so H-052 remains
      unresolved rather than accepted or rejected.
    evidence:
    - packing/campaign/series/series-000-smoke-and-calibration/experiments/exp-049-h-052-n17-independent-certificate-agreement.md
    - packing/campaign/agent-sessions/session-065-bc108-n17-certificate.md#w6-checkpoint--2026-09-01t102155z
    - packing/campaign/agent-sessions/session-065-bc108-n17-certificate.md#w6-checkpoint--2026-09-01t104155z
    stop_reason: The declared 3920-second W6 timebox expired before a canonical result existed.
    next_action: >-
      Enter the reserved final W3 phase, preserve H-052 readiness without a scientific
      disposition, and hand the frozen no-checkpoint timebox outcome to BC-116.
  - workflow: insight-iteration
    recording: contemporaneous
    clock_role: finalization
    focus: insight
    objective: >-
      Interpret the W6 process determination without promoting it to mathematical
      evidence, terminalize exp-049 and session-065 honestly, and hand the frozen
      unresolved no-checkpoint outcome to BC-116 without hypothesis or frontier
      adoption.
    commitment: BC-108
    bead: think-swtr
    status: completed
    entered_by: planned_checkpoint
    switch_reason: >-
      The declared W6 timebox expired with no canonical result, so the reserved final
      W3 phase must separate process evidence from the unmeasured H-052 criterion and
      close the lane.
    budget_minutes: 15
    started_at: '2026-09-01T10:56:55Z'
    deadline_at: '2026-09-01T11:11:55Z'
    expected_output: >-
      A validated unresolved exp-049 record and completed session handoff that retain
      the frozen revision, exact timebox cost, absent-result state and BC-116 route.
    validation_command: >-
      uv run --frozen softschema validate
      campaign/series/series-000-smoke-and-calibration/experiments/exp-049-h-052-n17-independent-certificate-agreement.md
      && uv run --frozen softschema validate
      campaign/agent-sessions/session-065-bc108-n17-certificate.md
    kill_condition: >-
      Stop if finalization would create a result file, rerun or alter the instrument,
      decide H-052 from missing output, change the frontier, or exceed 11:11:55Z.
    fallback: >-
      Preserve exp-049 as unresolved and review-pending with the smallest missing-output
      fact, leave session-065 stopped, and return the incomplete handoff to the
      coordinator.
    outcome: >-
      Separated the W6 process stop from the unmeasured H-052 criterion, removed the
      expired experiment lease, recorded the exact 3920-second cost and absent-result
      state, retained instrument readiness and needs_review, and validated exp-049 and
      session-065. No result JSON, rerun, hypothesis disposition or frontier adoption
      was created. BC-108 is executed-unresolved and the frozen no-checkpoint outcome is
      handed to BC-116.
    evidence:
    - packing/campaign/series/series-000-smoke-and-calibration/experiments/exp-049-h-052-n17-independent-certificate-agreement.md
    - packing/campaign/agent-sessions/session-065-bc108-n17-certificate.md#w6-timebox-stop
    - packing/campaign/agent-sessions/session-065-bc108-n17-certificate.md#final-w3--executed-unresolved
    stop_reason: The unresolved terminal records validated and the BC-116 handoff is complete.
    next_action: >-
      Coordinator review applies the needs_review disposition. BC-116 may plan a newly
      timeboxed replay from the frozen revision; no scientific claim changes before
      that review and measurement.
  budget:
    wall_minutes: 130
    max_cycles: 4
    checkpoint_minutes: 20
    slice_minutes: 30
    finalization_minutes: 15
  stop_conditions:
  - Any target output is read before preregistration and instrument readiness.
  - A source, provenance, independence, known-answer or mutation guard fails.
  - The 11:11:55Z lane deadline arrives.
  progress:
    metric: frozen H-052 invariants independently evaluated with retained controls
    before: No independent implementation or experiment record exists for the fixed certificate.
    after: >-
      W7 produced a hash-frozen ready instrument; the one exact W6 run consumed its
      declared 3920-second timebox without a canonical record or checkpoint, leaving
      H-052 scientifically unresolved and review-pending.
  delegations: []
  outputs:
  - packing/campaign/agent-sessions/session-065-bc108-n17-certificate.md
  - packing/campaign/series/series-000-smoke-and-calibration/experiments/exp-049-h-052-n17-independent-certificate-agreement.md
  - packing/campaign/hypotheses/H-052-n17-independent-certificate-agreement.md
  - packing/cases/n17_weighted_certificate/
  - packing/tests/test_n17_weighted_certificate.py
  - packing/campaign/resource-usage/codex-task-tree-session-065.yaml
  checks:
  - >-
    Recomputed the three Massaccesi source hashes listed in the retrieval receipt; all
    matched. Computed the README and H-052 hashes separately without opening or executing
    the target verifier.
  - >-
    uv run --frozen --all-extras --group dev ruff check
    cases/n17_weighted_certificate tests/test_n17_weighted_certificate.py passed.
  - >-
    uv run --frozen --all-extras --group dev basedpyright
    cases/n17_weighted_certificate tests/test_n17_weighted_certificate.py reported zero
    errors and zero warnings.
  - >-
    uv run --frozen --all-extras --group dev pytest -q
    tests/test_n17_weighted_certificate.py passed eleven tests.
  - >-
    uv run --frozen python -m cases.n17_weighted_certificate.run --selftest and the same
    command with python -O both passed with receipt hash
    9c43160ad7b9f7407c5c1f7057838a925a13b4553b4edcde580f8abc58d9ec00;
    both canonical stdout lines hashed to
    459af1bd0345bee04e5a3af0d1c7a93cec635920774b3d647be13bed9d617579.
  - >-
    The W6 phase budget is recorded as 65.34 minutes because its frozen
    09:51:35Z--10:56:55Z interval is 65 minutes 20 seconds. This corrects a rounded-down
    metadata scalar without changing either absolute clock or authorizing more runtime.
  - >-
    The exact exp-049 target command ran once for 3920 seconds. One hard-stop interrupt
    returned exit 130; process-table checks found neither uv nor Python command, and the
    result path was absent.
  - >-
    Enforced softschema validation passed for the terminal exp-049 and session-065
    records; H-052 remained instrument_ready true and exp-049 remained needs_review
    true.
  - >-
    The terminal session-065 Codex task-tree receipt is complete at the
    2026-09-01T11:01:05Z cutoff with no live descendant session.
  resource_rollups:
  - packing/campaign/resource-usage/codex-task-tree-session-065.yaml
  stop_reason: >-
    The 130-minute lane completed with a ready instrument and one executed W6 timebox,
    but no canonical measurement; BC-108 is executed-unresolved and routed to BC-116.
  next_action: >-
    Apply coordinator review to exp-049. Any replay belongs to BC-116 under a new
    declared timebox and the same frozen revision; do not infer an H-052 or frontier
    disposition from the missing result.
---
# Session 065 — BC-108 `n = 17` Certificate

## Frozen W6 Contract

### Claim and Fixture

The frozen claim is H-052 verbatim:

> The fixed retained Massaccesi `n = 17`, `L = 4.5058` certificate agrees on every
> preregistered exact invariant when evaluated by an independently written exact
> accumulation implementation that does not copy the published two-dimensional
> difference-array sweep.

Treat `L = 4.5058` as the exact rational `22529/5000`. The retained fixture is the
Massaccesi source snapshot and normalized verifier under
`packing/resources/web/n17-lower-bounds-2026/`. The verifier file was hashed as opaque
input during this cell; it was not opened, imported, or executed.

| Frozen input | SHA-256 |
| --- | --- |
| `README.md` | `b48c0c31cf62366d44cd12f02cf321dd38b5a23391caec95f04445938e0b3d75` |
| `massaccesi-linear-programming.html` | `cdd27897f4f6c3b83835d59a317b3248b4f94b888f8568b740c778524a11f177` |
| `massaccesi-lower-bound-4_5058.html` | `7dffb6e6e6cbff0ac2e887ca445b45f46c95055718219f7229d1c8cb06f84514` |
| `massaccesi-verify-n17-lower-bound-4_5058.py` | `04531a54da9a654f2318401aff43222daf721bd99e948b2491f91c05bd0b5d3f` |
| Historical target-blind W3 snapshot of `H-052-n17-independent-certificate-agreement.md` | `e5f2a976821e416d877beac63cd67dd4a741bce354d7004aa04c92b02de620d6` |

The retained metadata fixes 168 weighted atoms on a 29 by 29 grid, total mass
`9744/576`, 181 rational direction cells, and global checked minimum `576/576`. The
unchanged-input binding applies to the four retained-source rows and these values.
The H-052 row is only the historical W3 contract snapshot; W7 necessarily changes that
record when it binds the instrument and readiness evidence, so its digest is exempt from
the retained-source unchanged binding.

### Determination

The result shape is `determination`. For each of the 181 ordered rational directions,
both implementations must emit a canonical row containing the exact direction, ordered
event-axis hashes and counts, number of reduced event cells, exact cell minimum, and a
deterministically tie-broken minimizing cell.
The aggregate manifest must also contain:

- the certificate file hash, atom count, grid dimensions, ordered atom-data hash, and
  exact total mass;
- the ordered direction-net hash and count;
- exact per-direction event-cell rows and minima;
- exact global minimum; and
- Boolean decisions, with exact operands, for every declared angle-cover,
  shrunken-square-containment, and strict-scaling precondition.

The acceptance threshold is exact equality on every manifest field, total mass
`9744/576`, global minimum `576/576`, and rejection of every frozen mutation.
A reproducible exact disagreement rejects H-052 only after both implementations pass
their known-answer, provenance, independence, and mutation guards.
Any failed guard is a typed premeasurement stop or invalid-instrument result, not a
mathematical disagreement.

### Lane Budget and Cells

The lane budget is 130 minutes.
The clock started at `2026-09-01T09:01:55Z` and ends at `2026-09-01T11:11:55Z`.

| Offset and UTC interval | Minutes | Workflow | Frozen work |
| --- | ---: | --- | --- |
| 0–15, 09:01:55–09:16:55 | 15 | W3 | Freeze this contract without target access |
| 15–35, 09:16:55–09:36:55 | 20 | W7 | Build separate source-faithful and clean-room scalar interfaces without target execution |
| 35–55, 09:36:55–09:56:55 | 20 | W7 | Pass synthetic exact controls and mutations; complete the readiness handshake |
| 55–80, 09:56:55–10:21:55 | 25 | W6 | Execute the fixed target and compare the complete exact manifests |
| 80–100, 10:21:55–10:41:55 | 20 | W6 | Run the five frozen target mutations |
| 100–115, 10:41:55–10:56:55 | 15 | W6 | Run optimized-Python and retained source-defect controls |
| 115–130, 10:56:55–11:11:55 | 15 | W3 | Interpret shared assumptions, validate records, and hand off |

No later cell starts until the coordinator creates the exact H-052 experiment/result
preregistration and appends the next contemporaneous workflow phase to this session.

### Refusal Conditions

Stop before target measurement when any of these conditions holds:

- the target verifier, its output, or a derived target result is opened or executed
  before preregistration and instrument readiness;
- a retained fixture hash, atom count, grid dimension, direction count, or exact
  metadata constant differs from this contract;
- static fixture extraction cannot isolate certificate data without executing target
  code;
- the independent implementation imports, calls, translates, or is revised in response
  to the published difference-array control flow or target output;
- the source-faithful and independent paths cannot emit the same canonical manifest;
- a hand-checkable control fails, any required mutation is accepted, or optimized Python
  disables a required guard; or
- exact arithmetic, provenance, implementation independence, or the remaining lane
  deadline cannot be maintained.

After readiness, a target disagreement is retained with the first unequal manifest row,
exact operands, and smallest reproducing fixture.
Do not repair it against the target in place.
Route it to BC-116 for adjudication.

### Controls and Mutations

Before target access, both accumulation interfaces must pass a hand-computable synthetic
fixture with at least one interior cell, one atom exactly on each event-boundary
convention, two rational directions, and an exactly enumerated minimum.
The test owns its expected values; neither target path supplies them.

Freeze these mutations by deterministic rule and record the first rejecting guard:

1. **Atom:** remove the lexicographically first positive-weight atom; the atom-data
   hash, atom count, or total must reject it.
2. **Weight:** add `1/576` to that atom; the exact total and manifest must reject it.
3. **Direction cell:** remove the lexicographically last rational direction; the
   direction-net hash, count, or angle-cover precondition must reject it.
4. **Event boundary:** change the inclusive upper event convention to an exclusive one
   on the synthetic boundary fixture; its exact minimum must disagree with the frozen
   known answer.
5. **Scaling:** replace the retained exact internal side `2.9545` with the defective
   prose value `3.9545`; an exact shrink or scaling precondition must reject it.

The later source-defect controls separately exercise 28-interval versus `/29` grid
spacing and inclusive versus exclusive endpoint enumeration.
The optimized-Python control repeats the guard suite under `-O`; an assertion-only guard
makes the instrument invalid.

### Shared-Assumption Boundary

The two implementations deliberately share the retained certificate atoms and weights,
the rational direction net, exact geometry definitions, the reduction from continuous
translations to event cells, the angle-cover lemma, shrunken-square-containment lemma,
and strict-scaling argument.
They may also share the canonical manifest schema and exact-rational type.

Agreement therefore checks accumulation implementation, exact bookkeeping, and the
declared precondition calculations for this fixed fixture.
It does not independently prove the shared geometric reductions, authenticate the
original author’s derivation, establish a second proof method, authorize `4.5058` for
the frontier, transfer the value to `n = 18` or `n = 19`, or validate the LP generator.

## W7 Readiness

Artifact: `cases/n17_weighted_certificate/`, its focused test, exp-049 and H-052 now
bind the nonexecuting instrument and exact file hashes.

The post-W7 H-052 readiness revision is bound separately at
`156c0bbfaf8637e0a28077db541da2e8b2e34311fd3745b41292d899485f00b2`. This is a
readiness-record digest, not a retained-source fixture digest.

Result: Eleven focused tests pass; the production self-test passes with identical output
under normal and optimized project Python; Ruff and BasedPyright are clean; H-052 is
`instrument_ready: true`.

Guard: The clean-room accumulator froze at
`55d36239f1f7e860f059030d87f655d2ac0c82685d788b599a7dd23d33d18de0` before source
inspection, and the complete package hash manifest froze at
`309ec24158f73dd2e9b837c773b1e5c1642f357de5bdf73311b73232abdb6d54`; no target replay,
target-output read, sample, or result file exists.

Next: Return to the coordinator for an explicit W6 phase append and authorization; stop
at this boundary.

### Implementation-Independence Boundary

The clean-room path must be authored from this contract and synthetic fixtures before
the target algorithm or output is opened.
Freeze its file hash after the synthetic guard suite passes.
Subsequent target-informed edits to its accumulation logic require a typed independence
refusal and a new preregistration; repairs may not continue under the same
determination.

The independent path must not import or call the retained verifier, reuse its event
arrays, translate its sweep loops, or compare against target values during authorship.
It may consume only the frozen certificate-data manifest after a static extractor has
proved that extraction executes no target code.
The source-faithful adapter lives in a separate module and may be built only after the
independent module is hash-frozen.

### Proposed Instrument

Build a reusable package under `packing/cases/n17_weighted_certificate/` with four
seams: a nonexecuting static fixture extractor, a canonical exact manifest, a
source-faithful adapter, and an independent scalar accumulator.
The independent accumulator uses `fractions.Fraction`; for each rational direction it
constructs the ordered x- and y-event intervals, enumerates their Cartesian cells
directly, chooses a deterministic exact representative under the frozen boundary
convention, and sums every atom’s contribution by direct membership tests.
It must not use a two-dimensional difference array or prefix-sum sweep.

`packing/tests/test_n17_weighted_certificate.py` should own the synthetic known answers,
the five mutations, hash/provenance checks, an AST-level no-import/no-call guard against
the retained verifier, stable manifest serialization, and the `-O` replay.
Target execution becomes available only after these checks pass, the independent module
hash is recorded, H-052 is rebound to the implemented entry point, and the coordinator’s
preregistered experiment records readiness.

## W6 Checkpoint — 2026-09-01T10:21:55Z

Artifact: The sole authorized target process is PTY session 10924, started at
`2026-09-01T09:51:35Z` with the exact exp-049 command and still running silently after
30 minutes 20 seconds.

Result: The immutable result path is absent.
This checkpoint checked path presence only; it did not inspect target output.

Guard: No guard has fired.
The process has emitted no instrument stdout or error, and no rerun, signal, package
edit, test edit, hash change, or output inspection has occurred.

Next: Continue waiting on PTY session 10924 without intervention.
Report at process exit or `2026-09-01T10:41:55Z`, whichever comes first; the W6 hard
deadline remains `2026-09-01T10:56:55Z`.

## W6 Checkpoint — 2026-09-01T10:41:55Z

Artifact: The sole authorized target process remains PTY session 10924, running silently
for 50 minutes 20 seconds since `2026-09-01T09:51:35Z`.

Result: The immutable result path remains absent.
This checkpoint checked path presence only; it did not inspect target output.

Guard: No guard has fired.
The process has emitted no instrument stdout or error, and no rerun, signal, code edit,
test edit, hash change, control run, or output inspection has occurred.

Next: Keep PTY session 10924 alive without intervention until it exits or the exact W6
hard stop at `2026-09-01T10:56:55Z`. If it exits, hash the immutable JSON before
inspection.
If it remains live at the hard stop, report before taking any further action.

## W6 Timebox Stop

Artifact: The single registered exp-049 command ran from `2026-09-01T09:51:35Z` to the
declared hard stop at `2026-09-01T10:56:55Z`. One interrupt ended PTY session 10924 with
exit 130. Process-table checks then found neither the uv parent nor Python child
command.

Result: The 3920-second run emitted no canonical JSON, complete comparison, mutation
result or checkpoint.
The result path is absent.
This is a process determination of `no_progress`; it does not measure H-052’s agreement
criterion.

Guard: The target command ran exactly once.
No rerun, target-informed repair, package change, empty result file, hypothesis
disposition or frontier adoption occurred.
H-052 remains `instrument_ready: true`, and exp-049 remains `needs_review: true`.

Next: Final W3 must retain the frozen revision and no-checkpoint state, close BC-108 as
executed-unresolved, and route any newly timeboxed replay to BC-116.

## Final W3 — Executed Unresolved

Artifact: Exp-049 records the declared timebox, 3920 wall seconds, 65.33333333333333
agent minutes, the nonempty process determination, absent result and frozen resume
revision. Session-065 records the stopped W6 phase and this finalization handoff.

Result: H-052 is scientifically unresolved because no complete exact manifest comparison
exists. The lane produced a ready instrument and priced its current direct Cartesian
execution path, but it did not establish agreement, disagreement, certificate validity,
lower-bound adoption or transfer to another `n`.

Guard: Enforced softschema validation passes for both terminal records.
The result path remains absent, H-052 readiness remains true, exp-049 remains
review-pending, and no hypothesis or frontier state was changed.

Next: BC-108 is executed-unresolved.
Coordinator review applies the pending disposition; BC-116 owns any new timebox or
instrument-cost adjudication from the frozen revision.

## Target-Blind W3 Cell Ledger

- **Artifact:** Frozen H-052 contract in this session, with five retained hashes and a
  seven-cell 130-minute plan.
- **Result:** The target-blind W3 contract is complete; the target verifier remains
  unopened and unexecuted.
  Only the retained receipt metadata was read; no target-output artifact or live replay
  output was read.
- **Guard:** The three hashes declared by the source receipt match; future readiness
  requires synthetic known answers, provenance and independence checks, five mutations,
  and optimized-Python replay.
- **Next:** Return to the coordinator for serial H-052 experiment/result
  preregistration; stop here without entering W7 or W6.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
