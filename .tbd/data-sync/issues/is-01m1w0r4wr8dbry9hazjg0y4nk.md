---
type: is
id: is-01m1w0r4wr8dbry9hazjg0y4nk
title: "W5: retain incremental pytest phase timings through CI termination"
kind: task
status: open
priority: 2
version: 2
spec_path: docs/project/specs/active/plan-2026-09-06-validation-efficiency-and-checkpoints.md
labels: []
dependencies: []
parent_id: is-01m1vrrktbrd2scnaqfe40eby4
created_at: 2026-09-06T18:47:32.501Z
updated_at: 2026-09-06T20:17:02.816Z
---
Real cancellation audit of PR98 run34052435218 retained three command starts/partial logs and117 completed controls, but zero pytest per-case phase timings because JUnit/durations emit at exit. Add bounded incremental case/phase JSONL to the existing timing instrument, joining run/worker/node identity and preserving known completed phases after termination. Do not invent elapsed durations for unmatched starts. Test worker failures, xdist concurrency and hard process termination; bound overhead and retain current normal-run JUnit equivalence. Evidence: /tmp/pr98-cancelled-checkpoint-audit.json and run artifacts9995012355/9995012176. This addresses the documented incomplete-termination timing limit without another competing recorder.

## Notes

PR98 review restored the quick lane console filter at 12 seconds while retaining JUnit aggregate duration and outcome for every selected case. The follow-up therefore covers both incremental phase durability through termination and complete per-phase attribution for quick cases. Keep normal console output filtered; collect detailed machine-readable phase records with measured, bounded overhead. Current final ordinary run 34056428243 has 2,354 complete JUnit cases and only qualifying console phases, all matching case identities. Do not treat aggregate JUnit time as complete setup/call/teardown attribution.
