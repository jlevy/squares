---
type: is
id: is-01m2dzapemsrp1hn26art77r69
title: "Coordinator: require raw tasks to precede normalized exact tasks"
kind: bug
status: open
priority: 1
version: 3
spec_path: docs/project/specs/active/plan-2026-09-10-n11-daytime-strategy-and-explainer.md
labels:
  - n11
  - calibration
  - admission
dependencies: []
parent_id: is-01m2b883ztxn7qazs98bndea6b
hold: blocked
hold_until: null
created_at: 2026-09-13T18:09:02.932Z
updated_at: 2026-09-13T19:17:51.825Z
---
Independent exact-head review at fc3e314 found coherent swapped task/child times with republished digests accepted. Enforce cross-route chronology against producer phase observations and preserve legal touching boundaries.

## Notes

Repair committed in isolated 4b8d333a and integrated PR156 as dbbf8495. Producer/coordinator digest-consistent inverted raw/exact task control now refuses; legal serial/touching controls pass. Focused modules 132 passed (one host EPERM deselection). Independent exact-head review pending; no profile/target.
