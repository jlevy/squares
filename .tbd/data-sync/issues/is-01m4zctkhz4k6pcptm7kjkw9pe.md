---
type: is
id: is-01m4zctkhz4k6pcptm7kjkw9pe
title: Profile and reduce repeated witness-schema validation cost
kind: task
status: in_progress
priority: 1
version: 6
spec_path: docs/project/specs/active/plan-2026-10-13-site-changelog.md
delegate: codex@spud10.local
labels: []
dependencies: []
parent_id: is-01m4wtv34pphy5w434wk13b85x
child_order_hints:
  - is-01m4zjk1ck76q8j0j6v72pvd0c
hold: null
hold_until: null
created_at: 2026-10-15T09:03:24.705Z
updated_at: 2026-10-15T10:44:08.210Z
started_at: 2026-10-15T09:04:47.752Z
---
Astra systematic CI follow-up: profile a complete retained upper-bound report operation before optimizing. Diagnostic identifies repeated witness structural validation, not packet/receipt loading, as dominant. Evaluate an already-pinned native schema backend only with independent Python acceptance/refusal equivalence, fresh schema reads, no cache or validation bypass, preserved exact error diagnostics and all mathematical/custody checks. Preregister acceptance through maintained validation-efficiency campaign. No assertions or ceilings relaxed.

## Notes

The complete register-plan profile identified repeated Witness/v2 schema validation as the dominant measured diagnostic cost; profiler/concurrent-load timing is not an acceptance baseline. VE-016 attempted the already-pinned native backend, but the independent equivalence oracle rejected it before timing: native acceptance differs for multipleOf 0.1 with 0.3 and named regex syntax. Production and test candidates were restored byte-for-byte to control 97129538; no policy, schema, assertion, marker or ceiling changed. Exact source variants, failures, JUnit, profile and restoration evidence are preserved outside disposable scratch in .codex/regularization-closeout-evidence-2026-10-13/ci-ve016/. Retain the negative experiment record; pursue the separately scoped quick-push/default and native loadfile slice in think-gg64/think-ly7p without claiming the selected strict PR599 timing gate is fixed.
