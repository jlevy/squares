---
type: is
id: is-01m2m6zrysz50dnrmahfmh4cf7
title: "PR #180 addendum A2: make liveness fixtures signal the intended rules"
kind: bug
status: closed
priority: 2
version: 3
labels: []
dependencies: []
parent_id: is-01m2m6y4gw224dgrwf37bgqnhd
created_at: 2026-09-16T04:18:20.248Z
updated_at: 2026-09-16T05:39:00.552Z
closed_at: 2026-09-16T05:39:00.551Z
close_reason: Two-sided sample-byte and exclusion censuses plus exact tsc diagnostic liveness landed at 7db71dd6; focused controls, browser-floor contract, Ruff, BasedPyright, and embedded-JS checks are green.
resolution: null
duplicate_of: null
---
Remove or rebut the one-sided byte-size budgets, require the type-check liveness fixture to fail for the expected diagnostic rather than any syntax error, and make the exclusion drift check bidirectional while preserving the explicit file inventory.
