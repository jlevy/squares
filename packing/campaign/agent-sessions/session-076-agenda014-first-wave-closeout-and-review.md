---
title: session-076 — agenda-014 first-wave closeout, routing and independent review
softschema:
  contract: packing.squares:AgentSession/v2
  schema: ../schemas/agent-session.schema.yaml
  envelope: session
  status: enforced
session:
  id: session-076
  title: Agenda-014 first-wave closeout, routing and independent review
  date: '2026-09-02'
  started_at: '2026-09-02T04:01:34Z'
  deadline_at: '2026-09-02T08:01:34Z'
  branch: claude/squares-pr-73-resume-5lp3bz
  goal: >-
    Resume Agenda 014 from the pushed PR #73 first-wave checkpoint on the owner's
    explicit instruction: formalize the BC-127 efficiency decision, freeze the BC-128
    routing and review packets, and run the BC-135 independent review of every
    first-wave experiment decision, without opening a scientific target, a second-wave
    lane or the BC-136 overnight agenda.
  workflow_phases:
  - workflow: process-review
    focus: process
    recording: contemporaneous
    clock_role: work
    objective: >-
      BC-127 W4: verify the frozen first-wave revision 1e175108 and its hosted checks,
      confirm that sessions 072--075, exp-053--exp-055 and the four task-tree receipts
      are terminal and declared, confirm no live lane writer or process exists, and
      open this session record before any W5 analysis.
    commitment: BC-127
    bead: think-ne3d
    status: completed
    entered_by: session_start
    switch_reason: null
    budget_minutes: 40
    started_at: '2026-09-02T04:01:34Z'
    deadline_at: '2026-09-02T04:41:34Z'
    expected_output: >-
      A verified frozen evidence revision, a passing local record gate on the unchanged
      tree, terminal lane and session states confirmed from the records, and this
      session record with its first phase declared.
    validation_command: >-
      uv run --frozen --all-extras --group dev packing-validate --records
    kill_condition: >-
      Stop if the pushed revision's hosted checks are not green, a lane record or
      receipt is missing or non-terminal, a first-wave evidence path differs from
      1e175108, or a lane process is still live.
    fallback: >-
      Retain the exact blocker in this record and leave BC-127 blocked without opening
      W5, BC-128 or BC-135.
    outcome: >-
      Artifact: this session record, a passing local record gate on the unchanged
      frozen tree, and the environment bootstrap. Result: PR #73 head 1e175108 is green
      on hosted validate, macos-portability and packing-required; sessions 072--075 are
      terminal (stopped, stopped, completed, completed) and each declares a receipt that
      exists; exp-053--exp-055 are unresolved, unresolved and accepted, all
      needs_review true; agenda rows BC-123--BC-126 are stopped, complete, complete and
      complete; every first-wave evidence path is byte-identical to 1e175108 and no
      lane process is live. Guard: the container had no Python 3.14.7 build and the
      packaged uv did not know one, so uv was upgraded and 3.14.7 installed before any
      project command ran; no scientific artifact, target or record changed. Next: open
      the W5 efficiency phase from the four complete receipts.
    evidence:
    - packing/campaign/agent-sessions/session-072-agenda014-six-hour-first-wave.md
    - packing/campaign/resource-usage/codex-task-tree-session-072.yaml
    - packing/campaign/resource-usage/codex-task-tree-session-073.yaml
    - packing/campaign/resource-usage/codex-task-tree-session-074.yaml
    - packing/campaign/resource-usage/codex-task-tree-session-075.yaml
    stop_reason: >-
      Every W4 freeze condition held at 1e175108, so the W5 analysis may open.
    next_action: >-
      Enter the BC-127 W5 efficiency-loop phase from the complete emitted receipts.
  - workflow: efficiency-loop
    focus: efficiency
    recording: contemporaneous
    clock_role: work
    objective: >-
      BC-127 W5: from the four complete task-tree receipts and lane records, extract the
      common cell, output, rework, command, model-stream and wait baselines, compare
      literal-command failures, per-unit timing, review yield and hosted CI, apply the
      predeclared change-admission test and retain exactly one guarded change or
      `no-change`.
    commitment: BC-127
    bead: think-ne3d
    status: completed
    entered_by: planned_checkpoint
    switch_reason: >-
      The W4 freeze verification completed with every condition held.
    budget_minutes: 40
    started_at: '2026-09-02T04:10:00Z'
    deadline_at: '2026-09-02T04:50:00Z'
    expected_output: >-
      A durable W5 receipt in docs/project/reviews with a measured first-wave baseline
      rendered by a checked tool, a change-admission table and one explicit repayment
      decision.
    validation_command: >-
      uv run --frozen --all-extras --group dev pytest -q
      tests/test_render_wave_efficiency.py && uv run --frozen --all-extras --group dev
      python -m devtools.render_wave_efficiency --lanes session-073 session-074
      session-075 --coordinator session-072
    kill_condition: >-
      Stop if a baseline number cannot be read from a retained receipt or record, or
      if a candidate change would touch a frozen evidence path or an instrument under
      review.
    fallback: >-
      Record `no-change` with the exact failing guard and route the bottleneck to a
      later W7 entry.
    outcome: >-
      Artifact: docs/project/reviews/review-2026-09-02-agenda014-first-wave-efficiency.md,
      devtools/render_wave_efficiency.py with four controls, and the document-map
      registration. Result: the lane total is 17,294.963 s recursive agent-active over
      22 cells (a lower bound), agent wait is 29.1% of it and command time is 75.9%
      concentrated in the n = 17 lane; eight defect groups were found by different-lane
      review, three of them after author-side suites had passed, and two repeat
      agenda-013 findings. The one measured candidate, mapping the benchmarks root so
      the push tier stops selecting all 1,302 tests, fails the equivalence and
      repayment guards; the decision is no-change with five routed W7 or contract
      entries. Guard: no instrument, result, criterion or review flag changed; the
      tool's normal and optimized JSON agree. Next: open BC-128 routing from the
      recorded lane exits.
    evidence:
    - docs/project/reviews/review-2026-09-02-agenda014-first-wave-efficiency.md
    - packing/devtools/render_wave_efficiency.py
    - packing/tests/test_render_wave_efficiency.py
    stop_reason: >-
      The repayment decision is recorded with every admission guard named.
    next_action: >-
      Open BC-128 routing from the recorded lane exits.
  - workflow: insight-iteration
    focus: insight
    recording: contemporaneous
    clock_role: work
    objective: >-
      BC-128 W3/W4 routing checkpoint: inspect the four lane exits and the W5 decision,
      close unearned branches, freeze at most one candidate continuation per lane, and
      prepare at most three immutable review packets with exact hashes, declared
      absences, safe commands, one named mutation each and the unchanged claim
      boundary. Dispatch no second-wave agent and open no target.
    commitment: BC-128
    bead: think-8ih6
    status: completed
    entered_by: planned_checkpoint
    switch_reason: >-
      BC-127 is terminal with a recorded no-change decision.
    budget_minutes: 35
    started_at: '2026-09-02T04:14:00Z'
    deadline_at: '2026-09-02T04:49:00Z'
    expected_output: >-
      docs/project/reviews/review-2026-09-02-agenda014-first-wave-packets.md with three
      packets and one recorded routing decision per lane, plus matching agenda rows.
    validation_command: >-
      uv run --frozen --all-extras --group dev packing-validate --records
    kill_condition: >-
      Stop if a packet would require a scientific target, network or source command,
      if a listed evidence path differs from 1e175108, or if more than three experiment
      decisions would need review.
    fallback: >-
      Freeze the packets that are exact, leave the rest review-pending behind a typed
      continuation, and record why.
    outcome: >-
      Artifact: docs/project/reviews/review-2026-09-02-agenda014-first-wave-packets.md
      frozen at packet commit e9c92091 on evidence revision 1e175108, with the agenda
      rows BC-128--BC-131 updated. Result: BC-129 stopped (no paired sample, the 2.8x
      condition never held, sequential resumable wall priced at about 5.6 hours);
      BC-130 a conditional candidate needing an exp-054 pass and a separate
      side-semantics preregistration; BC-131 stopped with the source refusal retained
      behind the n = 54 negative-control and frozen-input repairs; BC-125 earns no
      branch. Three packets carry exp-053, exp-054 and exp-055 with exact hashes,
      declared absences, safe commands, one required mutation each and the unchanged
      claim boundary; n = 54 has no packet because BC-126 produced no experiment
      decision. Guard: no second-wave agent was dispatched, no target, network or
      source command was named as safe, and no hypothesis field or review flag
      changed. Next: dispatch three fresh reviewers, one packet each.
    evidence:
    - docs/project/reviews/review-2026-09-02-agenda014-first-wave-packets.md
    - packing/campaign/agendas/agenda-014-mechanism-first-continuation-and-provenance-closure.md
    stop_reason: >-
      Three packets and one routing decision per lane are frozen at a passing record
      gate.
    next_action: >-
      Dispatch the three BC-135 reviewers against packet commit e9c92091.
  - workflow: factual-review
    focus: correctness
    recording: contemporaneous
    clock_role: work
    objective: >-
      BC-135: three preassigned read-only reviewers replay only packet-declared safe
      loaders, self-tests and mutations in parallel, one packet each; reconcile
      experiment-level pass, bounded-caveat, discrepancy or cannot-reproduce findings;
      retain and validate the review record.
    commitment: BC-135
    bead: think-bpzq
    status: completed
    entered_by: planned_checkpoint
    switch_reason: >-
      BC-128 is terminal with three frozen packets at commit e9c92091.
    budget_minutes: 60
    started_at: '2026-09-02T04:21:11Z'
    deadline_at: '2026-09-02T05:21:11Z'
    expected_output: >-
      docs/project/reviews/review-2026-09-02-agenda014-first-wave-independent-review.md
      with one determination per experiment, each reviewer's Artifact / Result / Guard
      / Next, and no change to any frozen decision.
    validation_command: >-
      uv run --frozen --all-extras --group dev packing-validate --records
    kill_condition: >-
      Stop a reviewer on any repository write, network request, target or producer
      command, or on a listed evidence path that differs from 1e175108.
    fallback: >-
      Record the affected experiment as typed-incomplete and leave needs_review true.
    outcome: >-
      Artifact:
      docs/project/reviews/review-2026-09-02-agenda014-first-wave-independent-review.md
      with the frozen review surface, three assignments and three separate
      determinations. Result: exp-053, exp-054 and exp-055 each pass; every packet hash
      matched at 1e175108, every required mutation rejected, every declared absence
      held, and no reviewer found a frozen limitation that prevents clearance. Guard:
      no reviewer wrote a repository file, made a network request, or ran a pair,
      assemble, production or producer command; one commit landed during the window
      (377a155c, session-076 only) and every reviewer re-ran the evidence diff at the
      new head and found it clean. Eleven packet facts are retained for the next
      packet author. Next: BC-136 holds permission to clear the three review flags but
      remains paused; close this session without applying them.
    evidence:
    - docs/project/reviews/review-2026-09-02-agenda014-first-wave-independent-review.md
    stop_reason: >-
      Every in-cap first-wave experiment decision has a durable determination.
    next_action: >-
      Close the session: records, generated views, rollup, validation, tbd, push and
      the PR checkpoint comment, leaving BC-136 unopened.
  - workflow: process-review
    focus: process
    recording: contemporaneous
    clock_role: work
    objective: >-
      Close session-076: update the agenda, synopsis and generated views, write this
      session's Claude rollup, run the record and push validation tiers, synchronize
      tbd, commit, push and post the PR checkpoint comment. Do not open BC-136, clear a
      review flag or write an overnight agenda.
    commitment: BC-135
    bead: think-bpzq
    status: completed
    entered_by: planned_checkpoint
    switch_reason: >-
      BC-135 is complete with three determinations recorded.
    budget_minutes: 40
    started_at: '2026-09-02T04:30:30Z'
    deadline_at: '2026-09-02T05:10:30Z'
    expected_output: >-
      A pushed revision with green record and push tiers, a synchronized bead tree and
      a PR comment naming the revision, cost and next entry.
    validation_command: >-
      uv run --frozen --all-extras --group dev packing-validate --push
    kill_condition: >-
      Stop on a gate failure that would require changing a frozen evidence path or a
      review flag.
    fallback: >-
      Push the last green revision and report the exact failing step.
    outcome: >-
      Artifact: the closed agenda rows BC-127, BC-128 and BC-135, the Current Handoff,
      the regenerated document map, ledger, agenda map and session-cost views, this
      record's Claude rollup and six sub-agent rollups, and synchronized beads. Result:
      the record gate passed on the closed tree and the push tier ran before the push;
      the PR checkpoint comment names the pushed revision and its cost. Guard: BC-136
      stayed unopened, no review flag was cleared, no overnight agenda was written, and
      no frozen evidence path changed. The rollup was written before the final commit
      and push, so those last commands are outside its span. Next: BC-136 under
      think-oa22 on a new owner instruction.
    evidence:
    - packing/campaign/agendas/agenda-014-mechanism-first-continuation-and-provenance-closure.md
    - SYNOPSIS.md#current-handoff
    - packing/campaign/resource-usage/7e50f2aa-a36b-5d97-8e99-bf910369266c.yaml
    stop_reason: >-
      The three blocks the owner's resume instruction named are terminal and the
      checkpoint is published.
    next_action: >-
      Take BC-136 under think-oa22 only on a new owner instruction.
  primary_bead: think-v0rj
  status: completed
  budget:
    wall_minutes: 240
    max_cycles: 8
    orientation_minutes: 15
    checkpoint_minutes: 30
    slice_minutes: 30
    finalization_minutes: 45
  stop_conditions:
  - The 2026-09-02T08:01:34Z wall deadline arrives.
  - A frozen first-wave evidence path, scientific criterion, threshold or target scope would have to change.
  - A review would require running a scientific target, network or source command.
  - The owner asks for a pause or a checkpoint.
  progress:
    metric: reviewed first-wave experiment decisions and frozen routing decisions
    before: >-
      three review-pending experiment decisions, one blocked n = 54 packet, no W5
      receipt, no routing decision and no independent review
    after: >-
      three first-wave experiment decisions independently reviewed as pass, one
      no-change W5 decision with five routed entries, and one conditional candidate
      route (BC-130) with BC-129 and BC-131 stopped; no review flag cleared and no
      overnight agenda written
  delegations:
  - task: BC-135 Packet A review, n = 17 / exp-053
    operator: claude sub-agent reviewer-a
    status: completed
    recording: contemporaneous
    outcome: >-
      Determination pass. All twelve frozen hashes matched at 1e175108 and in the
      working tree; receipt.json reads mode serial and elapsed_ns 524743164166 with
      fragment hashes in packet order; seven focused tests passed; normal and
      optimized self-tests each emitted 30 guards and stdout SHA-256
      0c256e5a164078119ffb3a98e9de2825c733a02cfbcff1c1b0aa8a6d28da0958; both named
      mutations rejected; every declared absence held after replay. The records
      nowhere assert a paired sample, a measured 2.8x or a speedup claim for arm A.
    evidence:
    - docs/project/reviews/review-2026-09-02-agenda014-first-wave-packets.md
    - docs/project/reviews/review-2026-09-02-agenda014-first-wave-independent-review.md
    files:
    - none retained in the repository; temporary data only under the reviewer's scratchpad directory
    checks:
    - git diff --exit-code 1e175108 over the evidence paths was empty before and after replay.
    - git status --porcelain was empty at the end of the review; only gitignored __pycache__ was created.
    - No pair or assemble subcommand ran; selftest ran twice.
    uncertainty: >-
      The frozen run's host was macOS arm64 and the replay ran on Linux, so the
      identical self-test receipt is cross-platform evidence rather than a same-host
      repeat. The receipt hash is the SHA-256 of the self-test's stdout including its
      trailing newline, which the packet did not state.
    elapsed_seconds: 338
    elapsed_quality: platform_measured
    next_action: Return Artifact / Result / Guard / Next and one determination for exp-053.
    phase: 4
    budget_minutes: 35
    started_at: '2026-09-02T04:22:00Z'
    deadline_at: '2026-09-02T04:57:00Z'
    expected_output: One determination for exp-053 with replay evidence.
    validation_command: >-
      uv run --frozen --all-extras --group dev pytest -q
      tests/test_n17_weighted_certificate_parallel.py
    kill_condition: >-
      Any repository write, pair or assemble command, or evidence path differing from
      1e175108.
    fallback: Report cannot-reproduce with the exact failing step.
    write_scope:
    - operating-system and pytest temporary directories only
    excluded_commands:
    - benchmarks.n17_weighted_certificate_parallel pair or assemble with any real root
    - git, tbd or repository writes
  - task: BC-135 Packet B review, n = 68 / exp-054
    operator: claude sub-agent reviewer-b
    status: completed
    recording: contemporaneous
    outcome: >-
      Determination pass. All nine frozen hashes matched at 1e175108 and in the
      working tree; the entry point runs only the literal self-test with the synthetic
      SVG and a temporary root; mark_selected_path checks its bounds before descent;
      35 focused tests, Ruff and BasedPyright passed; the depth regression and
      whole-result verifier mutations rejected; the receipt observed inside the
      suite's subprocess was 1,112 bytes at SHA-256
      becb4c7f865f2f4b3a9d6bd22b11bb736efe73ba2d7dc97e025cd4becbd55906 under normal
      and optimized Python with exactly twenty mutation names; the exp-054 and
      exp-051 result paths stayed absent. The round supplies no H-058 sample.
    evidence:
    - docs/project/reviews/review-2026-09-02-agenda014-first-wave-packets.md
    - docs/project/reviews/review-2026-09-02-agenda014-first-wave-independent-review.md
    files:
    - none retained in the repository; temporary data only under the reviewer's scratchpad directory
    checks:
    - git diff --exit-code 1e175108 over the nine paths was empty before and after replay.
    - No network request; the one attempt to hand-run the registered command was refused by the permission classifier before executing.
    - The receipt hash came from a scratchpad-only pytest plugin hashing the stdout the test captures.
    uncertainty: >-
      The receipt hash is invariant across the depth-guard correction, so it attests
      the correction only together with the four current file hashes and the 34-to-35
      test count. Three n = 68 SVGs are tracked under the atlas and web archive; the
      production package opens no file on disk.
    elapsed_seconds: 423
    elapsed_quality: platform_measured
    next_action: Return Artifact / Result / Guard / Next and one determination for exp-054.
    phase: 4
    budget_minutes: 35
    started_at: '2026-09-02T04:22:00Z'
    deadline_at: '2026-09-02T04:57:00Z'
    expected_output: One determination for exp-054 with replay evidence.
    validation_command: >-
      uv run --frozen --all-extras --group dev pytest -q
      tests/test_unitsquare_precision_production.py
    kill_condition: >-
      Any repository write, network request, hand-run registered command, or evidence
      path differing from 1e175108.
    fallback: Report cannot-reproduce with the exact failing step.
    write_scope:
    - operating-system and pytest temporary directories only
    excluded_commands:
    - cases.unitsquare_precision.production.run invoked by hand
    - any network, source or target access
    - git, tbd or repository writes
  - task: BC-135 Packet C review, n = 50 / exp-055
    operator: claude sub-agent reviewer-c
    status: completed
    recording: contemporaneous
    outcome: >-
      Determination pass. All thirteen frozen hashes matched at 1e175108 and in the
      working tree; the result's six instrument bindings, producer binding and both
      exp-050 bindings equal the computed values; the independent verifier exited 0
      under normal and optimized Python with identical 390-byte stdout hashing to
      64d37a00c43384033adedc94e1c4ba42ad1010a6f419d5b17f07c14265b73ccc; 21 focused
      tests passed; all five named verifier mutations including review-cleared
      rejected; the four stage sentinels each calibrate once and all twelve
      producer-side mutation leaves are rejected true. The claim boundary is pinned
      verbatim in verify.py, the result and the record.
    evidence:
    - docs/project/reviews/review-2026-09-02-agenda014-first-wave-packets.md
    - docs/project/reviews/review-2026-09-02-agenda014-first-wave-independent-review.md
    files:
    - none retained in the repository; temporary data only under the reviewer's scratchpad directory
    checks:
    - git diff --exit-code 1e175108 over the thirteen paths was empty before and after replay.
    - The producer --record command and --selftest were not run; no network or geometry access.
    - exp-050 hashes ab00e50debe0bc60279ce3472ed0c09eb062e8271a481a38c6ac65036aff4a02 after replay.
    uncertainty: >-
      The 0.72-second publication figure is a session-record attestation that Packet
      C cannot replay. needs_review true exists both in the experiment record and
      inside the immutable result; only the record's field may ever be cleared, since
      the verifier requires the result's field and the review-cleared mutation proves
      it.
    elapsed_seconds: 319
    elapsed_quality: platform_measured
    next_action: Return Artifact / Result / Guard / Next and one determination for exp-055.
    phase: 4
    budget_minutes: 35
    started_at: '2026-09-02T04:22:00Z'
    deadline_at: '2026-09-02T04:57:00Z'
    expected_output: One determination for exp-055 with replay evidence.
    validation_command: >-
      uv run --frozen --all-extras --group dev pytest -q
      tests/test_n050_producer_refusal.py tests/test_n050_producer_refusal_independent.py
    kill_condition: >-
      Any repository write, exp-055 --record invocation, geometry or source access, or
      evidence path differing from 1e175108.
    fallback: Report cannot-reproduce with the exact failing step.
    write_scope:
    - operating-system and pytest temporary directories only
    excluded_commands:
    - cases.n050_producer_refusal.run --record
    - n = 19 or n = 50 geometry or source access
    - git, tbd or repository writes
  outputs:
  - packing/campaign/agent-sessions/session-076-agenda014-first-wave-closeout-and-review.md
  - docs/project/reviews/review-2026-09-02-agenda014-first-wave-efficiency.md
  - docs/project/reviews/review-2026-09-02-agenda014-first-wave-packets.md
  - docs/project/reviews/review-2026-09-02-agenda014-first-wave-independent-review.md
  - packing/devtools/render_wave_efficiency.py
  - packing/tests/test_render_wave_efficiency.py
  - packing/campaign/agendas/agenda-014-mechanism-first-continuation-and-provenance-closure.md
  - SYNOPSIS.md#current-handoff
  - packing/campaign/resource-usage/7e50f2aa-a36b-5d97-8e99-bf910369266c.yaml
  - packing/campaign/resource-usage/agent-a7d8aae14a834dc35.yaml
  - packing/campaign/resource-usage/agent-a7cd7d666385121d0.yaml
  - packing/campaign/resource-usage/agent-a6f56836f1d49ad37.yaml
  - packing/campaign/resource-usage/agent-a83a6c7bceb3e5328.yaml
  - packing/campaign/resource-usage/agent-aa6ff0a4866d6ae7a.yaml
  - packing/campaign/resource-usage/agent-a5781a0c4bc6c49b5.yaml
  checks:
  - >-
    The record gate passed on the unchanged frozen tree at session start (11.6 s) and
    again on the closed tree.
  - >-
    uv run --frozen --all-extras --group dev pytest -q tests/test_render_wave_efficiency.py
    passed four controls; Ruff and BasedPyright are clean on the new tool and test.
  - >-
    Every first-wave evidence path was byte-identical to 1e175108 before and after each
    reviewer's replay, and no reviewer wrote a repository file.
  - >-
    Three reviewers returned pass with every packet hash, required mutation and
    declared absence reproduced; needs_review stays true on exp-053, exp-054 and
    exp-055.
  - >-
    The push tier ran before the push; its outcome is recorded in the PR checkpoint
    comment.
  resource_rollups:
  - packing/campaign/resource-usage/7e50f2aa-a36b-5d97-8e99-bf910369266c.yaml
  - packing/campaign/resource-usage/agent-a7d8aae14a834dc35.yaml
  - packing/campaign/resource-usage/agent-a7cd7d666385121d0.yaml
  - packing/campaign/resource-usage/agent-a6f56836f1d49ad37.yaml
  - packing/campaign/resource-usage/agent-a83a6c7bceb3e5328.yaml
  - packing/campaign/resource-usage/agent-aa6ff0a4866d6ae7a.yaml
  - packing/campaign/resource-usage/agent-a5781a0c4bc6c49b5.yaml
  stop_reason: >-
    The owner's resume instruction named BC-127, BC-128 and BC-135; all three are
    terminal, every first-wave decision has an independent determination, and the
    checkpoint is published without opening BC-136.
  next_action: >-
    Take BC-136 under think-oa22 only on a new owner instruction; it may clear the
    three review flags and write the separate overnight agenda from the one
    conditional route.
---
# Session 076 — Agenda-014 First-Wave Closeout, Routing and Independent Review

This session resumes Agenda 014 from the pushed PR #73 checkpoint at revision
`1e175108`, on the owner’s explicit resume instruction.
It owns the shared campaign records, review documents, Git, tbd, validation and
publication.
Reviewer sub-agents own only read-only replay against packet-declared paths.

The recorded entry is BC-127, then BC-128, then BC-135 under `think-bpzq`. BC-136 and
every second-wave lane remain unopened unless the owner authorizes them separately.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
