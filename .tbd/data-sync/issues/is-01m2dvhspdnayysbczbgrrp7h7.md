---
type: is
id: is-01m2dvhspdnayysbczbgrrp7h7
title: Search ledgers can be decoded and re-checked, and one nonfinite partial does not break encoding
kind: task
status: open
priority: 2
version: 1
spec_path: docs/project/specs/active/plan-2026-09-11-workbench-from-spike-to-product.md
labels:
  - workbench-roadmap
dependencies: []
parent_id: is-01m2ckzy45b1b28pvt1nbh4gdm
created_at: 2026-09-13T17:03:01.324Z
updated_at: 2026-09-13T17:03:01.324Z
---
Review 2026-09-13: summary.ts takes block, budget and n from each outcome rather than from the plan (~97-107); there is no decodeSearchOutcomes, so a saved ledger cannot be re-admitted; a nonfinite partial result makes encodeSearchOutcomes throw for the whole ledger. Growth settings are also inert in Search because every start uses unit squares, so configurations differing only in growth run identically; either exclude growth from Search configuration or make it effective. Acceptance: decoder with negative controls, summary derived from the plan, per-outcome encoding failure isolated, growth either rejected or exercised.
