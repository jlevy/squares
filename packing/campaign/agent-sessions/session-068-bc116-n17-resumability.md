---
title: "session-068 — BC-116 n = 17 resumability"
softschema:
  contract: packing.squares:AgentSession/v2
  schema: ../schemas/agent-session.schema.yaml
  envelope: session
  status: enforced
session:
  id: session-068
  primary_bead: think-9zgs
  status: completed
  title: "BC-116 n = 17 resumability"
  date: '2026-09-01'
  started_at: '2026-09-01T12:16:55Z'
  deadline_at: '2026-09-01T14:56:55Z'
  branch: codex/w3-nine-hour-autonomous-run
  goal: >-
    Preserve the exp-049 midmeasurement no-checkpoint refusal, add target-blind
    direction-sliced resume support around the unchanged n = 17 scientific kernels,
    obtain independent readmission, and spend one newly preregistered W6 round without
    changing H-052's criterion or the frontier.
  workflow_phases:
  - workflow: insight-iteration
    recording: contemporaneous
    clock_role: work
    focus: insight
    objective: >-
      Freeze the actual exp-049 process outcome, immutable inputs, external checkpoint
      boundary, resume semantics, controls, lane cells, stop meanings and future path
      convention without opening target output or allocating an experiment.
    commitment: BC-116
    bead: think-9zgs
    status: completed
    entered_by: session_start
    switch_reason: null
    budget_minutes: 15
    started_at: '2026-09-01T12:16:55Z'
    deadline_at: '2026-09-01T12:31:55Z'
    expected_output: >-
      A complete target-blind W7, W2 and W6 contract returned to the coordinator for
      serial experiment and result-path assignment.
    validation_command: >-
      uv run --frozen softschema validate
      campaign/agent-sessions/session-068-bc116-n17-resumability.md
    kill_condition: >-
      Stop if target output is opened or executed, an experiment id is allocated, a
      frozen scientific-kernel file changes, or the process refusal is relabelled as a
      discrepancy or premeasurement guard.
    fallback: >-
      Retain the smallest missing checkpoint, path or semantic contract field and return
      to the coordinator without entering W7.
    outcome: >-
      Froze exp-049's executed midmeasurement no-checkpoint refusal, recomputed every
      retained source and package digest, fixed the external direction-sliced checkpoint
      boundary and hash-chain semantics, named synthetic equivalence and corruption
      guards, allocated all eight 15--25-minute cells, and reserved no experiment id. No
      target output or frozen scientific-kernel file was opened for execution or changed.
    evidence:
    - packing/campaign/agent-sessions/session-068-bc116-n17-resumability.md
    - packing/campaign/agent-sessions/session-065-bc108-n17-certificate.md
    - packing/campaign/series/series-000-smoke-and-calibration/experiments/exp-049-h-052-n17-independent-certificate-agreement.md
    - packing/campaign/hypotheses/H-052-n17-independent-certificate-agreement.md
    - docs/project/reviews/review-2026-09-01-agenda013-first-wave-efficiency.md
    stop_reason: The 0--15 target-blind W3 contract is complete.
    next_action: >-
      Return the contract to the coordinator. Stop until it assigns the next free
      experiment id, materializes the exact paths, appends W7 and authorizes that phase.
  - workflow: pipeline-improvement
    recording: contemporaneous
    clock_role: work
    focus: correctness
    objective: >-
      Build the external direction-sliced driver and atomic paired-row checkpoint writer
      around the unchanged frozen kernels, exercise the first synthetic round-trip and
      corruption guards, and retain the exact residue for the next W7 control cell
      without target access.
    commitment: BC-116
    bead: think-9zgs
    status: completed
    entered_by: evidence_checkpoint
    switch_reason: >-
      The coordinator allocated and validated exp-052 with its exact result, checkpoint
      and progress paths absent, then explicitly authorized the first W7 cell at the
      fixed 12:31:55Z boundary.
    budget_minutes: 20
    started_at: '2026-09-01T12:31:55Z'
    deadline_at: '2026-09-01T12:51:55Z'
    expected_output: >-
      A target-blind external checkpoint package and focused tests that preserve the
      frozen package hash, atomically retain only complete paired rows, validate a
      contiguous hash chain and report any remaining controls before the next fixed cell.
    validation_command: >-
      uv run --frozen --all-extras --group dev pytest -q
      tests/test_n17_weighted_certificate_resume.py
    kill_condition: >-
      Stop if any frozen package file changes, target data or output is loaded, a real
      result/checkpoint/progress path is created, a paired row can be accepted without
      both accumulators, or the 12:51:55Z boundary arrives.
    fallback: >-
      Retain the smallest incomplete interface or failed synthetic guard, leave W2 and
      W6 closed, and return without repairing against target-derived data.
    outcome: >-
      Added a target-blind external driver that verifies the frozen source and package
      digests, binds the exact fixture, paths and current driver revision, calls both
      unchanged per-direction accumulators, and atomically retains only contiguous,
      hash-chained complete pairs. Five focused synthetic tests passed for frozen-input
      verification, complete-pair round trip, source-only interruption and resume,
      changed-row-hash rejection, and exact agreement of the two imported accumulators.
      No target fixture was loaded or executed and no exp-052 output path was created.
    evidence:
    - packing/cases/n17_weighted_certificate_resume/__init__.py
    - packing/cases/n17_weighted_certificate_resume/run.py
    - packing/tests/test_n17_weighted_certificate_resume.py
    - packing/campaign/agent-sessions/session-068-bc116-n17-resumability.md
    - packing/campaign/series/series-000-smoke-and-calibration/experiments/exp-052-h-052-n17-resumable-certificate-agreement.md
    stop_reason: The authorized 15--35 W7 implementation cell is complete.
    next_action: >-
      Stop for coordinator authorization of the fixed 35--55 W7 cell. That cell must
      add the production CLI and selftest, complete every named interruption and
      corruption control under normal and optimized Python, bind byte-identical
      receipts, and freeze the external driver before W2.
  - workflow: pipeline-improvement
    recording: contemporaneous
    clock_role: work
    focus: correctness
    objective: >-
      Complete the target-blind exp-052 command-line adapter, result assembler,
      checkpoint and progress replay guards, full synthetic interruption and corruption
      matrix, and explicit normal-versus-optimized selftest receipt without changing or
      opening the frozen target.
    commitment: BC-116
    bead: think-9zgs
    status: completed
    entered_by: evidence_checkpoint
    switch_reason: >-
      The coordinator reviewed the first external checkpoint core, queued exact
      cross-lane repairs, and explicitly authorized the fixed second W7 cell.
    budget_minutes: 20
    started_at: '2026-09-01T12:51:55Z'
    deadline_at: '2026-09-01T13:11:55Z'
    expected_output: >-
      A frozen target-blind production revision whose explicit selftest and focused
      tests cover all preregistered path, checkpoint, progress, provenance,
      interruption, corruption and optimized-Python guards with zero skips.
    validation_command: >-
      uv run --frozen --all-extras --group dev pytest -q
      tests/test_n17_weighted_certificate_resume.py && uv run --frozen python -m
      cases.n17_weighted_certificate_resume.run --selftest
    kill_condition: >-
      Stop if any frozen package file changes, target data or output is loaded, a real
      exp-052 output path is created, any guard fails, or the 13:11:55Z boundary arrives.
    fallback: >-
      Retain the first unmet readiness guard, leave W2 and W6 closed, and return without
      repairing against target-derived data.
    outcome: >-
      Completed the exp-052 production command, exact three-path binding, atomic result
      assembler, result-existence refusal, canonical progress replay, validated
      stale-marker removal before publication, manifest direction and event-hash replay,
      and the complete synthetic
      interruption and corruption matrix. The explicit non-assert selftest passed with
      byte-identical normal and optimized-Python output; six focused tests, Ruff and
      BasedPyright passed. No target fixture was loaded or executed and no real exp-052
      output was created.
    evidence:
    - packing/cases/n17_weighted_certificate_resume/__init__.py
    - packing/cases/n17_weighted_certificate_resume/run.py
    - packing/tests/test_n17_weighted_certificate_resume.py
    - packing/campaign/agent-sessions/session-068-bc116-n17-resumability.md
    - packing/campaign/series/series-000-smoke-and-calibration/experiments/exp-052-h-052-n17-resumable-certificate-agreement.md
    stop_reason: The authorized 35--55 W7 readiness cell is complete.
    next_action: >-
      Stop for independent W2 review. W6 remains closed until the reviewer confirms the
      frozen revision, direct imports, result/path refusal, progress precedence,
      checkpoint replay, full zero-skip guard inventory and byte-identical selftests.
  - workflow: process-review
    recording: contemporaneous
    clock_role: work
    focus: correctness
    objective: >-
      Independently replay the frozen exp-052 readiness evidence, verify the unchanged
      scientific-kernel and direct-import boundaries, inspect checkpoint and result
      semantics, and admit or refuse the sole target process without changing the
      candidate implementation.
    commitment: BC-116
    bead: think-9zgs
    status: completed
    entered_by: evidence_checkpoint
    switch_reason: >-
      Both target-blind W7 cells are complete, their cross-audit repairs are frozen, the
      three real output paths remain absent, and W6 is still closed.
    budget_minutes: 15
    started_at: '2026-09-01T13:11:55Z'
    deadline_at: '2026-09-01T13:26:55Z'
    expected_output: >-
      An independent pass or first blocking guard bound to the exact driver, tests,
      package manifest, selftest receipt and three exp-052 output paths.
    validation_command: >-
      uv run --frozen --all-extras --group dev pytest -q
      tests/test_n17_weighted_certificate_resume.py && uv run --frozen python -m
      cases.n17_weighted_certificate_resume.run --selftest
    kill_condition: >-
      Refuse W6 if a frozen hash differs, either accumulator is translated or bypassed,
      a partial or reordered row can become canonical, a named guard skips or fails,
      optimized output differs, a real output path exists, or review would require an
      implementation edit.
    fallback: >-
      Retain the first exact blocker, keep exp-052 review-pending and do not authorize
      target access or repair the candidate inside W2.
    outcome: >-
      The coordinator independently reproduced six focused tests, twenty-seven
      zero-skip selftest guards, the frozen package manifest, exact exp-052 path
      bindings, absent output paths and byte-identical normal/optimized receipt SHA-256
      beaf5b2b9bcaa0b95ff053c8f6e0aa955d075d21d877460c52b779a68d60ca60. Static and
      synthetic replay confirmed direct imports of both unchanged accumulators and
      equality between the frozen assembler and the checkpoint assembler. No candidate
      file changed during W2; exp-052 is admitted for its sole fixed W6 process.
    evidence:
    - packing/cases/n17_weighted_certificate_resume/run.py
    - packing/tests/test_n17_weighted_certificate_resume.py
    - packing/campaign/series/series-000-smoke-and-calibration/experiments/exp-052-h-052-n17-resumable-certificate-agreement.md
    - packing/campaign/agent-sessions/session-068-bc116-n17-resumability.md
    stop_reason: Every frozen W2 admission guard passed without an implementation edit.
    next_action: >-
      Hold target access until the fixed 13:26:55Z boundary, then append and authorize
      the sole uninterrupted W6 process through 14:41:55Z.
  - workflow: research-loop
    recording: contemporaneous
    clock_role: work
    focus: correctness
    objective: >-
      Start the sole preregistered exp-052 target process at the admitted frozen
      revision, retain only complete paired rows and one active-stage marker, and carry
      the same process into the next cell without repair or restart.
    commitment: BC-116
    bead: think-9zgs
    status: completed
    entered_by: evidence_checkpoint
    switch_reason: >-
      Independent W2 passed every admission guard and the result, checkpoint and
      progress paths were absent at the fixed W6 opening.
    budget_minutes: 25
    started_at: '2026-09-01T13:26:55Z'
    deadline_at: '2026-09-01T13:51:55Z'
    expected_output: >-
      A terminal canonical result or a hash-valid checkpoint prefix plus exact active
      ordinal/stage and elapsed process cost, with no rerun or target-informed change.
    validation_command: >-
      uv run --frozen python -m cases.n17_weighted_certificate_resume.run --record
      campaign/series/series-000-smoke-and-calibration/results/exp-052-h-052-n17-resumable-certificate-agreement.json
      --checkpoint
      campaign/series/series-000-smoke-and-calibration/results/exp-052-h-052-n17-resumable-certificate-agreement.checkpoint.json
      --progress
      campaign/series/series-000-smoke-and-calibration/results/exp-052-h-052-n17-resumable-certificate-agreement.progress.json
    kill_condition: >-
      Stop on a frozen-input or checkpoint guard, target-process exit, an invalid
      checkpoint/progress artifact, or the final 14:41:55Z hard stop; cell boundaries
      alone do not stop or restart the process.
    fallback: >-
      Preserve the first immutable failure or last hash-valid paired prefix and active
      stage, then route it to final W3 without repair or rerun.
    outcome: >-
      Artifact: the sole process started at 2026-09-01T13:27:39Z and retained its
      canonical checkpoint and progress marker without restart. Result: the
      2026-09-01T13:52:11Z boundary observation found 11 contiguous paired rows,
      ordinals 0--10, all with exact source/independent agreement; row 11 was at
      `independent_started`, bound to the last committed row hash
      c7f49f47ec59c6bc2daa2205c16d788975c5edd7f571070f2e45fde4bb872f26.
      Guard: PID 30540 remained live at full CPU, the result path remained absent, and
      no process restart, repair, control or target-output interpretation occurred.
      Next: carry this same process into the 13:51:55Z--14:16:55Z cell.
    evidence:
    - packing/campaign/series/series-000-smoke-and-calibration/results/exp-052-h-052-n17-resumable-certificate-agreement.checkpoint.json
    - packing/campaign/series/series-000-smoke-and-calibration/results/exp-052-h-052-n17-resumable-certificate-agreement.progress.json
    stop_reason: The first W6 cell boundary was observed without stopping the live process.
    next_action: Continue the same process unchanged and report at 14:16:55Z.
  - workflow: research-loop
    recording: contemporaneous
    clock_role: work
    focus: correctness
    objective: >-
      Continue the sole exp-052 target process from its hash-valid eleven-row prefix,
      retaining only complete paired rows and the active-stage marker without repair or
      restart.
    commitment: BC-116
    bead: think-9zgs
    status: completed
    entered_by: planned_checkpoint
    switch_reason: >-
      The first W6 boundary retained eleven agreeing rows and a valid active-stage
      marker while the sole process remained live.
    budget_minutes: 25
    started_at: '2026-09-01T13:51:55Z'
    deadline_at: '2026-09-01T14:16:55Z'
    expected_output: >-
      A terminal canonical result or a larger hash-valid paired prefix plus exact active
      ordinal/stage and elapsed process cost from the same process.
    validation_command: >-
      Read-only canonical checkpoint and progress validation against the frozen exp-052
      binding; do not invoke the target command again.
    kill_condition: >-
      Stop on target-process exit, an invalid checkpoint/progress artifact or the final
      14:41:55Z hard stop; this cell boundary alone does not stop or restart the process.
    fallback: >-
      Preserve the first immutable failure or last hash-valid paired prefix and active
      stage, then route it to final W3 without repair or rerun.
    outcome: >-
      Artifact: the same PID pair 30456/30540 remained live without restart and
      advanced the canonical checkpoint. Result: the 2026-09-01T14:17:11Z boundary
      observation found 22 contiguous paired rows, ordinals 0--21, all with exact
      source/independent agreement; row 22 was at `independent_started`, bound to the
      last committed row hash
      981f4686df96a04d259f3f9e856f9138d8d633e9b8f49ccc333d3b9589696ee6.
      Guard: the observation was sixteen seconds after the scheduled boundary, PID
      30540 remained active at full CPU, the result path remained absent, and no
      restart, repair, control or target-output interpretation occurred. Next: carry
      this same process into the 14:16:55Z--14:41:55Z cell.
    evidence:
    - packing/campaign/series/series-000-smoke-and-calibration/results/exp-052-h-052-n17-resumable-certificate-agreement.checkpoint.json
    - packing/campaign/series/series-000-smoke-and-calibration/results/exp-052-h-052-n17-resumable-certificate-agreement.progress.json
    stop_reason: The second W6 cell boundary was observed without stopping the live process.
    next_action: Continue the sole live process unchanged and stop it once at 14:41:55Z.
  - workflow: research-loop
    recording: contemporaneous
    clock_role: work
    focus: correctness
    objective: >-
      Continue the sole exp-052 target process from its hash-valid twenty-two-row
      prefix, retaining only complete paired rows and the active-stage marker without
      repair or restart, then interrupt it exactly once at the final hard stop.
    commitment: BC-116
    bead: think-9zgs
    status: completed
    entered_by: planned_checkpoint
    switch_reason: >-
      The second W6 boundary retained twenty-two agreeing rows and a valid active-stage
      marker while the sole process remained live.
    budget_minutes: 25
    started_at: '2026-09-01T14:16:55Z'
    deadline_at: '2026-09-01T14:41:55Z'
    expected_output: >-
      A terminal canonical result or the final hash-valid paired prefix, exact active
      ordinal/stage, elapsed process cost and one-interrupt receipt from the same
      process.
    validation_command: >-
      Read-only canonical checkpoint and progress validation against the frozen exp-052
      binding; do not invoke the target command again.
    kill_condition: >-
      Stop on target-process exit, an invalid checkpoint/progress artifact or the fixed
      14:41:55Z hard stop. At the hard stop, interrupt the same process exactly once.
    fallback: >-
      Preserve the first immutable failure or last hash-valid paired prefix and active
      stage, then route it to final W3 without repair or rerun.
    outcome: >-
      Artifact: the same PID pair 30456/30540 ran without restart until the exact
      2026-09-01T14:41:55Z hard stop. One PTY interrupt returned exit 130 with a
      KeyboardInterrupt inside the unchanged independent accumulator; a process-table
      check then found both PIDs absent. Result: the frozen replay boundary retained 33
      contiguous paired rows, ordinals 0--32, all with exact source/independent
      agreement. The last row hash is
      9badcc57c05e328344b0ec7ae4fbf9815e8eae027a79bec1bf1a35b9871fade6;
      progress ordinal 33 remained at `independent_started`, chained to that hash, and
      the result path was absent. Guard: the checkpoint and progress marker passed the
      frozen driver's binding, canonical-serialization, direction, manifest,
      event-hash, row-hash, chain and nonfuture replay checks. No rerun, repair,
      completed sample or result interpretation occurred. Next: enter the fixed final
      W3 cell and terminalize exp-052 as an executed incomplete timebox outcome with
      H-052 scientifically unresolved and `needs_review: true`.
    evidence:
    - packing/campaign/series/series-000-smoke-and-calibration/results/exp-052-h-052-n17-resumable-certificate-agreement.checkpoint.json
    - packing/campaign/series/series-000-smoke-and-calibration/results/exp-052-h-052-n17-resumable-certificate-agreement.progress.json
    stop_reason: >-
      The fixed hard stop ended the sole process after 4456 seconds with a valid
      thirty-three-row prefix and no canonical result.
    next_action: >-
      Interpret only the preserved process evidence in final W3; do not resume target
      work or infer an H-052 or frontier disposition from prefix agreement.
  - workflow: insight-iteration
    recording: contemporaneous
    clock_role: finalization
    focus: insight
    objective: >-
      Validate the interrupted process's canonical checkpoint and progress boundary,
      record its exact cost and typed outcome, and hand off an unresolved,
      review-pending experiment without resuming target work or changing H-052 or the
      frontier.
    commitment: BC-116
    bead: think-9zgs
    status: completed
    entered_by: planned_checkpoint
    switch_reason: >-
      The sole W6 process reached the fixed 14:41:55Z hard stop, received its one
      authorized interrupt and left a canonical paired-row prefix rather than a result.
    budget_minutes: 15
    started_at: '2026-09-01T14:41:55Z'
    deadline_at: '2026-09-01T14:56:55Z'
    expected_output: >-
      A terminal session and experiment record that preserve the exact checkpoint,
      active progress marker, one-interrupt receipt, elapsed cost, absent result and
      unresolved H-052 boundary for independent coordinator review.
    validation_command: >-
      uv run --frozen softschema validate
      campaign/agent-sessions/session-068-bc116-n17-resumability.md && uv run --frozen
      softschema validate
      campaign/series/series-000-smoke-and-calibration/experiments/exp-052-h-052-n17-resumable-certificate-agreement.md
    kill_condition: >-
      Stop if finalization would resume target work, edit the frozen driver or kernels,
      treat prefix agreement as a completed H-052 sample, or change H-052 or the
      frontier.
    fallback: >-
      Preserve the checkpoint, progress marker and first validation defect for the
      coordinator; keep the experiment unresolved and review-pending.
    outcome: >-
      The frozen driver replayed the checkpoint and progress marker without target
      execution: 33 contiguous exact-agreeing rows, last hash
      9badcc57c05e328344b0ec7ae4fbf9815e8eae027a79bec1bf1a35b9871fade6,
      and ordinal 33 at `independent_started`. The checkpoint and progress artifacts
      hash to db5c156959b6de4e6f2c9be283454d01dd5f3a436e6489f5e6bb60c38559fdb8
      and 08e301b01c7ac6eef4b03c3a4daa5f72c5f1bdbe217dbbb061b57f5c94d947af.
      Exp-052 now records the 4456-second one-interrupt timebox as executed incomplete,
      unresolved and `needs_review: true`; no result JSON, hypothesis disposition or
      frontier change was created.
    evidence:
    - packing/campaign/series/series-000-smoke-and-calibration/experiments/exp-052-h-052-n17-resumable-certificate-agreement.md
    - packing/campaign/series/series-000-smoke-and-calibration/results/exp-052-h-052-n17-resumable-certificate-agreement.checkpoint.json
    - packing/campaign/series/series-000-smoke-and-calibration/results/exp-052-h-052-n17-resumable-certificate-agreement.progress.json
    - packing/campaign/agent-sessions/session-068-bc116-n17-resumability.md#final-w3--executed-incomplete
    - packing/campaign/resource-usage/codex-task-tree-session-068.yaml
    stop_reason: >-
      The preserved process boundary and terminal experiment record are complete for
      coordinator review; the scientific criterion remains unmeasured.
    next_action: >-
      Coordinator review may apply only the executed-incomplete process transition and
      generate the terminal resource receipt. Any scientific continuation requires a
      newly preregistered resume round from ordinal 33.
  budget:
    wall_minutes: 160
    max_cycles: 8
    checkpoint_minutes: 25
    slice_minutes: 25
    finalization_minutes: 15
  stop_conditions:
  - Any target output is opened or executed before serial preregistration and W7/W2 readiness.
  - Any file in packing/cases/n17_weighted_certificate/ changes.
  - A checkpoint, provenance, equivalence, corruption or optimized-Python guard fails.
  - The 2026-09-01T14:56:55Z lane deadline arrives.
  progress:
    metric: resumable paired n = 17 direction rows retained under the unchanged exact kernels
    before: >-
      Exp-049 consumed 3920 seconds and stopped midmeasurement without a canonical row,
      comparison, mutation result, checkpoint or result JSON.
    after: >-
      Independent W2 admitted the frozen external production candidate; one exact W6
      process then retained 33 contiguous agreeing paired rows and an active ordinal-33
      marker before its fixed hard stop. No complete result exists, so H-052 remains
      scientifically unresolved and review-pending.
  delegations: []
  outputs:
  - packing/campaign/agent-sessions/session-068-bc116-n17-resumability.md
  - packing/cases/n17_weighted_certificate_resume/__init__.py
  - packing/cases/n17_weighted_certificate_resume/run.py
  - packing/tests/test_n17_weighted_certificate_resume.py
  - packing/campaign/series/series-000-smoke-and-calibration/experiments/exp-052-h-052-n17-resumable-certificate-agreement.md
  - packing/campaign/series/series-000-smoke-and-calibration/results/exp-052-h-052-n17-resumable-certificate-agreement.checkpoint.json
  - packing/campaign/series/series-000-smoke-and-calibration/results/exp-052-h-052-n17-resumable-certificate-agreement.progress.json
  - packing/campaign/resource-usage/codex-task-tree-session-068.yaml
  checks:
  - Recomputed the four retained-source hashes and all Python-file hashes in the frozen package.
  - The sorted frozen-package sha256sum manifest still hashes to 309ec24158f73dd2e9b837c773b1e5c1642f357de5bdf73311b73232abdb6d54.
  - A presence-only check found the exp-049 result path absent; no target output was opened.
  - Enforced softschema repair required no changes and validation passed.
  - Pinned Flowmark 0.3.2 auto-check passed for this session file.
  - >-
    `uv run --frozen --all-extras --group dev pytest -q
    tests/test_n17_weighted_certificate_resume.py` passed all five target-blind tests.
  - >-
    `uv run --frozen ruff check cases/n17_weighted_certificate_resume
    tests/test_n17_weighted_certificate_resume.py` passed.
  - >-
    `uv run --frozen basedpyright cases/n17_weighted_certificate_resume
    tests/test_n17_weighted_certificate_resume.py` reported zero errors and warnings.
  - >-
    The final focused pytest command passed six tests; the production selftest exercised
    twenty-seven named guards with zero skips.
  - >-
    Normal and `python -O` selftests emitted byte-identical output with SHA-256
    `beaf5b2b9bcaa0b95ff053c8f6e0aa955d075d21d877460c52b779a68d60ca60`.
  - >-
    The frozen external driver hash is
    `3e5284fd56fd33f7b767954164128e9d43f5efad09eae4666035c3ef32c63f54`;
    the focused-test hash is
    `4226ab0cb5f9e46256b5fc47d5bc493dfbb6ef77354e9e7a61d624ba4db76a53`.
  - >-
    Independent W2 reproduced six focused tests, twenty-seven zero-skip guards, the
    frozen package manifest, byte-identical optimized receipt, absent output paths and
    synthetic equality with the frozen certificate assembler; no candidate file was
    edited during review.
  - >-
    The sole exp-052 process ran from 2026-09-01T13:27:39Z to the exact
    2026-09-01T14:41:55Z hard stop. One PTY interrupt returned exit 130; process-table
    checks found PIDs 30456 and 30540 absent, and the result path remained absent.
  - >-
    Read-only replay through the frozen driver validated 33 contiguous paired rows,
    ordinals 0--32, all agreement flags and manifests, the row-hash chain, and progress
    ordinal 33 at `independent_started`. The checkpoint and progress SHA-256 values are
    db5c156959b6de4e6f2c9be283454d01dd5f3a436e6489f5e6bb60c38559fdb8
    and 08e301b01c7ac6eef4b03c3a4daa5f72c5f1bdbe217dbbb061b57f5c94d947af.
  - >-
    Flowmark completed for both edited Markdown records; enforced softschema validation
    passed separately for session-068 and exp-052, and `git diff --check` found no
    whitespace defect in either file.
  resource_rollups:
  - packing/campaign/resource-usage/codex-task-tree-session-068.yaml
  stop_reason: >-
    BC-116 completed its 160-minute lane with a validated resumable prefix but no
    canonical result; exp-052 is executed-incomplete, unresolved and review-pending.
  next_action: >-
    Coordinator review may apply only the process transition. A continuation must be a
    newly preregistered resume round from ordinal 33; prefix agreement does not decide
    H-052 or alter the frontier.
---
# Session 068 — BC-116 `n = 17` Resumability

## Route and Evidentiary State

BC-116 is selected because BC-108 ended without the all-invariant agreement required to
enter BC-112. It is not selected because a discrepancy, `cannot-reproduce` result, or
premeasurement guard was observed.

Exp-049 ran exactly once from `2026-09-01T09:51:35Z` to its declared hard stop at
`2026-09-01T10:56:55Z`. One interrupt ended it with exit 130 while the independent
direct Cartesian accumulator was active.
The run emitted no canonical direction row, complete comparison, mutation result,
checkpoint, or result JSON. Its result path remains absent.
This is an executed midmeasurement `no_progress` process determination.
It does not measure H-052’s agreement criterion.

H-052 remains `instrument_ready: true` and scientifically unresolved.
Exp-049 remains `needs_review: true`. BC-112 is stopped for this wave because its
positive entry gate did not pass, not because the certificate was refuted.
Nothing in BC-116 adopts the proposed `4.5058` lower bound, transfers it to `n = 18` or
`n = 19`, validates the LP generator, or changes the frontier.

## Frozen Inputs

The new execution driver must refuse before target access unless every digest in this
section matches. The package-manifest digest is the SHA-256 of the sorted `sha256sum`
output for every Python file under `packing/cases/n17_weighted_certificate/`.

| Frozen input | SHA-256 |
| --- | --- |
| Retained-source `README.md` | `b48c0c31cf62366d44cd12f02cf321dd38b5a23391caec95f04445938e0b3d75` |
| `massaccesi-linear-programming.html` | `cdd27897f4f6c3b83835d59a317b3248b4f94b888f8568b740c778524a11f177` |
| `massaccesi-lower-bound-4_5058.html` | `7dffb6e6e6cbff0ac2e887ca445b45f46c95055718219f7229d1c8cb06f84514` |
| `massaccesi-verify-n17-lower-bound-4_5058.py` | `04531a54da9a654f2318401aff43222daf721bd99e948b2491f91c05bd0b5d3f` |
| Frozen Python package manifest | `309ec24158f73dd2e9b837c773b1e5c1642f357de5bdf73311b73232abdb6d54` |
| `extract.py` | `db176a8eff7235991c63c8e7f098e2e2979edf64905d8f76427e0cd218b011e2` |
| `fixture.py` | `3b37d03f311b62f6a2ad41b099629d6a1fcfaae9c9f0b6e8083065b80336995f` |
| `model.py` | `9321f6c7a43c2d2ffb72be4d540fcb91254fbdcfd63928c7da4927b7e14f96af` |
| `geometry.py` | `2b55425f9170af03ae577f5e291499628053aad365e0220a1cb3043c2515d3c1` |
| `independent.py` | `55d36239f1f7e860f059030d87f655d2ac0c82685d788b599a7dd23d33d18de0` |
| `source_faithful.py` | `aaccd145c61fb20bc2b83a8ded83dfdd3f2d4b6d6c730ff46df31e1f1d8ae305` |
| `target_independent.py` | `db86f6731180f8b82a9f54412c82713ac66ed9206458e222f8547574039a2ef0` |
| `run.py` | `177e8545400799b6a701f258b685f2712f2529132803d78bf984575b897d027c` |
| `selftest.py` | `4bfc564cf9cacbe8c50453ec30b41dadf134f1c3fec62f422fe699321426318d` |
| H-052 readiness revision | `156c0bbfaf8637e0a28077db541da2e8b2e34311fd3745b41292d899485f00b2` |
| Terminal exp-049 record | `f8bbb64a561198c07cfc80548014d090f5b6a9baf27e619017544979854abb92` |

The frozen fixture remains the retained Massaccesi certificate at exact side
`22529/5000`: 168 weighted atoms on a 29 by 29 grid, total mass `9744/576`, 181 ordered
rational directions, and claimed checked minimum `576/576`. These are retained fixture
values, not results newly established by this W3 cell.

## External Driver Boundary

W7 may create only a case-specific execution package at
`packing/cases/n17_weighted_certificate_resume/` and its focused test at
`packing/tests/test_n17_weighted_certificate_resume.py`. That package sits outside the
hash-frozen `packing/cases/n17_weighted_certificate/` directory.
It changes scheduling, atomic persistence, and recovery only.

The driver must:

1. verify every frozen input before loading target data;
2. call the existing `accumulate_source_faithful` and `accumulate_target_independent`
   per-direction functions without copying, replacing, memoizing, or changing their
   exact arithmetic;
3. reuse the frozen normalization, precondition, mutation, comparison, dataclass, and
   canonical-serialization semantics from the existing package rather than defining a
   favorable replacement;
4. preserve the fixture’s exact ordered direction sequence; and
5. keep the existing scientific kernels byte-for-byte unchanged after any target output
   becomes visible.

This is an observability and resumability capability, not a speedup or a new scientific
instrument. It does not supply the completed pre-change baseline that BC-122 found
missing and may not receive causal performance credit.

## Atomic Checkpoint and Resume Contract

The coordinator-assigned checkpoint has one immutable header and a contiguous prefix of
completed paired rows.

The header binds the eventual experiment id, H-052, session-068, all source digests, the
frozen package-manifest digest, exact fixture constants, ordered direction count and
hash, external-driver digest, result path, checkpoint path, and schema version.
A non-scientific progress marker is atomically replaced before each source or
independent stage. It may identify the active ordinal and stage, but it is not a
canonical row and cannot support an H-052 verdict.

For direction ordinal `k`, the driver may append a scientific checkpoint row only after
both unchanged accumulation functions return.
The row contains:

- ordinal `k` and the exact ordered direction;
- the complete source-faithful and independent `DirectionManifest` values;
- their exact equality decision;
- the previous paired-row hash; and
- a row hash over the canonical serialization of every preceding field.

The first row chains from a fixed genesis hash derived from the immutable header.
Each update writes a complete temporary checkpoint in the destination directory, flushes
it, and atomically replaces the prior checkpoint.
A partial temporary file never becomes a valid checkpoint.
Source-only or independent-only work may be named in the progress marker but is
recomputed after interruption and never counted as a completed row.

Resume must reverify every immutable input, the external-driver digest, header, genesis
hash, every row hash, the full previous-row chain, contiguous ordinals `0..k-1`, and the
exact direction at each ordinal.
It must reject a gap, duplicate, reordering, trailing partial row, malformed exact
value, stale digest, mismatched path, or changed schema.
It then starts at ordinal `k`; it may neither recompute and overwrite an accepted prefix
nor skip the first incomplete direction.

After 181 valid paired rows, the assembler reconstructs the two ordered
`CertificateManifest` values and the existing canonical exp-049 record semantics.
It then applies the unchanged precondition and five-mutation decisions.
A checkpoint is raw process evidence, not the experiment result.
Only the coordinator-assigned result path may carry the completed or typed scientific
determination.

## W7 Controls and W2 Readmission

All readiness work is target-blind.
Synthetic fixtures must show exact byte equality between the existing uninterrupted
assembly and the external driver’s uninterrupted and interrupted-plus-resumed
assemblies. Exercise interruptions at these boundaries:

- before the first paired row;
- after a source stage but before its independent partner;
- after at least one paired row; and
- after the final pair but before result assembly.

Named negative controls must reject a changed package, source or fixture digest; a wrong
direction ordinal; a missing, duplicated or reordered row; a changed previous-row hash;
a changed row payload; a truncated temporary file; a stale experiment or path binding;
and a malformed exact rational.
Normal and `python -O` readiness runs must emit byte-identical receipts and may not rely
on bare assertions.

The existing atom, weight, direction-cell, event-boundary, scaling, `/28` versus `/29`,
and omitted-final-endpoint controls remain frozen.
W7 does not weaken or reinterpret them.

A fresh W2 reviewer must independently confirm all of the following before W6:

- the original package-manifest and clean-room hashes are unchanged;
- the external driver imports the frozen functions and does not translate or bypass
  either accumulator;
- the checkpoint cannot turn partial or reordered work into a canonical row;
- every named synthetic equivalence and corruption control ran with zero skips; and
- the next experiment, result, checkpoint, progress, session, and driver hashes agree
  across the preregistration and readiness receipt.

Any failed W7 or W2 guard closes target access.
It leaves the existing H-052 instrument readiness intact, terminalizes the new round as
a typed premeasurement stop, and creates no target result.

## Fixed 160-Minute Lane

The lane begins at `2026-09-01T12:16:55Z` and ends at `2026-09-01T14:56:55Z`. The clocks
do not slide if a prerequisite returns late.

| Offset and UTC interval | Minutes | Workflow | Frozen work |
| --- | ---: | --- | --- |
| 0–15, 12:16:55–12:31:55 | 15 | W3 | Freeze this process and resume contract without target access or experiment allocation |
| 15–35, 12:31:55–12:51:55 | 20 | W7 | Build the external direction-sliced driver and atomic checkpoint writer |
| 35–55, 12:51:55–13:11:55 | 20 | W7 | Pass synthetic uninterrupted/resume equivalence and corruption controls; freeze the driver |
| 55–70, 13:11:55–13:26:55 | 15 | W2 | Independently replay readiness and admit or refuse W6 |
| 70–95, 13:26:55–13:51:55 | 25 | W6 | Start the sole preregistered target process and retain completed paired rows |
| 95–120, 13:51:55–14:16:55 | 25 | W6 | Continue the same process; record Artifact, Result, Guard, and Next without rerun |
| 120–145, 14:16:55–14:41:55 | 25 | W6 | Continue to immutable result or the fixed hard stop; run only frozen controls after completion |
| 145–160, 14:41:55–14:56:55 | 15 | W3 | Interpret immutable output or retained prefix, validate records, and hand off |

The coordinator must assign the next free experiment id, materialize the exact paths,
append the W7 phase, and authorize it before the 15–35 cell begins.
Before W6, the same coordinator must append an admitted measurement phase after W2. The
target process runs once across all three W6 cells.
Cell boundaries are reporting points, not permission to stop or restart it.
If it remains live at `14:41:55Z`, send one interrupt, confirm it is gone, retain the
last valid prefix and do not rerun.

## Typed Outcomes

- **W7 or W2 premeasurement stop:** retain the first failed guard, no target sample, no
  result JSON, and no H-052 disposition.
  The original instrument remains ready; the new execution driver does not.
- **Midmeasurement deadline with a valid prefix:** retain the exact prefix, active-stage
  marker, elapsed cost and restart ordinal as an unresolved process result with
  `needs_review: true`. This is not a discrepancy, guard failure, or H-052 verdict.
- **Post-start checkpoint or instrument failure:** preserve the first exact failure as
  `unresolved-invalid-instrument`; do not repair or rerun after seeing target-derived
  data.
- **Exact paired-row disagreement:** preserve the first unequal row.
  H-052 may be proposed rejected only if every provenance, independence, known-answer
  and mutation guard passes; otherwise the result is unresolved.
- **Complete agreement:** propose H-052 accepted only after all 181 paired rows, all
  frozen fixture values, preconditions and mutations pass.
  The result remains `needs_review: true` and does not authorize adoption.

## Future Paths and Exclusive Scope

This W3 cell allocates no experiment id.
`exp-NNN` below means the next globally free id that the coordinator assigns serially;
it is a placeholder, not a reservation.
The slug and one-id correspondence are frozen:

- experiment:
  `packing/campaign/series/series-000-smoke-and-calibration/experiments/exp-NNN-h-052-n17-resumable-certificate-agreement.md`;
- result:
  `packing/campaign/series/series-000-smoke-and-calibration/results/exp-NNN-h-052-n17-resumable-certificate-agreement.json`;
- checkpoint:
  `packing/campaign/series/series-000-smoke-and-calibration/results/exp-NNN-h-052-n17-resumable-certificate-agreement.checkpoint.json`;
  and
- progress marker:
  `packing/campaign/series/series-000-smoke-and-calibration/results/exp-NNN-h-052-n17-resumable-certificate-agreement.progress.json`.

After coordinator allocation, the lane’s exclusive write scope is:

- `packing/cases/n17_weighted_certificate_resume/`;
- `packing/tests/test_n17_weighted_certificate_resume.py`;
- this session;
- the one assigned experiment, result, checkpoint, and progress-marker paths; and
- the instrument/readiness fields only in
  `packing/campaign/hypotheses/H-052-n17-independent-certificate-agreement.md`, after W7
  and W2 pass.

The lane must not edit `packing/cases/n17_weighted_certificate/`, exp-049, either
agenda, generated views, resource receipts, frontier or strategy records, tbd state, Git
state, or the pull request.
The coordinator owns shared records, id allocation and terminal resource receipt.

## 0–15 W3 Cell Close

- **Artifact:** This enforced session records the actual exp-049 refusal, immutable
  hashes, external-driver boundary, checkpoint schema, resume rules, controls, full lane
  clock, typed outcomes, future path convention, and write scope.
- **Result:** The target-blind contract is complete.
  No experiment id or target result was allocated, opened, or executed.
  H-052 and exp-049 are unchanged.
- **Guard:** All four retained-source hashes and the frozen package-manifest digest were
  recomputed and match session-065. A presence-only check found the exp-049 result path
  absent. Only session-068 was edited.
- **Next:** Return this contract to the coordinator.
  Do not begin W7 until the coordinator assigns the next free experiment id, creates the
  exact preregistration, appends the next phase, and explicitly authorizes it.

## 15–35 W7 Cell Close

- **Artifact:** `packing/cases/n17_weighted_certificate_resume/` now contains the
  external direction-sliced driver and atomic checkpoint core; its focused synthetic
  tests live in `packing/tests/test_n17_weighted_certificate_resume.py`.
- **Result:** All five implemented target-blind tests passed.
  The checkpoint binds exp-052, H-052, session-068, source and package digests, exact
  fixture and direction hashes, the current driver revision, and all three assigned
  paths. It accepts only a contiguous hash-chained prefix of complete source/independent
  pairs and resumes at the first incomplete direction.
- **Guard:** The frozen package-manifest digest remains
  `309ec24158f73dd2e9b837c773b1e5c1642f357de5bdf73311b73232abdb6d54`. No target fixture
  was loaded or executed; the real exp-052 result, checkpoint and progress paths remain
  absent. Ruff and BasedPyright passed, and no file under the frozen package changed.
- **Next:** Stop for authorization of the fixed 35–55 W7 cell.
  The readiness residue is the production command-line adapter and assembler, the
  complete interruption and mutation matrix, an explicit non-assert selftest with
  byte-identical normal and `python -O` receipts, and the final frozen
  driver/package/path receipt.
  Until those pass and W2 admits the revision, W6 remains closed and H-052 readiness is
  unchanged.

## 35–55 W7 Cell Close

- **Artifact:** The production candidate at
  `packing/cases/n17_weighted_certificate_resume/run.py` implements the exact exp-052
  command, three repository-relative output bindings, atomic result assembly, strict
  checkpoint and progress replay, and a non-assert synthetic readiness selftest.
- **Result:** Six focused tests passed.
  The selftest exercised twenty-seven zero-skip guards, including interruption before
  row zero, between accumulators, after a paired row and after the final pair before
  assembly; changed input; gap, duplicate, reorder, chain, payload, event-hash,
  manifest-label, truncation and malformed-rational corruption; stale, future and
  malformed progress; a final-checkpoint/pre-unlink crash with validated stale-marker
  removal before publication; existing-result refusal in both checkpoint states; and
  exact production-path binding.
- **Guard:** Normal and optimized Python emitted byte-identical receipt SHA-256
  `beaf5b2b9bcaa0b95ff053c8f6e0aa955d075d21d877460c52b779a68d60ca60`. The external
  driver is `3e5284fd56fd33f7b767954164128e9d43f5efad09eae4666035c3ef32c63f54` and the
  focused test is `4226ab0cb5f9e46256b5fc47d5bc493dfbb6ef77354e9e7a61d624ba4db76a53`.
  The frozen scientific package remains
  `309ec24158f73dd2e9b837c773b1e5c1642f357de5bdf73311b73232abdb6d54`. No target fixture
  or output was opened or executed, and all three real exp-052 output paths remain
  absent.
- **Next:** Stop for independent W2 review.
  W2 must confirm this exact revision and receipt before the coordinator may append or
  authorize W6; H-052 and exp-052 remain review-pending.

## Final W3 — Executed Incomplete

- **Artifact:** The sole exp-052 process ran from `2026-09-01T13:27:39Z` to the exact
  `2026-09-01T14:41:55Z` hard stop.
  One PTY interrupt returned exit 130 with a `KeyboardInterrupt` inside the unchanged
  independent accumulator.
  Both process IDs were absent afterward.
  The result path is absent.
- **Result:** Frozen-driver replay validates 33 contiguous paired rows, ordinals 0--32,
  all with exact source/independent agreement.
  The last row hash is
  `9badcc57c05e328344b0ec7ae4fbf9815e8eae027a79bec1bf1a35b9871fade6`; progress ordinal
  33 is at `independent_started` and chains to that hash.
  The checkpoint and progress SHA-256 values are
  `db5c156959b6de4e6f2c9be283454d01dd5f3a436e6489f5e6bb60c38559fdb8` and
  `08e301b01c7ac6eef4b03c3a4daa5f72c5f1bdbe217dbbb061b57f5c94d947af`.
- **Guard:** The replay accepted the exact exp-052 binding, canonical serialization,
  frozen input digests, direction order, manifests, event hashes, row hashes,
  previous-row chain, agreement flags and nonfuture progress marker.
  No target work was resumed.
  Prefix agreement is not a sample-based H-052 decision: 148 paired directions and the
  frozen precondition and mutation decisions remain incomplete.
- **Next:** Exp-052 is executed-incomplete, scientifically unresolved and
  `needs_review: true`. Coordinator review may apply only that process transition and
  generate `packing/campaign/resource-usage/codex-task-tree-session-068.yaml`. Any
  continuation requires a newly preregistered resume round from ordinal 33; this lane
  makes no H-052 or frontier change.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
