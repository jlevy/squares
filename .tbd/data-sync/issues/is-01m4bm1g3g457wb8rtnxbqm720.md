---
type: is
id: is-01m4bm1g3g457wb8rtnxbqm720
title: Permit protected finalization reserve to use contiguous bounded phases
kind: bug
status: closed
priority: 1
version: 3
spec_path: docs/project/specs/active/plan-2026-10-06-n17-ten-hour-session.md
delegate: claude-code@spud10.local
labels: []
dependencies: []
parent_id: is-01m4bj7tj2ydjh2v673ga1mw8j
hold: null
hold_until: null
created_at: 2026-10-07T16:44:41.967Z
updated_at: 2026-10-07T16:53:54.930Z
started_at: 2026-10-07T16:44:50.712Z
closed_at: 2026-10-07T16:53:54.929Z
close_reason: "Limited repair committed f8ec2975937881c3e449e265735b4b24342305c4 after root review: contiguous finalization suffix accepted, later work refused, reserve/deadline/budget/final-only-active rules preserved. 21 focused session tests PASS 1.18s, independent two new controls PASS .24s, Ruff/format/types zero. Real JUnit and source/diff/static observation retained at attic/evidence/session-184-finalization-tail-800bba638/. This closes only the three-file repair; certification think-7hy3 and full current-source PASS obligation remain open."
resolution: null
duplicate_of: null
---
The session checker currently requires each finalization phase to be individually last, contradicting a protected finalization reserve split into bounded slices. Permit only a contiguous finalization suffix; preserve reserve-start, session/phase deadline budget and final-only in-progress rules. Own ledger.py, test_campaign_tools.py and agent-session.schema.yaml only. Two targeted controls must accept two finalization slices and refuse later work. This is additive focused source coverage, never a full checkpoint PASS.
