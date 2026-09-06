---
type: is
id: is-01m1vs7vtqsgtnh2m15kc2bw49
title: "W5: retain detailed timing records for long tests, controls, and CI"
kind: task
status: in_progress
priority: 1
version: 3
spec_path: docs/project/specs/active/plan-2026-09-06-validation-efficiency-and-checkpoints.md
labels: []
dependencies: []
parent_id: is-01m1vrrktbrd2scnaqfe40eby4
created_at: 2026-09-06T16:36:18.902Z
updated_at: 2026-09-06T19:50:29.409Z
---

## Notes

Detailed timing capture and failure artifacts are implemented and were audited on successful and failed hosted runs. Parallel review restored the quick lane console filter while retaining per-case aggregate JUnit times; separate subthreshold quick phases are not recorded, and incremental complete phase records remain tracked as think-uhxt. A combined regression exposed a fake-PID test calling real os.killpg; the call is now mocked and asserted, and 126 affected tests passed. Final combined hosted checkpoint remains pending.
