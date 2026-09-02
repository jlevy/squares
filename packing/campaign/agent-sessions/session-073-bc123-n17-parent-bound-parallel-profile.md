---
title: session-073 — BC-123 n = 17 parent-bound parallel profile
softschema:
  contract: packing.squares:AgentSession/v2
  schema: ../schemas/agent-session.schema.yaml
  envelope: session
  status: enforced
session:
  id: session-073
  title: BC-123 n = 17 parent-bound parallel profile
  date: '2026-09-01'
  started_at: '2026-09-02T00:27:47Z'
  deadline_at: '2026-09-02T02:45:00Z'
  branch: codex/agenda014-six-hour-run
  goal: >-
    Build, independently admit and run exp-053's exact three-pair fixed-input profile,
    preserving every complete pair and stopping all child processes at the common wall.
  workflow_phases:
  - workflow: insight-iteration
    focus: efficiency
    recording: contemporaneous
    clock_role: work
    objective: >-
      Recheck the immutable exp-052 checkpoint, progress, kernels and parent row; bind
      exp-053, session-073, the profile-only fragment schema, exact commands and
      corruption guards before implementation.
    commitment: BC-123
    bead: think-p2m6
    status: completed
    entered_by: session_start
    switch_reason: null
    budget_minutes: 15
    started_at: '2026-09-02T00:27:47Z'
    deadline_at: '2026-09-02T00:42:47Z'
    expected_output: A hash-bound exp-053 implementation and measurement contract with no target command run.
    validation_command: >-
      uv run --frozen softschema validate
      campaign/series/series-000-smoke-and-calibration/experiments/exp-053-h-057-n17-parent-bound-parallel-speedup.md
    kill_condition: >-
      Stop if any exp-052 input moved, the proposed chain could be mistaken for a
      continuation checkpoint, identifiers or paths overlap, or the profile regime is
      not isolated from concurrent heavy commands.
    fallback: Retain the exact frozen-input or regime defect and stop before implementation.
    outcome: >-
      Bound exp-053 to launch revision 909efafa, the unchanged exp-052 checkpoint and
      progress digests, parent binding and row hashes, retained fixture and direction
      hashes, fixed ordinals 33, 107 and 180, three workers, AB/BA/AB order and the 2.8x
      threshold. Both enforced artifacts validated, every output path remained absent,
      and no target computation ran.
    evidence:
    - packing/campaign/series/series-000-smoke-and-calibration/experiments/exp-053-h-057-n17-parent-bound-parallel-speedup.md
    stop_reason: The 15-minute frozen-input and measurement contract validated.
    next_action: Enter the external per-direction profiler W7 cell with no target run.
  - workflow: pipeline-improvement
    focus: correctness
    recording: contemporaneous
    clock_role: work
    objective: >-
      Build the external exact per-direction profile core, parent replay gate and serial
      arm around direct imports of both unchanged accumulators, without evaluating a
      retained target direction.
    commitment: BC-123
    bead: think-p2m6
    status: completed
    entered_by: planned_checkpoint
    switch_reason: >-
      The W3 contract validated at its observed 15-minute boundary with every frozen
      digest unchanged and all exp-053 output paths absent.
    budget_minutes: 20
    started_at: '2026-09-02T00:42:51Z'
    deadline_at: '2026-09-02T01:02:51Z'
    expected_output: >-
      A target-blind per-direction runner that replays the parent boundary, imports both
      exact kernels and produces a canonical serial-arm fragment set.
    validation_command: >-
      uv run --frozen --all-extras --group dev pytest -q
      tests/test_n17_weighted_certificate_parallel.py
    kill_condition: >-
      Stop if an exp-052 path is writable, a retained direction is evaluated, either
      kernel is translated, or the runner cannot bind its output beneath the fresh
      exp-053 raw root.
    fallback: Retain the first exact interface or provenance defect and leave W2 and W6 closed.
    outcome: >-
      Added the hash-bound external runner and benchmark adapter. The runner replays the
      exact 33-row parent and progress marker, directly imports both unchanged kernels,
      confines outputs to the exp-053 raw root, publishes fragments exclusively, and
      validates a complete canonical serial-arm merge. Three focused tests passed in
      0.12 seconds; Ruff and BasedPyright passed with zero skips.
    evidence:
    - packing/cases/n17_weighted_certificate_parallel/
    - packing/benchmarks/n17_weighted_certificate_parallel.py
    stop_reason: The target-blind serial profiler core and parent replay gate passed.
    next_action: Exercise three spawned workers, durable completed arms and interrupted cleanup.
  - workflow: pipeline-improvement
    focus: correctness
    recording: contemporaneous
    clock_role: work
    objective: >-
      Exercise the three-process spawn path on synthetic exact inputs, prove each worker
      writes only its preassigned fragment, and verify interruption cleanup preserves
      completed arms without re-execution.
    commitment: BC-123
    bead: think-p2m6
    status: completed
    entered_by: evidence_checkpoint
    switch_reason: >-
      The external serial profile core passed its focused tests and static checks with
      the retained target still unevaluated.
    budget_minutes: 20
    started_at: '2026-09-02T00:57:56Z'
    deadline_at: '2026-09-02T01:17:56Z'
    expected_output: >-
      Byte-identical synthetic serial and spawned-parallel fragment sets plus durable
      interruption, resume and child-cleanup receipts.
    validation_command: >-
      uv run --frozen --all-extras --group dev pytest -q
      tests/test_n17_weighted_certificate_parallel.py
    kill_condition: >-
      Stop if a worker can escape its assigned path, any child survives a failure,
      parallel bytes differ from serial, or a resumed pair reruns a completed arm.
    fallback: Retain the first process-boundary defect and leave deterministic merge, W2 and W6 closed.
    outcome: >-
      Three spawned workers produced fragment and merged SHA-256 lists identical to the
      serial arm on three synthetic directions. Durable arms replayed without changing
      their receipt bytes. An injected misbound worker path raised, terminated and
      joined the pool, removed its partial arm, left no child process, and preserved the
      completed serial arm; stale cleanup remained confined to its pair root. Six
      focused tests passed in 0.42 seconds with zero static warnings.
    evidence:
    - packing/cases/n17_weighted_certificate_parallel/runner.py
    - packing/tests/test_n17_weighted_certificate_parallel.py
    stop_reason: The 15-minute spawned-worker, interruption and cleanup cell passed.
    next_action: Fire every deterministic merge and corruption refusal before W2.
  - workflow: pipeline-improvement
    focus: correctness
    recording: contemporaneous
    clock_role: work
    objective: >-
      Complete the deterministic single-writer merger, fire gap, duplicate, reorder,
      foreign-parent, partial-row, event-hash and serialization mutations, and compare
      normal and optimized synthetic selftest receipts.
    commitment: BC-123
    bead: think-p2m6
    status: completed
    entered_by: evidence_checkpoint
    switch_reason: >-
      Spawned-worker exactness, interruption cleanup and completed-arm replay passed
      without evaluating a retained direction.
    budget_minutes: 15
    started_at: '2026-09-02T01:13:01Z'
    deadline_at: '2026-09-02T01:28:01Z'
    expected_output: >-
      One deterministic zero-skip selftest receipt, byte-identical under normal and
      optimized Python, with every preregistered corruption mutation observed rejecting.
    validation_command: >-
      uv run --frozen python -m benchmarks.n17_weighted_certificate_parallel selftest
      && uv run --frozen python -O -m benchmarks.n17_weighted_certificate_parallel selftest
    kill_condition: >-
      Stop if a malformed fragment reaches a merged arm, row order depends on completion
      order, normal and optimized receipts differ, or any check degrades to a skip.
    fallback: Retain the first nonrejecting mutation or nondeterministic receipt and leave W2 and W6 closed.
    outcome: >-
      The deterministic merger sorted only ordinals 33, 107 and 180, chained from the
      frozen exp-052 row and refused gaps, duplicate extras, reordered payloads, foreign
      parent bindings, partial JSON, changed event hashes and false agreement flags.
      The production selftest fired 18 guards with zero skips; normal and optimized
      Python emitted byte-identical receipt SHA-256
      f2cd76f21414b2a03da7a9f94e4a1685490d97653bb5090205d375ae0c28d51a.
      Seven focused tests passed in 0.62 seconds with zero static warnings.
    evidence:
    - packing/cases/n17_weighted_certificate_parallel/runner.py
    - packing/tests/test_n17_weighted_certificate_parallel.py
    stop_reason: The 15-minute deterministic merge and corruption cell passed every guard.
    next_action: Freeze the four instrument files and admit or refuse them under independent W2.
  - workflow: factual-review
    focus: correctness
    recording: contemporaneous
    clock_role: work
    objective: >-
      Independently replay the frozen profiler, direct-import, parent-binding,
      fragment-equivalence, mutation, cleanup and normal-versus-optimized evidence and
      admit or refuse the exact three-pair command without an implementation edit.
    commitment: BC-123
    bead: think-p2m6
    status: stopped
    entered_by: evidence_checkpoint
    switch_reason: >-
      All 18 target-blind guards passed with zero skips and the four instrument files
      were frozen by SHA-256 at the W7 boundary.
    budget_minutes: 15
    started_at: '2026-09-02T01:28:19Z'
    deadline_at: '2026-09-02T01:43:19Z'
    expected_output: >-
      A coordinator-independent admission or the first exact blocker, bound to the four
      instrument hashes, selftest receipt and absent exp-053 output inventory.
    validation_command: >-
      uv run --frozen --all-extras --group dev pytest -q
      tests/test_n17_weighted_certificate_parallel.py && uv run --frozen python -m
      benchmarks.n17_weighted_certificate_parallel selftest
    kill_condition: >-
      Refuse W6 if any frozen hash changes, either exact kernel is translated or bypassed,
      a mutation fails to reject, a child survives, a check skips, an exp-053 output is
      present, or review would require an implementation edit.
    fallback: Retain the exact blocker, type exp-053 unresolved and do not open the profile.
    outcome: >-
      Coordinator W2 refused the profiler before target access: `write_fragment()` bound
      only the filename, so a forged WorkItem with the correct basename and a different
      parent directory could publish outside its assigned fragment root. The existing
      mutation changed the basename and did not exercise this escape. No exp-053 output
      or retained-direction process had started when the review found it.
    evidence:
    - packing/cases/n17_weighted_certificate_parallel/runner.py
    - packing/cases/n17_weighted_certificate_parallel/__init__.py
    - packing/benchmarks/n17_weighted_certificate_parallel.py
    - packing/tests/test_n17_weighted_certificate_parallel.py
    stop_reason: Independent review found an untested same-basename fragment-root escape.
    next_action: Reopen only W7, bind each WorkItem to its exact fragment root and add the missing controls.
  - workflow: pipeline-improvement
    focus: correctness
    recording: contemporaneous
    clock_role: work
    objective: >-
      Bind every WorkItem to its exact allowed fragment root, require lexical and resolved
      parent/path equality before computation or publication, and add same-basename
      outside-root and symlink-root regressions to the zero-skip selftest. Add a
      target-blind three-pair assembler control that recomputes the median and minimum,
      refuses missing or corrupt pairs and result overwrite, and preserves the
      review-pending profile-only claim boundary.
    commitment: BC-123
    bead: think-p2m6
    status: completed
    entered_by: evidence_checkpoint
    switch_reason: >-
      Independent W2 found a concrete path-containment defect before profile and returned
      the smallest target-blind repair plus negative control.
    budget_minutes: 15
    started_at: '2026-09-02T01:30:46Z'
    deadline_at: '2026-09-02T01:45:46Z'
    expected_output: >-
      Refrozen instrument bytes whose worker refuses a correct basename outside its
      assigned root and any symlink-root alias before evaluating either accumulator,
      plus a synthetic fixed-order assembler receipt that fires every final decision and
      publication guard without target access.
    validation_command: >-
      uv run --frozen --all-extras --group dev pytest -q
      tests/test_n17_weighted_certificate_parallel.py && uv run --frozen python -m
      benchmarks.n17_weighted_certificate_parallel selftest
    kill_condition: >-
      Stop if either escape writes one byte, a symlink alias reaches computation, any
      assembler accepts a missing or corrupt pair, overwrites a result, emits a
      scientific claim, any prior guard regresses, a check skips, or an exp-053 target
      path appears.
    fallback: Retain the path defect, type exp-053 unresolved and do not reopen W2 or W6.
    outcome: >-
      Bound each WorkItem to one exact fragment root and refused lexical path changes,
      correct-basename outside-root paths, resolved-parent escapes and symlink-root
      aliases before either accumulator runs. Added a target-blind three-pair assembler
      control that required AB/BA/AB, recomputed the 2.9x median and 2.8x minimum,
      exercised the greater-than-1x minimum rejection, refused a missing pair, corrupt
      pair and result overwrite, and retained `profile_only: true`, `needs_review: true`
      and the exp-052 nondecision boundary. Seven focused tests passed in 1.25 seconds;
      Ruff and BasedPyright passed; normal and optimized selftests fired 30 of 30 guards
      with zero skips and identical SHA-256
      0c256e5a164078119ffb3a98e9de2825c733a02cfbcff1c1b0aa8a6d28da0958. At the
      01:45:46Z boundary both exp-053 output paths remained absent and no profiler,
      spawn or resource-tracker child survived. The admitted instrument-ready H-057
      record is frozen at SHA-256
      77c82bd2c82886933a82cbe9c175183dcdac3d037ea8d5b8e648cd66a7f7bbbd.
    evidence:
    - packing/cases/n17_weighted_certificate_parallel/runner.py
    - packing/tests/test_n17_weighted_certificate_parallel.py
    stop_reason: >-
      Both admission repairs passed at the declared 15-minute boundary and coordinator
      W2 admitted the refrozen instrument without target access.
    next_action: Await the coordinator's explicit quiet-window release before any W6 pair command.
  - workflow: research-loop
    focus: efficiency
    recording: contemporaneous
    clock_role: work
    objective: >-
      Run only exp-053's preregistered Pair 1 AB command on fixed ordinals 33, 107 and
      180 in the coordinator-released quiet window, preserving any complete arm and
      reporting exact bytes, elapsed times and child state at the 15-minute boundary.
    commitment: BC-123
    bead: think-p2m6
    status: stopped
    entered_by: evidence_checkpoint
    switch_reason: >-
      Coordinator W2 admitted the refrozen 30-guard instrument and explicitly released
      the quiet CPU window for Pair 1 only after the W7 receipt closed.
    budget_minutes: 15
    started_at: '2026-09-02T01:48:50Z'
    deadline_at: '2026-09-02T02:03:50Z'
    expected_output: >-
      One durable pair-01-ab receipt, or a contemporaneous in-flight checkpoint naming
      the exact complete arm and live child state without a rerun.
    validation_command: >-
      uv run --frozen --all-extras --group dev python -m
      benchmarks.n17_weighted_certificate_parallel pair --experiment exp-053 --session
      session-073 --parent-checkpoint
      campaign/series/series-000-smoke-and-calibration/results/exp-052-h-052-n17-resumable-certificate-agreement.checkpoint.json
      --parent-progress
      campaign/series/series-000-smoke-and-calibration/results/exp-052-h-052-n17-resumable-certificate-agreement.progress.json
      --ordinals 33 107 180 --workers 3 --start-method spawn --pair-index 1 --order AB
      --output-root
      campaign/series/series-000-smoke-and-calibration/results/exp-053-h-057-n17-parent-bound-parallel-speedup.raw/pair-01-ab
    kill_condition: >-
      Stop on frozen-input or instrument-hash drift, nonexact output, unsafe path,
      process failure or contamination; at the hard wall stop children and preserve only
      complete durable arms or pairs.
    fallback: >-
      Preserve a complete arm, type the interruption or timebox stop and do not rerun it;
      leave Pair 2 closed.
    outcome: >-
      Pair 1's serial arm completed durably in 524.743164166 seconds with all three exact
      fragments and merged SHA-256
      bd383747cfcfaf2c13c800c1b09fa4e430ef3d2f5f04106d7d9f37482dce33ba. During the
      later parallel arm, the coordinator observed unrelated sustained CPU-heavy work
      that had begun after the control completed and invoked the asymmetric-load kill
      guard. SIGINT reached the sole profile process inside `pool.map`; the runner
      terminated and joined all workers, removed the partial arm B and preserved arm A.
      The Pair 1 receipt and paired sample, arm B, Pairs 2--3 and the canonical result
      remain absent; the Pair 1 root and arm A remain durable.
    evidence:
    - packing/campaign/series/series-000-smoke-and-calibration/results/exp-053-h-057-n17-parent-bound-parallel-speedup.raw/pair-01-ab/
    stop_reason: >-
      The quiet-host timing regime failed asymmetrically during the candidate arm, so
      the incomplete pair is invalid rather than slow and no further measurement is
      authorized.
    next_action: Terminalize exp-053 as unresolved and preserve arm A only as process-cost evidence.
  - workflow: insight-iteration
    focus: insight
    recording: contemporaneous
    clock_role: work
    objective: >-
      Type the asymmetric external-load guard stop, validate the retained arm and absent
      pair/result boundary, reconcile exp-053 and session-073, and leave a replayable
      future-round handoff without claiming a paired speedup.
    commitment: BC-123
    bead: think-p2m6
    status: stopped
    entered_by: evidence_checkpoint
    switch_reason: >-
      The coordinator invoked the contamination kill guard; cleanup retained only the
      valid completed serial arm and closed every further measurement command.
    budget_minutes: 15
    started_at: '2026-09-02T02:03:10Z'
    deadline_at: '2026-09-02T02:18:10Z'
    expected_output: >-
      Enforced terminal experiment and session records with exact arm-A hashes, an
      unresolved review-pending verdict, zero live children and no Pair 1 receipt or
      sample, arm B, Pair 2, Pair 3 or canonical result.
    validation_command: >-
      uv run --frozen softschema validate
      campaign/series/series-000-smoke-and-calibration/experiments/exp-053-h-057-n17-parent-bound-parallel-speedup.md
      && uv run --frozen softschema validate
      campaign/agent-sessions/session-073-bc123-n17-parent-bound-parallel-profile.md
    kill_condition: >-
      Stop and report if arm A fails exact replay, any child or partial arm survives,
      another pair opened, or terminal prose implies a paired or scientific result.
    fallback: Preserve the first reconciliation defect for coordinator review; never resume measurement.
    outcome: >-
      Replayed the durable arm without evaluating a target: all three fragments reparsed,
      source-faithful equaled target-independent at ordinals 33, 107 and 180, event
      hashes matched and the deterministic child chain rebuilt from the frozen parent
      row to merged SHA-256
      bd383747cfcfaf2c13c800c1b09fa4e430ef3d2f5f04106d7d9f37482dce33ba. Exp-053 is
      enforced, unresolved and review-pending; H-057 remains instrument-ready and
      undecided. The Pair 1 receipt and sample, arm B, Pairs 2--3 and canonical result
      are absent, and no profiler child survives. The approximate serial publication
      intervals of 177, 181 and 166 seconds leave about 6.4 seconds of overhead at the
      2.8x threshold; this is a scheduling diagnostic, not a paired result.
    evidence:
    - packing/campaign/series/series-000-smoke-and-calibration/results/exp-053-h-057-n17-parent-bound-parallel-speedup.raw/pair-01-ab/arm-A/
    - packing/campaign/series/series-000-smoke-and-calibration/experiments/exp-053-h-057-n17-parent-bound-parallel-speedup.md
    stop_reason: >-
      The contamination decision, bounded exactness result, process cost, claim boundary
      and fresh-root resume constraint are reconciled in enforced records.
    next_action: >-
      Coordinator renders the session resource receipt and routes exp-053 through
      BC-135 or BC-136; exp-053 itself must not resume.
  primary_bead: think-p2m6
  status: stopped
  budget:
    wall_minutes: 150
    max_cycles: 9
    checkpoint_minutes: 25
    slice_minutes: 25
    finalization_minutes: 15
  stop_conditions:
  - The fixed 2026-09-02T02:45:00Z deadline arrives.
  - A frozen exp-052 binding changes or a worker touches its canonical files.
  - Exact equivalence, corruption, interruption, process cleanup or timing-regime admission fails.
  progress:
    metric: complete exact paired profiles admitted by independent review
    before: zero; only the 33-row serial resumability boundary exists
    after: >-
      zero complete paired profiles; one independently admitted instrument and one
      replay-valid 524.743164166-second serial arm with three exact agreeing fragments,
      stopped before a pair by asymmetric external-load contamination
  delegations:
  - task: Independent W2 readmission of the frozen exp-053 profiler
    operator: coordinator
    status: completed
    recording: contemporaneous
    outcome: >-
      Refused W6 after finding that correct-basename output could escape the assigned
      fragment root; prescribed an exact-root binding and same-basename outside-root
      negative control without running or editing the instrument.
    evidence:
    - packing/cases/n17_weighted_certificate_parallel/runner.py
    - packing/benchmarks/n17_weighted_certificate_parallel.py
    - packing/tests/test_n17_weighted_certificate_parallel.py
    files:
    - packing/cases/n17_weighted_certificate_parallel/runner.py
    - packing/benchmarks/n17_weighted_certificate_parallel.py
    - packing/tests/test_n17_weighted_certificate_parallel.py
    checks:
    - focused pytest, Ruff, BasedPyright and normal/optimized selftest replay
    uncertainty: Whether an independent reading finds a process or provenance defect missed by the author.
    elapsed_seconds: 147
    elapsed_quality: operator_reported_approximate
    next_action: Re-review only after the author refreezes the bounded containment repair.
    phase: 5
    budget_minutes: 15
    started_at: '2026-09-02T01:28:19Z'
    deadline_at: '2026-09-02T01:43:19Z'
    expected_output: A read-only admission bound to exact hashes and absent output paths.
    validation_command: >-
      uv run --frozen --all-extras --group dev pytest -q
      tests/test_n17_weighted_certificate_parallel.py
    kill_condition: Stop on any hash drift, skipped guard, surviving child or required implementation edit.
    fallback: Return the first blocker and keep W6 closed.
    excluded_commands:
    - all pair and assemble commands under benchmarks.n17_weighted_certificate_parallel
  - task: Second independent W2 readmission after the bounded repair
    operator: coordinator
    status: completed
    recording: contemporaneous
    outcome: >-
      Replayed Ruff, BasedPyright, seven focused tests and byte-identical normal and
      optimized selftests; manually confirmed exact fragment-root containment, all 30
      zero-skip guards, the synthetic assembler's statistic, corruption and exclusive
      result controls, and the review-pending profile-only claim boundary.
    evidence:
    - packing/cases/n17_weighted_certificate_parallel/runner.py
    - packing/cases/n17_weighted_certificate_parallel/__init__.py
    - packing/benchmarks/n17_weighted_certificate_parallel.py
    - packing/tests/test_n17_weighted_certificate_parallel.py
    files:
    - packing/cases/n17_weighted_certificate_parallel/runner.py
    - packing/cases/n17_weighted_certificate_parallel/__init__.py
    - packing/benchmarks/n17_weighted_certificate_parallel.py
    - packing/tests/test_n17_weighted_certificate_parallel.py
    checks:
    - Ruff passed on four instrument files.
    - BasedPyright reported zero errors, warnings or notes.
    - Seven focused tests passed.
    - Normal and optimized selftests emitted identical SHA-256 0c256e5a164078119ffb3a98e9de2825c733a02cfbcff1c1b0aa8a6d28da0958.
    uncertainty: Retained-ordinal runtime and therefore completion within the remaining wall are still unmeasured.
    elapsed_seconds: null
    elapsed_quality: unavailable
    next_action: Keep W6 closed until the author records the W7 boundary and the coordinator releases a quiet window.
    phase: 6
    budget_minutes: 15
    started_at: '2026-09-02T01:38:42Z'
    deadline_at: '2026-09-02T01:45:46Z'
    expected_output: A read-only admission bound to exact hashes, zero skips and absent exp-053 output paths.
    validation_command: >-
      uv run --frozen --all-extras --group dev pytest -q
      tests/test_n17_weighted_certificate_parallel.py && uv run --frozen python -m
      benchmarks.n17_weighted_certificate_parallel selftest
    kill_condition: Stop on hash drift, a nonrejecting mutation, a surviving child or any target output.
    fallback: Return the first blocker and keep W6 closed.
    excluded_commands:
    - all pair and assemble commands under benchmarks.n17_weighted_certificate_parallel
  outputs:
  - packing/campaign/agent-sessions/session-073-bc123-n17-parent-bound-parallel-profile.md
  - packing/campaign/series/series-000-smoke-and-calibration/experiments/exp-053-h-057-n17-parent-bound-parallel-speedup.md
  - packing/cases/n17_weighted_certificate_parallel/
  - packing/benchmarks/n17_weighted_certificate_parallel.py
  - packing/tests/test_n17_weighted_certificate_parallel.py
  - packing/campaign/series/series-000-smoke-and-calibration/results/exp-053-h-057-n17-parent-bound-parallel-speedup.raw/
  - packing/campaign/series/series-000-smoke-and-calibration/results/exp-053-h-057-n17-parent-bound-parallel-speedup.json
  - packing/campaign/resource-usage/codex-task-tree-session-073.yaml
  checks:
  - Ruff passed on the four instrument files.
  - BasedPyright reported zero errors, warnings or notes on the four instrument files.
  - Seven focused tests passed in 1.25 seconds.
  - Normal and optimized selftests fired 30 of 30 guards with zero skips and identical receipt SHA-256 0c256e5a164078119ffb3a98e9de2825c733a02cfbcff1c1b0aa8a6d28da0958.
  - Exact arm-A replay rebuilt all three agreeing rows and merged SHA-256 bd383747cfcfaf2c13c800c1b09fa4e430ef3d2f5f04106d7d9f37482dce33ba.
  - Softschema validated exp-053, H-057 and session-073 as enforced records.
  - Final inventory found no Pair 1 receipt or sample, arm B, Pair 2, Pair 3, canonical result, partial arm or profiler child.
  resource_rollups:
  - packing/campaign/resource-usage/codex-task-tree-session-073.yaml
  stop_reason: >-
    The preregistered quiet-host guard failed asymmetrically during Pair 1's candidate
    arm. Measurement stopped, cleanup preserved only the completed control, and no
    admissible paired speed result exists.
  next_action: >-
    Review exp-053 under BC-135 on think-bpzq. Any later timing round requires fresh
    paired roots and a host-wide quiet lease; exp-053 must not resume.
---
# Session-073 — BC-123 `n = 17` Parent-Bound Parallel Profile

The noncontiguous ordinals `33`, `107` and `180` form a profile-only chain.
No output from this session may be appended to or described as the exp-052 checkpoint.

## Terminal Handoff

**Artifact.** The independently admitted profiler, 30-guard selftest and durable Pair 1
serial arm remain replayable.
The arm receipt has SHA-256
`30c40271a8e8fc71dac8c3f8ee9750b09338ca1d3e8375cfb79cf0daba0f6b93`, elapsed time
`524743164166` nanoseconds and merged SHA-256
`bd383747cfcfaf2c13c800c1b09fa4e430ef3d2f5f04106d7d9f37482dce33ba`.

**Result.** Exp-053 is unresolved and review-pending.
The serial arm is process-cost evidence and a bounded exactness guard: its three
fragments independently confirm source-faithful equals target-independent at ordinals
`33`, `107` and `180`, in a valid child chain from the frozen parent hash.
This is not serial-versus-parallel equivalence or a paired timing sample.
No Pair 1 receipt exists, Pairs 2 and 3 never opened, and the canonical result is
absent. It neither accepts nor rejects H-057 and does not decide H-052.

**Guard.** Unrelated sustained CPU-heavy work began only during the parallel arm.
That asymmetric load invalidated the comparison.
SIGINT stopped the sole profile process; the runner joined its workers and removed the
partial arm B. No profiler, spawn worker or resource tracker survived.

**Next.** BC-135 or BC-136 must review the new experiment decision.
Any later speed round needs fresh paired roots and conditions under a host-wide quiet
lease that remains active for the whole pair; it may bind this arm only as historical
cost evidence. The approximately `177`, `181` and `166` second serial publication
intervals imply an ideal three-worker ceiling near `2.90x`; the registered `2.8x`
threshold leaves roughly `6.4` seconds beyond the slowest interval for startup and
merge. This is a scheduling diagnostic, not a paired measurement.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
