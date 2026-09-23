---
title: Session 154 — PR 221 and PR 222 frontier reconciliation
softschema:
  contract: packing.squares:AgentSession/v2
  schema: ../schemas/agent-session.schema.yaml
  envelope: session
  status: enforced
session:
  id: session-154
  title: PR 221 and PR 222 frontier reconciliation
  date: '2026-09-22'
  started_at: '2026-09-22T22:46:28.122Z'
  deadline_at: '2026-09-23T02:46:28.122Z'
  branch: codex/reconcile-pr-221-frontier
  resource_rollups:
  - packing/campaign/resource-usage/codex-task-tree-session-154.yaml
  - packing/campaign/resource-usage/codex-task-tree-session-154-takeover.yaml
  primary_bead: think-t30b
  status: completed
  ended_at: '2026-09-23T02:53:56Z'
  goal: >-
    Merge PR 221 at dfbb28dc48ab28924382b9409097d4fffdd36d3d atop PR 222 at
    7d4a755fc9ab42340d5d72e57f277a3cd0152450 while preserving every PR 221 research
    result and receipt, retaining the strongest justified current bounds from PR 222,
    and leaving an auditable disposition for every overlap or deferred finding.
  workflow_phases:
  - workflow: remediation
    focus: correctness
    recording: contemporaneous
    clock_role: work
    objective: >-
      Reconcile the two branches as one history, distinguish historical first-party
      results from current verified bounds, and regenerate every affected view from the
      merged record.
    status: completed
    entered_by: session_start
    switch_reason: null
    budget_minutes: 210
    started_at: '2026-09-22T22:46:28.122Z'
    deadline_at: '2026-09-23T02:16:28.122Z'
    expected_output: >-
      A merge commit retaining PR 221 ancestry, a complete identifier and result
      disposition, focused and records validation, and a reviewable pull request stacked
      on codex/pr-219-followup.
    validation_command: >-
      cd packing && uv run --frozen --all-extras --group dev packing-validate --records
    kill_condition: >-
      Any retained first-party result loses its frozen artifact or replay receipt, any
      current Frontier field regresses below PR 222, or any record claim exceeds its
      cited evidence.
    fallback: >-
      Stop publication, preserve the unresolved merge and failing receipt, and name the
      exact record or evidence conflict for a new reviewed slice.
    outcome: >-
      Reconciled PR 221 with the final PR 222 head without losing T-033, its three
      evidence records, or any frozen proof bytes. The merged record keeps T-024 at C3,
      assesses T-033's current role at S3 while preserving its historical S5
      registration, and retains PR 222's strict n11 bound and all twenty promoted case
      fields. Generated views remain pinned to their last data commit because the final
      PR 222 wording was already byte-identical in this branch's source record.
    evidence:
    - packing/frontier/results.yaml
    - packing/frontier/evidence.yaml
    - docs/project/reviews/review-2026-09-22-external-square-certificates-integration.md
    - packing/campaign/series/series-000-smoke-and-calibration/results/agenda-041/exp-226-n11-net2880-receipt.md
    stop_reason: >-
      The identifier crosswalk is complete, the exact PR 222 base is merged, the full
      five-job checkpoint passed on the pre-restack research head, and hosted validation
      on the restacked merge passed every substantive job. Its sole direct failure was
      the campaign guard correctly refusing this session after its declared deadline;
      this terminal record removes that final publication blocker.
    next_action: >-
      Render T-033's missing standalone claim document under think-vx26.
  budget:
    wall_minutes: 240
    slice_minutes: 30
    finalization_minutes: 30
  stop_conditions:
  - Preserve PR 221's T-033 identity, three evidence records, frozen certificate, limit record, receipt, and exact result.
  - Preserve PR 222's stronger current verified bounds and all twenty promoted case fields.
  - Do not repeat the 31-minute T-033 limit replay when the frozen source and limit-record identities are unchanged.
  - Do not publish until record, focused, and hosted validation cover the reconciled source.
  progress:
    metric: PR 221 findings with explicit retained, corrected, superseded, or deferred dispositions
    before: >-
      PR 221 and PR 222 diverged from b22c1436941fd7cc95193110f0ec4078ca4737eb and
      presented conflicting n11 current-bound prose, generated views, and atlas exports.
    after: >-
      PR 221's T-033 and three evidence records are retained with their exact artifacts
      and corrected current assurance/significance, while PR 222's strict n11 bound and
      all twenty case promotions remain the current Frontier state.
  delegations: []
  outputs:
  - packing/campaign/agent-sessions/session-154-pr221-pr222-reconciliation.md
  - packing/frontier/results.yaml
  - packing/frontier/evidence.yaml
  - packing/frontier/n-011.md
  - packing/frontier/RESULTS.md
  - packing/frontier/INVENTORY.md
  - packing/frontier/CERTIFICATE-REACH.md
  - packing/frontier/STATUS.md
  checks:
  - Identifier definitions compared on both tips against merge base b22c1436941fd7cc95193110f0ec4078ca4737eb; no cross-branch definition collision found.
  - The 1440- and 2880-step frozen certificates differ only in id, direction_steps, and provenance; all atoms, weights, shrink, and declared charge fields agree.
  - packing-validate --records passed every selected record check with two workers; the bead-tree check was omitted because the parallel native lane was already measuring the known worktree fallback.
  - pytest -n 2 tests/test_results_register.py tests/test_rung_figures.py tests/test_negative_controls.py passed 78 tests.
  - >-
    The first full atlas update reached raster export and failed because Cairo was not
    discoverable under DYLD_FALLBACK_LIBRARY_PATH=/opt/homebrew/lib. The retry first
    imported cairocffi and cairosvg successfully with the installed
    /opt/homebrew/opt/cairo/lib path, then updated all 324 witnesses, 324 house
    renderings, two composites, four PNG rasters, and two PDFs with two workers.
  - >-
    The pre-commit focused release/citation/atlas/register test set passed 203 of 204
    tests. The sole refusal was the intended byte-for-byte publication snapshot test,
    which compares the working SVG to HEAD and therefore cannot accept regenerated
    bytes before their pin commit. Its exact test is rerun after the commit.
  - The refused byte-for-byte poster snapshot test passed after commit 385a3f03e made the regenerated SVG the committed publication.
  - >-
    Interim lane-only cost receipt through 2026-09-22T23:27:00Z: 146 model responses,
    0.69 agent-hours, a 0.67-hour active-union and wall envelope, 81.6 seconds of
    parallel overlap, and 51,169 output tokens. The snapshot is incomplete while this
    session remains live, so these are lower bounds; shared root review and coordination
    are excluded from this branch declaration.
  - 'full gate: full at 852d70c42ab575d10408d495702919c10a2f3f69: passed'
  - >-
    Hosted
    checkpoint 35800270156 passed validate, exhaustive, slow-lane, screen, and macOS
    portability without repeating the unchanged T-033 proof replays.
  - >-
    The change-scoped local push gate on afcd75431 ran 1,975 reachable behavioral tests:
    1,972 passed and the three refusals were the sandbox denying `ps`; the local Ruff and
    BasedPyright executables were absent. The same exact merge head then passed hosted
    typecheck, both test shards, frontend, geometry, sweeps, macOS portability, PDF
    reproduction, pages accounting, and mergeability in runs 35811713856, 35811713822,
    and 35811711286. The validate job's only failure was the campaign record correctly
    reporting this in-progress session and workflow phase past their deadlines.
  - >-
    Final lane accounting uses two adjacent, explicitly attributed intervals. The
    original lane through 2026-09-23T02:24:33.584Z records 358 model responses, 3.03
    agent-hours, a 2.95-hour active union, 5.03 minutes of parallel overlap, and 84,705
    output tokens. The takeover through 2026-09-23T02:53:56Z records 72 model responses,
    0.49 agent-hours, a 0.49-hour active union, 15.63 seconds of overlap, and 14,138
    output tokens. Both snapshots retain a live-session tail, so every total is a lower
    bound through its named cutoff; work after the cutoffs and shared root review are not
    included.
  stop_reason: >-
    The reconciled branch preserves every approved PR 221 result and historical
    identifier, retains every stronger PR 222 current field, and has no remaining
    substantive validation failure. The only hosted refusal was this session's expired
    in-progress marker, which this closeout resolves.
  next_action: >-
    Render T-033's missing standalone claim document under think-vx26.
---
# Session 154: One Record from Two Valid Branches

The workflow entry point is W8 reconciliation.
PR 221 carries a new first-party result and its frozen evidence.
PR 222 carries a stronger external result and the current case state.
The merge keeps both facts and assigns each to the field it can support.

## Identifier inventory

The merge base is `b22c1436941fd7cc95193110f0ec4078ca4737eb`.

PR 221 adds one primary result, `T-033`, and three evidence definitions:

- `E-n011-threshold-net2880-certificate`
- `E-n011-threshold-net2880-interval-decision`
- `E-n011-threshold-net2880-dilation-limit`

It adds no session, agenda, experiment, exploration, defect, `R-NNN`, hypothesis, or
bounded-commitment definition.
`X-042`, `agenda-041`, `exp-226`, and `BC-373` already exist at the merge base; PR 221
extends their records.

PR 222 adds `session-152`, twelve external-evidence definitions, and two witness ids.
It adds no `T-NNN`, exploration, agenda, experiment, hypothesis, or bounded-commitment
definition. `D-490` is updated rather than allocated; both tips already carry the defect
namespace through `D-507`.

There is no cross-branch definition collision.
PR 221 keeps `T-033`; session 152 remains PR 222’s. Session 153 belongs to the parallel
native-verifier lane, and this reconciliation uses the reserved `session-154`.

## Disposition crosswalk

| PR 221 item | Disposition in the reconciliation |
| --- | --- |
| `T-033` exact result | Retained at `V4/C3` with its exact surd, source digest, controls, and artifacts. Its current significance is `S3`: it is substantive first-party method and calibration evidence, while the stronger verified `s(11) > 31/8` result now sets the current bound. Git retains PR 221’s earlier `S5` assessment. |
| Three `E-n011-threshold-net2880-*` records | Retained. Novelty is narrowed to the project-specific frozen 2880-step rung and exact fixed-core evaluation. The later Kleddamag source is named and supersedes any reading of these entries as the current public-bound advance. |
| 2880-step certificate and limit record | Retained byte-for-byte. Independent comparison confirms that the 1440- and 2880-step certificate records differ only in `id`, `direction_steps`, and `provenance.derivation`. The internal id remains frozen. |
| Full exp-226 gate and limit receipts | Retained without repeating the 40-minute certificate gate or 31-minute limit replay. The source and limit-record checks bind the preserved bytes. |
| `X-042` and exp-226 prose | Retained with dated reconciliation notes. Their first-party chronology stands; their former current-gap language is historical after the external intake. |
| Frontier procedure corrections | Retained, including the source-path requirement, provenance caveat, endpoint distinction, and the rule that the two source-certificate decisions do not raise the one-method derived corollary above C3. |
| `T-024` confirmation mismatch found by PR 221 | Corrected from C4 to C3. The source certificate reaches C4, but the derived dilation-limit claim has one load-bearing exact-algebraic decision and takes the minimum rung under `epistemics.md`. |
| Central-case significance calibration | T-033 is assessed at S3 for its current role as method and calibration evidence; Git preserves PR 221’s registration-time S5 rationale. `think-380b` owns the open rubric question for superseded central-case rungs, so this reconciliation does not silently rescore earlier results. |
| Independent interval decision of the dilation corollary | Retained as the explicit C4 route in T-024’s and T-033’s `next_rung`: decide the corollary itself by a method distinct from its exact-algebraic derivation. The existing exact and interval decisions of the source certificate do not satisfy that step. |
| Missing standalone T-033 claim document | Deferred to `think-vx26`. The register states the missing artifact and does not treat the exp-226 receipt as a standalone third-party claim package. |
| Hard-coded producer provenance | Deferred to `think-tzg7`. The retained bytes disclose that `derived_from` names the original certificate while the multiplier is relative to the 1440-step input. The frozen file is not rewritten. |
| Agenda-041 negative-control pruning | Merged with PR 222’s dependency-audit explanation. Linked receipts and registered artifacts return through the existing snapshot copy-back path; bulk numerical output remains pruned from each private worker. |
| PR 221 atlas exports | Superseded as current views because they embed the weaker 3.8269975 lower bound. PR 222’s atlas exports remain byte-for-byte current; adding a historical T result does not change their case-bound inputs. |
| README, synopsis, n11 case, and generated Frontier views | Reconciled so `31/8` remains the current verified lower bound and T-033 remains the stronger historical first-party rung. Generated views are rebuilt from the merged source records. |
| `BC-373` and `think-gvlg` | Completed by the retained T-033 registration and its qualifying full-gate evidence on the reconciled branch. Session 151 remains stopped as historical fact. |

## Bound relationship

T-033 proves `s(11) >= 955000*sqrt(2073600042893309449)/359341754646249 =
3.826997548829543624`. The result is exact and remains registered.

The current verified lower bound is the stronger strict result `s(11) > 31/8 = 3.875`.
The unchanged T-025/T-026/T-033 fixed-core family has refinement ceiling
`955000/249507 ≈ 3.82755`, already below `3.875`. Further net refinement alone cannot
improve the current global bound.
This says nothing about changed weights, sites, parent domains, or richer charge atoms.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
