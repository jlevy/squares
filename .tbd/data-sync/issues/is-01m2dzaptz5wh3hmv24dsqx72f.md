---
type: is
id: is-01m2dzaptz5wh3hmv24dsqx72f
title: "Coordinator: bound disjoint phase durations by worker lifetime"
kind: bug
status: closed
priority: 1
version: 6
spec_path: docs/project/specs/active/plan-2026-09-10-n11-daytime-strategy-and-explainer.md
labels:
  - n11
  - calibration
  - admission
dependencies: []
parent_id: is-01m2b883ztxn7qazs98bndea6b
child_order_hints:
  - is-01m2e3bq7xfcqvn4apvvt3kxmc
hold: null
hold_until: null
created_at: 2026-09-13T18:09:03.326Z
updated_at: 2026-09-13T19:34:28.787Z
closed_at: 2026-09-13T19:34:28.776Z
close_reason: Disjoint worker phase sums and finite overflow now refuse against worker elapsed at integrated repair 775c71d5; independently accepted exact-head with finite near-limit controls. Later operational admission remains parent gate.
resolution: null
duplicate_of: null
---
Independent exact-head review at fc3e314 found raw_seconds 100 with worker_elapsed_seconds 1 accepted. Check each phase and the sum of guaranteed disjoint worker phases against worker lifetime and exit ordering without summing overlapping parent phases.

## Notes

Original disjoint-phase lifetime repair at dbbf8495 passed independent chronology/phase controls. A finite fsum OverflowError edge was then tracked under child think-dgfk and repaired at 775c71d5. Independent exact-head review accepted producer/coordinator domain refusal and finite near-limit acceptance; 141 focused tests passed. Later integrated operational gate remains under think-5dql/think-pp3j; no profile/target.
