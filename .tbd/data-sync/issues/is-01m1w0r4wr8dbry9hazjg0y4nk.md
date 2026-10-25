---
type: is
id: is-01m1w0r4wr8dbry9hazjg0y4nk
title: "W5: retain incremental pytest phase timings through CI termination"
kind: task
status: in_progress
priority: 2
version: 8
spec_path: docs/project/specs/active/plan-2026-09-06-validation-efficiency-and-checkpoints.md
delegate: codex-phase-timings-20261019
labels: []
dependencies: []
parent_id: is-01m0r7q50gw0wepeaj1dzb7g3r
child_order_hints:
  - is-01m5hetwhsq2nctxq35syf8e3p
hold: null
hold_until: null
created_at: 2026-09-06T18:47:32.501Z
updated_at: 2026-10-25T04:44:05.696Z
started_at: 2026-10-19T01:26:10.067Z
---
Real cancellation audit of PR98 run34052435218 retained three command starts/partial logs and117 completed controls, but zero pytest per-case phase timings because JUnit/durations emit at exit. Add bounded incremental case/phase JSONL to the existing timing instrument, joining run/worker/node identity and preserving known completed phases after termination. Do not invent elapsed durations for unmatched starts. Test worker failures, xdist concurrency and hard process termination; bound overhead and retain current normal-run JUnit equivalence. Evidence: /tmp/pr98-cancelled-checkpoint-audit.json and run artifacts9995012355/9995012176. This addresses the documented incomplete-termination timing limit without another competing recorder.

## Notes

PR98 review restored the quick lane console filter at 12 seconds while retaining JUnit aggregate duration and outcome for every selected case. The follow-up therefore covers both incremental phase durability through termination and complete per-phase attribution for quick cases. Keep normal console output filtered; collect detailed machine-readable phase records with measured, bounded overhead. Current final ordinary run 34056428243 has 2,354 complete JUnit cases and only qualifying console phases, all matching case identities. Do not treat aggregate JUnit time as complete setup/call/teardown attribution.

2026-10-22 coordinator recovery:
Continuation authorized 2026-10-22 09:05:03-14:05:03 UTC, finalization from13:35:03, with unchanged4GiB/no-swap/two-CPU/one-workload limits. Reclaimed as verified original owner, synced and reread. Current source main0281e776342f2f1b63d3df66dc3c1737e8202945; branch codex/phase-timings-20261022; reserve Session188. Existing three timing/progress/report test files pass47tests in10.74s. Old unpublished producer and v1 observations are preserved separately. New implementation will reuse the current progress writer and timing/report modules, add actual completed-phase durations and real worker/termination controls, and measure a separately declared v2 six-observation whole-CLI overhead protocol. Independent design review found no blocker; current-source implementation/measurement/CI acceptance remains pending.

2026-10-23 coordinator closeout (Asia/Shanghai):

The operator requested prompt final closeout. Autonomous research has stopped; the original October 22 09:05:03-14:05:03 UTC window was not extended. A separate bounded administrative closeout preserves the interrupted source, honest terminal record and handoff. Session188 is stopped with certification_pending: think-uhxt. Keep this task open; this note does not certify the contribution.

The local codex/phase-timings-20261022 branch retains completed pytest phase durations, existing-writer/recorder/reader integration, 158 passing focused controls and the single fixed six-observation v2 overhead screen. The fixture-specific median ratio is 1.0482579964409449 and the added median is 0.05250601399995958 seconds; no general CI performance or mathematical claim follows. Independent source/evidence and privacy review was completed. The prior records rerun passed all52 selected checks with unchanged source and verified cleanup.

The complete local pre-push result remains failed:68 of69 selected steps passed, but the390-dark native-frontier HTTP test observed longestTaskMs339 against the unchanged300ms limit, and the reachable behavior lane subsequently hit its unchanged900-second cap. The assertion's cause is unisolated and coverage is incomplete. Neither limits nor verdicts were relaxed.

The service usage interruption occurred before submission. No new PR, remote branch push, data release, asset upload or hosted CI was performed for this phase-timing branch. Original and redacted evidence, exact source freezes and all failed/interrupted receipts remain retained locally. The native cost checkpoint is explicitly incomplete and ends at10:44:02UTC; the interruption gap is not claimed as active work. Historical Session187 and think-1ozu remain unchanged.

Next action, only on subsequent operator authorization: refresh upstream/TBD and source ownership, inspect the saved local commit/freeze and independent handoff, resolve or establish a supported disposition for the actual HTTP failure, then obtain required exact-source/base qualification and audit before public acceptance. No unattended continuation is scheduled.

2026-10-25 authorized continuation:
Guzhou authorized work from 2026-10-25T04:30:32Z until06:40:00Z, with finalization from06:10:00Z. The canonical branch is codex/phase-timings-20261025, integrating current main3699ce15ee119beb0c4714cab4b0692c4bb44f1f while retaining producered63f11c and the exact stopped Session188 history. Resource limits remain4GiB hard memory, no task swap, two visible CPUs and one owned workload. Current upstream requires edit plus directly affected tests before a draft push; hosted acceptance remains separate and exact-head. No auto-merge is authorized. Historical HTTP339ms/300ms failure and900-second incomplete lane remain retained; changed current page/probe inputs do not explain that observation.
Continue the smallest unfinished contribution: durable completed-phase timing, current-source qualification, independent audit and provisional draft if ready. Do not repeat the fixed v2 experiment or claim final certification from a records-tier or draft pass. Keep the task open until its actual acceptance contract is satisfied.
