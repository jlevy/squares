---
type: is
id: is-01m4jjgm8npn9zv9h0wcq2yp2y
title: Qualify squish custody replay controls under final checkpoint resource contention
kind: bug
status: in_progress
priority: 1
version: 4
delegate: claude-code@spud10.local
labels: []
dependencies: []
parent_id: is-01m4h9s465x7mphy1xxkmdyqc9
hold: null
hold_until: null
created_at: 2026-10-10T09:32:41.610Z
updated_at: 2026-10-10T09:56:26.395Z
started_at: 2026-10-10T09:35:43.581Z
---
Hda22 final broad pre-push normal lane exposed existing 30-second and 60-second custody baseline subprocess deadlines in squish_followup_packets and second-squish controls while other host validation schedulers were active. Both traces report TimeoutExpired without semantic assertion failure; causes remain unestablished. Retain failed run, diagnose under a focused serial run, preserve all custody assertions and existing limits, and qualify actual hosted slow-lane execution. Root owns tracking and publication; no timeout relaxation by speculation.

## Notes

Focused serial rerun preserved every custody assertion and existing 30/60-second child deadlines: both replay controls passed in 116.15s. Original Hda22 timeouts remain failed evidence; host contention was observed but causal explanation remains unestablished. No control, cap or source edits. Actual hosted slow-lane execution at repaired published head remains required. Evidence final/replay-control-focused/focused.log and focused.xml.
