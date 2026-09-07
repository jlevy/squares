---
type: is
id: is-01m1xpbwytf7473w9eyxag7hte
title: Isolate no-history gate fixtures from an enclosing Git checkout
kind: bug
status: closed
priority: 1
version: 3
spec_path: packing/campaign/agendas/agenda-028-hybrid-strength-and-angular-release.md
labels: []
dependencies: []
parent_id: is-01m1x7d097z73jgvwb22rh8brz
created_at: 2026-09-07T10:24:34.265Z
updated_at: 2026-09-07T10:36:03.945Z
closed_at: 2026-09-07T10:36:03.944Z
close_reason: Minimal fixture-only correction independently accepted; production ancestry semantics unchanged. Exact full-run red case retained; coordinator20 tests passed2.22s and independent nested-attic20 passed2.07s. Ruff and formatting passed. Full checkpoint validation remains separately tracked by session092.
resolution: null
duplicate_of: null
---
Full checkpoint57b85302 completed1644.33s with65 steps passing and one fast-test failure: test_session_gate.py no-git fixture lives under the authorized attic and Git discovers the enclosing repository, returning complete instead of unavailable. Preserve production ancestry semantics and all real-graph assertions; isolate only the two source-snapshot fixtures from ancestor discovery. Reproduce the exact failure, pass focused real-graph tests and independent review, then replay appropriate validation.

## Notes

Full57b85302 receipt supplies the exact red case. Minimal correction sets a per-test Git discovery ceiling for the two existing no-history fixtures only; production ancestry and real-graph tests unchanged. Focused replay and independent eight-minute review are in flight.
