---
type: is
id: is-01m1w1x25n4vdmsy28kr4dxr9y
title: "PR #98 review R10: validation_report writes report.md non-atomically"
kind: bug
status: closed
priority: 2
version: 3
labels: []
dependencies: []
parent_id: is-01m1w1w81t7vmr0gem6d91wg8b
created_at: 2026-09-06T19:07:42.132Z
updated_at: 2026-09-06T19:16:35.294Z
closed_at: 2026-09-06T19:16:35.294Z
close_reason: "Fixed: report.md is written with strif.atomic_write_text."
resolution: null
duplicate_of: null
---
packing/benchmarks/validation_report.py:292 write_text. Fix: strif.atomic_write_text.
