---
type: is
id: is-01m0nym2fzzr8g8vr5j8sh9xzz
title: Differential test against the Python oracle, plus certificate round-trip
kind: task
status: closed
priority: 1
version: 2
spec_path: explorations/packing/docs/project/specs/active/plan-2026-08-22-minimal-packing-toolkit.md
labels: []
dependencies: []
parent_id: is-01m0nykzwb0b8kwndbvf27aefk
created_at: 2026-08-22T23:59:13.407Z
updated_at: 2026-08-23T05:26:18.301Z
closed_at: 2026-08-23T05:26:18.301Z
close_reason: "Done and in the gate: differential_test.py checks sqsearch pair energy against sqpack validity on 20,000 near-contact pairs, mutation-checked. Certificate round-trip remains with think-0md2."
---
The pure-Python verifier is the permanent reference. Rust must match it on Trump's packing, all six perturbations in negative_control.py down to delta=1e-100, and every corpus entry with exact data -- INCLUDING reproducing the float verifier's failure, since a fast path that accidentally became sound would mean the test is not testing what it claims.
