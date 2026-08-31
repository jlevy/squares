---
type: is
id: is-01m0sgpp5e5z3n0s1r0q9b9nhb
title: Fix provenance gate skipping unquoted engine commits
kind: bug
status: closed
priority: 1
version: 2
spec_path: explorations/packing/test.sh
labels:
  - packing
  - focus-discipline
dependencies: []
parent_id: is-01m0r7q3zk8x6cg4e30d149698
created_at: 2026-08-24T09:12:56.749Z
updated_at: 2026-08-24T09:16:38.761Z
closed_at: 2026-08-24T09:16:38.749Z
close_reason: D-138 fixed. The provenance gate now accepts quoted or unquoted YAML engine_commit strings, validates each as a 7-to-40 digit hexadecimal revision, and independently requires its checked count to equal all declarations. The focused step now reports exp-011 at 60a50cc, exp-013 at faba023, and all 13 declared commits; schemas, generated defect view, count mutation control, synopsis, and shell syntax pass.
resolution: null
duplicate_of: null
---
The full strict/deep gate printed provenance for exp-001 through exp-012 but silently omitted exp-011 and exp-013 because step_provenance extracts only single-quoted engine_commit values, while the enforced experiment schema permits unquoted YAML strings. This is a recurrence of D-006: a green provenance gate did not cover every declared execution revision. Parse both quoted and unquoted hashes, fail if any declared field is not checked, add a mutation/known-answer regression, log the defect, and verify exp-011 and exp-013 appear.
