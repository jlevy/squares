---
type: is
id: is-01m0tzvjfq05namakg1pwn7q5q
title: "PR 24 review R7: avoid mandatory review churn after routine W6 rounds"
kind: bug
status: closed
priority: 2
version: 3
spec_path: explorations/packing/docs/project/specs/active/plan-2026-08-23-overnight-cartography-run.md
labels:
  - packing
  - pr24-review
dependencies: []
parent_id: is-01m0tz8s4yps8zgqwk8cng9qnx
created_at: 2026-08-24T22:56:59.894Z
updated_at: 2026-08-24T23:24:50.849Z
closed_at: 2026-08-24T23:24:50.848Z
close_reason: "Fixed in 0775c20: W2 is required for promoted/high-risk claims, optional for routine guarded results, and may apply authorized bounded factual corrections."
resolution: null
duplicate_of: null
---
PR #24 always hands W6 to W2 then W3, even when guarded replay already closes a routine result; W2 read-only language also conflicts with obvious factual correction. Require W2 for promoted, novel, disputed, or high-risk claims and permit bounded obvious corrections.
