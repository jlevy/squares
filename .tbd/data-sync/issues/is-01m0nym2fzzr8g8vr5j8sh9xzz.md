---
type: is
id: is-01m0nym2fzzr8g8vr5j8sh9xzz
title: Differential test against the Python oracle, plus certificate round-trip
kind: task
status: open
priority: 1
version: 1
spec_path: explorations/packing/docs/project/specs/active/plan-2026-08-22-minimal-packing-toolkit.md
labels: []
dependencies: []
parent_id: is-01m0nykzwb0b8kwndbvf27aefk
created_at: 2026-08-22T23:59:13.407Z
updated_at: 2026-08-22T23:59:13.407Z
---
The pure-Python verifier is the permanent reference. Rust must match it on Trump's packing, all six perturbations in negative_control.py down to delta=1e-100, and every corpus entry with exact data -- INCLUDING reproducing the float verifier's failure, since a fast path that accidentally became sound would mean the test is not testing what it claims.
