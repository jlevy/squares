---
title: session-016 — final-hour exact-instrument continuation
softschema:
  contract: packing.squares:AgentSession/v2
  schema: ../schemas/agent-session.schema.yaml
  envelope: session
  status: enforced
session:
  id: session-016
  title: Final-hour exact-instrument continuation
  date: '2026-08-25'
  started_at: '2026-08-25T19:08:08-07:00'
  deadline_at: '2026-08-25T20:08:08-07:00'
  goal: >-
    Preserve the last hour of the four-hour BC-010 loop after session 015 reaches its
    declared phase cap: use one bounded W7 slice to derive the remaining exact scale and
    mutation contract, then reserve thirty minutes for validation and handoff.
  workflow_phases:
  - workflow: pipeline-improvement
    recording: contemporaneous
    clock_role: work
    focus: insight
    objective: >-
      Derive a finite exact scale-routing and production-mutation design for the
      remaining exp-044 instrument boundary, using the accepted row, stress, and sheet
      helpers without implementing or measuring a pure -W target.
    status: in_progress
    entered_by: session_start
    switch_reason: null
    budget_minutes: 30
    started_at: '2026-08-25T19:08:08-07:00'
    deadline_at: '2026-08-25T19:38:08-07:00'
    expected_output: >-
      A source-bound scale case split, mutation-to-guard map, and exact implementation
      boundary retained in this session, or a smaller finite blocker list.
    validation_command: >-
      uv run --directory explorations/packing --frozen softschema validate
      campaign/agent-sessions/session-016-final-hour-continuation.md && uv run
      --directory explorations/packing --frozen packing-ledger check && git diff --check
    kill_condition: >-
      Stop on one assumed scale, copied target coefficient, mutation after certificate
      construction, scientific disposition, missing source identity, or at the phase
      deadline.
    fallback: >-
      Retain the unresolved scale branches, unguarded mutation, and exact next test in
      this session; begin finalization at its fixed absolute start without target work.
    outcome: null
    evidence:
    - >-
      Published checkpoint 8ee367b provides the accepted row, normalized-stress, and
      formula-derived sheet substrate from which the remaining contract can be audited.
    - >-
      Independent scale derivation identifies three bounded symbolic-beta records and
      two unbounded sign records, with exact tied-row gradient and cusp identities.
    - >-
      Independent mutation and scope audits retain the twelve production entry points,
      identify the missing guards, and accept exp-044 as coherent but terminal.
    stop_reason: null
    next_action: >-
      Apply the repository-only portability audit, validate and publish the retained
      design, and stop for finalization no later than 19:38:08-07:00.
  primary_bead: think-1s0h
  status: in_progress
  budget:
    wall_minutes: 60
    max_cycles: 2
    checkpoint_minutes: 20
    slice_minutes: 30
    finalization_minutes: 30
  stop_conditions:
  - The finalization phase begins at 19:38:08-07:00.
  - Two phases open, including finalization.
  - The scale or mutation design would require a scientific target execution.
  - A clean committed checkpoint and exact repository handoff cannot be preserved.
  progress:
    metric: exact pure -W instrument blockers reduced before finalization
    before: >-
      Exact production row jets, normalized nine-row stresses, and the exp-034 positive
      sheet control are accepted. Scale routing, production mutations, and all target
      dispositions remain open; exp-044 is terminal with no result JSON.
    after: null
  delegations:
  - task: Derive the exact finite owner-3 scale-routing contract from production helpers.
    operator: /root/r4_derivation
    status: completed
    recording: contemporaneous
    outcome: >-
      Derived the exact five-record split, formal-real bounded representation, all
      fifteen ordinary cancellation columns, and two source-derived unbounded cusp
      coefficients without a target disposition.
    evidence:
    - >-
      The tied production gradients give b_plus=1/4-alpha/2 and
      b_minus=5/4-alpha/2 under d_beta=e_theta3.
    files: []
    checks:
    - Read-only source, row-jet, stress, and exp-044 reconciliation.
    uncertainty: A successor must freeze the record keys before implementation.
    elapsed_seconds: null
    elapsed_quality: unavailable
    next_action: Implement only after a successor preregisters the retained record contract.
    phase: 1
  - task: Map all frozen mutations and refusals to real production guards.
    operator: /root/r5_derivation
    status: completed
    recording: contemporaneous
    outcome: >-
      Mapped all twelve identifiers to production entry points, separated covered,
      partial, and missing guards, and rejected sentinel, post-result, and broad-catch
      controls in the predecessor draft.
    evidence:
    - >-
      Five production guards are missing; the other seams still need exact typed driver
      translation and fresh certificate receipts.
    files: []
    checks:
    - Read-only mutation-by-mutation audit against exp-044 and current helper tests.
    uncertainty: No target-level integration driver exists yet.
    elapsed_seconds: null
    elapsed_quality: unavailable
    next_action: Use the retained table as the successor's preregistered control contract.
    phase: 1
  - task: Audit the scale and mutation boundary for soundness and implementability.
    operator: /root/r4_r5_scope_audit
    status: completed
    recording: contemporaneous
    outcome: >-
      Accepted exp-044's criterion as coherent and implementable from repository state,
      while requiring a new monotonic experiment because exp-044 is terminal.
    evidence:
    - >-
      The accepted row, stress, and sheet helpers are sufficient substrate; the old
      obstruction draft remains inadmissible because it hand-builds formulas, copies
      predecessor constants, asserts scale exhaustion, and has only eight controls.
    files: []
    checks:
    - Independent read-only ACCEPT with a finite implementation and evidence list.
    uncertainty: No scientific target or disposition was evaluated.
    elapsed_seconds: null
    elapsed_quality: unavailable
    next_action: Require post-change review before any successor target run.
    phase: 1
  outputs:
  - campaign/agent-sessions/session-016-final-hour-continuation.md
  checks:
  - Session 015 stopped at its declared eight-phase cap with checkpoint 8ee367b pushed.
  - >-
    A read-only exact diagnostic reproduces the two owner-3 tied-row theta3 gradients
    `1/4-alpha/2` and `5/4-alpha/2` from production jets.
  - >-
    Softschema, generated-ledger freshness, campaign-record validation, and git diff
    checks pass with sixteen sessions and forty-four rounds.
  stop_reason: null
  next_action: >-
    Under think-1s0h and BC-010, finish only the active W7 scale-and-mutation design
    phase, then enter finalization at 19:38:08-07:00.
---
# Session 016 — Final-Hour Exact-Instrument Continuation

Session 015 used its eighth declared phase after publishing the reviewed exact row,
stress, and sheet helpers.
This explicit continuation preserves the original four-hour deadline without weakening
that cap or relying on a controller’s private memory.

## Fresh-Agent Resume

The authoritative branch is `origin/codex/packing-4h-research-loop-2026-08-25`;
checkpoint `f35e60b` contains the latest retained design, while `8ee367b` is the
accepted helper-substrate checkpoint.
Fetch and switch to that branch, then read:

1. [`session-015`](session-015-four-hour-r4-r5-loop.md) for the complete prior phase and
   audit history.
2. The terminal
   [`exp-044`](../series/series-000-smoke-and-calibration/experiments/exp-044-h-023-n5-minus-w-row-jets.md)
   for the frozen target boundary and unimplemented obligations.
3. [`minus_w_row_jets.py`](../../cases/n5/minus_w_row_jets.py),
   [`minus_w_stress.py`](../../cases/n5/minus_w_stress.py), and
   [`minus_w_sheet.py`](../../cases/n5/minus_w_sheet.py) with their focused tests.
4. [`H-023`](../hypotheses/H-023-n5-terminal-connectivity.md), `BC-010` in
   [`agenda-001`](../agendas/agenda-001-basin-confidence-ladder.md), and the owning bead
   `think-1s0h` for the wider dependency state.

From the repository root, verify the checkout before writing:

```shell
git fetch origin codex/packing-4h-research-loop-2026-08-25
git switch codex/packing-4h-research-loop-2026-08-25 2>/dev/null || \
  git switch --track -c codex/packing-4h-research-loop-2026-08-25 \
  origin/codex/packing-4h-research-loop-2026-08-25
git pull --ff-only
tbd prime
date -Iseconds
git status --short --branch
tbd show think-1s0h --max-lines 260
uv run --directory explorations/packing --frozen packing-ledger check
```

Before 19:38:08-07:00, continue only the declared scale-and-mutation design.
At or after 19:38:08-07:00, open or continue only the finalization phase.
At or after 20:08:08-07:00, stop all substantive work and preserve the terminal records,
validation receipt, pushed commit, synced bead note, and exact next action.

Do not run a pure `-W` target, create a result JSON, infer an obstruction, or launch the
generic numerical campaign.
A native goal, heartbeat, chat history, or Codex memory may wake an agent, but none is
part of the scientific state.

## Retained W7 Design

This section is an implementation handoff, not a result or an amendment to exp-044.
Exp-044 remains terminal unresolved.
A successor criterion must freeze the names and failure identifiers below before target
implementation or measurement.

### Five exact owner-3 scale records

Use `delta = theta3 - theta4`, pass to a sign-stable subsequence, and represent the
bounded limit symbolically.
The exact record set is:

| Key | Regime | Sign-decisive tied row |
| --- | --- | --- |
| `bounded_beta_negative` | `abs(delta)/t^2` bounded and `beta < 0` | `contact:3-4:owner3:a+:square4-feature-1` |
| `bounded_beta_zero` | `abs(delta)/t^2` bounded and `beta = 0` | both tied rows |
| `bounded_beta_positive` | `abs(delta)/t^2` bounded and `beta > 0` | `contact:3-4:owner3:a+:square4-feature+1` |
| `unbounded_delta_negative` | `abs(delta)/t^2 -> infinity` and `delta < 0` | `contact:3-4:owner3:a+:square4-feature-1` |
| `unbounded_delta_positive` | `abs(delta)/t^2 -> infinity` and `delta > 0` | `contact:3-4:owner3:a+:square4-feature+1` |

Require this exact five-key set separately for each `A`, `interior`, and `B` owner-3
stratum, for an exact fifteen-record Cartesian inventory.
Every record retains the full normalized nine-row stress, including both tied rows and
both weights.
The last column identifies only the row whose cusp coefficient decides that
sign case; it never removes the other tied row.

The bounded record uses a formal affine real, never a sampled value or a `FieldElement`
stand-in:

```text
P(a, beta) = C + sum(G_j * a_j, j=0..14) + B * beta
B = G dot d_beta
d_beta = e_theta3
```

The canonical section has `dtheta3 - dtheta4 = 1`. Retain all fifteen `G_j`, derive them
from the normalized production stress, and require every `G_j` and `B` to be exact zero
before checking the sign of `C`. This proves the statement for arbitrary real `beta`;
sampling negative, zero, and positive field values does not.

For the unbounded records, derive the following values from source centers and the two
production tied-row gradients:

```text
tau = (p4 - p2) dot (-alpha/2, alpha/2) = alpha/2 - 3/4
b_plus  = grad(g_plus)  dot d_beta = 1/4 - alpha/2
b_minus = grad(g_minus) dot d_beta = 5/4 - alpha/2
h = (b_minus - b_plus)/2 = 1/2
kappa_positive = b_plus = -(h + tau) < 0
kappa_negative = -b_minus = -(h - tau) < 0
```

The router must verify these identities from the current row jets, not store their
right-hand constants.
It then retains the formal bounded polynomial, the two tied labels and gradients, the
source-derived `tau`, the two exact cusp coefficients, and exact five-key equality.
Each unbounded record also retains nuisance-column cancellation and the limits
`t^2/abs(delta) -> 0`, `t*abs(delta)/abs(delta) -> 0`, and `delta^2/abs(delta) -> 0`.
Its return type contains proof data only; it does not choose an obstruction,
sign-symmetry, or H-023 disposition.

### Mutation-to-production-guard map

Every control changes an input before rebuilding a fresh certificate.
A driver may map a helper failure to the frozen identifier only by matching the exact
exception type and specific message; a broad exception catcher, altered completed
result, or sentinel flag is invalid.

| Frozen identifier | Current coverage | Required production entry and guard |
| --- | --- | --- |
| `source.minus_w` | Partial | Apply one indexed coordinate override before exact equality with all fifteen coordinates of regenerated `-W`. |
| `source.strata` | Partial | Require exact `A`, `interior`, and `B` key equality before any case certificate. |
| `source.owner_exhaustion` | Partial | Require both owners and exact six-case key equality before disposition. |
| `source.tied_rows` | Partial | Remove one actual row after `owner_row_jets` and before weights; translate only the named missing-label inventory failure. |
| `jet.center_axis_cross` | Missing | Mutate one designated nonzero symmetric center-angle Hessian entry before substitution and validate that production entry independently. |
| `jet.correction_unused` | Missing | Keep declared and applied corrections separate; verify every row equals `gradient dot declared_correction + velocity_curvature`. |
| `jet.absolute_branch` | Partial | Override one strict nonzero SAT feature sign before `sat_gap`; require its existing exact sign-disagreement failure. |
| `jet.curvature_homogeneity` | Missing | Evaluate zero-correction `W` and `2W` through production stress and require a nonzero `C(2W) = 4 C(W)` before certificate construction. |
| `certificate.weighted_curvature` | Covered | Perturb one real weight through `weight_adjustments` and translate only the exact combined-gradient-cancellation failure. |
| `control.sheet_witness` | Covered by helper, missing driver | Require the good formula-derived path to pass first; run the `-1/2` correction through the same 17-row evaluator and retain its named negative tight row. |
| `certificate.scale_exhaustion` | Missing | Delete one real handler from the exact five-key map and reject before any case disposition. |
| `scope.overclaim` | Missing | Insert a mixed or component claim into the actual emitted claim map and reject by exact allowed-key and refusal-record validation. |

The thirteen refusal names from exp-044 must be dictionary keys, each with its own
`status: refused` record and claim-specific reason.
A list plus `all_refused: true` does not satisfy that contract.
The exp-036 `+W` fixture must also run through the same source, row, stress, scale, and
validation path and reach its required positive-control outcome; asserted source
metadata is not a fixture.

### Successor implementation order

1. Preregister
   `campaign/series/series-000-smoke-and-calibration/experiments/exp-045-h-023-n5-minus-w-scale-and-controls.md`
   before implementation.
   It freezes the five scale keys, formal-real record shape, exact helper-to-identifier
   mappings, thirteen refusal-record shapes, and valid baseline disposition routing.
2. Implement the scale-only proof data in `cases/n5/minus_w_scale.py` and
   `tests/test_minus_w_scale.py`.
3. Replace the hand-formula draft in
   [`minus_w_obstruction.py`](../../cases/n5/minus_w_obstruction.py) with a case builder
   that consumes the accepted helpers and scale router; add
   `tests/test_minus_w_obstruction.py`. Mutation seams live on source inputs or
   production intermediates, never on completed certificates.
4. Implement the missing production guards and partial seams above with focused negative
   controls. Run a valid baseline of any scientific disposition and the same-builder
   exp-036 positive fixture before the twelve mutations.
5. Obtain independent post-change acceptance before any target command or result JSON.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
