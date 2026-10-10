---
type: is
id: is-01m4jjgm8npn9zv9h0wcq2yp2y
title: Qualify squish custody replay controls under final checkpoint resource contention
kind: bug
status: in_progress
priority: 1
version: 3
delegate: claude-code@spud10.local
labels: []
dependencies: []
parent_id: is-01m4h9s465x7mphy1xxkmdyqc9
hold: null
hold_until: null
created_at: 2026-10-10T09:32:41.610Z
updated_at: 2026-10-10T09:36:04.154Z
started_at: 2026-10-10T09:35:43.581Z
---
Hda22 final broad pre-push normal lane exposed existing 30-second and 60-second custody baseline subprocess deadlines in squish_followup_packets and second-squish controls while other host validation schedulers were active. Both traces report TimeoutExpired without semantic assertion failure; causes remain unestablished. Retain failed run, diagnose under a focused serial run, preserve all custody assertions and existing limits, and qualify actual hosted slow-lane execution. Root owns tracking and publication; no timeout relaxation by speculation.
