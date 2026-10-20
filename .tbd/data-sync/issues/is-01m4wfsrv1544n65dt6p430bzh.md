---
type: is
id: is-01m4wfsrv1544n65dt6p430bzh
title: Correct current n17 literal-check summaries to192 plus partition
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
created_at: 2026-10-14T05:57:39.809Z
updated_at: 2026-10-14T08:44:52.641Z
started_at: 2026-10-14T05:58:20.246Z
closed_at: 2026-10-14T08:44:52.641Z
close_reason: Fixed, independently confirmed in PR592 reviews D/E/F/G, green fast+Pages+full checkpoint38530454327 at final7a184720, and merged as f73e9de13d8ccc40b91d844b164f9c2ad9c032c1. Full mathematical proof replays remain tracked separately; no new verified n17 bound claimed.
resolution: null
duplicate_of: null
---
B5: current verifier summary and top packet README say194 while actual retained replay has192literal checks and one15000atom partition check,193OKlines. Correct current summaries and generated views, preserve historical review and discrepancy note.
