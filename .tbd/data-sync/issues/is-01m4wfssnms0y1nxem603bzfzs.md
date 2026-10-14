---
type: is
id: is-01m4wfssnms0y1nxem603bzfzs
title: Keep malformed coverage shapes from crashing schema diagnostics
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
created_at: 2026-10-14T05:57:40.659Z
updated_at: 2026-10-14T08:44:52.655Z
started_at: 2026-10-14T05:58:20.259Z
closed_at: 2026-10-14T08:44:52.655Z
close_reason: Fixed, independently confirmed in PR592 reviews D/E/F/G, green fast+Pages+full checkpoint38530454327 at final7a184720, and merged as f73e9de13d8ccc40b91d844b164f9c2ad9c032c1. Full mathematical proof replays remain tracked separately; no new verified n17 bound claimed.
resolution: null
duplicate_of: null
---
B7: independence coverage list [sample] is schema-invalid but later evidence_problems raisesAttributeError list.get, interrupting validate_schemas remainingdiagnostics. Guardmapping access or skipinvalidshapes; add regression preserving diagnostic and failclosed semantics.
