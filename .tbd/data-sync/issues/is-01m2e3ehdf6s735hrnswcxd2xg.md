---
type: is
id: is-01m2e3ehdf6s735hrnswcxd2xg
title: "Coordinator: reject parsed or derived infinite deadline identity"
kind: bug
status: open
priority: 1
version: 1
spec_path: docs/project/specs/active/plan-2026-09-10-n11-daytime-strategy-and-explainer.md
labels: []
dependencies: []
parent_id: is-01m2b883ztxn7qazs98bndea6b
created_at: 2026-09-13T19:21:03.132Z
updated_at: 2026-09-13T19:21:03.132Z
---
Independent coordinator review at dbbf8495 found a digest/count-consistent synthetic receipt with finite origin=1e308, calibration_seconds=1e308, external_seconds=1.1e308 and deadline JSON numerals 1e999 accepted by real inventory_profile. Python json parses 1e999 to inf; expected origin+allowance also overflows to inf, so equality passes. Confirm producer parity and refuse nonfinite parsed or derived deadlines before matching. This is a preexisting boundary, not evidence the dbbf repair caused it. Add target-free control; no positive profile/BC329 target.
