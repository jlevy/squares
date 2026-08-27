---
title: session-032 — agenda-004 block 1, build the missing mutations
softschema:
  contract: packing.squares:AgentSession/v2
  schema: ../schemas/agent-session.schema.yaml
  envelope: session
  status: enforced
session:
  id: session-032
  title: Build exp-045's four missing pre-certificate mutations
  date: '2026-08-27'
  started_at: '2026-08-27T15:05:52-07:00'
  deadline_at: '2026-08-27T20:05:52-07:00'
  goal: >-
    Close BC-036 by raising the enforced pre-certificate mutation count from eight to the
    declared twelve, each new control exercising a proof invariant no existing mutation
    reaches, and without weakening any frozen criterion.
  workflow_phases:
  - workflow: pipeline-improvement
    recording: contemporaneous
    clock_role: work
    focus: correctness
    objective: >-
      Extend the `ProofInputs` mutation surface so four currently unreachable proof
      invariants each become reachable by one declared perturbation, and raise the
      enforced control count to twelve.
    status: completed
    entered_by: session_start
    switch_reason: null
    budget_minutes: 60
    started_at: '2026-08-27T15:05:52-07:00'
    deadline_at: '2026-08-27T16:05:52-07:00'
    expected_output: >-
      Twelve keyed mutations, each mapping to a distinct expected failure identifier, with
      the count guard raised from eight to twelve and exp-045's admission re-checked.
    validation_command: >-
      uv run --directory explorations/packing --frozen pytest -q
      tests/test_minus_w_scale.py tests/test_minus_w_owner4.py
    kill_condition: >-
      Stop on amending exp-045's declared twelve down to the implemented count, on a
      mutation whose expected failure identifier duplicates one already covered, on
      targeting `control.keys` or `control.identifiers` (which guard the mutation
      machinery itself and would be circular), on weakening any frozen criterion, or on
      generating target data.
    fallback: >-
      Retain whichever mutations are built with their exact coverage, leave the enforced
      count at its true value, and record the first invariant that cannot be reached by a
      declared perturbation.
    outcome: >-
      BC-036 is closed. The enforced pre-certificate mutation count is twelve, matching
      exp-045's declared twelve, and all twelve controls fire on twelve distinct expected
      failure identifiers. No frozen criterion was weakened and the declared twelve was
      never amended.
    evidence:
    - 'Four `ProofInputs` fields were added, one per new control: `geometry_separation_offset`, `scale_single_weight`, `weight_scale_offset` and `tilt_direction`.'
    - 'The shared identifier `certificate.acceleration_elimination` was split into `certificate.acceleration_correction` and `certificate.acceleration_farkas`, so each control matches only its own frozen identifier as the admission requires. This refines the failure vocabulary and changes nothing that is proved.'
    - >-
      Mode three needed a perturbation preserving the zero pose sum, because perturbing
      any single weight trips the correction check first. Scaling every weight by a
      positive factor preserves that sum by linearity while moving the side coefficient
      off the exact alpha, which reaches the Farkas identity check and nothing else.
    - 'Verified by direct call: twelve controls, twelve distinct expected identifiers, twelve passing, actual equal to expected in every case.'
    - Thirty-seven related minus-W and n=5 tests pass in 270 seconds; focused Ruff, formatting and BasedPyright are clean.
    - 'Admission conditions three and four now both hold: twelve mutations enforced against twelve declared, and thirteen keyed refusals against thirteen declared.'
    - The retired identifier is referenced nowhere in code, tests, atlas records or schemas; the only mentions are in this session's own narrative describing the state before the split.
    stop_reason: >-
      The declared output is complete and independently exercised inside the slice budget,
      and the two admission conditions this commitment owns are satisfied.
    next_action: >-
      Conditions five and six of exp-045's admission remain and belong to BC-037: retained
      generation and replay must agree, and an independent post-change audit must accept
      the complete instrument. Neither is target generation this commitment may perform.
  - workflow: pipeline-improvement
    recording: contemporaneous
    clock_role: work
    focus: correctness
    objective: >-
      Close BC-039 by regenerating the durable n=29 rational certificate at a deliberately
      chosen `rational_digits`, with the choice argued rather than maximized.
    status: completed
    entered_by: planned_checkpoint
    switch_reason: >-
      BC-036 is closed, and BC-039 is the independent second half of block one that does
      not depend on its outcome.
    budget_minutes: 30
    started_at: '2026-08-27T16:05:58-07:00'
    deadline_at: '2026-08-27T16:35:58-07:00'
    expected_output: >-
      A regenerated witness whose certificate metadata, the `E-n029-schadt-rational-upper`
      limitations text and both gated checker paths agree, with the chosen
      `rational_digits` and its reason recorded.
    validation_command: >-
      uv run --directory explorations/packing --frozen python -m
      devtools.check_rational_witness_independent
      witnesses/schadt-n029-2025-rational.yaml
    kill_condition: >-
      Stop on treating decimal precision as a certificate, on record-improvement,
      rigidity or optimality language, on accepting a witness the independent checker did
      not verify, or on maximizing `rational_digits` without arguing the tradeoff against
      artifact size.
    fallback: >-
      Leave the recorded witness unchanged and retain the measured tradeoff, rather than
      regenerating on an unargued parameter.
    outcome: >-
      BC-039 is closed. The durable certificate is regenerated at `rational_digits: 36`,
      the CLI default, and the argued reason is reproducibility rather than tightness. The
      claim boundary is unchanged: this remains an upper bound at a relaxed rational side,
      weaker than the reported record, certifying no source decimal and proving no
      optimality.
    evidence:
    - >-
      The size tradeoff does not arbitrate the choice. Artifact size grows linearly at
      about 1.4 kB per digit while the relaxation shrinks exponentially as 10^-(d-5), and
      with 4.46 MiB of mutation-snapshot headroom even sixty digits costs sixty kB. Size
      is not a binding constraint, and the relaxation has no minimum on this route, so the
      choice needed a non-numeric reason.
    - >-
      That reason is a reproducibility defect. `frontier/n-029.md` described the artifact
      as the output of "the generic promotion command", but the recorded witness carried
      `rational_digits: 16` while the CLI default is 36. Running the documented command
      did not reproduce the recorded artifact.
    - Regenerating at the default closes that gap, and the twenty-orders-tighter bound is a side effect of the choice rather than its justification.
    - 'Measured: 22,890 bytes at d=16 against 50,319 at d=36; relaxation 4.933898e-11 against 4.933884e-31, exactly 1e20 tighter.'
    - 'Both gated checker paths accept the regenerated witness, the independent exact checker over 29 squares and 406 pairs and the generic verifier, and the certificate metadata now records `rational_digits: 36` with its matching dilation.'
    - Six coordinated references were reconciled across the case record, the evidence limitations, the synopsis and two generated views; the terminal session records that quote the old figure were left as recorded.
    stop_reason: >-
      The regeneration, both checker paths, and every durable reference agree inside the
      slice budget, and the choice is recorded with a reason that does not appeal to the
      number itself.
    next_action: >-
      Block one is complete. Block two runs BC-037: exp-045 to a terminal H-023
      disposition, halting at `needs_review` rather than writing an accepting verdict.
  primary_bead: think-oyn9
  status: completed
  budget:
    wall_minutes: 300
    slice_minutes: 60
    orientation_minutes: 15
    finalization_minutes: 30
  stop_conditions:
  - The declared twelve is never amended downward to match what was built.
  - No mutation may share an expected failure identifier with another.
  - The full gate must be green before the block boundary closes.
  - A quota or API failure halts the run; it is not retried on a timer.
  progress:
    metric: enforced pre-certificate mutation count against exp-045's declared twelve
    before: >-
      Eight mutations are implemented and hard-enforced against a declared twelve, and
      BC-029 is blocked at execution admission because of the gap.
    after: >-
      Twelve mutations are enforced on twelve distinct identifiers, so exp-045's admission
      conditions three and four both hold and BC-037 is unblocked. The n=29 certificate is
      regenerated at the tool's default precision, closing a reproducibility gap between
      the documented command and the recorded artifact. Both block-one commitments closed
      inside their slices, and no scientific claim widened.
  delegations: []
  outputs:
  - SYNOPSIS.md
  - cases/n5/minus_w_obstruction.py
  - campaign/agendas/agenda-004-guard-repair-and-instrument-unblock.md
  - campaign/agent-sessions/session-032-block1-missing-mutations.md
  - frontier/evidence.yaml
  - frontier/n-029.md
  - witnesses/schadt-n029-2025-rational.yaml
  checks:
  - >-
    Orientation inventory before declaring this slice: the proof core raises 17 distinct
    failure identifiers and exactly 8 are exercised by mutations. Of the 9 uncovered,
    `control.keys` and `control.identifiers` guard the mutation machinery itself and
    cannot be mutation targets without circularity, leaving seven genuine candidates:
    `source.geometry`, `source.first_order`, `certificate.acceleration_elimination`,
    `baseline.obstruction`, `scope.refusal_set`, `source.replay` and `replay.drift`.
  - >-
    That retires BC-036's declared risk. The four required controls exist to be built, so
    exp-045's twelve was not aspirational and no preregistration amendment is warranted.
  - 'The mutation surface is narrow by construction: `ProofInputs` carries exactly eight fields, one per existing control, so each new control needs one new field.'
  - >-
    Correction to the first inventory, found by tracing the call graph rather than
    grepping: only three of the seven candidates are reachable. Mutations run through
    `proof_core`, and `source.replay`, `baseline.obstruction`, `scope.refusal_set` and
    `replay.drift` are raised in `source_bindings`, `build_result` and `main`, all outside
    its call graph. A `ProofInputs` perturbation can never reach them.
  - >-
    `evaluate_necessary_inequality:264` is unreachable on the proof path. `selected_rows`
    filters `tangent_inventory.matrix`, so its rows are a subset of the `all_rows` that
    `minus_w_cases:338` already tests the direction against; a direction passing 338
    necessarily passes 264. It is a defensive guard for direct callers, not a reachable
    proof invariant.
  - >-
    That leaves exactly four distinct reachable failure modes and no slack: geometry
    constant drift at `geometry_constants:246`, a retained correction coordinate at
    `acceleration_eliminator:206`, positive Farkas identity drift at
    `acceleration_eliminator:219`, and an active source row left by -W at
    `minus_w_cases:338`.
  - >-
    Two of those four share the identifier `certificate.acceleration_elimination`, so as
    the code stands two controls could not match only their own frozen failure identifier,
    which is what exp-045's admission requires. Splitting that identifier in two is a
    refinement of the failure vocabulary rather than a weakening of any criterion: it
    changes nothing that is proved and makes each mode separately identifiable.
  stop_reason: >-
    Both block-one commitments reached terminal state with their declared outputs
    exercised, and the block's checkpoint question is answered in the affirmative.
  next_action: >-
    Under BC-037 and think-1s0h, run exp-045 to a terminal H-023 disposition, recording
    `unresolved` with `needs_review` rather than an accepting verdict.
---
# Session 032 — Agenda-004 Block 1

The first block of the
[blocked agenda-004](../agendas/agenda-004-guard-repair-and-instrument-unblock.md) leads
with BC-036 because it is both the gate and the largest binary unknown: if four
genuinely distinct pre-certificate failure modes could not be defined, BC-037 and BC-038
would never run.

The orientation inventory settles that in the conservative direction.
Seven uncovered proof invariants exist, four are needed, and the two that cannot be used
are excluded for a stated reason rather than overlooked.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
