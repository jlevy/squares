---
type: is
id: is-01m2hjppdejfnbxg96mbzcrhdt
title: "Records gate: check that frontmatter source paths exist"
kind: task
status: open
priority: 2
version: 1
labels: []
dependencies: []
created_at: 2026-09-15T03:45:22.349Z
updated_at: 2026-09-15T03:45:22.349Z
---
Found while addressing PR #160 review R20 (defect D44, fixed in 43e6a46e): X-034's `sources` list had a deleted path folded into another entry's YAML, and nothing noticed.

The records gate (`packing-ledger check`, `packing-validate --records`) does not check that the repository paths an exploration, hypothesis or experiment lists under `sources` (or similar path-valued frontmatter) exist at HEAD. A renamed or deleted file leaves a dangling source that looks authoritative.

Done when: the ledger check (or a records-tier step) resolves every repository-relative path in those fields and fails on a missing one, with a negative control. Any historical records that intentionally cite deleted paths must declare that, for example with a commit-pinned form. Survey the current records first and fix or declare the existing dangling ones, as `think-7e1j` does for `method.record`.
