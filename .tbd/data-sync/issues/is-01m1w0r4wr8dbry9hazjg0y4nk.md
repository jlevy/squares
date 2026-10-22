---
type: is
id: is-01m1w0r4wr8dbry9hazjg0y4nk
title: "W5: retain incremental pytest phase timings through CI termination"
kind: task
status: in_progress
priority: 2
version: 6
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
updated_at: 2026-10-22T09:24:50.872Z
started_at: 2026-10-19T01:26:10.067Z
---
Real cancellation audit of PR98 run34052435218 retained three command starts/partial logs and117 completed controls, but zero pytest per-case phase timings because JUnit/durations emit at exit. Add bounded incremental case/phase JSONL to the existing timing instrument, joining run/worker/node identity and preserving known completed phases after termination. Do not invent elapsed durations for unmatched starts. Test worker failures, xdist concurrency and hard process termination; bound overhead and retain current normal-run JUnit equivalence. Evidence: /tmp/pr98-cancelled-checkpoint-audit.json and run artifacts9995012355/9995012176. This addresses the documented incomplete-termination timing limit without another competing recorder.

## Notes

PR98 review restored the quick lane console filter at 12 seconds while retaining JUnit aggregate duration and outcome for every selected case. The follow-up therefore covers both incremental phase durability through termination and complete per-phase attribution for quick cases. Keep normal console output filtered; collect detailed machine-readable phase records with measured, bounded overhead. Current final ordinary run 34056428243 has 2,354 complete JUnit cases and only qualifying console phases, all matching case identities. Do not treat aggregate JUnit time as complete setup/call/teardown attribution.

2026-10-22 coordinator recovery:
Continuation authorized 2026-10-22 09:05:03-14:05:03 UTC, finalization from13:35:03, with unchanged4GiB/no-swap/two-CPU/one-workload limits. Reclaimed as verified original owner, synced and reread. Current source main0281e776342f2f1b63d3df66dc3c1737e8202945; branch codex/phase-timings-20261022; reserve Session188. Existing three timing/progress/report test files pass47tests in10.74s. Old unpublished producer and v1 observations are preserved separately. New implementation will reuse the current progress writer and timing/report modules, add actual completed-phase durations and real worker/termination controls, and measure a separately declared v2 six-observation whole-CLI overhead protocol. Independent design review found no blocker; current-source implementation/measurement/CI acceptance remains pending.
