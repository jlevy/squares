---
type: is
id: is-01m2e3bq7xfcqvn4apvvt3kxmc
title: "Coordinator: refuse finite phase-sum overflow as invalid metrics"
kind: bug
status: closed
priority: 1
version: 2
spec_path: docs/project/specs/active/plan-2026-09-10-n11-daytime-strategy-and-explainer.md
labels: []
dependencies: []
parent_id: is-01m2dzaptz5wh3hmv24dsqx72f
created_at: 2026-09-13T19:19:30.812Z
updated_at: 2026-09-13T19:34:24.323Z
closed_at: 2026-09-13T19:34:24.321Z
close_reason: Isolated repair 30f69dca integrated as 775c71d5; independent exact-head review accepted producer/coordinator domain refusals for finite phase-sum OverflowError and JSON/derived infinite deadlines. Supervised terminal now retains invalid/metrics-refused, finite near-limit controls pass, 141 focused tests passed. No positive profile/BC329 target.
resolution: null
duplicate_of: null
---
Independent exact-head coordinator review at dbbf8495 found two individually finite 1e308 worker phase durations cause math.fsum OverflowError in producer terminal admission and coordinator inventory. The supervised producer turns this into partial/operational-failure instead of an invalid metrics refusal; the coordinator raises raw OverflowError. Add finite aggregate refusal semantics and target-free controls on both paths, preserving finite boundary acceptance. No positive calibration profile or BC329 target.
