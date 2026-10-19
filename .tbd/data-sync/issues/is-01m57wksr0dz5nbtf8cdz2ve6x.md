---
type: is
id: is-01m57wksr0dz5nbtf8cdz2ve6x
title: Fix supervisor signal test worker PID capture
kind: bug
status: in_progress
priority: 2
version: 3
delegate: codex@spud10.local
labels: []
dependencies: []
parent_id: is-01m578snhcmb9xf25bnb3atvy8
hold: null
hold_until: null
created_at: 2026-10-18T16:13:14.354Z
updated_at: 2026-10-18T16:18:11.760Z
started_at: 2026-10-18T16:13:56.625Z
---
At clean #676 head372902046, the CPU6/n5 push signal control failed ProcessLookupError because its global subprocess.Popen monkeypatch overwrote worker-SIGTERM.pid with RSS observer PID1992; the retained receipt identifies actual worker/coordinator1989 with exit-15 and process_group_reaped true. Restrict the test-only publication and injected-signal path to the exact start_new_session worker command, assert captured PID equals receipt coordinator_pid, and retain the existing process-absence assertion. Production supervision and deadlines remain unchanged. Retained failure and diagnosis: /Volumes/spud-ext1/agent-source/squares-intake-20261018-evidence/signal-fixture-372902046-n5/. Timed subprocess controls and full qualification wait for the coordinator-released heavy slot.

## Notes

2026-10-18 narrow fixture repair committed clean2a7a11ea6bb7503e6a46b23a5d95451827d64c1b. Exactly7 test lines: define exact worker_command; guard PID publication/injected signal by command equality and start_new_session=True; assert captured PID equals receipt coordinator_pid. Existing ProcessLookupError assertion and production behavior/deadlines unchanged. Two mapped reports disclose the actual mismatch and stopped gate. Ruff check/format pass; normal isolated Flowmark/paper-title hooks pass2.27s. Timed3-param signal controls and neighbors are deliberately held until #665 releases the heavy slot. Failed receipt, PID and rss samples retained in signal-fixture-372902046-n5; diagnosis.json records captured1992 versus worker1989, worker exit-15/group_reaped true. Do not close before focused controls and exact-head qualification pass.
