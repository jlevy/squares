---
type: is
id: is-01m0r7rb2hs1vdeebqb33471w3
title: Cache reusable validation and build work with sound invalidation
kind: feature
status: open
priority: 1
version: 2
spec_path: explorations/packing/docs/project/specs/active/plan-2026-08-25-research-loop-efficiency-infrastructure.md
labels:
  - packing
  - review
  - focus-efficiency
  - performance
dependencies: []
parent_id: is-01m0r7q50gw0wepeaj1dzb7g3r
created_at: 2026-08-23T21:17:19.312Z
updated_at: 2026-08-26T03:02:05.329Z
---
Remove repeated source builds, parser startup, and unchanged artifact validation from hot loops using explicit dependency keys and inspectable cache metadata. Never cache scientific conclusions without all semantic inputs in the key.

Acceptance: invalidation tests cover source, schema, toolchain, options, and input changes; a no-cache mode produces equivalent results; cache hits are reported rather than inferred; stale entries fail closed; and cold/warm benchmarks quantify the speedup and storage cost.
