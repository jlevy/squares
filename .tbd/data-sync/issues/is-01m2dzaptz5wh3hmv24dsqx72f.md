---
type: is
id: is-01m2dzaptz5wh3hmv24dsqx72f
title: "Coordinator: bound disjoint phase durations by worker lifetime"
kind: bug
status: open
priority: 1
version: 4
spec_path: docs/project/specs/active/plan-2026-09-10-n11-daytime-strategy-and-explainer.md
labels:
  - n11
  - calibration
  - admission
dependencies: []
parent_id: is-01m2b883ztxn7qazs98bndea6b
child_order_hints:
  - is-01m2e3bq7xfcqvn4apvvt3kxmc
hold: blocked
hold_until: null
created_at: 2026-09-13T18:09:03.326Z
updated_at: 2026-09-13T19:19:30.812Z
---
Independent exact-head review at fc3e314 found raw_seconds 100 with worker_elapsed_seconds 1 accepted. Check each phase and the sum of guaranteed disjoint worker phases against worker lifetime and exit ordering without summing overlapping parent phases.

## Notes

Repair committed in isolated 4b8d333a and integrated PR156 as dbbf8495. Producer validation and coordinator inventory now bound disjoint worker phase sum to elapsed, with combined and rounding-edge controls. Focused modules 132 passed (one host EPERM deselection). Independent exact-head review pending; no profile/target.
