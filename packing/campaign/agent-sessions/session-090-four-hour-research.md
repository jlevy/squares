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
  resource_rollups:
  - packing/campaign/resource-usage/codex-task-tree-session-090.yaml
  goal: >-
    Execute the selected four-active-hour Agenda 024 allocation after PR 101 merged:
    one H-093 scalar attempt, complete-density verification controls, and
    continuous-angle certificate controls, with independent review and one
    integrated research PR. Select later slices from evidence and remaining cost.
  workflow_phases:
  - workflow: pipeline-improvement
    focus: correctness
    recording: contemporaneous
    clock_role: work
    objective: >-
      Build BC-243 exact facet controls and BC-255 closed-angle controls in parallel,
      while independently auditing and prospectively freezing BC-251's scalar run.
    bead: think-9qrx
    status: stopped
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
    outcome: >-
      The independent scalar audit passed; exp-116 is prospectively committed and
      all 31 record checks pass at 97ba816e. The density author completed 10 controls;
      independent review and angle controls continue on their original allocations.
    evidence: [packing/campaign/series/series-000-smoke-and-calibration/experiments/exp-116-h-093-scalar-61-16.md]
    stop_reason: The scalar is ready for its single invocation and the first density controls are complete.
    next_action: Launch exp116 once and complete the independently reviewed control checkpoint.
  - workflow: research-loop
    focus: insight
    recording: contemporaneous
    clock_role: work
    objective: Supervise the frozen scalar invocation and finish the two independent control-readiness decisions.
    commitment: BC-251
    bead: think-0za3
    status: stopped
    entered_by: evidence_checkpoint
    switch_reason: The prospective scalar protocol and unchanged instrument passed their launch guards.
    budget_minutes: 30
    started_at: '2026-09-07T00:46:18Z'
    deadline_at: '2026-09-07T01:16:18Z'
    expected_output: Retained scalar progress, independent control decisions, and a priced next instrument slice.
    validation_command: uv run --frozen --all-extras --group dev packing-ledger check
    kill_condition: A scientific guard fails, the scalar stops under its frozen rules, or the supervision slice ends.
    fallback: Preserve the bounded outcome and continue only separately selected work; never restart the scalar.
    outcome: Both first control kernels passed independent review and were committed as ea9d2898; the scalar remains active and unconverged.
    evidence: [packing/devtools/density_face_verifier.py, packing/devtools/angle_tile_certificate.py]
    stop_reason: The completed control reviews justify the next bounded instrument work.
    next_action: Finish the slab reader and build the algebraic source-control extension; preserve existing author and scalar caps.
  - workflow: pipeline-improvement
    focus: correctness
    recording: contemporaneous
    clock_role: work
    objective: Complete independent density coverage and the same-kernel algebraic angle source control while supervising exp-116.
    bead: think-9qrx
    status: in_progress
    entered_by: evidence_checkpoint
    switch_reason: Both first control kernels passed review; source binding audits identified the next concrete prerequisites.
    budget_minutes: 30
    started_at: '2026-09-07T01:03:19Z'
    deadline_at: '2026-09-07T01:33:19Z'
    expected_output: A reviewed complete slab kernel, an algebraic source-control disposition, and the first integrated PR checkpoint.
    validation_command: uv run --frozen --all-extras --group dev packing-validate --push
    kill_condition: An instrument premise fails or the bounded author allocation ends; no unresolved prerequisite authorizes target work.
    fallback: Retain the exact obligation and price only a changed continuation with independent work still active.
    outcome: null
    evidence: []
    stop_reason: null
    next_action: Publish the reviewed rational/facet checkpoint while the two disjoint instrument authors continue.
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
      PR 101 merged as 4d305597 with no file-tree difference from its validated head.
      H-093 is ready but unrun. Exp-113 leaves H-099 unresolved, exp-114 accepts only
      H-104's exact-angle auxiliaries, and exp-115 rejects only H-105's pair obstruction.
    after: null
  delegations:
  - task: BC243 / H099 complete facet-kernel controls; think-ejwh
    operator: Codex bound_lane_strategy, max mathematical reasoning
    status: completed
    recording: contemporaneous
    outcome: Exact facet kernel completed and independently reviewed; no target geometry loaded.
    evidence: [packing/tests/test_density_face_verifier.py]
    files: [packing/devtools/density_face_verifier.py, packing/tests/test_density_face_verifier.py]
    checks: [10 tests passed in 1.98s; 2.23s process wall and 2.16s CPU; Ruff and BasedPyright clean.]
    uncertainty: Complete source-distinct slab reader and target readiness remain separate work.
    elapsed_seconds: 706
    elapsed_quality: operator_reported_approximate
    next_action: Complete the separately commissioned slab kernel and its independent review.
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
    status: completed
    recording: contemporaneous
    outcome: Rational near-axis source/toy kernel completed; source binding and near-45-degree arithmetic remain absent.
    evidence: [packing/tests/test_angle_tile_certificate.py]
    files: [packing/devtools/angle_tile_certificate.py, packing/tests/test_angle_tile_certificate.py]
    checks: [8 tests passed in 0.06s; 0.40s process wall and 0.32s CPU; Ruff and BasedPyright clean.]
    uncertainty: A sufficient certificate may remain unresolved at interior polynomial zeros.
    elapsed_seconds: 757
    elapsed_quality: operator_reported_approximate
    next_action: Price the source-bound packet adapter; no target is authorized by these toy controls.
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
    status: completed
    recording: contemporaneous
    outcome: Source and locked-runtime inputs match 5267bd34; the exact family-file replay requirement was added before launch.
    evidence: [packing/campaign/series/series-000-smoke-and-calibration/experiments/exp-116-h-093-scalar-61-16.md]
    files: []
    checks: []
    uncertainty: Launch readiness is not convergence, a bound, or a family-ceiling result.
    elapsed_seconds: null
    elapsed_quality: unavailable
    next_action: Review the frozen density facet kernel independently.
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
  - task: Independent BC243 facet-kernel review; think-qbrc
    operator: Codex gpt6_coverage_audit, max mathematical reasoning
    status: completed
    recording: contemporaneous
    outcome: Control-only GO; complete facet argument is sound on validated PairFamily inputs. No target readiness accepted.
    evidence: [packing/devtools/density_face_verifier.py, packing/tests/test_density_face_verifier.py]
    files: []
    checks: [10 controls passed independently in 1.91s; 2.21s process wall and 2.12s CPU; existing malformed guard passed separately.]
    uncertainty: The complete slab reader and target binding are not reviewed by this control-only slice.
    elapsed_seconds: null
    elapsed_quality: unavailable
    next_action: Author the separately commissioned source-distinct slab kernel under think-w0nb.
    phase: 1
    budget_minutes: 15
    started_at: '2026-09-07T00:44:00Z'
    deadline_at: '2026-09-07T00:59:00Z'
    expected_output: Source-distinct mathematical assessment of facet completeness and excess-box soundness.
    validation_command: uv run --frozen --all-extras --group dev pytest tests/test_density_face_verifier.py
    kill_condition: A completeness premise fails or the review allocation ends.
    fallback: Return the exact defect and refuse target readiness.
    write_scope: [none; read-only review messages]
    excluded_commands: [target geometry, target measurements, file edits, git mutations, tbd mutations]
  - task: BC243 source-distinct slab-kernel controls; think-w0nb
    operator: Codex gpt6_coverage_audit, max mathematical reasoning
    status: in_progress
    recording: contemporaneous
    outcome: null
    evidence: []
    files: []
    checks: []
    uncertainty: Shared field and validated geometry foundations remain explicit; target binding is separate.
    elapsed_seconds: null
    elapsed_quality: unavailable
    next_action: Return complete vertical-event and open-band controls, then obtain independent review.
    phase: 2
    budget_minutes: 30
    started_at: '2026-09-07T00:54:43Z'
    deadline_at: '2026-09-07T01:16:18Z'
    expected_output: Independent exact slab kernel without facet incidence or probe imports.
    validation_command: uv run --frozen --all-extras --group dev pytest tests/test_density_slab_verifier.py
    kill_condition: A completeness premise fails or the control-only allocation ends.
    fallback: Preserve the incomplete obligation; do not run the target.
    write_scope: [packing/devtools/density_slab_verifier.py, packing/tests/test_density_slab_verifier.py]
    excluded_commands: [target geometry, target measurements, git mutations, tbd mutations, registry edits]
  - task: BC255 algebraic original-source clause control; think-ggs2
    operator: Codex structural_lane_strategy, max mathematical reasoning
    status: in_progress
    recording: contemporaneous
    outcome: null
    evidence: []
    files: []
    checks: []
    uncertainty: This is one original-source clause, not the seven-clause theorem or the prospective target.
    elapsed_seconds: null
    elapsed_quality: unavailable
    next_action: Preserve rational controls, implement quadratic coefficients, and attempt the frozen source control once after admission checks.
    phase: 3
    budget_minutes: 30
    started_at: '2026-09-07T01:03:56Z'
    deadline_at: '2026-09-07T01:33:19Z'
    expected_output: Same-kernel original axis-ten-cover control or its exact unresolved obstruction.
    validation_command: uv run --frozen --all-extras --group dev pytest tests/test_angle_tile_certificate.py tests/test_angle_source_control.py
    kill_condition: Source child exceeds 10 seconds, subdivision exceeds depth 10 or 256 leaves, a control fails, or the writer boundary arrives.
    fallback: Retain the bounded source outcome without a cap retry; no target is authorized.
    write_scope: [packing/devtools/angle_tile_certificate.py, packing/tests/test_angle_tile_certificate.py, packing/devtools/angle_source_control.py, packing/tests/test_angle_source_control.py]
    excluded_commands: [target geometry, target measurements, git mutations, tbd mutations, registry edits]
  outputs:
  - packing/campaign/agent-sessions/session-090-four-hour-research.md
  checks:
  - Fetched main 4d305597; PR 101 is merged and its tree is identical to validated 8f30be8c.
  - Isolated record checkpoint 97ba816e passed 31 of 66 steps in 20.72s; this is not the full gate.
  - Updated narrative-count negative control fired in 1.568s using a private source snapshot.
  - Root independently reviewed the rational angle kernel and replayed 8 controls; 0.05s pytest, 0.57s process wall, 0.42s CPU.
  stop_reason: null
  next_action: Supervise exp-116 handle 16679 without restarting; finish the slab reader and source-binding designs, then publish the first checkpoint.
---
# Session 090 — Four-Hour Research Block

The user authorized this continuation after merging PR 101.
[Agenda 024](../agendas/agenda-024-post-381-24h-portfolio.md#current-allocation) sets
the priorities; this session records execution under `think-9qrx`, within the research
program `think-jgnv`. The branch starts at merged main `4d305597`; no open PR head was
imported.

## Allocation and Checkpoints

The coordinator owns shared records, scientific acceptance, the single-CPU scalar
process, integration, and the successor PR. Two authors work on disjoint instruments;
the third worker performs independent review.
Mathematical judgment uses max reasoning; mechanical work may use high or xhigh.

| Active offset | Selected work and decision |
| --- | --- |
| 0–30 minutes | Audit and freeze BC-251; build BC-243 facet controls and BC-255 angle controls. No density or angle target runs. |
| 30–60 minutes | Independently review completed controls. Price the complete slab reader and full-domain angle step; allocate only work justified by those results. |
| 60–120 minutes | Continue the selected steps in slices of at most 30 minutes. Publish a two-hour evidence checkpoint; keep the scalar command’s unchanged 150-minute process cap. |
| 120–220 minutes | Exactify and independently verify a scalar candidate if one appears. Otherwise retain the bounded scalar outcome and finish the best-supported density or angle discriminator. |
| 220–240 minutes | Reconcile records, validation, costs, documentation decisions, and the next executable handoff on the same PR. |

BC-231’s larger adaptive build remains conditional.
Reserve roughly three quarters of the next available research capacity for
exactification of a promising bound.
The density candidate can establish a limitation of mass-eleven area-density
certificates at the exact Trump side; it does not directly improve a packing bound or
rule out below-Trump density methods.
A failed angle certificate remains unresolved unless a separate geometric counterexample
is verified.

## Clocks and Publication

Exp-116 launched once at `2026-09-07T00:46:18Z`; the retained execution handle is
`16679`. Its source worktree is `/private/tmp/squares-session090-scalar.rw72vS` at
`4d305597`. Stdout is `/private/tmp/squares-session090-exp116.stdout.log`; stderr and
the outer process timer are `/private/tmp/squares-session090-exp116.stderr.log`. The
four scientific output paths are frozen in the experiment.
Do not consume the state in the bridge while its writer is active.
The nominal 150-minute loop boundary is `03:16:18Z`, with any cooperative tail recorded
separately. No convergence or bound is claimed at launch.

The density author’s assigned interval ended at 00:43:08 UTC, 706 seconds after
dispatch; this is assigned elapsed time, not measured attention.
The angle author’s first reported execution observation was 00:36:44 UTC; its original
01:01:22 writer boundary was retained rather than extended.
Initial record-check failures were view/anchor drift and environment setup; all were
corrected before scalar launch, and none was a failed research experiment.

The first retained worker-start observation is `2026-09-07T00:31:22Z`. The timestamps
above are the uninterrupted schedule for this fresh allocation, not a reset of Session
089 or an earlier experiment.
Operational interruptions pause the affected active allocation and receive explicit
accounting entries. Assigned time, attentive agent time, and process wall/CPU costs are
distinct; unknown attention stays unknown.
The scalar invocation retains its own prospective process deadline.

Publish the first coherent checkpoint as one successor PR, then update it at block
boundaries. `think-qnyf` owns validation and publication; `think-qbrc` owns independent
review. The upstream monitor follows newly landed main without importing open heads.
Apply Practical Prose at documentation boundaries and the repository’s Flowmark hook; do
not add redundant checksum manifests or complicate the core 3.81 exposition for a
marginal improvement.

## First Control Checkpoint

The facet kernel passed source-distinct mathematical review: splitting every supporting
line at its exact crossings gives a segment on every positive-area face boundary.
Its two probes preserve every other line’s sign, so every adjacent open face is visited.
Coincident boundaries and contact-only excess do not create an area violation.
Duplicate placements are aliases with equal weights, not additive copies.
This result commissions the independent vertical-slab reader under `think-w0nb`; it does
not establish target readiness or settle H-099.

The rational angle kernel passed coordinator review and independent replay of all eight
controls. Its positive denominator clearing, affine center map, three-vertex point
assignments, complete binary triangulations, and contiguous closed angle slabs suffice
for the supplied near-axis test domains.
Near-45-degree arithmetic and frozen-source binding remain absent.
Interior tangencies may stay unresolved; a failed point assignment is not a geometric
counterexample. `think-26or` records this review.

The angle author stopped at 00:49:21 UTC, an observed author span of 757 seconds.
The prose-only editor stopped at 00:55:45 UTC after 118 assigned seconds.
`think-4tqm` prices source-bound adapters without loading target geometry: the angle
design starts at 00:54:49 UTC with a 01:04:49 boundary; the density design has its own
ten-minute limit. These readiness costs are not target-runtime measurements.

The slab author’s initial 30-minute deadline would have exceeded the enclosing
supervision phase. It was corrected to 01:16:18 UTC before that boundary, leaving 21
minutes 35 seconds from the observed start.
Any unfinished work needs a newly selected continuation; neither the phase nor a
scientific budget was extended.

The angle source audit identified a prerequisite: the original axis-ten-cover control
uses side $2+\tfrac43\sqrt2$, which the rational-only kernel cannot represent.
The side-two toy does not replace this source instance.
Price the algebraic extension and the same-kernel original-source clause before target
binding.
The original seven-clause theorem includes further localization and multiplicity
obligations and is not silently replaced by this one-clause control.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
