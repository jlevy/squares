---
title: session-075 — BC-125 n = 50 producer refusal ordering
softschema:
  contract: packing.squares:AgentSession/v2
  schema: ../schemas/agent-session.schema.yaml
  envelope: session
  status: enforced
session:
  id: session-075
  title: BC-125 n = 50 producer refusal ordering
  date: '2026-09-01'
  started_at: '2026-09-02T00:15:00Z'
  deadline_at: '2026-09-02T02:45:00Z'
  branch: codex/agenda014-six-hour-run
  goal: >-
    Verify prospectively that the hash-bound frozen n = 50 producer refuses an existing
    result before binding observation, fixture loading, receipt evaluation or
    publication, without changing exp-050.
  workflow_phases:
  - workflow: insight-iteration
    focus: correctness
    recording: contemporaneous
    clock_role: work
    objective: >-
      Bind the frozen producer, result, exp-050, session-070 and H-059 hashes; freeze the
      four live sentinel seams, exact refusal, fresh paths and normal/optimized mutation
      matrix before implementation.
    commitment: BC-125
    bead: think-17q7
    status: completed
    entered_by: session_start
    switch_reason: null
    budget_minutes: 15
    started_at: '2026-09-02T00:15:00Z'
    deadline_at: '2026-09-02T00:30:00Z'
    expected_output: A validated exp-055 sentinel and provenance contract with exp-050 read-only.
    validation_command: >-
      uv run --frozen softschema validate
      campaign/series/series-000-smoke-and-calibration/experiments/exp-055-h-059-n50-producer-refusal-ordering.md
    kill_condition: >-
      Stop if a frozen hash differs, an ordinary import would load the real intake before
      injection, a sentinel lacks liveness calibration, or source or geometry access is required.
    fallback: Retain the exact provenance or injection defect and stop before W7.
    outcome: >-
      Artifact: the frozen W3 contract in exp-055 and this session. Result: launch
      revision 909efafa0773fbea23b24de072ef59a03a01317a, the producer, exp-050 result,
      exp-050 record, session-070 and H-059 matched their preregistered identities; both
      enforced records validated and the exp-055 result path was absent. Guard: no
      producer import, intake, source or geometry access occurred. Next: build the
      separate fake-module sentinel harness and its liveness calibrations in W7.
    evidence:
    - packing/campaign/series/series-000-smoke-and-calibration/experiments/exp-055-h-059-n50-producer-refusal-ordering.md
    stop_reason: W3 contract and frozen binding checks completed at the declared boundary.
    next_action: Build only the separate target-blind sentinel harness in the first W7 cell.
  - workflow: pipeline-improvement
    focus: correctness
    recording: contemporaneous
    clock_role: work
    objective: >-
      Build the isolated fake-module import seam, four live sentinels, canonical receipt
      and no-overwrite publisher without running exp-055 or opening a real intake.
    commitment: BC-125
    bead: think-17q7
    status: completed
    entered_by: evidence_checkpoint
    switch_reason: The W3 hashes, fresh path and preregistered criterion all validated.
    budget_minutes: 15
    started_at: '2026-09-02T00:30:00Z'
    deadline_at: '2026-09-02T00:45:00Z'
    expected_output: A target-blind four-sentinel harness with one-call liveness calibration.
    validation_command: >-
      uv run --frozen --all-extras --group dev pytest -q
      tests/test_n050_producer_refusal.py
    kill_condition: >-
      Stop if fake-module injection cannot precede dynamic producer import, any real intake
      loads, a sentinel cannot prove liveness or a path outside the exclusive scope is needed.
    fallback: Retain the exact injection defect and stop exp-055 before measurement.
    outcome: >-
      Artifact: the fake-module harness, controller and focused target-blind tests. Result:
      the producer and immutable result were hash-bound before dynamic import; the fake
      intake was installed first; all four sentinels fired exactly once in isolated
      calibrations; and the existing-result branch produced the exact canonical zero-call
      trace under normal and optimized Python without changing exp-050. Guard: no real
      intake, source, geometry or network seam opened, and the exp-055 result stayed
      absent. Next: freeze the full executable closure and fire every registered mutation.
    evidence:
    - packing/cases/n050_producer_refusal/
    - packing/tests/test_n050_producer_refusal.py
    stop_reason: The separate injected harness and four live sentinel seams passed their focused controls.
    next_action: Run the complete registered mutation matrix and freeze the instrument hashes.
  - workflow: pipeline-improvement
    focus: correctness
    recording: contemporaneous
    clock_role: work
    objective: >-
      Freeze the complete executable closure, fire changed-runner, changed-result,
      reordered-stage, missing-sentinel, changed-refusal and overwrite mutations, and
      prove normal/optimized controller equivalence while exp-055 remains unmeasured.
    commitment: BC-125
    bead: think-17q7
    status: completed
    entered_by: evidence_checkpoint
    switch_reason: The fake-module injection and four sentinel liveness guards passed.
    budget_minutes: 15
    started_at: '2026-09-02T00:45:00Z'
    deadline_at: '2026-09-02T01:00:00Z'
    expected_output: A hash-frozen instrument whose full mutation matrix rejects deterministically.
    validation_command: >-
      uv run --frozen pytest -q tests/test_n050_producer_refusal.py && uv run
      --frozen ruff check cases/n050_producer_refusal
      tests/test_n050_producer_refusal.py && uv run --frozen basedpyright
      cases/n050_producer_refusal tests/test_n050_producer_refusal.py
    kill_condition: >-
      Stop if any named mutation survives, normal and optimized bytes differ, the
      executable closure is incomplete or exp-050 changes.
    fallback: Retain the first typed W7 defect and stop before W2 or W6.
    outcome: >-
      Artifact: the frozen controller, harness, verifier and two focused test modules.
      Result: changed-runner, changed-result, all four reordered-stage, all four
      missing-sentinel, changed-refusal and overwrite mutations rejected; three normal
      and three optimized controller runs produced identical prospective SHA-256
      9c90a04e5691f168f042a455780cbdd5a66eac248e617930b79d084496a8654c;
      and the 13 W7 tests, Ruff and BasedPyright passed. Guard: exp-050 retained SHA-256
      ab00e50debe0bc60279ce3472ed0c09eb062e8271a481a38c6ac65036aff4a02,
      exp-055 remained absent and no ephemeral path entered the receipt. Next: admit the
      closure with the separately implemented no-import verifier in W2.
    evidence:
    - packing/cases/n050_producer_refusal/
    - packing/tests/test_n050_producer_refusal.py
    stop_reason: The full deterministic mutation matrix and executable-closure guards passed.
    next_action: Run the independent no-import W2 admission under normal and optimized Python.
  - workflow: factual-review
    focus: correctness
    recording: contemporaneous
    clock_role: work
    objective: >-
      Independently admit the frozen prospective receipt without importing the harness
      or producer, under normal and optimized Python, and fire the verifier's named
      structural, binding, trace, review-state and mutation-inventory corruptions.
    commitment: BC-125
    bead: think-17q7
    status: completed
    entered_by: evidence_checkpoint
    switch_reason: The complete W7 mutation matrix and interpreter-equivalence guards passed.
    budget_minutes: 15
    started_at: '2026-09-02T01:00:00Z'
    deadline_at: '2026-09-02T01:15:00Z'
    expected_output: An independent W2 admission decision and exact H-059 readiness binding.
    validation_command: >-
      uv run --frozen pytest -q tests/test_n050_producer_refusal_independent.py
    kill_condition: >-
      Stop premeasurement if the verifier imports the harness or producer, differs under
      optimized Python, accepts a named mutation or finds any frozen binding mismatch.
    fallback: Retain the first typed independent-admission defect and leave H-059 unready.
    outcome: >-
      Artifact: independent verifier SHA-256
      950fd4a4c41224792742d11e5e6b3f2caeeb4937204d680671892ba28820a0df
      and its focused tests. Result: eight independent tests passed in 4.75 seconds;
      normal and optimized verification receipts agreed at SHA-256
      64d37a00c43384033adedc94e1c4ba42ad1010a6f419d5b17f07c14265b73ccc;
      the verifier imported neither harness nor producer and rejected all five named
      receipt corruptions. H-059 became instrument-ready with SHA-256
      3ffd27df1cd7b387ac7b17fbce782f0ca0d39019c2bd01f6facb8f2ef41cccd9.
      Guard: exp-055 remained absent through W2, exp-050 was unchanged and the
      coordinator independently replayed 21 focused tests before authorizing W6 at
      01:05:44Z. Next: execute the registered command once without changing instrument code.
    evidence:
    - packing/cases/n050_producer_refusal/verify.py
    - packing/tests/test_n050_producer_refusal_independent.py
    - packing/campaign/hypotheses/H-059-n50-producer-refusal-ordering.md
    stop_reason: Every independent admission and readiness guard passed before measurement.
    next_action: Execute the exact registered exp-055 command once in W6.
  - workflow: research-loop
    focus: correctness
    recording: contemporaneous
    clock_role: work
    objective: >-
      Execute the registered exp-055 command exactly once into the absent fresh result,
      retain the first outcome without repair or rerun and recheck exp-050 immediately.
    commitment: BC-125
    bead: think-17q7
    status: completed
    entered_by: evidence_checkpoint
    switch_reason: >-
      W2 admitted the frozen instrument, H-059 became ready and the coordinator explicitly
      authorized W6 after an independent replay at 2026-09-02T01:05:44Z.
    budget_minutes: 15
    started_at: '2026-09-02T01:15:00Z'
    deadline_at: '2026-09-02T01:30:00Z'
    expected_output: One immutable exp-055 result or the first typed one-shot W6 failure.
    validation_command: >-
      uv run --frozen python -m cases.n050_producer_refusal.run --record
      campaign/series/series-000-smoke-and-calibration/results/exp-055-h-059-n50-producer-refusal-ordering.json
    kill_condition: >-
      Stop after the single process exits, whether it publishes or fails; never repair,
      rerun or replace the result, and stop if exp-050 changes.
    fallback: Retain the first typed W6 failure with no result repair or second measurement.
    outcome: >-
      Artifact: immutable exp-055 result SHA-256
      9c90a04e5691f168f042a455780cbdd5a66eac248e617930b79d084496a8654c,
      5,211 bytes. Result: the one authorized command exited zero in 0.72 seconds and
      published the preregistered criterion-met receipt exactly once. Guard: exp-050
      retained SHA-256
      ab00e50debe0bc60279ce3472ed0c09eb062e8271a481a38c6ac65036aff4a02;
      every instrument hash remained frozen; no repair, rerun, source, geometry or real
      intake access followed the one-shot process. Next: verify the retained result under
      normal and optimized Python with only the independent no-import verifier.
    evidence:
    - packing/campaign/series/series-000-smoke-and-calibration/results/exp-055-h-059-n50-producer-refusal-ordering.json
    - packing/campaign/series/series-000-smoke-and-calibration/experiments/exp-055-h-059-n50-producer-refusal-ordering.md
    stop_reason: The sole registered W6 process published one immutable result and exited zero.
    next_action: Independently verify the retained result without importing harness or producer.
  - workflow: factual-review
    focus: correctness
    recording: contemporaneous
    clock_role: work
    objective: >-
      Verify the retained exp-055 result under normal and optimized Python using only the
      frozen independent verifier, recheck all bound hashes and preserve needs_review true.
    commitment: BC-125
    bead: think-17q7
    status: completed
    entered_by: evidence_checkpoint
    switch_reason: The sole W6 process exited zero and published the immutable fresh result.
    budget_minutes: 15
    started_at: '2026-09-02T01:30:00Z'
    deadline_at: '2026-09-02T01:45:00Z'
    expected_output: Byte-identical normal and optimized independent verification receipts.
    validation_command: >-
      uv run --frozen python -m cases.n050_producer_refusal.verify
      campaign/series/series-000-smoke-and-calibration/results/exp-055-h-059-n50-producer-refusal-ordering.json
    kill_condition: >-
      Retain the first discrepancy and stop before experiment or session terminalization;
      never run the producer, harness or record command again.
    fallback: Report the exact immutable-result verification discrepancy for coordinator review.
    outcome: >-
      Artifact: independent verification of the immutable exp-055 result. Result: normal
      and optimized verifier processes each exited zero in 0.07 seconds and emitted
      byte-identical canonical receipt SHA-256
      64d37a00c43384033adedc94e1c4ba42ad1010a6f419d5b17f07c14265b73ccc,
      binding result SHA-256
      9c90a04e5691f168f042a455780cbdd5a66eac248e617930b79d084496a8654c,
      producer SHA-256
      52baeb1b6ad52aa504498ba21aeb6b3d361aaaec2461c76904a357d8d95cf29d
      and exp-050 SHA-256
      ab00e50debe0bc60279ce3472ed0c09eb062e8271a481a38c6ac65036aff4a02.
      Guard: neither verifier process imported the harness or producer; needs_review
      remained true; no result or instrument byte changed. Next: terminalize exp-055 and
      this session with the narrow claim boundary unchanged.
    evidence:
    - packing/cases/n050_producer_refusal/verify.py
    - packing/campaign/series/series-000-smoke-and-calibration/results/exp-055-h-059-n50-producer-refusal-ordering.json
    stop_reason: Normal and optimized independent verification passed byte-identically.
    next_action: Retain the accepted but review-pending experiment and terminal session record.
  - workflow: insight-iteration
    focus: correctness
    recording: contemporaneous
    clock_role: work
    objective: >-
      Terminalize exp-055 and session-075 from the immutable result and independent
      review, preserving needs_review true and the prospective-protocol limitation.
    commitment: BC-125
    bead: think-17q7
    status: completed
    entered_by: evidence_checkpoint
    switch_reason: >-
      The retained result passed normal and optimized independent verification, and the
      coordinator independently replayed the same evidence before authorizing closeout.
    budget_minutes: 60
    started_at: '2026-09-02T01:45:00Z'
    deadline_at: '2026-09-02T02:00:00Z'
    expected_output: A terminal accepted-but-review-pending exp-055 and complete session-075.
    validation_command: >-
      uv run --frozen softschema validate
      campaign/series/series-000-smoke-and-calibration/experiments/exp-055-h-059-n50-producer-refusal-ordering.md
      && uv run --frozen softschema validate
      campaign/agent-sessions/session-075-bc125-n50-producer-refusal-ordering.md
    kill_condition: >-
      Stop if terminal prose clears review, broadens the claim, changes any frozen hash
      or requires another producer, harness or result execution.
    fallback: Retain the immutable evidence and report the exact terminal-record schema defect.
    outcome: >-
      Artifact: terminal exp-055, immutable result and complete session-075. Result:
      exp-055 is accepted with needs_review true from result SHA-256
      9c90a04e5691f168f042a455780cbdd5a66eac248e617930b79d084496a8654c
      and byte-identical normal/optimized independent verification SHA-256
      64d37a00c43384033adedc94e1c4ba42ad1010a6f419d5b17f07c14265b73ccc.
      Guard: the decision covers only H-059's prospective existing-result refusal
      ordering; it does not repair exp-050, clear any review, change H-054, establish n
      = 50 feasibility or authorize source or geometry work. Next: independent campaign
      review may clear or challenge exp-055's review flag without rerunning this round.
    evidence:
    - packing/campaign/series/series-000-smoke-and-calibration/experiments/exp-055-h-059-n50-producer-refusal-ordering.md
    - packing/campaign/agent-sessions/session-075-bc125-n50-producer-refusal-ordering.md
    stop_reason: >-
      The terminal records validated from the immutable result and coordinator replay;
      the coordinator requested immediate closeout before the reserved window expired.
    next_action: Hand the immutable accepted-but-review-pending record to independent campaign review.
  primary_bead: think-17q7
  status: completed
  budget:
    wall_minutes: 150
    max_cycles: 7
    checkpoint_minutes: 20
    slice_minutes: 20
    finalization_minutes: 35
  stop_conditions:
  - Active BC-125 work reaches the fixed 2026-09-02T02:10:00Z cap.
  - The common 2026-09-02T02:45:00Z first-wave deadline arrives.
  - A frozen binding changes, exp-050 bytes move or a real source or geometry seam opens.
  - A sentinel calibration, mutation, interpreter-equivalence or independent-verifier guard fails.
  progress:
    metric: independently verified zero-call producer refusal receipts
    before: zero; exp-050 has a bounded unclosed producer-provenance gap
    after: one immutable independently verified zero-call producer refusal receipt
  delegations: []
  outputs:
  - packing/campaign/agent-sessions/session-075-bc125-n50-producer-refusal-ordering.md
  - packing/campaign/series/series-000-smoke-and-calibration/experiments/exp-055-h-059-n50-producer-refusal-ordering.md
  - packing/campaign/hypotheses/H-059-n50-producer-refusal-ordering.md
  - packing/campaign/series/series-000-smoke-and-calibration/results/exp-055-h-059-n50-producer-refusal-ordering.json
  - packing/cases/n050_producer_refusal/
  - packing/tests/test_n050_producer_refusal.py
  - packing/tests/test_n050_producer_refusal_independent.py
  - packing/campaign/resource-usage/codex-task-tree-session-075.yaml
  checks:
  - >-
    At 2026-09-02T00:29:46Z, the launch revision and all frozen W3 hashes matched;
    session-075 and exp-055 validated, and the fresh result path was absent.
  - >-
    At 2026-09-02T00:45:00Z, 12 focused harness tests passed; Ruff and BasedPyright
    passed; all four isolated sentinels were live; normal/optimized controller bytes
    agreed; exp-050 retained SHA-256 ab00e50debe0bc60279ce3472ed0c09eb062e8271a481a38c6ac65036aff4a02;
    and the exp-055 result remained absent.
  - >-
    At 2026-09-02T01:00:00Z, 13 focused W7 tests passed in 2.41 seconds; Ruff and
    BasedPyright passed; every registered mutation rejected; three normal and three
    optimized prospective receipts had SHA-256
    9c90a04e5691f168f042a455780cbdd5a66eac248e617930b79d084496a8654c;
    and exp-055 remained absent.
  - >-
    Before the W2 readiness transition, the coordinator repaired session-072's BC-125
    files and write_scope to include H-059, reconciling the launch omission with
    Agenda-014 while exp-055 was still absent.
  - >-
    At 2026-09-02T01:05:44Z, the coordinator independently replayed 21 focused tests,
    Ruff, BasedPyright, every frozen hash and normal/optimized no-import verification,
    confirmed exp-055 absent and explicitly authorized the one-shot W6 command.
  - >-
    At 2026-09-02T01:15:39Z, the one-shot registered W6 command exited zero in 0.72
    seconds and published one 5,211-byte result with SHA-256
    9c90a04e5691f168f042a455780cbdd5a66eac248e617930b79d084496a8654c;
    exp-050 remained ab00e50debe0bc60279ce3472ed0c09eb062e8271a481a38c6ac65036aff4a02.
  - >-
    At 2026-09-02T01:30:44Z, normal and optimized no-import verification each exited
    zero in 0.07 seconds and emitted byte-identical SHA-256
    64d37a00c43384033adedc94e1c4ba42ad1010a6f419d5b17f07c14265b73ccc.
  - >-
    The coordinator independently replayed the retained result and authorized exact
    accepted-but-review-pending terminalization; no producer, harness or result command
    ran during W3.
  resource_rollups:
  - packing/campaign/resource-usage/codex-task-tree-session-075.yaml
  stop_reason: >-
    BC-125 answered H-059's prospective protocol question and terminalized from the
    immutable result; no lane work remains.
  next_action: Independent campaign review may clear or challenge exp-055 needs_review without rerunning it.
---
# Session-075 — BC-125 `n = 50` Producer Refusal Ordering

A zero-call trace counts only after each sentinel fires in a separate synthetic
calibration. The independent verifier imports neither the new harness nor the frozen
producer.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
