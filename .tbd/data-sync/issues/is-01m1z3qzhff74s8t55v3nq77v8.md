---
type: is
id: is-01m1z3qzhff74s8t55v3nq77v8
title: Include runner identity in gate-budget reference matching
kind: bug
status: open
priority: 2
version: 2
labels: []
dependencies: []
created_at: 2026-09-07T23:37:36.045Z
updated_at: 2026-09-08T07:04:39.748Z
---
Session105 exposed a reference-shape collision: the clean bdc28e8985663827aae2f7d8219537197cfff189 fast run on a native 10-CPU macOS host used PYTHON_CPU_COUNT=4 and --jobs 3 --inner-jobs 1. It passed all 62 checks and the quick per-test guards in 254.691046958 seconds, but Reference.matches treated it as comparable to the recorded four-CPU Linux CI baseline of 502.3 seconds and failed the stale ratio at 0.507. The Linux baseline remains unchanged. development.md already states matching counts do not establish comparable hardware or load, while the implementation matches only CPU and worker counts. Preserve the run receipt in packing/campaign/agent-sessions/session-105-validation/fast-cpu4-bdc28e89.json. Specify a runner/platform-aware reference identity, including how CPU overrides are reported, before changing enforcement; independently calibrate the hosted Linux baseline. This is not evidence of a speedup and not a reason to weaken correctness or per-test guards.

Rename provenance: the source review was renamed from session-097 to session-105 during PR120’s collision reconciliation with PR116. The historical receipt contents are unchanged.
