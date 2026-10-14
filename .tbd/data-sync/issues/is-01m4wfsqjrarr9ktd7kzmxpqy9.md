---
type: is
id: is-01m4wfsqjrarr9ktd7kzmxpqy9
title: Fix second-proof rung composition for single bounds and structural results
kind: bug
status: in_progress
priority: 2
version: 2
delegate: codex@spud10.local
labels: []
dependencies: []
parent_id: is-01m4wajcx0q76t3ppdzfbjxq4d
hold: null
hold_until: null
created_at: 2026-10-14T05:57:38.519Z
updated_at: 2026-10-14T05:58:20.217Z
started_at: 2026-10-14T05:58:20.216Z
---
B2 independent senior review at9af2b0b7: formalization/simplification _claim_pools invents both bound sides regardless of the actual prior result and conclusion. Complete lower-bound second proof accepted by kind checks derivesV0/C0 instead ofV3/C3. Derive required claims from actual repeated result, retain per-count completeness and component exclusions.
