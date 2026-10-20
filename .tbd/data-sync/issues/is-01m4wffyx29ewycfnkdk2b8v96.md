---
type: is
id: is-01m4wffyx29ewycfnkdk2b8v96
title: Require a formalization’s own proof-assistant evidence to match its claim and scope
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
created_at: 2026-10-14T05:52:18.338Z
updated_at: 2026-10-14T08:44:52.615Z
started_at: 2026-10-14T05:52:39.873Z
closed_at: 2026-10-14T08:44:52.615Z
close_reason: Fixed, independently confirmed in PR592 reviews D/E/F/G, green fast+Pages+full checkpoint38530454327 at final7a184720, and merged as f73e9de13d8ccc40b91d844b164f9c2ad9c032c1. Full mathematical proof replays remain tracked separately; no new verified n17 bound claimed.
resolution: null
duplicate_of: null
---
Independent senior Review B on PR592 at9af2b0b7 confirms unrelated existing n11 proof-assistant report can make T154 n17 formalization kind checks pass after its own report is changed to published-proof. Full check_results accepts this mutation. Require own proof-assistant evidence to substantiate the second-proof claim and scope; reject unrelated n and component evidence, preserve permitted simplification evidence.
