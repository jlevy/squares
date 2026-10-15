---
type: is
id: is-01m4zctkhz4k6pcptm7kjkw9pe
title: Profile and reduce repeated witness-schema validation cost
kind: task
status: in_progress
priority: 1
version: 4
spec_path: docs/project/specs/active/plan-2026-10-13-site-changelog.md
delegate: codex@spud10.local
labels: []
dependencies: []
parent_id: is-01m4wtv34pphy5w434wk13b85x
hold: null
hold_until: null
created_at: 2026-10-15T09:03:24.705Z
updated_at: 2026-10-15T09:27:46.358Z
started_at: 2026-10-15T09:04:47.752Z
---
Astra systematic CI follow-up: profile a complete retained upper-bound report operation before optimizing. Diagnostic identifies repeated witness structural validation, not packet/receipt loading, as dominant. Evaluate an already-pinned native schema backend only with independent Python acceptance/refusal equivalence, fresh schema reads, no cache or validation bypass, preserved exact error diagnostics and all mathematical/custody checks. Preregister acceptance through maintained validation-efficiency campaign. No assertions or ceilings relaxed.

## Notes

At CI97129538d, exact retained MISHAPOLK593 register-plan plus independent fresh check_claims passes38.14s under cProfile/concurrentload; diagnostic only.326witness validations19.54s cumulative,321fact validations19.32s;1247501schema descents/390878refs. Declaration38loads0.618s,custody36acquisitions1.334s,321recordreads0.093s,2receiptparses0.006s: packetbundle not justified. VE014 schema-reference inlining previously withdrew at12.80%; new VE016 native-witness backend is distinct and preregistered before execution. Uses existing jsonschema-rs0.49.9, successfulvalidationonly, refusing native retriever, formatsfalse, unchanged Python refusaldiagnostics/fallback. First oracle25pass/1fail caught native tuple coercion; failedreceipt retained, no speedupclaim. A small plain-JSON eligibility guard is under implementation with unsupportedtypes/cycles/nonfinite/customschema edge tests; reject if complexity grows or equivalencefails. Three alternating uncontended complete-operation pairs must allpass/noskips,median>=15%,nonoverlap,allocation<=1.25. Acceptance timings held during focused UIgate. Agent owns only witness/testcontract/campaign, rootcommits.
