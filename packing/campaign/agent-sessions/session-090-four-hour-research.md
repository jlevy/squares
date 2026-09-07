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
    status: stopped
    entered_by: evidence_checkpoint
    switch_reason: Both first control kernels passed review; source binding audits identified the next concrete prerequisites.
    budget_minutes: 30
    started_at: '2026-09-07T01:03:19Z'
    deadline_at: '2026-09-07T01:33:19Z'
    expected_output: A reviewed complete slab kernel, an algebraic source-control disposition, and the first integrated PR checkpoint.
    validation_command: uv run --frozen --all-extras --group dev packing-validate --push
    kill_condition: An instrument premise fails or the bounded author allocation ends; no unresolved prerequisite authorizes target work.
    fallback: Retain the exact obligation and price only a changed continuation with independent work still active.
    outcome: Slab coverage passed independent review. The quadratic source attempt hit its frozen leaf cap; independent review accepted its unresolved scope. Both are committed as 2ded0b4e.
    evidence: [packing/devtools/density_slab_verifier.py, packing/campaign/series/series-000-smoke-and-calibration/results/agenda-026/bc-255-angle-source-control.json]
    stop_reason: The source outcome and hand-derived alternative justify a changed root representation, not a binary-cap retry.
    next_action: Preserve the density adapter's original writer cap; commission a distinct grid-source control and source-distinct reader.
  - workflow: pipeline-improvement
    focus: correctness
    recording: contemporaneous
    clock_role: work
    objective: Implement the changed 6x3 original-source mesh and independent source-only reader while density adapters and exp-116 continue.
    bead: think-ibdk
    status: stopped
    entered_by: evidence_checkpoint
    switch_reason: The original binary source attempt is frozen unresolved; an exact hand-derived grid changes the certificate representation.
    budget_minutes: 30
    started_at: '2026-09-07T01:26:36Z'
    deadline_at: '2026-09-07T01:56:36Z'
    expected_output: One changed-representation source control, independent source-only replay, and a scoped readiness decision.
    validation_command: uv run --frozen --all-extras --group dev packing-validate --push
    kill_condition: Source producer or reader exceeds its separately frozen ten-second cap, a premise fails, or the author/review slice ends.
    fallback: Retain the precise unresolved result; do not retry the original binary cap or authorize the target.
    outcome: The changed angle source mesh and independent corner reader pass. Original density source passes both routes; uniform facet control times out at60seconds and has no reader invocation.
    evidence: [packing/devtools/angle_grid_source_control.py, packing/devtools/check_angle_grid_source_control.py]
    stop_reason: Source dispositions identify a density arithmetic bottleneck and permit the next continuous-angle instrument slice.
    next_action: Cache repeated exact clearance inverses and independently disposition the completed scalar; no unchanged source retry.
  - workflow: pipeline-improvement
    focus: efficiency
    recording: contemporaneous
    clock_role: work
    objective: Reduce repeated exact clearance inversions, build the continuous near-axis adapter, and review the terminal scalar evidence.
    bead: think-063l
    status: stopped
    entered_by: evidence_checkpoint
    switch_reason: The uniform density source exceeded its fixed cap; static assessment identified repeated field inversions without changing geometry or the proof.
    budget_minutes: 30
    started_at: '2026-09-07T01:54:24Z'
    deadline_at: '2026-09-07T02:24:24Z'
    expected_output: An independently reviewed local arithmetic cache, source-bound angle controls, and a scoped scalar disposition.
    validation_command: uv run --frozen --all-extras --group dev packing-validate --push
    kill_condition: A theorem-preservation premise fails or the bounded author/review slice ends; targets need separate prospective authority.
    fallback: Keep the measured source timeout and scalar outcome; price only a changed next discriminator.
    outcome: Scalar disposition, cache and continuous producer review completed. Cached original source and replay passed; remaining worker reports were interrupted and retained files require recovery review.
    evidence: [packing/campaign/series/series-000-smoke-and-calibration/experiments/exp-116-h-093-scalar-61-16.md, packing/devtools/angle_near_axis_control.py]
    stop_reason: At02:22:33UTC the worker tree was empty after operational handoff; temporary source checkouts had disappeared.
    next_action: Recover retained evidence without repeating completed commands; independently review the unfinished reader and finish only the unstarted uniform control.
  - workflow: pipeline-improvement
    focus: correctness
    recording: contemporaneous
    clock_role: work
    objective: Recover interrupted worker evidence, finish independent angle readiness and publish the integrated checkpoint.
    bead: think-hbni
    status: stopped
    entered_by: evidence_checkpoint
    switch_reason: Retained files survived the operational interruption, but worker completion reports and temporary checkouts did not.
    budget_minutes: 30
    started_at: '2026-09-07T02:23:47Z'
    deadline_at: '2026-09-07T02:53:47Z'
    expected_output: Independent reader disposition, remaining changed-code source outcome, current records and a pushed checkpoint with validation in flight.
    validation_command: uv run --frozen --all-extras --group dev packing-validate --push
    kill_condition: A readiness premise fails, a frozen process cap expires, or the bounded recovery slice ends.
    fallback: Publish exact unresolved obligations without restarting a completed experiment or extending a scientific cap.
    outcome: H106 passed its sole producer and independent exact reader; scalar disposition and source outcomes are retained. Checkpoint2707ea39 is pushed and the full gate is running.
    evidence: [packing/campaign/series/series-000-smoke-and-calibration/experiments/exp-117-h-106-continuous-near-axis.md]
    stop_reason: The recovery boundary arrived with independent H106 acceptance and a changed density algorithm ready for source controls.
    next_action: Record the accepted auxiliary lemma, test the changed density source controls and review the fixed-site adapter without resetting its author cap.
  - workflow: research-loop
    focus: insight
    recording: contemporaneous
    clock_role: work
    objective: Disposition H106, test the changed density source controls and select the next useful scalar or restricted-angle discriminator.
    bead: think-9qrx
    status: in_progress
    entered_by: evidence_checkpoint
    switch_reason: The complete near-axis lemma passed independent replay; remaining lanes have new reviewed instruments or bounded assessments, not unchanged retries.
    budget_minutes: 30
    started_at: '2026-09-07T02:55:03Z'
    deadline_at: '2026-09-07T03:25:03Z'
    expected_output: Recorded H106 acceptance, changed-algorithm source readiness and one prospectively priced continuation from the returned assessments.
    validation_command: uv run --frozen --all-extras --group dev packing-validate --records
    kill_condition: A scientific guard fails, its frozen process cap expires, or the30-minute selection slice ends.
    fallback: Publish the exact accepted and unresolved scope; preserve unspent target allowances and the finalization reserve.
    outcome: null
    evidence: []
    stop_reason: null
    next_action: Run only newly selected controls; a new target requires its own registered claim, reviewed instrument and committed protocol.
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
    status: completed
    recording: contemporaneous
    outcome: Complete vertical-event and open-band controls passed source-distinct review; no target readiness accepted.
    evidence: [packing/devtools/density_slab_verifier.py, packing/tests/test_density_slab_verifier.py]
    files: [packing/devtools/density_slab_verifier.py, packing/tests/test_density_slab_verifier.py]
    checks: [18 author controls passed in 0.72s; 18 independent controls passed in 0.73s; Ruff and BasedPyright clean.]
    uncertainty: Shared field and validated geometry foundations remain explicit; target binding is separate.
    elapsed_seconds: 895
    elapsed_quality: operator_reported_approximate
    next_action: Complete source-bound adapters and separately measured original/uniform source controls.
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
    status: completed
    recording: contemporaneous
    outcome: The single source attempt hit 256 leaves with 68 assigned and 188 unresolved; independent review accepted this limited disposition.
    evidence: [packing/campaign/series/series-000-smoke-and-calibration/results/agenda-026/bc-255-angle-source-control.json]
    files: [packing/devtools/angle_source_control.py, packing/tests/test_angle_source_control.py]
    checks: [15 toy controls passed; independent toy replay passed in 0.15s; source attempt took 1.54s outer wall.]
    uncertainty: This is one original-source clause, not the seven-clause theorem or the prospective target.
    elapsed_seconds: 736
    elapsed_quality: operator_reported_approximate
    next_action: Preserve the failed binary control and evaluate only the separately commissioned changed grid representation.
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
  - task: BC243 source-bound density adapters; think-6ngf
    operator: Codex bound_lane_strategy, max mathematical reasoning
    status: completed
    recording: contemporaneous
    outcome: Thin fixed-source producer and independent slab reader passed root review and 23 toy/refusal controls.
    evidence: [packing/tests/test_full_size_density_faces.py]
    files: [packing/devtools/run_full_size_density_faces.py, packing/devtools/check_full_size_density_faces.py, packing/tests/test_full_size_density_faces.py]
    checks: [23 author controls passed in 1.50s; independent replay passed in 1.35s; Ruff and BasedPyright clean.]
    uncertainty: Process ceiling 120 seconds is not a measured target budget; source controls remain separate.
    elapsed_seconds: 862
    elapsed_quality: operator_reported_approximate
    next_action: Run separately commissioned original and uniform source controls from immutable c5f3a97f.
    phase: 3
    budget_minutes: 19
    started_at: '2026-09-07T01:15:05Z'
    deadline_at: '2026-09-07T01:33:19Z'
    expected_output: Compact bound receipts, strict parser/control refusals, and independent complete positive replay.
    validation_command: uv run --frozen --all-extras --group dev pytest tests/test_full_size_density_faces.py
    kill_condition: A binding or soundness premise fails, or the writer deadline arrives.
    fallback: Retain the incomplete adapter; do not execute source-scale or target geometry.
    write_scope: [packing/devtools/run_full_size_density_faces.py, packing/devtools/check_full_size_density_faces.py, packing/tests/test_full_size_density_faces.py]
    excluded_commands: [source-scale geometry, target measurements, git mutations, tbd mutations, registry edits]
  - task: BC255 changed 6x3 source-grid control; think-ibdk
    operator: Codex structural_lane_strategy, max mathematical reasoning
    status: completed
    recording: contemporaneous
    outcome: The original zero-angle clause passes all432triangle inequalities with no unresolved obligations.
    evidence: [packing/campaign/series/series-000-smoke-and-calibration/results/agenda-026/bc-255-angle-source-grid-control.json]
    files: [packing/devtools/angle_grid_source_control.py]
    checks: [25author controls passed; independent replay passed; source outer wall0.34s and CPU0.31s.]
    uncertainty: A positive producer receipt still needs the separately written source-only checker.
    elapsed_seconds: 676
    elapsed_quality: operator_reported_approximate
    next_action: Preserve the source result; a continuous-angle driver and independent reader remain separate.
    phase: 4
    budget_minutes: 20
    started_at: '2026-09-07T01:29:07Z'
    deadline_at: '2026-09-07T01:49:07Z'
    expected_output: Complete fixed-grid source packet or an explicit unresolved obligation.
    validation_command: uv run --frozen --all-extras --group dev pytest tests/test_angle_grid_source_control.py
    kill_condition: The ten-second source child cap, a failed control, or the author deadline.
    fallback: Preserve the new source outcome without retrying either source representation or accessing the target.
    write_scope: [packing/devtools/angle_tile_certificate.py, packing/tests/test_angle_tile_certificate.py, packing/devtools/angle_grid_source_control.py, packing/tests/test_angle_grid_source_control.py, packing/campaign/series/series-000-smoke-and-calibration/results/agenda-026/bc-255-angle-source-grid-control.json, packing/campaign/series/series-000-smoke-and-calibration/results/agenda-026/bc-255-angle-source-grid-control.log]
    excluded_commands: [target geometry, original binary source retry, git mutations, tbd mutations, registry edits]
  - task: BC255 source-distinct grid reader; think-0rez
    operator: Codex gpt6_coverage_audit, max mathematical reasoning
    status: completed
    recording: contemporaneous
    outcome: Independent replay proves all18rectangles through72corners and288signed inequalities.
    evidence: [packing/campaign/series/series-000-smoke-and-calibration/results/agenda-026/bc-255-angle-source-grid-replay.json]
    files: [packing/devtools/check_angle_grid_source_control.py]
    checks: [9toy/refusal controls passed; one source replay took0.07s wall and0.07s CPU.]
    uncertainty: Direct rectangle checks cover only the original theta-zero source clause, not continuous target angles.
    elapsed_seconds: 799
    elapsed_quality: operator_reported_approximate
    next_action: Preserve the source-only guarantee; the next full-range clause needs its own protocol.
    phase: 4
    budget_minutes: 20
    started_at: '2026-09-07T01:29:36Z'
    deadline_at: '2026-09-07T01:49:36Z'
    expected_output: Strict bounded source-packet reader using independent source reconstruction and corner inequalities.
    validation_command: uv run --frozen --all-extras --group dev pytest tests/test_check_angle_grid_source_control.py
    kill_condition: A source-binding or completeness premise fails, or the author deadline arrives.
    fallback: Preserve the missing reader obligation; producer acceptance is not independent verification.
    write_scope: [packing/devtools/check_angle_grid_source_control.py, packing/tests/test_check_angle_grid_source_control.py, packing/devtools/check_full_size_density_support_ceiling.py]
    excluded_commands: [original-source execution before authorization, target geometry, git mutations, tbd mutations, registry edits]
  - task: BC243 original and uniform density source controls; think-wc2h
    operator: Codex bound_lane_strategy, max mathematical reasoning
    status: completed
    recording: contemporaneous
    outcome: Original producer and independent slab replay prove maximum1 and mass11; uniform producer times out at60seconds and its reader is not invoked.
    evidence: [packing/campaign/series/series-000-smoke-and-calibration/results/agenda-026/bc-243-uniform-face-control.log]
    files: []
    checks: [Original producer20.35s wall19.30s CPU; reader4.48s wall4.44s CPU; uniform producer60.10s wall59.74s CPU.]
    uncertainty: These measure source-scale readiness, not the exp-113 candidate or a packing bound.
    elapsed_seconds: 248
    elapsed_quality: operator_reported_approximate
    next_action: Assess a justified arithmetic change; do not increase the cap or rerun unchanged source code.
    phase: 4
    budget_minutes: 10
    started_at: '2026-09-07T01:35:10Z'
    deadline_at: '2026-09-07T01:45:10Z'
    expected_output: Original and uniform source dispositions, separate replay outcomes, and measured wall/CPU costs.
    validation_command: uv run --frozen --all-extras --group dev packing-ledger check
    kill_condition: Each process has its own 60-second cap; the operator slice also ends at its declared boundary.
    fallback: A timeout or partial producer remains unresolved; do not replay it, retry its cap, or authorize a target.
    write_scope: [packing/campaign/series/series-000-smoke-and-calibration/results/agenda-026/bc-243-original-face-control.json, packing/campaign/series/series-000-smoke-and-calibration/results/agenda-026/bc-243-original-face-control.log, packing/campaign/series/series-000-smoke-and-calibration/results/agenda-026/bc-243-original-face-replay.json, packing/campaign/series/series-000-smoke-and-calibration/results/agenda-026/bc-243-original-face-replay.log, packing/campaign/series/series-000-smoke-and-calibration/results/agenda-026/bc-243-uniform-face-control.json, packing/campaign/series/series-000-smoke-and-calibration/results/agenda-026/bc-243-uniform-face-control.log, packing/campaign/series/series-000-smoke-and-calibration/results/agenda-026/bc-243-uniform-face-replay.json, packing/campaign/series/series-000-smoke-and-calibration/results/agenda-026/bc-243-uniform-face-replay.log]
    excluded_commands: [target geometry, source cap retries, git mutations, tbd mutations, registry edits]
  - task: BC243 local clearance reciprocal cache; think-063l
    operator: Codex bound_lane_strategy, max mathematical reasoning
    status: completed
    recording: contemporaneous
    outcome: Local lazy cache reduces the degree-eight toy clearance inversions from588to8 with identical exact outputs; root independently accepted theorem preservation.
    evidence: [packing/devtools/density_face_verifier.py]
    files: [packing/devtools/density_face_verifier.py, packing/tests/test_density_face_verifier.py]
    checks: [35author controls7.78s wall7.70s CPU; independent replay7.77s wall7.73s CPU; Ruff and BasedPyright clean.]
    uncertainty: Any source speedup and source readiness need separately allocated changed-code controls.
    elapsed_seconds: 543
    elapsed_quality: operator_reported_approximate
    next_action: Run only the separately selected changed-code source controls from frozen b379bfc6.
    phase: 5
    budget_minutes: 20
    started_at: '2026-09-07T01:54:24Z'
    deadline_at: '2026-09-07T02:14:24Z'
    expected_output: Theorem-preserving exact cache and durable equivalence/operation-count controls.
    validation_command: uv run --frozen --all-extras --group dev pytest tests/test_density_face_verifier.py
    kill_condition: A scientific premise fails or the declared slice boundary arrives.
    fallback: Preserve the exact unresolved obligation without extending its allocation.
    write_scope: [packing/devtools/density_face_verifier.py, packing/tests/test_density_face_verifier.py]
    excluded_commands: [new target measurements, unchanged retries, git mutations, tbd mutations, shared registry edits]
  - task: BC255 continuous near-axis source-bound driver; think-2gy1
    operator: Codex structural_lane_strategy, max mathematical reasoning
    status: completed
    recording: contemporaneous
    outcome: Source-bound two-slab driver frozen with864obligations; root review accepted its complete-domain and refusal semantics, not a target result.
    evidence: [packing/devtools/angle_near_axis_control.py]
    files: [packing/devtools/angle_near_axis_control.py, packing/tests/test_angle_near_axis_control.py]
    checks: [34author controls2.80s wall1.50s CPU; independent replay1.28s wall1.23s CPU.]
    uncertainty: An independent continuous reader and prospective target record are still required.
    elapsed_seconds: 795
    elapsed_quality: operator_reported_approximate
    next_action: Complete the independent reader and freeze the target experiment before any target invocation.
    phase: 5
    budget_minutes: 20
    started_at: '2026-09-07T01:55:02Z'
    deadline_at: '2026-09-07T02:15:02Z'
    expected_output: Fixed source-bound two-slab driver with toy/refusal controls and no target invocation.
    validation_command: uv run --frozen --all-extras --group dev pytest tests/test_angle_near_axis_control.py tests/test_angle_tile_certificate.py
    kill_condition: A scientific premise fails or the declared slice boundary arrives.
    fallback: Preserve the exact unresolved obligation without extending its allocation.
    write_scope: [packing/devtools/angle_near_axis_control.py, packing/tests/test_angle_near_axis_control.py, packing/devtools/angle_tile_certificate.py, packing/tests/test_angle_tile_certificate.py]
    excluded_commands: [new target measurements, unchanged retries, git mutations, tbd mutations, shared registry edits]
  - task: BC251 terminal scalar evidence and exact family replay; think-m8tj
    operator: Codex gpt6_coverage_audit, max mathematical reasoning
    status: completed
    recording: contemporaneous
    outcome: H093 remains unresolved; one exact replay reproduces depth1 and mass20843712108/2067791663, failing K3; all19row solves are unconverged.
    evidence: [packing/campaign/series/series-000-smoke-and-calibration/experiments/exp-116-h-093-scalar-61-16.md]
    files: []
    checks: [One replay took134.64s wall and132.92s CPU; all181directions and frozen input/state/family identities match.]
    uncertainty: The checker exit code means reproduction; rejection additionally needs mass at least eleven.
    elapsed_seconds: null
    elapsed_quality: unavailable
    next_action: Preserve the unresolved scalar outcome without bridge or retry; continue the independent angle reader.
    phase: 5
    budget_minutes: 10
    started_at: '2026-09-07T01:55:11Z'
    deadline_at: '2026-09-07T02:05:11Z'
    expected_output: Independent disposition of the one terminal scalar run; no unchanged retry or premature bridge.
    validation_command: uv run --frozen --all-extras --group dev python -m devtools.replay_ceiling_family --check FAMILY.json
    kill_condition: A scientific premise fails or the declared slice boundary arrives.
    fallback: Preserve the exact unresolved obligation without extending its allocation.
    write_scope: [packing/campaign/series/series-000-smoke-and-calibration/results/agenda-025/bc-234-scalar-61-16-leg-01-replay.log]
    excluded_commands: [new target measurements, unchanged retries, git mutations, tbd mutations, shared registry edits]
  - task: BC255 source-distinct continuous near-axis reader; think-3xaz
    operator: Codex gpt6_coverage_audit, max mathematical reasoning
    status: blocked
    recording: contemporaneous
    outcome: Reader and tests survived, but no author completion report survived the operational handoff; independent recovery review is required.
    evidence: [packing/devtools/check_angle_near_axis_control.py, packing/tests/test_check_angle_near_axis_control.py]
    files: []
    checks: []
    uncertainty: Fixed-grid failure is unresolved; only full actual-angle coverage or a separately checked avoider decides H106.
    elapsed_seconds: null
    elapsed_quality: unavailable
    next_action: Return source-distinct toy/refusal controls before independent review and prospective target dispatch.
    phase: 5
    budget_minutes: 20
    started_at: '2026-09-07T02:02:02Z'
    deadline_at: '2026-09-07T02:22:02Z'
    expected_output: Strict source-bound two-slab rectangle reader with independent polynomial construction and exact signs.
    validation_command: uv run --frozen --all-extras --group dev pytest tests/test_check_angle_near_axis_control.py
    kill_condition: A completeness premise fails or the author deadline arrives.
    fallback: Preserve the missing proof obligation; do not run a target or accept a producer alone.
    write_scope: [packing/devtools/check_angle_near_axis_control.py, packing/tests/test_check_angle_near_axis_control.py]
    excluded_commands: [target geometry or measurements, source retries, git mutations, tbd mutations, shared registry edits]
  - task: BC243 changed-cache source controls; think-zkj0
    operator: Codex coordinator, max mathematical reasoning
    status: blocked
    recording: contemporaneous
    outcome: Cached original producer and independent replay passed; uniform invocation was not found and the temporary source checkout disappeared during interruption.
    evidence: [packing/campaign/series/series-000-smoke-and-calibration/results/agenda-026/bc-243-original-cached-face-control.json, packing/campaign/series/series-000-smoke-and-calibration/results/agenda-026/bc-243-original-cached-face-replay.json]
    files: []
    checks: []
    uncertainty: Toy inversion reduction does not establish source speedup or target readiness.
    elapsed_seconds: null
    elapsed_quality: unavailable
    next_action: Measure original and uniform source producers once; replay only complete receipts.
    phase: 5
    budget_minutes: 10
    started_at: '2026-09-07T02:06:57Z'
    deadline_at: '2026-09-07T02:16:57Z'
    expected_output: Changed-code original/uniform source dispositions with separate wall/CPU costs.
    validation_command: python -m devtools.run_full_size_density_faces --control CONTROL --timeout-seconds 60
    kill_condition: Each process reaches its unchanged60-second cap, a source control fails, or the operator slice ends.
    fallback: Retain the unresolved obligation and no target; no unchanged retry or cap increase.
    write_scope: [packing/campaign/series/series-000-smoke-and-calibration/results/agenda-026]
    excluded_commands: [target weights or measurements, unchanged source retries, cap increases]
  - task: BC252 changed scalar mechanism assessment; think-csgu
    operator: Codex bound_lane_strategy, max mathematical reasoning
    status: blocked
    recording: contemporaneous
    outcome: No assessment report survived the operational handoff; the scalar evidence is intact and no new measurement was run.
    evidence: [packing/campaign/series/series-000-smoke-and-calibration/experiments/exp-116-h-093-scalar-61-16.md]
    files: []
    checks: []
    uncertainty: A changed row-completion or support proposal remains unmeasured and needs its own hypothesis and controls.
    elapsed_seconds: null
    elapsed_quality: unavailable
    next_action: Price one changed discriminator from retained evidence without solver or geometry execution.
    phase: 5
    budget_minutes: 10
    started_at: '2026-09-07T02:05:45Z'
    deadline_at: '2026-09-07T02:15:45Z'
    expected_output: A source-backed explanation of the scalar stop and a prioritized changed next test.
    validation_command: Read-only inspection of exp116 receipts and the frozen row-generation driver.
    kill_condition: The ten-minute assessment ends; no new measurement is authorized.
    fallback: Keep H093 unresolved and prioritize independently active density/angle work.
    write_scope: [none; read-only messages]
    excluded_commands: [solver runs, geometry construction, profiling, retries, file edits, git or tbd mutations]
  - task: Independent retained near-axis reader review; think-3xaz
    operator: Codex angle_reader_recovery, max mathematical reasoning
    status: completed
    recording: contemporaneous
    outcome: Independent review accepts the full fixed near-axis reader after root completed missing byte/CLI/alarm controls; no target has run.
    evidence: [packing/devtools/check_angle_near_axis_control.py, packing/tests/test_check_angle_near_axis_control.py]
    files: []
    checks: [16source-free tests passed0.58s wall0.55s CPU; Ruff and BasedPyright clean.]
    uncertainty: Recovery does not establish a new mathematical result or authorize an unchanged retry.
    elapsed_seconds: null
    elapsed_quality: unavailable
    next_action: Return retained evidence and measured costs before the declared deadline.
    phase: 6
    budget_minutes: 10
    started_at: '2026-09-07T02:23:47Z'
    deadline_at: '2026-09-07T02:33:47Z'
    expected_output: Independent mathematical and source-free control disposition of the retained reader.
    validation_command: Source-free targeted controls or the separately frozen uniform-source CLI.
    kill_condition: A proof premise fails, a frozen process cap expires, or the recovery slice ends.
    fallback: Preserve unresolved evidence and no retry.
    write_scope: [packing/campaign/series/series-000-smoke-and-calibration/results/agenda-026/bc-255-near-axis-reader-independent-review.md]
    excluded_commands: [target measurements, repeated completed commands, cap increases, Git mutations, shared registry edits]
  - task: Complete only the unstarted changed uniform source; think-zkj0
    operator: Codex density_control_recovery, max mathematical reasoning
    status: completed
    recording: contemporaneous
    outcome: Uniform cached producer times out after60.09s wall58.94s CPU, with empty stdout; replay not invoked and source readiness remains unresolved.
    evidence: [packing/campaign/series/series-000-smoke-and-calibration/results/agenda-026/bc-243-uniform-cached-face-control.log, packing/campaign/series/series-000-smoke-and-calibration/results/agenda-026/bc-243-uniform-cached-face-replay.log]
    files: []
    checks: []
    uncertainty: Recovery does not establish a new mathematical result or authorize an unchanged retry.
    elapsed_seconds: 272
    elapsed_quality: operator_reported_approximate
    next_action: Return retained evidence and measured costs before the declared deadline.
    phase: 6
    budget_minutes: 8
    started_at: '2026-09-07T02:25:16Z'
    deadline_at: '2026-09-07T02:33:16Z'
    expected_output: One changed-code uniform producer and conditional complete-packet replay, each capped at60seconds.
    validation_command: Source-free targeted controls or the separately frozen uniform-source CLI.
    kill_condition: A proof premise fails, a frozen process cap expires, or the recovery slice ends.
    fallback: Preserve unresolved evidence and no retry.
    write_scope: [packing/campaign/series/series-000-smoke-and-calibration/results/agenda-026]
    excluded_commands: [target measurements, repeated completed commands, cap increases, Git mutations, shared registry edits]
  - task: Recover changed scalar mechanism assessment; think-csgu
    operator: Codex scalar_followup_assessment, max mathematical reasoning
    status: completed
    recording: contemporaneous
    outcome: Fixed-site row completion is the next proposed discriminator; the stopped truncated dual does not establish site or row saturation. No launch allocated.
    evidence: [packing/campaign/series/series-000-smoke-and-calibration/results/agenda-025/bc-252-exp116-next-discriminator.md]
    files: []
    checks: []
    uncertainty: Recovery does not establish a new mathematical result or authorize an unchanged retry.
    elapsed_seconds: 462
    elapsed_quality: operator_reported_approximate
    next_action: Return retained evidence and measured costs before the declared deadline.
    phase: 6
    budget_minutes: 10
    started_at: '2026-09-07T02:24:24Z'
    deadline_at: '2026-09-07T02:34:24Z'
    expected_output: A read-only explanation and priced next discriminator, with no solver or geometry execution.
    validation_command: Source-free targeted controls or the separately frozen uniform-source CLI.
    kill_condition: A proof premise fails, a frozen process cap expires, or the recovery slice ends.
    fallback: Preserve unresolved evidence and no retry.
    write_scope: [packing/campaign/series/series-000-smoke-and-calibration/results/agenda-025/bc-252-exp116-next-discriminator.md]
    excluded_commands: [target measurements, repeated completed commands, cap increases, Git mutations, shared registry edits]
  - task: BC243 exact facet-side membership reuse; think-8zdl
    operator: Codex density_control_recovery, max mathematical reasoning
    status: completed
    recording: contemporaneous
    outcome: Exact line-incidence reuse preserves direct membership and witness construction; committed22ef5f6c after independent root review.
    evidence: [packing/devtools/density_face_verifier.py, packing/tests/test_density_face_verifier.py]
    files: [packing/devtools/density_face_verifier.py, packing/tests/test_density_face_verifier.py]
    checks: [Root replay passed all50focused controls in9.84s wall9.78s CPU; Ruff and BasedPyright clean.]
    uncertainty: Membership operation reduction is not a source speedup; independent review and changed-code source controls remain separate.
    elapsed_seconds: 1012
    elapsed_quality: operator_reported_approximate
    next_action: Run the separately selected changed-code source controls, without candidate access.
    phase: 6
    budget_minutes: 20
    started_at: '2026-09-07T02:31:32Z'
    deadline_at: '2026-09-07T02:51:32Z'
    expected_output: Complete canonical inward-edge incidence and exact membership reuse with durable agreement/operation-count controls.
    validation_command: uv run --frozen --all-extras --group dev pytest tests/test_density_face_verifier.py
    kill_condition: An orientation/completeness premise fails or the20-minute writer boundary arrives.
    fallback: Preserve direct membership and source timeout evidence; no source or target invocation.
    write_scope: [packing/devtools/density_face_verifier.py, packing/tests/test_density_face_verifier.py]
    excluded_commands: [source or target geometry runs, cap increases, Git mutations, registry edits]
  outputs:
  - packing/campaign/agent-sessions/session-090-four-hour-research.md
  checks:
  - Fetched main 4d305597; PR 101 is merged and its tree is identical to validated 8f30be8c.
  - Isolated record checkpoint 97ba816e passed 31 of 66 steps in 20.72s; this is not the full gate.
  - Updated narrative-count negative control fired in 1.568s using a private source snapshot.
  - Root independently reviewed the rational angle kernel and replayed 8 controls; 0.05s pytest, 0.57s process wall, 0.42s CPU.
  stop_reason: null
  next_action: Continue PR105 with accepted H106, the next restricted-angle clause and fixed-site scalar readiness; density remains source-blocked and exp116 must not be retried unchanged.
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
The nominal 150-minute loop boundary was `03:16:18Z`; the producer instead stopped
adding sites and finished by `01:43:23Z`. Its 3424.81 seconds outer wall and the sole
134.64-second independent family replay are retained in exp-116. Every row solve was
unconverged, and the exact dual mass is below eleven.
The outcome is unresolved, with no covering bridge or unchanged retry.
The completed state is safe to retain, but its existence does not satisfy the bridge’s
convergence guard.

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

## Integrated Publication and Source Controls

[PR 105](https://github.com/jlevy/squares/pull/105) is the single draft successor.
Its published `dc5ef612` checkpoint passed all required hosted checks, including Linux
validation, geometry, sweeps and suite, macOS portability, and mergeability.
Local pre-push validation was composed from all passing non-behavioral steps, 643
passing reachable tests, and the remaining snapshot test passing unchanged after
explicitly binding the synced environment.
The earlier failures were missing cache, process-inspection access, and a snapshot
without its dependency environment; no assertion, test selection, or dependency was
changed. `think-5vpo` retains that repair.

The independently reviewed slab and quadratic-source snapshot is `2ded0b4e`; the
source-bound density adapters are `c5f3a97f`. These later commits are not covered by the
earlier hosted verdict until the next push and completed checks.
The density source controls use the immutable validation checkout at `c5f3a97f`. Each
original/uniform producer and its independent reader gets one 60-second process cap,
with no replay of an incomplete producer.
The original source has expected maximum one; the uniform D4 average has expected
maximum at most one, without presuming equality.
Source costs are measured separately from any future candidate allocation.

The new angle control changes the root mesh, not the old binary cap.
Its fixed six-by-three grid, source labels, 36 triangles, and 432 vertex inequalities
are specified in the
[BC-255 design](../series/series-000-smoke-and-calibration/results/agenda-026/bc-255-angle-instrument-design.md).
The producer gets one ten-second source invocation after toy/refusal controls.
The source-distinct reader reconstructs the original K4 ten-set and checks all rectangle
corners directly; its own ten-second source replay needs separate dispatch after review.
Neither route accepts a continuous-angle target or the remaining theorem clauses.
The shared bounded loader may accept a smaller caller-supplied byte cap but cannot
exceed its existing two-MiB ceiling.

## Efficiency Slice and Continuous-Angle Registration

Phase 5 is the explicitly selected efficiency slice: the uniform source timeout
motivates a local cache of exact normal-pair clearance inverses.
Static review priced the cache before implementation; operation-count and exact-output
controls precede any new source measurement.
The previous timeout stays in its original record.
There is no cap increase or target authorization in this change.

In parallel, H-106 registers the unchanged ten-point set at side `1939/500` throughout
the full near-axis neighborhood.
The author and source-distinct reader use complete closed rational outer angle slabs and
a fixed center grid, without target construction in their toy controls.
This is one auxiliary clause, not all of H-036. Both implementations, their reviews, and
a prospective experiment must be ready before target dispatch.

## Operational Recovery at the Two-Hour Checkpoint

At `02:22:33Z`, the coordinator observed that the previous worker tree was empty.
Git still knew the temporary worktrees, but their directories and the temporary PR-body
file were absent.
Repository files, completed scientific outputs and bead state remained.
The unavailable interval was not measured precisely; it is not charged as attentive
agent time or a scientific timeout.
No experimental budget resets.
The nominal block milestones remain reference times until any documented active-time
adjustment is made.

Exp-116 and both original cached-density invocations were already complete and are not
repeated.
A fresh detached checkout at `b379bfc6` restores the same scientific source for
the still-unstarted uniform control.
Independent recovery review treats the retained continuous reader as unfinished author
work until its mathematics and controls pass.
The scalar follow-up is a read-only assessment, not another solver invocation.

## Continuous Lemma and Next Selection

Exp-117 accepted H-106 after one producer and one independently implemented exact
reader. All 36 closed slab-rectangles and their 576 corner inequalities passed; summed
process costs were 0.37 seconds wall and 0.34 CPU. The reader’s operator interval was
02:49:20–02:50:19 UTC under `think-tv58`. H-036 and the global bound remain unchanged.
Near-45-degree localization, forced points and twelve-point coverage are still separate
obligations.
`think-hkpi` owns a read-only comparison of those next clauses from 02:54:21
to the original 03:09:21 boundary.

The density sign-incidence author finished at 02:48:24 UTC. Root independently reviewed
the inward-sign and clearance argument under `think-sxbg`, and all 50 focused controls
passed before commit `22ef5f6c`. `think-2sd2` then ran the original and uniform source
controls once each, with the unchanged 60-second process caps.
The original producer and independent slab replay passed at maximum one; the uniform
producer timed out with empty stdout, so its reader was not invoked.
Total process costs were 73.61 seconds wall and 69.33 CPU; the operator interval was
02:56:55–03:02:12 UTC. These shared-host timings do not establish a speedup.
No further density optimization or candidate run is selected in this slice.

For BC-252, `think-au9i` completed the fixed-site receipt adapter in the original
02:42:09–02:54:37 author interval.
The root review found that a failed later LP can leave dual vectors indexed by a shorter
row prefix; the receipt now names that prefix explicitly and has a regression.
`think-36uc` owns the separate final review.
The read-only protocol assessment ran 02:57:26–03:02:58 UTC under `think-u7c9`. Its
proposed 45-minute target, 15-minute source controls and 20-minute candidate
verification do not fit before the closing reserve.
Reuse of already-running, unchanged proof-chain controls and a shorter external target
cap need an explicit allocation decision; no scalar target is authorized by the adapter
alone.

The published `2707ea39` checkpoint passed every required hosted check at 02:52:03 UTC.
The full local gate remains active on that immutable snapshot.
The fresh upstream fetch found no new main commit and no other outstanding PR. PR 105’s
body now records the terminal scalar outcome, accepted auxiliary lemma, source-control
limits and current validation scope.
Core README and TUTORIAL exposition remains unchanged.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
