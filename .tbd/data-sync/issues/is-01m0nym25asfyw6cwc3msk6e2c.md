---
type: is
id: is-01m0nym25asfyw6cwc3msk6e2c
title: "PyO3 bindings: load, verify, Packing, Certificate"
kind: task
status: closed
priority: 2
version: 5
spec_path: docs/project/specs/paused/plan-2026-08-22-minimal-packing-toolkit.md
labels: []
dependencies: []
parent_id: is-01m0p5tswc9s27gb5c1d3da27b
created_at: 2026-08-22T23:59:13.065Z
updated_at: 2026-10-12T23:52:06.528Z
closed_at: 2026-10-06T08:46:10.112Z
close_reason: "Superseded by decision: the Phase 5 epic think-u83z says the boundary is a native binary or a cdylib called with ctypes, not PyO3, and think-h0hd records 'PyO3 deferred indefinitely' in the toolkit plan."
resolution: canceled
duplicate_of: null
---
The simple surface. Existing verify_packing(..., sign=...) signature stays unchanged so test.sh keeps passing.
