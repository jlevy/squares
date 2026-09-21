---
type: is
id: is-01m31gntf2vew7hbf18qkxe2z4
title: check_class_record_claims reads untracked and gitignored JSON
kind: bug
status: open
priority: 1
version: 1
labels: []
dependencies: []
parent_id: is-01m31gn7263sfhfbq8xfabkh3p
created_at: 2026-09-21T08:17:47.489Z
updated_at: 2026-09-21T08:17:47.489Z
---
PR 207 re-review, new Medium introduced by fix commit 5c30aa93. check_class_record_claims.records() walks Path.rglob('*.json') with a hardcoded SKIP set, so it reads files not in the repository. Demonstrated: one JSON in a gitignored attic/ turns the step into exit 1. Contradicts both comments the same commit added to sqpack/cli/validate.py ('a byte scan of every tracked JSON' and, in TREE_REUSABLE_FAST_STEPS, 'A pure function of the tracked JSON'). The reuse memoization is keyed on content the step does not read. Fix: drive the sweep from git ls-files rather than rglob.
