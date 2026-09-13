---
type: is
id: is-01m2e2cgg1w6jatzr0h3x8424p
title: "F6d: reject finite phase clocks whose aggregate overflows to infinity"
kind: bug
status: in_progress
priority: 1
version: 3
spec_path: docs/project/specs/active/plan-2026-09-10-n11-daytime-strategy-and-explainer.md
labels: []
dependencies: []
parent_id: is-01m2e19ncq107301gs2q7rg8b6
created_at: 2026-09-13T19:02:28.081Z
updated_at: 2026-09-13T19:16:19.582Z
---
Astra Max full real-binder review of reader commit 40600964 found seven finite 4e307 phase durations sum to infinity; _not_later(inf, finite) accepts due infinite ULP allowance. Producer permits finite clocks. Reject nonfinite aggregate/allowance arithmetic and retain boundary-positive finite controls; rereview exact integrated head before admission.

## Notes

Finite-clock repair committed as isolated 9bc76b32, cherry-picked to integrated PR156 as a5701e73. Real-binder overflow now refuses; finite equality passes. Reader module 112 passed; Ruff and BasedPyright clean. Independent exact-head rereview remains pending; no calibration admission or profile/target.
