---
type: is
id: is-01m4ef8v5j2n64y9bmvbkzt1n9
title: Measure the delayed startup control within its own readiness wait
kind: bug
status: in_progress
priority: 1
version: 2
spec_path: docs/project/specs/active/plan-2026-10-06-exact-side-values.md
delegate: codex@spud10.local
labels: []
dependencies: []
parent_id: is-01m4e2gm6ya1mxg40qmv53ysbn
hold: null
hold_until: null
created_at: 2026-10-08T19:19:03.078Z
updated_at: 2026-10-08T19:23:14.628Z
started_at: 2026-10-08T19:23:14.620Z
---
Parent Pages typography control compares two independent navigation timings, so slow baseline startup can hide the injected 300 ms readiness delay. Use the probe's measured readiness-call wait for the known-delay control, retain missing-instrumentation refusal and all production geometry/latency checks, add negative controls, and verify both stack layers.
