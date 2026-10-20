---
type: is
id: is-01m4wk41j03apkqqt3m5ch1gp8
title: Align legacy independence label contract with unknown reading history
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
created_at: 2026-10-14T06:55:42.143Z
updated_at: 2026-10-14T08:44:52.681Z
started_at: 2026-10-14T06:57:10.882Z
closed_at: 2026-10-14T08:44:52.681Z
close_reason: Fixed, independently confirmed in PR592 reviews D/E/F/G, green fast+Pages+full checkpoint38530454327 at final7a184720, and merged as f73e9de13d8ccc40b91d844b164f9c2ad9c032c1. Full mathematical proof replays remain tracked separately; no new verified n17 bound claimed.
resolution: null
duplicate_of: null
---
PR592 verifier-registry test still expects after-reading for unstructured legacyrecord, while B4 correctlyrendersneutral independentimplementation. Update truthful expectation without weakening deciding-program, cleanroom or per-run independence controls.
