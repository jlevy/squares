---
type: is
id: is-01m4zjk1ck76q8j0j6v72pvd0c
title: Evaluate native validation only for the built-in witness schema
kind: task
status: in_progress
priority: 1
version: 4
spec_path: docs/project/specs/active/plan-2026-10-13-site-changelog.md
delegate: claude-code@spud10.local
labels: []
dependencies: []
parent_id: is-01m4zctkhz4k6pcptm7kjkw9pe
hold: blocked
hold_until: null
created_at: 2026-10-15T10:44:08.210Z
updated_at: 2026-10-15T13:21:52.248Z
started_at: 2026-10-15T10:44:18.254Z
---
Distinct bounded follow-up to rejected VE016: assess whether the native backend can be used only for the built-in Witness/v2 schema, with every explicit/custom schema continuing through the unchanged Python validator. Inspect actual default-schema constraints and fresh-read/mutation semantics before any candidate. Reject if preserving defaults requires a broad compatibility layer, schema hash binding or disabling an oracle. If viable, preregister a separate experiment and prove independent acceptance/refusal equivalence, full witness semantics and custom-schema fallback before timing. No implementation or speed claim is accepted from the failed VE016 run; all rejected evidence stays retained. Root coordinates any complete-operation timing after delivery work so it is uncontended.

## Notes

VE017 is evidence-only under primary .codex/regularization-closeout-evidence-2026-10-13/ci-default-witness/. Initial earlier variant passed55 portable controls; final56-case variant, full target/custody oracle, format/type and six timing samples remain unexecuted. Independent read-only review found no new semantic defect but identified instrument prerequisites: run_oracles.py selects only portable, and benchmarks.validation_timing removes PYTEST_ADDOPTS, so explicit external basetemp/failed-only retention/cache-disabled configuration and proof of loaded variant must be added before timing. Frozen protocol: three alternating A/B pairs, fresh serial Python3.14.7 processes,300s sample deadline, zero skips, at least15percent lower median inclusive wall, nonoverlapping ranges, allocation ratio at most1.25. Candidate maintenance is97productionlines and349testlines. Both delegated execution attempts were rejected by automatic approval review before process creation; relayed authorization was not accepted as direct trusted human authorization. Root asked the human directly via async tool; execution is paused pending reply. No acceptance, timing improvement or three-minute claim. All alternate resolved schema paths and ineligible schema/value profiles retain Python fallback; no schema hash/caching/math bypass.
