---
title: 'Session 187: Canonical Rust Multiplication Promotion'
softschema:
  contract: packing.squares:AgentSession/v2
  schema: ../schemas/agent-session.schema.yaml
  envelope: session
  status: enforced
session:
  id: session-187
  title: Canonical Rust Multiplication Promotion
  date: '2026-10-19'
  started_at: '2026-10-19T00:21:25Z'
  deadline_at: '2026-10-19T06:21:25Z'
  branch: codex/canonical-mul-20261019
  goal: Promote the measured exact Rust multiplication helper only if fresh equal-work controls, explicit
    reference modes, independent review and required validation support the change.
  workflow_phases:
  - workflow: efficiency-loop
    focus: efficiency
    recording: contemporaneous
    clock_role: work
    objective: Refresh ownership and source; declare the bounded canonical multiplication promotion
      and independent audit; preserve the original reference baseline.
    status: completed
    entered_by: session_start
    switch_reason: null
    budget_minutes: 30
    started_at: '2026-10-19T00:21:25Z'
    deadline_at: '2026-10-19T00:51:25Z'
    expected_output: Claimed think-1ozu and think-2psd; isolated branch; original reference build
      and exact controls, followed by a frozen same-source paired protocol.
    validation_command: python -m devtools.check_session_clocks; python -m devtools.check_exact_rust_kernel
      --binary <original-reference-release-binary>
    kill_condition: Stop on ownership conflict, source drift, resource refusal, changed exact output,
      or failed input admission; no candidate timing before instrument controls pass.
    fallback: Retain the exact failure and narrow the next slice to the blocking instrument or correctness
      defect; never relax the acceptance rule.
    outcome: Claim/sync/readback and independent source audits completed. Original default release
      passed 210 polygon comparisons, 10 refusals and two verifier controls; both fixed-work baseline
      reports match retained digests.
    evidence:
    - 'Original reference controls: 210 polygon comparisons, 10 refusals and two whole-verifier controls;
      retained coordinator run 20261019T004001Z-459.'
    - packing/sqverify_exact/src/lib.rs
    stop_reason: Original reference baseline completed; feature-selection and portable fresh-build
      repairs are the next bounded objective.
    next_action: Implement the declared narrow default promotion and instrument controls for think-1ozu.
  - workflow: efficiency-loop
    focus: efficiency
    recording: contemporaneous
    clock_role: work
    objective: Promote the existing helper by default, retain distinct reference/normalized feature
      modes, and repair fresh-build provenance before any paired candidate timing.
    status: completed
    entered_by: evidence_checkpoint
    switch_reason: Original reference and source audit are complete; the inherited benchmark requires
      portable scratch and explicit arm admission.
    budget_minutes: 30
    started_at: '2026-10-19T00:41:56+00:00'
    deadline_at: '2026-10-19T01:11:56+00:00'
    expected_output: Minimal Cargo/default delta, direct canonical ingress tests, explicit feature-matrix
      controls and a fresh paired benchmark with negative admission tests.
    validation_command: cargo test --locked --all-targets; python -m pytest tests/test_rectangle_rust_transport_benchmark.py
      tests/test_rectangle_rust_verifier_ab.py tests/test_validation_cli.py -k "exact_rust_geometry
      or variant_builder or verifier"
    kill_condition: Stop on ownership conflict, source drift, resource refusal, changed exact output,
      or failed input admission; no candidate timing before instrument controls pass.
    fallback: Retain the exact failure and narrow the next slice to the blocking instrument or correctness
      defect; never relax the acceptance rule.
    outcome: Core design and complete fresh-build instrument independently reviewed without material
      blockers. Five Rust feature modes, 210/10/2 controls, 33 instrument tests and all 377 related
      Python tests passed.
    evidence:
    - packing/tests/test_rectangle_rust_verifier_ab.py
    - packing/tests/test_rectangle_rust_transport_benchmark.py
    - 'Related eight-file pytest selection: 377 passed in 31.10 seconds, zero skips; retained source-bound
      coordinator run related-tests-20261019T004650Z.'
    stop_reason: Instrument-readiness criteria met before target timing.
    next_action: Run the frozen three-pair comparison for think-1ozu.
  - workflow: efficiency-loop
    focus: efficiency
    recording: contemporaneous
    clock_role: work
    objective: Run the frozen same-source reference/default paired comparison, retain all outcomes
      and admit a production promotion only under the existing exact and material rules.
    status: completed
    entered_by: evidence_checkpoint
    switch_reason: Independent reviewer cleared the fixed instrument and core source for bounded measurement.
    budget_minutes: 30
    started_at: '2026-10-19T00:48:36+00:00'
    deadline_at: '2026-10-19T01:18:36+00:00'
    expected_output: Complete twelve-report paired receipt, per-arm current differential evidence
      and an explicit pass, miss or guard-refusal disposition.
    validation_command: python -m benchmarks.bench_rectangle_rust_verifier_ab --target-root <external>/verifier-arms
      --output <external>/verifier-ab.json; python -m devtools.check_exact_rust_kernel --binary <each-release-arm>
    kill_condition: Stop on ownership conflict, source drift, resource refusal, changed exact output,
      or failed input admission; no candidate timing before instrument controls pass.
    fallback: Retain the exact failure and narrow the next slice to the blocking instrument or correctness
      defect; never relax the acceptance rule.
    outcome: All twelve paired reports match the retained exact census. External child-CPU median
      ratio 0.847562 with disjoint ranges; both wall ratios below 1.05. Each freshly built release
      arm also passes 210/10/2 Python differential controls. Existing material criterion passes at
      its exploratory scope.
    evidence:
    - packing/resources/web/wand125-tools-2026-09-29/receipts/rust-exact-canonical-default-ab-2026-10-19.json
    - packing/resources/web/wand125-tools-2026-09-29/receipts/rust-exact-canonical-default-controls-2026-10-19.json
    stop_reason: Complete paired protocol and current-arm controls; no timeout, source drift or omitted
      observation.
    next_action: Finish documentation, independent evidence review and contribution gates for think-1ozu.
  - workflow: efficiency-loop
    focus: efficiency
    recording: contemporaneous
    clock_role: work
    objective: Integrate measured evidence, current guidance and resource accounting; complete independent
      precommit review and the required local/hosted validation without reducing coverage.
    status: completed
    entered_by: evidence_checkpoint
    switch_reason: The predeclared performance and exact-output criteria passed; submission readiness
      is now the bounded objective.
    budget_minutes: 30
    started_at: '2026-10-19T00:53:01+00:00'
    deadline_at: '2026-10-19T01:23:01+00:00'
    expected_output: Reviewed contribution with explicit source-bound validation, honest cost record
      and one integrated draft PR when the submission requirements are met.
    validation_command: packing-validate --edit --jobs 1 --inner-jobs 1 --format json
    kill_condition: Stop on ownership conflict, source drift, resource refusal, changed exact output,
      or failed input admission; no candidate timing before instrument controls pass.
    fallback: Retain the exact failure and narrow the next slice to the blocking instrument or correctness
      defect; never relax the acceptance rule.
    outcome: Independent source/document review resolved all four findings. The corrected complete
      records selection passed 52/52 with zero skips; performance and exact-output evidence remain
      accepted at their declared scope.
    evidence:
    - packing/campaign/agent-sessions/session-187-canonical-rust-multiplication.md
    - 'Complete source-bound records-v3 run, 20261019T010832Z: 52/52 passed.'
    stop_reason: Source/document review and records acceptance complete; required pre-push behavioral
      coverage is the next bounded objective.
    next_action: Run the full affected pre-push floor and retain its exact selection for think-1ozu.
  - workflow: efficiency-loop
    focus: efficiency
    recording: contemporaneous
    clock_role: work
    objective: Complete the change-reachable pre-push floor including applicable edit prerequisites
      and quick behavioral tests, then submit the independently reviewed narrow contribution.
    status: stopped
    entered_by: evidence_checkpoint
    switch_reason: The reviewed candidate and all 52 record checks pass; pre-push execution and a
      first public checkpoint are now admissible.
    budget_minutes: 30
    started_at: '2026-10-19T01:12:05+00:00'
    deadline_at: '2026-10-19T01:42:05+00:00'
    expected_output: Source-bound pre-push selection and complete execution receipt; reviewed commit
      and draft PR if requirements pass, otherwise exact failure and bounded repair.
    validation_command: packing-validate --push --jobs 1 --inner-jobs 1 --format json
    kill_condition: Stop at the phase deadline or on resource refusal. Never omit selected tests,
      relax diagnostic/timeout rules, or claim an incomplete check passed.
    fallback: Retain source, partial receipts and exact failure; use the next declared slice only
      for an attributable repair or justified continuation.
    outcome: 'Complete push-v5 ran 69 steps in 1200.425 seconds: all 68 edit steps passed, reachable
      behavioral tests failed with 6656 passed, 38 skipped and seven failures. Source remained stable;
      no timeout or OOM occurred. Peak memory was 3868241920 bytes, below the 4 GiB hard cap and 3190784
      bytes above the memory-high pressure threshold; swap peak was zero. The seven traces identify
      missing jq and Liberation Serif/Sans in the local environment.'
    evidence:
    - packing/tests/test_pages_workflow.py
    - packing/tests/test_site_rendering.py
    - Retained complete push-v5 source-bound receipt, 20261019T011411Z; no public submission.
    stop_reason: Full pre-push execution completed but failed environmental prerequisites. Preserve
      the failure and repair only the task-scoped environment before acceptance.
    next_action: Install the missing task-local runtime dependencies, rerun all seven failures, then
      repeat the full pre-push selection for think-1ozu.
  - workflow: efficiency-loop
    focus: efficiency
    recording: contemporaneous
    clock_role: work
    objective: Repair demonstrated task-local runtime prerequisites, verify the seven actual failures,
      then complete the unchanged full pre-push floor.
    status: stopped
    entered_by: evidence_checkpoint
    switch_reason: The first complete pre-push run exposed missing jq and required local font families;
      no contribution source or assertion change is indicated.
    budget_minutes: 30
    started_at: '2026-10-19T01:39:32+00:00'
    deadline_at: '2026-10-19T02:09:32+00:00'
    expected_output: Task-local package/font provenance; all seven failures passing; complete source-bound
      pre-push receipt or preserved remaining failure.
    validation_command: packing-validate --push --jobs 1 --inner-jobs 1 --format json
    kill_condition: Stop at the phase deadline, dependency provenance failure, resource refusal or
      a newly attributable test failure. Do not change test assertions, skips, coverage or resource
      limits.
    fallback: Preserve the incomplete contribution and exact environment/test receipts; continue only
      the necessary bounded repair.
    outcome: All four pinned runtime packages were verified against cached apt SHA256 metadata and
      extracted only into the authorized task sysroot. The task-local font configuration resolves
      Liberation Sans/Serif. All seven original failures now pass in 31.01 seconds, with stable source.
      Download failures and transport changes are retained; no test or resource rule changed.
    evidence:
    - packing/tests/test_pages_workflow.py
    - packing/tests/test_site_rendering.py
    - 'Source-bound environment-seven-20261019T015115Z: seven passed, no skips; complete pre-push
      acceptance remains pending.'
    stop_reason: The environment-repair portion passed its seven controls. The original objective
      also included complete pre-push validation, which carried forward unchanged into phase 7; phase
      6 stops with that scope unfinished.
    next_action: Repeat the complete unchanged pre-push selection for think-1ozu.
  - workflow: efficiency-loop
    focus: efficiency
    recording: contemporaneous
    clock_role: work
    objective: Complete the unchanged full pre-push floor on the repaired task environment and reviewed
      source, then create the first bounded public checkpoint.
    status: stopped
    entered_by: evidence_checkpoint
    switch_reason: All seven environment controls pass; repeating the full selected floor is required
      before contribution acceptance.
    budget_minutes: 30
    started_at: '2026-10-19T01:59:06+00:00'
    deadline_at: '2026-10-19T02:29:06+00:00'
    expected_output: All selected steps and reachable tests executed with exact-source receipts; independently
      reviewed commit/PR only after acceptance, otherwise the complete failure.
    validation_command: packing-validate --push --jobs 1 --inner-jobs 1 --format json
    kill_condition: Stop at the phase deadline or resource refusal. Preserve all diagnostics and existing
      conditional skips; no test, coverage, limit or threshold changes to obtain acceptance.
    fallback: Preserve the failed or incomplete contribution and continue only an attributable bounded
      repair.
    outcome: 'Complete push-v7 ran all 69 steps in 1201.665 seconds with stable source: all 68 edit
      steps passed; reachable tests reported 6663 passed, 36 skipped and two failures. The previously
      skipped workflow controls now ran but deliberately removed LD_LIBRARY_PATH, so the task-local
      jq could not load libjq.so.1. Peak memory 3870076928 bytes was below the 4 GiB hard limit but
      above the memory-high threshold; swap remained zero, no OOM or timeout was reported and owned
      cleanup was confirmed.'
    evidence:
    - packing/tests/test_pages_workflow.py
    - Source-bound push-v7-20261019T020011Z and task-scoped resource receipt retained privately.
    stop_reason: Two newly exercised minimal-environment controls expose incomplete task dependency
      launch configuration; preserve the full failure and repair the launcher without changing tests.
    next_action: Complete the task-local jq launcher repair and rerun the unchanged complete contribution
      floor.
  - workflow: efficiency-loop
    focus: efficiency
    recording: contemporaneous
    clock_role: work
    objective: Verify the task-local jq launcher under minimal environments, then complete unchanged
      contribution checks and the first reviewed public checkpoint.
    status: in_progress
    entered_by: evidence_checkpoint
    switch_reason: The full run isolated two missing-library failures in previously skipped controls;
      the installed package binary and source need no changes.
    budget_minutes: 30
    started_at: '2026-10-19T02:23:44+00:00'
    deadline_at: '2026-10-19T02:53:44+00:00'
    expected_output: All workflow controls, complete records and pre-push selections pass on frozen
      source; a reviewed checkpoint follows only accepted checks.
    validation_command: packing-validate --push --jobs 1 --inner-jobs 1 --format json
    kill_condition: Stop at the phase deadline or resource refusal; do not change tests, coverage,
      limits, skips or thresholds to obtain acceptance.
    fallback: Retain the exact failure and actionable repair; keep the contribution incomplete.
    outcome: The repaired local contribution gate passed all 69 steps in 1218.142 seconds, including
      6668 passing and 36 conditionally skipped reachable cases; the same frozen source passed
      all 52 records steps. PR 679 was submitted, but its first hosted run failed release-impact
      decisions and a frontend command deadline. Hosted acceptance remains incomplete.
    evidence:
    - https://github.com/jlevy/squares/pull/679
    - https://github.com/jlevy/squares/actions/runs/39191999508
    - https://github.com/jlevy/squares/pull/679#pullrequestreview-5566794562
    stop_reason: null
    next_action: Address review A1-A3 under think-hv53, then obtain complete ordinary and deferred
      hosted gates on matching final source and base before acceptance of think-1ozu.
  primary_bead: think-1ozu
  status: in_progress
  budget:
    wall_minutes: 360
    max_cycles: 18
    orientation_minutes: 30
    checkpoint_minutes: 20
    slice_minutes: 30
    finalization_minutes: 30
  stop_conditions:
  - Stop new implementation at 2026-10-19T05:51:25Z and all owned computation by 2026-10-19T06:21:25Z.
  - Preserve the existing 4 GiB hard memory, zero swap, two visible CPUs and one owned workload limits.
  - Refuse changed exact outputs, invalid or incomplete pairs, source/input drift, or a weakened admission
    or performance threshold.
  - Independent audit precedes public submission; pending CI is not completion; no auto-merge.
  progress:
    metric: Production-default readiness with unchanged exact controls
    before: The feature-gated helper has prior bounded evidence; default promotion, current-host controls
      and independent acceptance remain pending.
    after: null
  delegations:
  - task: Design and fresh-build instrument
    operator: GPT-6.1 Sol / xhigh
    status: completed
    recording: retrospective
    phase: 2
    outcome: Identified the default-feature ablation trap and supplied the two-file fresh-build instrument
      patch; coordinator integrated it and ran validation.
    evidence:
    - packing/campaign/agent-sessions/session-187-canonical-rust-multiplication.md
    files:
    - packing/benchmarks/bench_rectangle_rust_verifier_ab.py
    - packing/tests/test_rectangle_rust_verifier_ab.py
    checks:
    - Source-only review; no subagent builds or tests. Coordinator instrument selection passed 33
      tests before publication repair.
    uncertainty: Reconstructed from completed coordinator exchanges; separate delegation wall time
      is unavailable. No execution is attributed to the reviewer.
    elapsed_seconds: null
    elapsed_quality: unavailable
    next_action: Retain the result and review the final delta before submission.
  - task: Upstream overlap and session identity
    operator: GPT-6.1 Sol / high
    status: completed
    recording: retrospective
    phase: 1
    outcome: Read main and all 17 open PR heads; no overlapping arithmetic implementation found and
      the highest observed AgentSession identifier was 186.
    evidence:
    - packing/campaign/agent-sessions/session-187-canonical-rust-multiplication.md
    files:
    - packing/campaign/agent-sessions/session-187-canonical-rust-multiplication.md
    checks:
    - Read-only GitHub/source inspection; current PR head states distinguished from old failures.
    uncertainty: Reconstructed from completed coordinator exchanges; separate delegation wall time
      is unavailable. No execution is attributed to the reviewer.
    elapsed_seconds: null
    elapsed_quality: unavailable
    next_action: Retain the result and review the final delta before submission.
  - task: Independent arithmetic, instrument and paired-evidence audit
    operator: GPT-6 Astra / max
    status: completed
    recording: retrospective
    phase: 3
    outcome: Verified canonical closure, feature modes, source manifests and all twelve paired observations.
      Found inherited non-atomic receipt publication; coordinator fixed it and final delta review
      is pending.
    evidence:
    - packing/campaign/agent-sessions/session-187-canonical-rust-multiplication.md
    files:
    - packing/sqverify_exact/src/lib.rs
    - packing/sqverify_exact/Cargo.toml
    - packing/benchmarks/bench_rectangle_rust_verifier_ab.py
    checks:
    - Independent source hashes and arithmetic derivations; independent ratio recomputation; coordinator-run
      377-test and per-arm 210/10/2 receipts reviewed.
    uncertainty: Reconstructed from completed coordinator exchanges; separate delegation wall time
      is unavailable. No execution is attributed to the reviewer.
    elapsed_seconds: null
    elapsed_quality: unavailable
    next_action: Retain the result and review the final delta before submission.
  - task: Final publication, public evidence and documentation delta audit
    operator: GPT-6 Astra / max
    status: completed
    recording: contemporaneous
    phase: 4
    budget_minutes: 12
    started_at: '2026-10-19T01:01:36+00:00'
    deadline_at: '2026-10-19T01:13:36+00:00'
    expected_output: Independent A1 disposition and final code/document review, with exact remaining
      gate obligations and no invented execution.
    validation_command: Read and hash the exported candidate, compare public evidence with raw receipts,
      and inspect actual retained check receipts.
    kill_condition: Stop on source/receipt mismatch, authority uncertainty or the declared deadline;
      do not run project compute.
    fallback: Return exact findings and unchecked scope; coordinator preserves incomplete submission
      status.
    write_scope:
    - Private independent audit report only
    excluded_commands:
    - WSL compute
    - source edits
    - tracker mutations
    - GitHub writes
    outcome: A1 atomic publication and A2-A4 record findings resolved. All eighteen candidate-v3 hashes,
      public receipt projection, privacy-reduced usage and scoped claims independently accepted; no
      material code/document blocker remains. Required contribution gates remain separate.
    evidence:
    - packing/campaign/agent-sessions/session-187-canonical-rust-multiplication.md
    files:
    - packing/benchmarks/bench_rectangle_rust_verifier_ab.py
    - packing/tests/test_rectangle_rust_verifier_ab.py
    - docs/project/research/research-2026-09-30-exact-arithmetic-verifier-performance.md
    - SYNOPSIS.md
    checks:
    - Independent eighteen-file manifest and patch verification; exact public/raw receipt comparison;
      65 usage deltas checked; actual publication and record-fix receipts inspected.
    uncertainty: Source and evidence review only; no reviewer execution or merge approval. Subsequent
      ordinary record completion may reuse the substantive review with record checks.
    elapsed_seconds: null
    elapsed_quality: unavailable
    next_action: Coordinator completes required pre-push and matching-source/base hosted validation
      for think-1ozu.
  - task: Read-only comparison of the next independent efficiency candidates
    operator: GPT-6.1 Sol / xhigh
    status: completed
    recording: contemporaneous
    phase: 5
    budget_minutes: 28
    started_at: '2026-10-19T01:13:24+00:00'
    deadline_at: '2026-10-19T01:41:24+00:00'
    expected_output: Source-grounded candidate ranking, current implementation gaps, overlap risks
      and smallest meaningful verification plan; no implementation or experimental claim.
    validation_command: Read current tracked source and the saved fresh task/PR metadata; cite exact
      code and test paths.
    kill_condition: Stop on an ownership ambiguity or deadline. No project compute, benchmark, source
      mutation or held experiment.
    fallback: Return a scoped preflight with unknowns; coordinator must refresh and claim separately
      before any implementation.
    write_scope:
    - Private candidate-preflight report only
    excluded_commands:
    - WSL compute
    - source edits
    - tracker writes
    - GitHub writes
    outcome: Read-only preflight identified think-uhxt as the next narrow opportunity. Existing progress
      machinery is retained; actual phase durations and standalone timing integration remain missing.
    evidence:
    - packing/devtools/reachable_progress.py
    - packing/benchmarks/validation_timing.py
    files: []
    checks:
    - Current source, existing controls and fresh PR599 overlap inspected.
    uncertainty: No implementation or measurement; candidate ownership was subsequently claimed and
      separately synced by the coordinator.
    elapsed_seconds: null
    elapsed_quality: unavailable
    next_action: Keep follow-up source edits pending while the first contribution acceptance is repaired.
  outputs:
  - packing/campaign/agent-sessions/session-187-canonical-rust-multiplication.md
  - packing/resources/web/wand125-tools-2026-09-29/receipts/rust-exact-canonical-default-ab-2026-10-19.json
  - packing/resources/web/wand125-tools-2026-09-29/receipts/rust-exact-canonical-default-controls-2026-10-19.json
  - docs/project/research/research-2026-09-30-exact-arithmetic-verifier-performance.md
  - packing/campaign/resource-usage/codex-task-tree-session-187.yaml
  checks:
  - Opening upstream main was 804eff369193b698d497a9c06847059eb9de0470; Windows-owned tracker claim/sync/readback
    completed.
  - Independent review supports the canonical-input argument and twelve-report exploratory improvement;
    publication fix and full contribution gates are still under review.
  - 'Complete records-v3: 52/52 passed, zero skips, stable candidate-v3 source; prior 49/52 failure
    retained and three record defects corrected.'
  - 'Independent GPT-6 Astra/max review A: all A1-A4 findings resolved; no arithmetic or timing rerun
    needed for publication/record-only deltas. Applicable pre-push and hosted gates remain pending.'
  - 'Complete push-v5: 68 edit steps passed; reachable tests reported 6656 passed, 38 skipped and
    seven environment failures. This is not pre-push acceptance. Runtime dependencies will be repaired
    locally with the test and resource contracts unchanged.'
  - 'Task-local runtime repair: jq/libjq1 1.8.1-4ubuntu2, libonig5 6.9.10-1build1 and Liberation fonts
    2.1.5-3build1 admitted by exact cached apt hashes; seven original failures pass. Native/host HTTPS
    transport receipts are retained privately. No global apt source or package database was modified.'
  - 'Hosted run 39191999508 at PR head c78cc5e271: validate, frontend and packing-required failed.
    The frontend completed 425 cases with 6 skips, then its serial forwarder command timed out
    after 488.387 seconds. Retained progress identifies test_the_deployed_site_check_follows_the_same_forwarders
    in its call phase after 18 completed cases; the underlying Playwright wait is not yet diagnosed.'
  - 'Independent formal reviews A-D cover senior engineering, correctness, security and performance.
    Only A has findings: missing release dispositions, incomplete frontend validation and a stale
    current-phase handoff. Review repair integrates main d167d4b86; the mathematical result and
    retained performance measurements are unchanged.'
  stop_reason: null
  next_action: Complete PR 679 review A1-A3 through think-hv53, obtain passing ordinary and deferred
    hosted gates on matching final source and base, then submit think-1ozu for acceptance. Keep
    the separately claimed follow-up experiment pending.
  resource_rollups:
  - packing/campaign/resource-usage/codex-task-tree-session-187.yaml
---
# Canonical Rust Multiplication Promotion

This six-hour block is authorized for one narrow efficiency contribution.
The existing Rust operator path remains an explicit reference.
The external certificate stays INCONCLUSIVE; neither a component speedup nor a passing
diagnostic proves it valid.

## Bounded Slot Plan

Slots start at 00:21:25 UTC on 2026-10-19. Later slots are maximum allocations, revised
from retained evidence at each boundary.
Current phase is 8: the runtime-repaired local records and pre-push checks passed, and
PR [#679](https://github.com/jlevy/squares/pull/679) is awaiting hosted acceptance.
Its first hosted run failed the release-impact gate and stalled in the serial forwarder
test. Review A1-A3 is tracked in think-hv53; the next checkpoint must complete the
ordinary PR surface and deferred hosted checks on the final source and base.
The cycle ceiling is prospectively revised from 12 to 18 because earlier checkpoints
finished before their 30-minute allocations; the six-hour hard deadline and final
30-minute reserve are unchanged.

| UTC Start | Objective and Dependency | Expected Evidence | Cost and Stop Rule |
| --- | --- | --- | --- |
| 00:21 | Refresh main/TBD, claim, inspect source and peers | Ownership readback, source audit, original control | 30 min; stop on conflict or exact mismatch |
| 00:51 | Repair instrument selection and freeze protocol | Distinct modes and negative controls | 30 min; no target timing before readiness |
| 01:21 | Narrow default promotion and direct ingress tests | Reviewed source delta | 30 min; no arithmetic redesign |
| 01:51 | Serial paired comparison and focused gate | Equal reports and complete sample census | 30 min; fixed threshold, preserve misses |
| 02:21 | Independent audit and edit/push validation | Review disposition and current-source receipts | 30 min; no submission with unresolved findings |
| 02:51 | Integration checkpoint and PR preparation | Exact-head checks and generated cost record | 30 min; preserve any incomplete gate |
| 03:21 | CI inspection and attributable fixes | Terminal CI or bounded continuation | 30 min; no unrelated repairs |
| 03:51 | Reconcile the first four-hour checkpoint | Measured progress and remaining value | 30 min; replan from actual evidence |
| 04:21 | Only a separately claimed bounded follow-up if useful | One scoped result or preserved negative | 30 min; defer if verification cannot fit |
| 04:51 | Complete existing scope and validation | Audited current-source outcome | 30 min; no new substantial feature |
| 05:21 | Final contribution checks and handoff preparation | Current PR, tracker and continuation state | 30 min; stop implementation at 05:51:25 |
| 05:51 | Finalization only | Durable records, cleanup of owned processes and report | 30 min; hard stop 06:21:25 |

Builds and tests use the task-scoped public runner.
Source-only reviewers may run concurrently; heavy compute remains serial.
The initial reference build has a 90-second ceiling, each verifier invocation 40
seconds, and the paired diagnostic retains its declared sample census and exact-output
guards. Full checks are budgeted from measured cost; their acceptance criteria are not
reduced to fit this schedule.

## Promotion Protocol

Declared at 2026-10-19T00:41:56+00:00, after the original reference check and before
candidate measurements.
Use three alternating reference/default pairs for each fixed workload: all 201 analytic
angles (1,781 nodes, VERIFIED) and external angle 1 (1,000 nodes, INCONCLUSIVE with
pending geometry retained).
Preserve the maintained input and normalized-report digests.
This repeats the existing exploratory protocol; it is not a confirmatory estimate or a
whole-certificate throughput claim.

The candidate passes the existing material rule only if external Rust-child CPU median
is at most 90% of reference with strictly separated sample ranges, and invocation-wall
median is at most 105% of reference on both fixtures.
Report medians, ranges and paired ratios separately.
Do not retune the threshold or omit an unfavorable pair.
Both arms must be freshly built from the same frozen source, compiler and flags;
reference uses `--no-default-features`, and candidate uses production defaults.
Source/input/binary drift, nonzero exit, timeout, changed exact report,
duplicate/missing pair or wrong build mode refuses the run.
Build limits remain 90 seconds per arm, invocation limit 40 seconds and measurement
limit 300 seconds. The outer resource limits remain unchanged.

The original benchmark admitted only one macOS scratch volume.
Linux uses explicitly configured writable absolute scratch outside the source checkout;
macOS keeps its existing mounted-volume policy.
This storage portability change does not alter the timing, resource, mathematical or
acceptance rules.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
