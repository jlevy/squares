---
type: is
id: is-01m4wfsqjrarr9ktd7kzmxpqy9
title: Fix second-proof rung composition for single bounds and structural results
kind: bug
status: closed
priority: 2
version: 3
delegate: codex@spud10.local
labels: []
dependencies: []
parent_id: is-01m4wajcx0q76t3ppdzfbjxq4d
hold: null
hold_until: null
created_at: 2026-10-14T05:57:38.519Z
updated_at: 2026-10-14T08:44:52.621Z
started_at: 2026-10-14T05:58:20.216Z
closed_at: 2026-10-14T08:44:52.621Z
close_reason: Fixed, independently confirmed in PR592 reviews D/E/F/G, green fast+Pages+full checkpoint38530454327 at final7a184720, and merged as f73e9de13d8ccc40b91d844b164f9c2ad9c032c1. Full mathematical proof replays remain tracked separately; no new verified n17 bound claimed.
resolution: null
duplicate_of: null
---
B2 independent senior review at9af2b0b7: formalization/simplification _claim_pools invents both bound sides regardless of the actual prior result and conclusion. Complete lower-bound second proof accepted by kind checks derivesV0/C0 instead ofV3/C3. Derive required claims from actual repeated result, retain per-count completeness and component exclusions.
