---
title: session-090 — scalar, density, and restricted-angle research
softschema:
  contract: packing.squares:AgentSession/v2
  schema: ../schemas/agent-session.schema.yaml
  envelope: session
  status: enforced
session:
  id: session-090
  title: Scalar, density, and restricted-angle research
  date: '2026-09-07'
  started_at: '2026-09-07T00:31:22Z'
  deadline_at: '2026-09-07T04:31:22Z'
  branch: codex/post-381-four-hour-research
  goal: >-
    Execute the selected four-active-hour Agenda024 allocation after PR101 merged:
    one H093 scalar attempt, complete-density verification controls, and
    continuous-angle certificate controls, with independent review and one
    integrated research PR. Select later slices from evidence and remaining cost.
  workflow_phases:
  - workflow: pipeline-improvement
    focus: correctness
    recording: contemporaneous
    clock_role: work
    objective: >-
      Build BC243 exact facet controls and BC255 closed-angle controls in parallel,
      while independently auditing and prospectively freezing BC251's scalar run.
    bead: think-9qrx
    status: in_progress
    entered_by: session_start
    switch_reason: null
    budget_minutes: 30
    started_at: '2026-09-07T00:31:22Z'
    deadline_at: '2026-09-07T01:01:22Z'
    expected_output: >-
      Two bounded control packages, a scalar launch decision, measured command
      costs, independent review obligations, and a prospective target record.
    validation_command: uv run --frozen --all-extras --group dev packing-validate --records --jobs 3 --inner-jobs 1
    kill_condition: A missing proof premise or failed control blocks its target; the slice ends at its stated boundary.
    fallback: Preserve the exact gap, finish independent work already assigned, and price a changed next slice.
    outcome: null
    evidence: []
    stop_reason: null
    next_action: Review the scalar launch and freeze exp116 before running it once.
  primary_bead: think-9qrx
  status: in_progress
  budget:
    wall_minutes: 240
    checkpoint_minutes: 30
    slice_minutes: 30
    finalization_minutes: 20
  stop_conditions:
  - The user stops or redirects the work.
  - A scientific cell reaches its frozen acceptance, refusal, or process cap.
  - An external blocker prevents useful work on every selected lane.
  - Publish the four-active-hour checkpoint and its selected continuation without silently extending any scientific allocation.
  progress:
    metric: Independently reviewed mathematical evidence and instrument readiness for the three selected directions.
    before: >-
      PR101 merged as4d305597 with no file-tree difference from its validated head.
      H093 is ready but unrun. Exp113 leaves H099 unresolved, exp114 accepts only
      H104's exact-angle auxiliaries, and exp115 rejects only H105's pair obstruction.
    after: null
  delegations:
  - task: BC243 / H099 complete facet-kernel controls; think-ejwh
    operator: Codex bound_lane_strategy, max mathematical reasoning
    status: in_progress
    recording: contemporaneous
    outcome: null
    evidence: []
    files: []
    checks: []
    uncertainty: Complete source-distinct slab reader and target readiness remain separate work.
    elapsed_seconds: null
    elapsed_quality: unavailable
    next_action: Return the exact facet-control package and price the separate reader.
    phase: 1
    budget_minutes: 30
    started_at: '2026-09-07T00:31:22Z'
    deadline_at: '2026-09-07T01:01:22Z'
    expected_output: Complete facet probes on toy/source controls, tests, and explicit soundness obligations.
    validation_command: uv run --frozen --all-extras --group dev pytest tests/test_density_face_verifier.py
    kill_condition: A soundness premise fails or the control-only allocation ends.
    fallback: Retain the failing control and incomplete obligations; do not run the target.
    write_scope: [packing/devtools/density_face_verifier.py, packing/tests/test_density_face_verifier.py]
    excluded_commands: [target measurements, git mutations, tbd mutations, registry edits]
  - task: BC255 / H036 and H102 closed-angle controls; think-vttn
    operator: Codex structural_lane_strategy, max mathematical reasoning
    status: in_progress
    recording: contemporaneous
    outcome: null
    evidence: []
    files: []
    checks: []
    uncertainty: A sufficient certificate may remain unresolved at interior polynomial zeros.
    elapsed_seconds: null
    elapsed_quality: unavailable
    next_action: Return source/toy coverage controls and price the next full-domain auxiliary step.
    phase: 1
    budget_minutes: 30
    started_at: '2026-09-07T00:31:22Z'
    deadline_at: '2026-09-07T01:01:22Z'
    expected_output: Closed-triangle coverage and exact polynomial sign controls without a target verdict.
    validation_command: uv run --frozen --all-extras --group dev pytest tests/test_angle_tile_certificate.py
    kill_condition: A source premise fails or the bounded control allocation ends.
    fallback: Preserve an unresolved certificate obligation; failed assignment is not a geometric counterexample.
    write_scope: [packing/devtools/angle_tile_certificate.py, packing/tests/test_angle_tile_certificate.py]
    excluded_commands: [target measurements, git mutations, tbd mutations, registry edits]
  - task: Independent BC251 scalar launch audit; think-qbrc
    operator: Codex gpt6_coverage_audit, max mathematical reasoning
    status: in_progress
    recording: contemporaneous
    outcome: null
    evidence: []
    files: []
    checks: []
    uncertainty: No new target is authorized until the coordinator commits its prospective protocol.
    elapsed_seconds: null
    elapsed_quality: unavailable
    next_action: Return the exact invocation and launch decision, then rotate to source-distinct control review.
    phase: 1
    budget_minutes: 15
    started_at: '2026-09-07T00:31:22Z'
    deadline_at: '2026-09-07T00:46:22Z'
    expected_output: Read-only source comparison and complete scalar launch requirements.
    validation_command: git diff 5267bd34 HEAD -- packing/devtools/run_fractional_cutting.py packing/devtools/freeze_cutting_primal.py packing/src/sqpack/fractional
    kill_condition: A readiness premise fails or the review allocation ends.
    fallback: Name the exact blocker without running a target or replacing its recipe.
    write_scope: [none; read-only messages]
    excluded_commands: [target measurements, file edits, git mutations, tbd mutations]
  outputs:
  - packing/campaign/agent-sessions/session-090-four-hour-research.md
  checks:
  - Fetched main4d305597; PR101 is merged and its tree is identical to validated8f30be8c.
  stop_reason: null
  next_action: Freeze and launch BC251 once after independent review; integrate the two control slices and allocate their independent reviews.
---
# Session 090 — Four-Hour Research Block

The user authorized this continuation after merging PR101.
[Agenda024](../agendas/agenda-024-post-381-24h-portfolio.md#current-allocation) owns
priorities; this session records execution under `think-9qrx`, within the research
program `think-jgnv`.
The branch starts at merged main `4d305597`; no open PR head was imported.

## Allocation and Checkpoints

The coordinator owns shared records, scientific acceptance, the single-CPU scalar
process, integration, and the successor PR. Two authors work on disjoint instruments;
the third worker performs independent review. Mathematical judgment uses max reasoning;
mechanical work may use high or xhigh.

| Active offset | Selected work and decision |
| --- | --- |
| 0–30 minutes | Audit and freeze BC251; build BC243 facet controls and BC255 angle controls. No density or angle target runs. |
| 30–60 minutes | Independently review completed controls. Price the complete slab reader and full-domain angle step; allocate only work justified by those results. |
| 60–120 minutes | Continue the earned steps in slices of at most30minutes. Publish a two-hour evidence checkpoint; keep the scalar command's unchanged150-minute process cap. |
| 120–220 minutes | Exactify and independently verify a scalar candidate if one appears. Otherwise retain the bounded scalar outcome and finish the best-supported density or angle discriminator. |
| 220–240 minutes | Reconcile records, validation, costs, documentation decisions, and the next orchestratable handoff on the same PR. |

BC231's larger adaptive build remains conditional. A promising bound receives roughly
three quarters of the next available research capacity for exactification.
The density candidate can establish a limitation of mass-eleven area-density
certificates at the exact Trump side; it does not directly improve a packing bound or
rule out below-Trump density methods. A failed angle certificate remains unresolved
unless a separate geometric counterexample is verified.

## Clocks and Publication

The first retained worker-start observation is `2026-09-07T00:31:22Z`.
The timestamps above are the uninterrupted schedule for this fresh allocation, not a
reset of Session089 or an earlier experiment. Operational interruptions pause the
affected active allocation and receive explicit accounting entries. Assigned time,
attentive agent time, and process wall/CPU costs are distinct; unknown attention stays
unknown. The scalar invocation retains its own prospective process deadline.

Publish the first coherent checkpoint as one successor PR, then update it at block
boundaries. `think-qnyf` owns validation and publication; `think-qbrc` owns independent
review. The upstream monitor follows newly landed main without importing open heads.
Apply Practical Prose at documentation boundaries and the repository's Flowmark hook;
do not add redundant checksum manifests or complicate the core3.81 exposition for a
marginal improvement.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
